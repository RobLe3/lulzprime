#!/usr/bin/env python3
"""
Scale characterization benchmark for resolve() at larger indices.

Tests resolve() at 50k, 100k, 250k to characterize scaling behavior.
This is measurement-only work - no algorithmic changes.

See docs/manual/part_6.md for performance model and constraints.
See docs/benchmark_policy.md for time caps and approval rules.
"""

import sys
import time
import statistics
import tracemalloc
import argparse
import os
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
    """Run scale characterization benchmarks with time cap enforcement."""
    # Parse command line arguments
    parser = argparse.ArgumentParser(
        description="Scale characterization benchmark for LULZprime",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="See docs/benchmark_policy.md for time caps and approval rules."
    )
    parser.add_argument(
        '--max-seconds', '-t',
        type=int,
        default=int(os.environ.get('MAX_SECONDS', 60)),
        help='Maximum seconds per index (default: 60, override via MAX_SECONDS env var)'
    )
    parser.add_argument(
        '--indices',
        type=str,
        default='50000,100000,250000',
        help='Comma-separated list of indices to test (default: 50000,100000,250000)'
    )
    args = parser.parse_args()

    max_seconds = args.max_seconds
    test_indices = [int(x.strip()) for x in args.indices.split(',')]

    print("=" * 80)
    print("LULZprime Scale Characterization Benchmark")
    print(f"Target: Characterize resolve() behavior at indices: {', '.join(str(i) for i in test_indices)}")
    print(f"Time Cap: {max_seconds} seconds per index (per docs/benchmark_policy.md)")
    print("=" * 80)
    print()

    # Check for stress benchmarks (500k+) without approval
    stress_indices = [i for i in test_indices if i >= 500000]
    if stress_indices:
        print("⚠️  WARNING: Stress benchmarks (500k+) detected")
        print(f"   Indices: {stress_indices}")
        print("   These require explicit approval per docs/benchmark_policy.md")
        print("   Approval must be documented in docs/milestones.md")
        print()
        response = input("Continue anyway? (yes/no): ")
        if response.lower() != 'yes':
            print("Benchmark aborted per policy.")
            return None

    results = []
    benchmark_start_time = time.perf_counter()

    print(f"Note: Using 3 iterations per index (reduced from 5 for efficiency)")
    print(f"Note: Time cap is {max_seconds}s per index")
    print()

    for index in test_indices:
        print(f"Benchmarking resolve({index:,})...", flush=True)

        # Timeout guard: check time before each index
        index_start_time = time.perf_counter()

        try:
            result = benchmark_resolve_with_memory(index, iterations=3)
            index_elapsed = time.perf_counter() - index_start_time

            # Check if we exceeded the time cap
            if index_elapsed > max_seconds:
                results.append({
                    'index': index,
                    'result': None,
                    'status': 'TIMEOUT',
                    'elapsed_seconds': index_elapsed
                })
                print(f"  ⏱ TIMEOUT: Exceeded {max_seconds} second cap after {index_elapsed:.1f} seconds")
                print(f"  ⚠️  Stopping benchmark run per docs/benchmark_policy.md")
                print(f"  Remaining indices not tested.")
                print()
                break

            # Success - record results
            result['status'] = 'SUCCESS'
            result['elapsed_seconds'] = index_elapsed
            results.append(result)
            print(f"  ✓ p_{index:,} = {result['result']:,}")
            print(f"    Time: {result['mean_time_ms']:.1f} ms avg (median: {result['median_time_ms']:.1f} ms)")
            print(f"    Memory: {result['peak_memory_mb']:.2f} MB peak")
            print(f"    Elapsed: {index_elapsed:.1f}s (within {max_seconds}s cap)")
            print()
        except Exception as e:
            print(f"  ✗ FAILED: {e}")
            import traceback
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
    print(f"{'Index':<12} {'Status':<12} {'Result (p_n)':<15} {'Mean (ms)':<12} {'Peak Mem (MB)':<15}")
    print("-" * 80)

    for r in results:
        status = r.get('status', 'SUCCESS')
        if status == 'TIMEOUT':
            print(f"{r['index']:<12,} {'TIMEOUT':<12} {'N/A':<15} {'N/A':<12} {'N/A':<15}")
        else:
            print(f"{r['index']:<12,} {status:<12} {r['result']:<15,} "
                  f"{r['mean_time_ms']:<12.1f} {r['peak_memory_mb']:<15.2f}")

    print()
    print("=" * 80)
    print("Performance Notes:")
    print("- All timings are for deterministic, exact resolution (Tier A)")
    print("- Current π(x): Segmented sieve (x >= 100k), O(x log log x)")
    print("- Memory constraint: < 25 MB per Part 6 section 6.4")
    print(f"- Time cap: {max_seconds}s per index per docs/benchmark_policy.md")
    print()

    # Check for timeouts
    timeouts = [r for r in results if r.get('status') == 'TIMEOUT']
    if timeouts:
        print("⏱ TIMEOUTS DETECTED:")
        for t in timeouts:
            print(f"   Index {t['index']:,}: exceeded {max_seconds}s cap ({t['elapsed_seconds']:.1f}s)")
        print("   See docs/benchmark_policy.md for stress benchmark approval process")
        print()

    # Check for constraint violations (only for successful runs)
    successful_results = [r for r in results if r.get('status') == 'SUCCESS']
    if successful_results:
        max_memory = max(r['peak_memory_mb'] for r in successful_results)
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
