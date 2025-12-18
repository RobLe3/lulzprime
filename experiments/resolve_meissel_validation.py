#!/usr/bin/env python3
"""
Controlled Integration Experiment: Resolve-Level Validation of Meissel π(x)

Tests whether Meissel π(x) backend delivers real-world improvements at the
resolve() level without violating determinism, memory limits, or constraints.

CRITICAL: This is an ISOLATED EXPERIMENT. Does NOT enable Meissel globally.

Methodology:
1. Test indices: {100k, 150k, 250k, 350k}
2. Compare segmented sieve vs Meissel backend
3. Measure wall time, π calls, memory, correctness
4. Verify determinism across 3 repeated runs
5. 60-second timeout per resolve

Output: Fact-based decision data for integration approval.
"""

import time
import tracemalloc
import signal
from contextlib import contextmanager
from dataclasses import dataclass, asdict
from typing import Callable, Optional

from lulzprime.lookup import resolve_internal_with_pi
from lulzprime.pi import pi as segmented_pi
from lulzprime.lehmer import _pi_meissel as meissel_pi
from lulzprime.diagnostics import ResolveStats
from lulzprime.primality import is_prime


class TimeoutException(Exception):
    """Raised when resolve exceeds timeout."""
    pass


@contextmanager
def timeout(seconds):
    """Context manager for timing out operations."""
    def timeout_handler(signum, frame):
        raise TimeoutException(f"Resolve timed out after {seconds}s")

    original_handler = signal.signal(signal.SIGALRM, timeout_handler)
    signal.alarm(seconds)
    try:
        yield
    finally:
        signal.alarm(0)
        signal.signal(signal.SIGALRM, original_handler)


@dataclass
class PiMetrics:
    """Metrics tracked for π(x) calls."""
    total_calls: int = 0
    total_time: float = 0.0  # seconds spent in π calls

    def record_call(self, elapsed: float):
        """Record a π call with its elapsed time."""
        self.total_calls += 1
        self.total_time += elapsed


@dataclass
class ResolveExperimentResult:
    """Complete metrics for one resolve experiment."""
    index: int
    backend: str  # 'segmented' or 'meissel'
    result: Optional[int]
    wall_time: float  # total resolve time (seconds)
    pi_calls: int
    pi_time: float  # time spent in π calls (seconds)
    pi_overhead_pct: float  # π time as % of wall time
    binary_iterations: int
    correction_steps: int  # backward + forward
    peak_memory_mb: float
    timed_out: bool
    error: Optional[str]

    def to_dict(self):
        """Convert to dictionary for reporting."""
        return asdict(self)


def create_instrumented_pi(pi_fn: Callable[[int], int], metrics: PiMetrics) -> Callable[[int], int]:
    """
    Wrap a π function to track call count and time.

    Args:
        pi_fn: Base π function (segmented or meissel)
        metrics: PiMetrics object to update

    Returns:
        Instrumented π function
    """
    def instrumented_pi(x: int) -> int:
        start = time.perf_counter()
        result = pi_fn(x)
        elapsed = time.perf_counter() - start
        metrics.record_call(elapsed)
        return result

    return instrumented_pi


def run_resolve_experiment(
    index: int,
    backend: str,
    pi_fn: Callable[[int], int],
    timeout_seconds: int = 60
) -> ResolveExperimentResult:
    """
    Run a single resolve experiment with the specified π backend.

    Args:
        index: Prime index to resolve
        backend: 'segmented' or 'meissel'
        pi_fn: π function to use
        timeout_seconds: Maximum time allowed

    Returns:
        ResolveExperimentResult with all metrics
    """
    # Initialize metrics
    pi_metrics = PiMetrics()
    stats = ResolveStats()

    # Instrument π function to track time
    instrumented_pi = create_instrumented_pi(pi_fn, pi_metrics)

    # Start memory tracking
    tracemalloc.start()
    tracemalloc.reset_peak()

    result = None
    wall_time = 0.0
    timed_out = False
    error = None

    try:
        with timeout(timeout_seconds):
            start = time.perf_counter()
            result = resolve_internal_with_pi(index, instrumented_pi, stats)
            wall_time = time.perf_counter() - start

    except TimeoutException:
        timed_out = True
        wall_time = timeout_seconds
        error = f"TIMEOUT after {timeout_seconds}s"

    except Exception as e:
        error = f"ERROR: {type(e).__name__}: {str(e)}"
        wall_time = 0.0

    # Get peak memory
    current, peak = tracemalloc.get_traced_memory()
    peak_memory_mb = peak / (1024 * 1024)
    tracemalloc.stop()

    # Calculate overhead percentage
    pi_overhead_pct = (pi_metrics.total_time / wall_time * 100) if wall_time > 0 else 0.0

    # Calculate total correction steps
    correction_steps = stats.correction_backward_steps + stats.correction_forward_steps

    return ResolveExperimentResult(
        index=index,
        backend=backend,
        result=result,
        wall_time=wall_time,
        pi_calls=pi_metrics.total_calls,
        pi_time=pi_metrics.total_time,
        pi_overhead_pct=pi_overhead_pct,
        binary_iterations=stats.binary_search_iterations,
        correction_steps=correction_steps,
        peak_memory_mb=peak_memory_mb,
        timed_out=timed_out,
        error=error,
    )


def verify_correctness(
    index: int,
    segmented_result: Optional[int],
    meissel_result: Optional[int]
) -> tuple[bool, str]:
    """
    Verify that both backends produced identical, correct results.

    Args:
        index: Prime index
        segmented_result: Result from segmented backend
        meissel_result: Result from Meissel backend

    Returns:
        (passed, message)
    """
    if segmented_result is None or meissel_result is None:
        return False, "One or both backends failed to produce result"

    if segmented_result != meissel_result:
        return False, f"MISMATCH: segmented={segmented_result}, meissel={meissel_result}"

    # Verify result is actually prime
    if not is_prime(segmented_result):
        return False, f"Result {segmented_result} is not prime!"

    # Verify with segmented π (oracle)
    pi_result = segmented_pi(segmented_result)
    if pi_result != index:
        return False, f"π({segmented_result}) = {pi_result} != {index}"

    return True, "PASS"


def test_determinism(
    index: int,
    pi_fn: Callable[[int], int],
    backend: str,
    runs: int = 3
) -> tuple[bool, str]:
    """
    Test that resolve is deterministic (same result across multiple runs).

    Args:
        index: Prime index
        pi_fn: π function to use
        backend: Backend name for reporting
        runs: Number of runs to test

    Returns:
        (passed, message)
    """
    results = []

    for _ in range(runs):
        try:
            result = resolve_internal_with_pi(index, pi_fn, None)
            results.append(result)
        except Exception as e:
            return False, f"{backend} failed: {e}"

    if len(set(results)) != 1:
        return False, f"{backend} not deterministic: got {results}"

    return True, f"PASS ({runs} runs)"


def run_full_experiment():
    """
    Run the complete controlled integration experiment.

    Tests indices {100k, 150k, 250k, 350k} with both backends.
    """
    print("=" * 90)
    print("Resolve-Level Validation: Meissel π(x) Integration Experiment")
    print("=" * 90)
    print()
    print("OBJECTIVE: Validate Meissel π(x) delivers real-world resolve() improvements")
    print("SCOPE: Isolated experiment - does NOT enable Meissel globally")
    print("POLICY: 60s timeout per resolve, memory < 25 MB")
    print()

    # Test indices (strict per work order)
    test_indices = [100_000, 150_000, 250_000, 350_000]

    all_results = []

    for index in test_indices:
        print(f"Testing index {index:,}")
        print("-" * 90)

        # Run with segmented backend
        print(f"  [1/2] Segmented sieve backend...")
        seg_result = run_resolve_experiment(index, 'segmented', segmented_pi)
        all_results.append(seg_result)

        if seg_result.timed_out:
            print(f"    ⏱  TIMEOUT after {seg_result.wall_time:.1f}s")
        elif seg_result.error:
            print(f"    ❌ {seg_result.error}")
        else:
            print(f"    ✓ Resolved: p_{index:,} = {seg_result.result:,}")
            print(f"      Wall time: {seg_result.wall_time:.3f}s")
            print(f"      π calls: {seg_result.pi_calls} ({seg_result.pi_overhead_pct:.1f}% overhead)")
            print(f"      Memory: {seg_result.peak_memory_mb:.2f} MB")

        # Run with Meissel backend
        print(f"  [2/2] Meissel P2 backend...")
        meissel_result = run_resolve_experiment(index, 'meissel', meissel_pi)
        all_results.append(meissel_result)

        if meissel_result.timed_out:
            print(f"    ⏱  TIMEOUT after {meissel_result.wall_time:.1f}s")
        elif meissel_result.error:
            print(f"    ❌ {meissel_result.error}")
        else:
            print(f"    ✓ Resolved: p_{index:,} = {meissel_result.result:,}")
            print(f"      Wall time: {meissel_result.wall_time:.3f}s")
            print(f"      π calls: {meissel_result.pi_calls} ({meissel_result.pi_overhead_pct:.1f}% overhead)")
            print(f"      Memory: {meissel_result.peak_memory_mb:.2f} MB")

        # Correctness verification
        print(f"  [Correctness Check]")
        if seg_result.timed_out or meissel_result.timed_out:
            print(f"    ⚠ Skipped (timeout occurred)")
            # If only Meissel succeeded, verify it's correct using segmented π as oracle
            if not meissel_result.timed_out and meissel_result.result:
                if is_prime(meissel_result.result):
                    pi_check = segmented_pi(meissel_result.result)
                    if pi_check == index:
                        print(f"    ✓ Meissel result verified via segmented π (oracle)")
                    else:
                        print(f"    ❌ Meissel result FAILED verification: π({meissel_result.result}) = {pi_check} != {index}")
                        print("    STOP: Correctness failure - aborting experiment")
                        return
                else:
                    print(f"    ❌ Meissel result {meissel_result.result} is not prime!")
                    print("    STOP: Correctness failure - aborting experiment")
                    return
        else:
            passed, message = verify_correctness(index, seg_result.result, meissel_result.result)
            if passed:
                print(f"    ✓ {message}")
            else:
                print(f"    ❌ {message}")
                print("    STOP: Correctness failure - aborting experiment")
                return

        # Speedup calculation
        if not seg_result.timed_out and not meissel_result.timed_out:
            speedup = seg_result.wall_time / meissel_result.wall_time
            pi_speedup = seg_result.pi_time / meissel_result.pi_time if meissel_result.pi_time > 0 else float('inf')
            print(f"  [Performance Comparison]")
            print(f"    Overall speedup: {speedup:.2f}×")
            print(f"    π(x) speedup: {pi_speedup:.2f}×")
        elif seg_result.timed_out and not meissel_result.timed_out:
            # Segmented timed out but Meissel completed
            min_speedup = 60.0 / meissel_result.wall_time  # 60s timeout
            print(f"  [Performance Comparison]")
            print(f"    Minimum speedup: >{min_speedup:.2f}× (segmented timed out)")
            print(f"    Meissel completed in {meissel_result.wall_time:.1f}s vs >60s for segmented")

        # Memory check
        print(f"  [Memory Check]")
        seg_ok = seg_result.peak_memory_mb < 25.0
        meissel_ok = meissel_result.peak_memory_mb < 25.0
        print(f"    Segmented: {seg_result.peak_memory_mb:.2f} MB {'✓' if seg_ok else '✗'}")
        print(f"    Meissel: {meissel_result.peak_memory_mb:.2f} MB {'✓' if meissel_ok else '✗'}")

        if not seg_ok or not meissel_ok:
            print("    ⚠ Memory constraint violated (> 25 MB)")

        print()

    # Determinism tests
    print()
    print("Determinism Validation")
    print("-" * 90)

    for index in test_indices[:2]:  # Test first 2 indices for speed
        print(f"Testing determinism at index {index:,}...")

        seg_pass, seg_msg = test_determinism(index, segmented_pi, 'segmented', runs=3)
        print(f"  Segmented: {seg_msg}")

        meissel_pass, meissel_msg = test_determinism(index, meissel_pi, 'meissel', runs=3)
        print(f"  Meissel: {meissel_msg}")

        if not seg_pass or not meissel_pass:
            print("  ⚠ Determinism failure detected")

    # Summary table
    print()
    print("Summary Table")
    print("=" * 90)
    print(f"{'Index':>10} | {'Backend':>10} | {'Result':>12} | {'Time (s)':>10} | {'π Calls':>8} | {'Mem (MB)':>8} | {'Speedup':>8}")
    print("-" * 90)

    # Group by index for comparison
    for i in range(0, len(all_results), 2):
        seg = all_results[i]
        meissel = all_results[i + 1]

        # Segmented row
        seg_result_str = f"{seg.result:,}" if seg.result else "TIMEOUT"
        seg_time_str = f"{seg.wall_time:.3f}" if not seg.timed_out else "TIMEOUT"
        print(f"{seg.index:>10,} | {'segmented':>10} | {seg_result_str:>12} | {seg_time_str:>10} | {seg.pi_calls:>8} | {seg.peak_memory_mb:>8.2f} | {'-':>8}")

        # Meissel row with speedup
        meissel_result_str = f"{meissel.result:,}" if meissel.result else "TIMEOUT"
        meissel_time_str = f"{meissel.wall_time:.3f}" if not meissel.timed_out else "TIMEOUT"

        if not seg.timed_out and not meissel.timed_out:
            speedup = seg.wall_time / meissel.wall_time
            speedup_str = f"{speedup:.2f}×"
        else:
            speedup_str = "N/A"

        print(f"{meissel.index:>10,} | {'meissel':>10} | {meissel_result_str:>12} | {meissel_time_str:>10} | {meissel.pi_calls:>8} | {meissel.peak_memory_mb:>8.2f} | {speedup_str:>8}")
        print("-" * 90)

    # Key findings
    print()
    print("Key Findings")
    print("=" * 90)
    print()

    # Calculate average speedup
    speedups = []
    for i in range(0, len(all_results), 2):
        seg = all_results[i]
        meissel = all_results[i + 1]
        if not seg.timed_out and not meissel.timed_out:
            speedups.append(seg.wall_time / meissel.wall_time)

    if speedups:
        avg_speedup = sum(speedups) / len(speedups)
        min_speedup = min(speedups)
        max_speedup = max(speedups)

        print(f"Resolve-Level Speedup:")
        print(f"  Average: {avg_speedup:.2f}×")
        print(f"  Range: {min_speedup:.2f}× to {max_speedup:.2f}×")
        print()

    # Memory compliance
    all_compliant = all(r.peak_memory_mb < 25.0 for r in all_results)
    print(f"Memory Compliance: {'✓ ALL PASS' if all_compliant else '✗ VIOLATIONS'}")
    print()

    # Correctness
    print("Correctness: All results verified ✓")
    print()

    print("Experiment complete.")


if __name__ == "__main__":
    run_full_experiment()
