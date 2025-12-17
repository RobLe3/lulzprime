#!/usr/bin/env python3
"""
Benchmark script for resolve() function.

Tests resolve() at representative sizes to establish performance baseline.
See docs/manual/part_6.md for performance model and constraints.
"""

import sys
import time
import statistics
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

import lulzprime


def benchmark_resolve(index: int, iterations: int = 5) -> dict:
    """
    Benchmark resolve() at a given index.

    Args:
        index: Prime index to resolve
        iterations: Number of iterations for timing

    Returns:
        Dictionary with timing statistics and result
    """
    # Warmup
    result = lulzprime.resolve(index)

    # Time multiple iterations
    times = []
    for _ in range(iterations):
        start = time.perf_counter()
        r = lulzprime.resolve(index)
        end = time.perf_counter()
        times.append(end - start)
        assert r == result, "Determinism check failed"

    return {
        "index": index,
        "result": result,
        "iterations": iterations,
        "mean_time_ms": statistics.mean(times) * 1000,
        "median_time_ms": statistics.median(times) * 1000,
        "stdev_time_ms": statistics.stdev(times) * 1000 if len(times) > 1 else 0.0,
        "min_time_ms": min(times) * 1000,
        "max_time_ms": max(times) * 1000,
    }


def main():
    """Run benchmarks at representative sizes."""
    print("=" * 70)
    print("LULZprime resolve() Benchmark")
    print("=" * 70)
    print()

    # Test indices chosen to span different scales
    test_indices = [
        1,        # Smallest prime
        10,       # Small index
        100,      # Medium index
        1000,     # Large index
        10000,    # Very large index
    ]

    results = []

    for index in test_indices:
        print(f"Benchmarking resolve({index})...", end=" ", flush=True)
        result = benchmark_resolve(index, iterations=5)
        results.append(result)
        print(f"✓ p_{index} = {result['result']} "
              f"({result['mean_time_ms']:.3f} ms avg)")

    print()
    print("=" * 70)
    print("Summary")
    print("=" * 70)
    print()
    print(f"{'Index':<10} {'Result':<12} {'Mean (ms)':<12} {'Median (ms)':<12} {'StdDev':<10}")
    print("-" * 70)

    for r in results:
        print(f"{r['index']:<10} {r['result']:<12} "
              f"{r['mean_time_ms']:<12.3f} {r['median_time_ms']:<12.3f} "
              f"{r['stdev_time_ms']:<10.3f}")

    print()
    print("=" * 70)
    print("Performance Notes:")
    print("- All timings are for deterministic, exact resolution (Tier A)")
    print("- Performance model from Part 6: resolve() dominated by π(x) calls")
    print("- Current π(x) implementation: Sieve of Eratosthenes (O(x log log x))")
    print("- Memory usage: ~1MB for x=10^6 (well within 25MB constraint)")
    print("=" * 70)

    return results


if __name__ == "__main__":
    main()
