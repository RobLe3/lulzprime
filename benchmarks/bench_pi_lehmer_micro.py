#!/usr/bin/env python3
"""
Micro-benchmark for π(x) counting: lehmer_pi() vs pi() performance comparison.

Measures pure π(x) computation time (no prime generation, no resolution).
Demonstrates sublinear O(x^(2/3)) scaling of Legendre formula.

Usage:
    python benchmarks/bench_pi_lehmer_micro.py

Expected results:
- lehmer_pi() should be faster than pi() for large x
- lehmer_pi() should show sublinear growth (not proportional to x)
- All results must be exact (matching between implementations)

Note: This benchmark runs pure prime counting only. It does NOT run
resolve() or any index-based resolution operations.
"""

import time
from lulzprime.lehmer import lehmer_pi
from lulzprime.pi import pi


def benchmark_pi_comparison():
    """
    Compare lehmer_pi() vs pi() for various x values.

    Tests pure π(x) counting performance at different scales.
    30 second cap per x (should complete instantly for correct implementation).
    """
    print("π(x) Micro-Benchmark: lehmer_pi() vs pi()")
    print("=" * 70)
    print()

    test_values = [
        10_000,
        100_000,
        1_000_000,
        2_000_000,
        5_000_000,
    ]

    results = []

    for x in test_values:
        print(f"Benchmarking π({x:,})...")

        # Benchmark pi() (segmented sieve)
        start = time.perf_counter()
        result_pi = pi(x)
        time_pi = time.perf_counter() - start

        # Benchmark lehmer_pi() (Legendre formula)
        start = time.perf_counter()
        result_lehmer = lehmer_pi(x)
        time_lehmer = time.perf_counter() - start

        # Verify exactness
        if result_pi != result_lehmer:
            print(f"  ❌ MISMATCH: pi({x}) = {result_pi}, lehmer_pi({x}) = {result_lehmer}")
            continue

        # Calculate speedup
        speedup = time_pi / time_lehmer if time_lehmer > 0 else float('inf')

        results.append({
            'x': x,
            'result': result_pi,
            'time_pi': time_pi,
            'time_lehmer': time_lehmer,
            'speedup': speedup,
        })

        print(f"  ✓ π({x:,}) = {result_pi:,}")
        print(f"    pi():        {time_pi:.4f}s")
        print(f"    lehmer_pi(): {time_lehmer:.4f}s")
        print(f"    Speedup:     {speedup:.2f}x")
        print()

    # Summary table
    print()
    print("Summary Table")
    print("=" * 70)
    print(f"{'x':>12} | {'π(x)':>10} | {'pi() (s)':>10} | {'lehmer() (s)':>12} | {'Speedup':>8}")
    print("-" * 70)

    for r in results:
        print(f"{r['x']:>12,} | {r['result']:>10,} | {r['time_pi']:>10.4f} | {r['time_lehmer']:>12.4f} | {r['speedup']:>8.2f}x")

    print()

    # Complexity analysis
    print("Complexity Analysis")
    print("=" * 70)
    print()

    if len(results) >= 2:
        # Compare scaling from 100k to 5M (50x increase in x)
        r1 = results[1]  # 100k
        r2 = results[-1]  # 5M

        x_ratio = r2['x'] / r1['x']
        time_ratio_pi = r2['time_pi'] / r1['time_pi']
        time_ratio_lehmer = r2['time_lehmer'] / r1['time_lehmer']

        # Expected scaling:
        # Linear: time_ratio ≈ x_ratio
        # O(x^(2/3)): time_ratio ≈ x_ratio^(2/3)
        expected_linear = x_ratio
        expected_sublinear = x_ratio ** (2/3)

        print(f"Scaling from x={r1['x']:,} to x={r2['x']:,} (x increases {x_ratio:.1f}×):")
        print()
        print(f"pi() (segmented sieve):")
        print(f"  Actual time increase:   {time_ratio_pi:.2f}×")
        print(f"  Expected if linear:     {expected_linear:.2f}×")
        print(f"  Scaling exponent:       ~{(time_ratio_pi ** (1/x_ratio)):.3f}")
        print()
        print(f"lehmer_pi() (Legendre):")
        print(f"  Actual time increase:   {time_ratio_lehmer:.2f}×")
        print(f"  Expected if O(x^2/3):   {expected_sublinear:.2f}×")
        print(f"  Expected if linear:     {expected_linear:.2f}×")
        print()

        if time_ratio_lehmer < expected_linear * 0.8:
            print("✓ lehmer_pi() shows sublinear scaling (better than O(x))")
        else:
            print("⚠ lehmer_pi() scaling appears linear or worse")

    print()
    print("Benchmark complete.")


if __name__ == "__main__":
    benchmark_pi_comparison()
