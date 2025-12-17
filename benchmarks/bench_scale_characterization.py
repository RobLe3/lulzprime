#!/usr/bin/env python3
"""
Scale characterization benchmark for resolve() at larger indices.

Tests resolve() at 50k, 100k, 250k to characterize scaling behavior.
This is measurement-only work - no algorithmic changes.

See docs/manual/part_6.md for performance model and constraints.
"""

import sys
import time
import statistics
import tracemalloc
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

import lulzprime


def benchmark_resolve_with_memory(index: int, iterations: int = 3) -> dict:
    """
    Benchmark resolve() at a given index with memory tracking.

    Args:
        index: Prime index to resolve
        iterations: Number of iterations for timing (reduced for large indices)

    Returns:
        Dictionary with timing statistics, result, and memory usage
    """
    # Warmup
    result = lulzprime.resolve(index)

    # Time multiple iterations
    times = []
    memory_peaks = []

    for _ in range(iterations):
        # Start memory tracking
        tracemalloc.start()

        start = time.perf_counter()
        r = lulzprime.resolve(index)
        end = time.perf_counter()

        # Get peak memory usage for this iteration
        current, peak = tracemalloc.get_traced_memory()
        tracemalloc.stop()

        times.append(end - start)
        memory_peaks.append(peak / 1024 / 1024)  # Convert to MB
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
        "mean_memory_mb": statistics.mean(memory_peaks),
        "peak_memory_mb": max(memory_peaks),
    }


def main():
    """Run scale characterization benchmarks."""
    print("=" * 80)
    print("LULZprime Scale Characterization Benchmark")
    print("Target: Characterize resolve() behavior at 50k, 100k, 250k indices")
    print("=" * 80)
    print()

    # Large-scale test indices
    # Note: Using 3 iterations instead of 5 due to longer execution times
    test_indices = [
        50000,      # 50k index
        100000,     # 100k index
        250000,     # 250k index
    ]

    results = []

    print("Note: Using 3 iterations per index (reduced from 5 for efficiency)")
    print()

    for index in test_indices:
        print(f"Benchmarking resolve({index:,})...", flush=True)
        try:
            result = benchmark_resolve_with_memory(index, iterations=3)
            results.append(result)
            print(f"  ✓ p_{index:,} = {result['result']:,}")
            print(f"    Time: {result['mean_time_ms']:.1f} ms avg (median: {result['median_time_ms']:.1f} ms)")
            print(f"    Memory: {result['peak_memory_mb']:.2f} MB peak")
            print()
        except Exception as e:
            print(f"  ✗ FAILED: {e}")
            print(f"    Traceback:")
            traceback.print_exc()
            print()
            break

    if not results:
        print("ERROR: No benchmarks completed successfully")
        return None

    print("=" * 80)
    print("Summary")
    print("=" * 80)
    print()
    print(f"{'Index':<12} {'Result (p_n)':<15} {'Mean (ms)':<12} {'Median (ms)':<12} {'Peak Mem (MB)':<15}")
    print("-" * 80)

    for r in results:
        print(f"{r['index']:<12,} {r['result']:<15,} "
              f"{r['mean_time_ms']:<12.1f} {r['median_time_ms']:<12.1f} "
              f"{r['peak_memory_mb']:<15.2f}")

    print()
    print("=" * 80)
    print("Performance Notes:")
    print("- All timings are for deterministic, exact resolution (Tier A)")
    print("- Current π(x): Sieve of Eratosthenes (O(x log log x))")
    print("- Memory constraint: < 25 MB per Part 6 section 6.4")
    print()

    # Check for constraint violations
    max_memory = max(r['peak_memory_mb'] for r in results)
    if max_memory > 25.0:
        print(f"⚠️  WARNING: Memory constraint violated!")
        print(f"   Peak memory: {max_memory:.2f} MB exceeds 25 MB limit")
        print(f"   This should be logged in docs/issues.md")
    else:
        print(f"✓ Memory constraint satisfied (peak: {max_memory:.2f} MB < 25 MB)")

    print("=" * 80)

    return results


if __name__ == "__main__":
    main()
