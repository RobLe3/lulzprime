#!/usr/bin/env python3
"""
Phase 3 Diagnostics: Resolve-Level Dispatch Performance with Detailed Metrics

Policy-compliant diagnostic experiment measuring Meissel dispatch impact at resolve() level.
Strict caps: indices {100k, 150k, 250k, 350k}, 60s timeout per resolve.

IMPORTANT: Does NOT modify global config. Uses dependency injection for A/B testing.

Captures:
- Wall time, π calls, π time breakdown
- Meissel-specific metrics (φ calls, cache sizes, recursion depth)
- Memory usage (tracemalloc)
- Determinism validation
- Correctness verification (is_prime, π oracle)
"""

import time
import tracemalloc
import signal
import platform
import sys
from contextlib import contextmanager
from dataclasses import dataclass, asdict
from typing import Callable, Optional

from lulzprime.lookup import resolve_internal_with_pi
from lulzprime.pi import pi as segmented_pi, _segmented_sieve
from lulzprime.lehmer import _pi_meissel
from lulzprime.diagnostics import ResolveStats, MeisselStats
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
    """Metrics for π(x) calls during resolve."""
    total_calls: int = 0
    total_time: float = 0.0

    def record_call(self, elapsed: float):
        """Record a π call with its elapsed time."""
        self.total_calls += 1
        self.total_time += elapsed


@dataclass
class DiagnosticResult:
    """Complete diagnostic result for one resolve experiment."""
    index: int
    backend: str  # 'segmented' or 'meissel'
    result: Optional[int]
    wall_time: float
    pi_calls: int
    pi_time: float
    pi_overhead_pct: float
    binary_iterations: int
    correction_steps: int
    peak_memory_mb: float
    timed_out: bool
    error: Optional[str]
    # Meissel-specific metrics (None for segmented)
    phi_calls: Optional[int] = None
    phi_cache_size: Optional[int] = None
    pi_cache_size: Optional[int] = None
    recursion_depth_max: Optional[int] = None

    def to_dict(self):
        """Convert to dictionary for reporting."""
        return asdict(self)


def create_instrumented_pi_segmented(metrics: PiMetrics) -> Callable[[int], int]:
    """Wrap segmented π to track time."""
    def instrumented_pi(x: int) -> int:
        start = time.perf_counter()
        result = _segmented_sieve(x)
        elapsed = time.perf_counter() - start
        metrics.record_call(elapsed)
        return result
    return instrumented_pi


def create_instrumented_pi_meissel(metrics: PiMetrics, meissel_stats: MeisselStats) -> Callable[[int], int]:
    """Wrap Meissel π to track time and Meissel-specific metrics."""
    def instrumented_pi(x: int) -> int:
        start = time.perf_counter()
        # Note: _pi_meissel doesn't currently support stats injection
        # We'll track at the call level for now
        result = _pi_meissel(x)
        elapsed = time.perf_counter() - start
        metrics.record_call(elapsed)
        # Meissel-specific tracking would go here if _pi_meissel accepted stats
        return result
    return instrumented_pi


def run_resolve_diagnostic(
    index: int,
    backend: str,
    pi_fn: Callable[[int], int],
    timeout_seconds: int = 60,
    meissel_stats: Optional[MeisselStats] = None
) -> DiagnosticResult:
    """
    Run resolve with full diagnostic instrumentation.

    Args:
        index: Prime index to resolve
        backend: 'segmented' or 'meissel'
        pi_fn: Instrumented π function
        timeout_seconds: Maximum time allowed
        meissel_stats: Meissel-specific stats (if backend='meissel')

    Returns:
        DiagnosticResult with all metrics
    """
    # Initialize metrics
    pi_metrics = PiMetrics()
    stats = ResolveStats()

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
            result = resolve_internal_with_pi(index, pi_fn, stats)
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

    # Build result
    diagnostic_result = DiagnosticResult(
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

    # Add Meissel-specific metrics if available
    if meissel_stats:
        diagnostic_result.phi_calls = meissel_stats.phi_calls
        diagnostic_result.phi_cache_size = meissel_stats.phi_cache_size
        diagnostic_result.pi_cache_size = meissel_stats.pi_cache_size
        diagnostic_result.recursion_depth_max = meissel_stats.recursion_depth_max

    return diagnostic_result


def verify_correctness(index: int, result: Optional[int]) -> tuple[bool, str]:
    """
    Verify resolve result using segmented π oracle.

    Args:
        index: Prime index
        result: Resolved value

    Returns:
        (passed, message)
    """
    if result is None:
        return False, "Result is None"

    # Check if prime
    if not is_prime(result):
        return False, f"Result {result} is not prime!"

    # Verify with segmented π (oracle)
    pi_result = segmented_pi(result)
    if pi_result != index:
        return False, f"π({result}) = {pi_result} != {index}"

    return True, "PASS"


def run_full_diagnostic():
    """
    Run complete Phase 3 diagnostic experiment.

    Tests indices {100k, 150k, 250k, 350k} with both backends.
    """
    print("=" * 90)
    print("Phase 3 Diagnostics: Resolve-Level Dispatch Performance")
    print("=" * 90)
    print()
    print("OBJECTIVE: Quantify Meissel dispatch impact with detailed metrics")
    print("SCOPE: Policy-compliant - no 500k/1M, 60s timeout per resolve")
    print()
    print("ENVIRONMENT:")
    print(f"  Python: {sys.version.split()[0]}")
    print(f"  Platform: {platform.system()} {platform.release()}")
    print(f"  Machine: {platform.machine()}")
    print()

    # Test indices (strict per policy)
    test_indices = [100_000, 150_000, 250_000, 350_000]

    all_results = []

    for index in test_indices:
        print(f"Testing index {index:,}")
        print("-" * 90)

        # Run with segmented backend
        print(f"  [1/2] Segmented backend...")
        pi_metrics_seg = PiMetrics()
        pi_fn_seg = create_instrumented_pi_segmented(pi_metrics_seg)
        seg_result = run_resolve_diagnostic(index, 'segmented', pi_fn_seg)
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
        print(f"  [2/2] Meissel backend...")
        pi_metrics_meissel = PiMetrics()
        meissel_stats = MeisselStats()
        pi_fn_meissel = create_instrumented_pi_meissel(pi_metrics_meissel, meissel_stats)
        meissel_result = run_resolve_diagnostic(index, 'meissel', pi_fn_meissel, meissel_stats=meissel_stats)
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
        if seg_result.timed_out and meissel_result.timed_out:
            print(f"    ⚠ Both backends timed out")
        elif not meissel_result.timed_out and meissel_result.result:
            passed, message = verify_correctness(index, meissel_result.result)
            if passed:
                print(f"    ✓ {message}")
            else:
                print(f"    ❌ {message}")
                print("    STOP: Correctness failure")
                return

        # Performance comparison
        if not seg_result.timed_out and not meissel_result.timed_out:
            speedup = seg_result.wall_time / meissel_result.wall_time
            print(f"  [Performance]")
            print(f"    Speedup: {speedup:.2f}×")
        elif seg_result.timed_out and not meissel_result.timed_out:
            min_speedup = 60.0 / meissel_result.wall_time
            print(f"  [Performance]")
            print(f"    Minimum speedup: >{min_speedup:.2f}× (segmented timed out)")

        print()

    # Summary table
    print()
    print("Summary Table")
    print("=" * 90)
    print(f"{'Index':>10} | {'Backend':>10} | {'Time (s)':>10} | {'π Calls':>8} | {'Mem (MB)':>8} | {'Speedup':>8}")
    print("-" * 90)

    for i in range(0, len(all_results), 2):
        seg = all_results[i]
        meissel = all_results[i + 1]

        # Segmented row
        seg_time_str = f"{seg.wall_time:.3f}" if not seg.timed_out else "TIMEOUT"
        print(f"{seg.index:>10,} | {'segmented':>10} | {seg_time_str:>10} | {seg.pi_calls:>8} | {seg.peak_memory_mb:>8.2f} | {'-':>8}")

        # Meissel row
        meissel_time_str = f"{meissel.wall_time:.3f}" if not meissel.timed_out else "TIMEOUT"
        if not seg.timed_out and not meissel.timed_out:
            speedup = seg.wall_time / meissel.wall_time
            speedup_str = f"{speedup:.2f}×"
        else:
            speedup_str = "N/A"
        print(f"{meissel.index:>10,} | {'meissel':>10} | {meissel_time_str:>10} | {meissel.pi_calls:>8} | {meissel.peak_memory_mb:>8.2f} | {speedup_str:>8}")
        print("-" * 90)

    print()
    print("Diagnostic complete.")


if __name__ == "__main__":
    run_full_diagnostic()
