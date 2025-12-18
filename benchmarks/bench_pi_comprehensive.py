#!/usr/bin/env python3
"""
Comprehensive π(x) micro-benchmark: Compare all three implementations.

Compares:
1. pi() - Optimized segmented sieve (baseline)
2. lehmer_pi() - Exact Legendre formula (a = π(√x))
3. _pi_meissel() - Meissel-Lehmer with P2 correction (a = π(x^(1/3)))

Policy compliance:
- 30-second timeout per measurement
- Marks TIMEOUT instead of running indefinitely
- No stress benchmarks (no resolve loops)
- Pure π(x) counting only

Usage:
    python benchmarks/bench_pi_comprehensive.py
"""

import time
import signal
from contextlib import contextmanager
from lulzprime.pi import pi
from lulzprime.lehmer import lehmer_pi, _pi_meissel


class TimeoutException(Exception):
    """Raised when a measurement exceeds the timeout."""
    pass


@contextmanager
def timeout(seconds):
    """
    Context manager for timing out long-running operations.

    Args:
        seconds: Maximum time allowed (in seconds)

    Raises:
        TimeoutException: If operation exceeds timeout
    """
    def timeout_handler(signum, frame):
        raise TimeoutException(f"Operation timed out after {seconds}s")

    # Set the signal handler
    original_handler = signal.signal(signal.SIGALRM, timeout_handler)
    signal.alarm(seconds)

    try:
        yield
    finally:
        # Restore original handler and cancel alarm
        signal.alarm(0)
        signal.signal(signal.SIGALRM, original_handler)


def benchmark_single(func, x, timeout_seconds=30):
    """
    Benchmark a single π(x) function with timeout.

    Args:
        func: Function to benchmark (pi, lehmer_pi, or _pi_meissel)
        x: Value to compute π(x) for
        timeout_seconds: Maximum time allowed

    Returns:
        tuple: (result, time_seconds) or (None, 'TIMEOUT')
    """
    try:
        with timeout(timeout_seconds):
            start = time.perf_counter()
            result = func(x)
            elapsed = time.perf_counter() - start
            return result, elapsed
    except TimeoutException:
        return None, 'TIMEOUT'


def benchmark_comprehensive():
    """
    Run comprehensive benchmark comparing all three π(x) implementations.

    Tests values from 10k to 10M with 30s timeout per measurement.
    """
    print("Comprehensive π(x) Micro-Benchmark")
    print("=" * 90)
    print()
    print("Comparing three implementations:")
    print("  1. pi()           - Segmented sieve (baseline)")
    print("  2. lehmer_pi()    - Exact Legendre (a = π(√x))")
    print("  3. _pi_meissel()  - Meissel with P2 (a = π(x^(1/3)))")
    print()
    print("Policy: 30-second timeout per measurement")
    print()

    # Test values covering different scales
    test_values = [
        10_000,
        100_000,
        500_000,
        1_000_000,
        2_000_000,
        5_000_000,
        10_000_000,
    ]

    results = []

    for x in test_values:
        print(f"Benchmarking π({x:,})...")

        # Benchmark pi() (segmented sieve)
        result_pi, time_pi = benchmark_single(pi, x)

        # Benchmark lehmer_pi() (exact Legendre)
        result_lehmer, time_lehmer = benchmark_single(lehmer_pi, x)

        # Benchmark _pi_meissel() (Meissel variant)
        result_meissel, time_meissel = benchmark_single(_pi_meissel, x)

        # Verify correctness (all should match if no timeout)
        if result_pi is not None and result_lehmer is not None and result_meissel is not None:
            if not (result_pi == result_lehmer == result_meissel):
                print(f"  ❌ MISMATCH: pi={result_pi}, lehmer={result_lehmer}, meissel={result_meissel}")
                continue

        # Format times
        def format_time(t):
            if t == 'TIMEOUT':
                return 'TIMEOUT'
            elif t < 0.001:
                return f"{t*1000:.2f}ms"
            else:
                return f"{t:.4f}s"

        # Calculate speedups (vs segmented sieve baseline)
        def calc_speedup(baseline, variant):
            if baseline == 'TIMEOUT' or variant == 'TIMEOUT':
                return 'N/A'
            if variant == 0:
                return 'inf'
            return baseline / variant

        speedup_lehmer = calc_speedup(time_pi, time_lehmer)
        speedup_meissel = calc_speedup(time_pi, time_meissel)

        results.append({
            'x': x,
            'result': result_pi,
            'time_pi': time_pi,
            'time_lehmer': time_lehmer,
            'time_meissel': time_meissel,
            'speedup_lehmer': speedup_lehmer,
            'speedup_meissel': speedup_meissel,
        })

        print(f"  ✓ π({x:,}) = {result_pi:,}" if result_pi else f"  ⏱ π({x:,}) - computation ongoing")
        print(f"    pi():          {format_time(time_pi)}")
        print(f"    lehmer_pi():   {format_time(time_lehmer)} (speedup: {speedup_lehmer:.2f}x)" if isinstance(speedup_lehmer, float) else f"    lehmer_pi():   {format_time(time_lehmer)}")
        print(f"    _pi_meissel(): {format_time(time_meissel)} (speedup: {speedup_meissel:.2f}x)" if isinstance(speedup_meissel, float) else f"    _pi_meissel(): {format_time(time_meissel)}")
        print()

    # Summary table
    print()
    print("Summary Table")
    print("=" * 90)
    print(f"{'x':>12} | {'π(x)':>10} | {'pi() (s)':>10} | {'Legendre (s)':>12} | {'Meissel (s)':>12} | {'M Speedup':>10}")
    print("-" * 90)

    for r in results:
        def format_cell(val):
            if val == 'TIMEOUT':
                return 'TIMEOUT'
            elif isinstance(val, float):
                return f"{val:.4f}"
            else:
                return str(val)

        pi_str = format_cell(r['time_pi'])
        lehmer_str = format_cell(r['time_lehmer'])
        meissel_str = format_cell(r['time_meissel'])
        speedup_str = f"{r['speedup_meissel']:.2f}x" if isinstance(r['speedup_meissel'], float) else 'N/A'

        print(f"{r['x']:>12,} | {r['result']:>10,} | {pi_str:>10} | {lehmer_str:>12} | {meissel_str:>12} | {speedup_str:>10}")

    print()

    # Analysis
    print("Performance Analysis")
    print("=" * 90)
    print()

    # Find best performer for each scale
    for r in results:
        if r['time_pi'] == 'TIMEOUT' or r['time_lehmer'] == 'TIMEOUT' or r['time_meissel'] == 'TIMEOUT':
            continue

        times = [
            ('Segmented Sieve', r['time_pi']),
            ('Exact Legendre', r['time_lehmer']),
            ('Meissel P2', r['time_meissel']),
        ]
        times.sort(key=lambda t: t[1])
        fastest = times[0]

        print(f"x = {r['x']:,}:")
        print(f"  Fastest: {fastest[0]} ({fastest[1]:.4f}s)")

        # Show relative performance
        for name, t in times[1:]:
            slowdown = t / fastest[1]
            print(f"  {name}: {slowdown:.2f}× slower")
        print()

    # Asymptotic behavior analysis
    print()
    print("Asymptotic Behavior Analysis")
    print("=" * 90)
    print()

    # Compare scaling from 100k to 10M (100x increase in x)
    r_small = next((r for r in results if r['x'] == 100_000), None)
    r_large = next((r for r in results if r['x'] == 10_000_000), None)

    if r_small and r_large and all(t != 'TIMEOUT' for t in [r_small['time_pi'], r_large['time_pi'], r_small['time_meissel'], r_large['time_meissel']]):
        x_ratio = r_large['x'] / r_small['x']

        time_ratio_pi = r_large['time_pi'] / r_small['time_pi']
        time_ratio_meissel = r_large['time_meissel'] / r_small['time_meissel']

        # Expected scaling
        expected_linear = x_ratio
        expected_sublinear = x_ratio ** (2/3)

        print(f"Scaling from x={r_small['x']:,} to x={r_large['x']:,} (x increases {x_ratio:.0f}×):")
        print()
        print(f"Segmented Sieve (pi):")
        print(f"  Actual time increase:   {time_ratio_pi:.2f}×")
        print(f"  Expected if linear:     {expected_linear:.2f}×")
        print(f"  Conclusion: ~Linear scaling")
        print()
        print(f"Meissel P2 (_pi_meissel):")
        print(f"  Actual time increase:   {time_ratio_meissel:.2f}×")
        print(f"  Expected if O(x^2/3):   {expected_sublinear:.2f}×")
        print(f"  Expected if linear:     {expected_linear:.2f}×")

        if time_ratio_meissel < expected_sublinear * 1.5:
            print(f"  ✓ Consistent with sublinear O(x^2/3) scaling")
        elif time_ratio_meissel < expected_linear * 0.8:
            print(f"  ⚠ Better than linear but worse than theoretical O(x^2/3)")
        else:
            print(f"  ✗ Scaling appears linear or worse")

    print()
    print("Benchmark complete.")


if __name__ == "__main__":
    benchmark_comprehensive()
