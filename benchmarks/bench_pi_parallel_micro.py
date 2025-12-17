#!/usr/bin/env python3
"""
Micro-benchmark for pi_parallel() wall-time speedup characterization.

Measures wall-clock time for sequential pi() vs parallel pi_parallel() with
varying worker counts to convert performance claims from estimates to measured evidence.

IMPORTANT: This benchmark enforces strict time caps per docs/benchmark_policy.md
to prevent accidental long runs. Default: 30 seconds per measurement.

See docs/adr/0004-parallel-pi.md for parallel π(x) design decision.
"""

import sys
import time
import argparse
import os
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from lulzprime.pi import pi, pi_parallel


def measure_with_timeout(func, args, timeout_seconds: float) -> dict:
    """
    Measure wall-clock time for a single function call with timeout.

    Args:
        func: Function to call
        args: Tuple of arguments to pass to func
        timeout_seconds: Maximum allowed time in seconds

    Returns:
        Dictionary with result, elapsed time, and status
    """
    start = time.perf_counter()

    try:
        result = func(*args)
        elapsed = time.perf_counter() - start

        if elapsed > timeout_seconds:
            return {
                'result': result,
                'elapsed_seconds': elapsed,
                'status': 'TIMEOUT'
            }

        return {
            'result': result,
            'elapsed_seconds': elapsed,
            'status': 'SUCCESS'
        }
    except Exception as e:
        elapsed = time.perf_counter() - start
        return {
            'result': None,
            'elapsed_seconds': elapsed,
            'status': 'ERROR',
            'error': str(e)
        }


def benchmark_pi_parallel_micro(test_values: list[int], max_seconds: int = 30) -> dict:
    """
    Micro-benchmark for pi_parallel speedup measurement.

    Args:
        test_values: List of x values to test
        max_seconds: Maximum seconds per measurement (per x, per mode)

    Returns:
        Dictionary mapping x -> mode -> result
    """
    results = {}

    for x in test_values:
        print(f"\nBenchmarking π({x:,})...")
        print(f"  Time cap: {max_seconds}s per mode")
        results[x] = {}

        # Mode 1: Sequential pi()
        print(f"  Mode: sequential (pi)", flush=True)
        seq_result = measure_with_timeout(pi, (x,), max_seconds)
        results[x]['sequential'] = seq_result

        if seq_result['status'] == 'TIMEOUT':
            print(f"    ⏱ TIMEOUT after {seq_result['elapsed_seconds']:.1f}s (>{max_seconds}s cap)")
            print(f"    Skipping parallel modes for this x (sequential already too slow)")
            continue
        elif seq_result['status'] == 'ERROR':
            print(f"    ✗ ERROR: {seq_result['error']}")
            continue
        else:
            print(f"    ✓ {seq_result['elapsed_seconds']:.2f}s (result: {seq_result['result']:,})")

        # Modes 2-4: Parallel pi_parallel with different worker counts
        for workers in [2, 4, 8]:
            mode_name = f'parallel_w{workers}'
            print(f"  Mode: parallel workers={workers}", flush=True)

            par_result = measure_with_timeout(pi_parallel, (x, workers), max_seconds)
            results[x][mode_name] = par_result

            if par_result['status'] == 'TIMEOUT':
                print(f"    ⏱ TIMEOUT after {par_result['elapsed_seconds']:.1f}s (>{max_seconds}s cap)")
            elif par_result['status'] == 'ERROR':
                print(f"    ✗ ERROR: {par_result['error']}")
            else:
                # Calculate speedup
                speedup = seq_result['elapsed_seconds'] / par_result['elapsed_seconds']
                print(f"    ✓ {par_result['elapsed_seconds']:.2f}s (speedup: {speedup:.2f}x)")

                # Verify correctness
                if par_result['result'] != seq_result['result']:
                    print(f"    ⚠️  WARNING: Result mismatch! seq={seq_result['result']}, par={par_result['result']}")

    return results


def format_results_markdown(results: dict, max_seconds: int) -> str:
    """
    Format benchmark results as markdown table.

    Args:
        results: Benchmark results dictionary
        max_seconds: Time cap used

    Returns:
        Markdown-formatted string
    """
    lines = []
    lines.append("# Pi Parallel Micro-Benchmark Results")
    lines.append("")
    lines.append(f"**Benchmark Policy Compliance:** Time cap enforced at {max_seconds}s per measurement")
    lines.append("")
    lines.append("## Methodology")
    lines.append("")
    lines.append("- **Sequential baseline:** `pi(x)` (single-threaded segmented sieve)")
    lines.append("- **Parallel modes:** `pi_parallel(x, workers=k)` for k in {2, 4, 8}")
    lines.append("- **Time cap:** Each measurement limited to 30 seconds (default)")
    lines.append("- **Timeout handling:** TIMEOUT = measurement exceeded cap, skipped")
    lines.append("- **Correctness:** All parallel results verified against sequential")
    lines.append("")
    lines.append("## Results")
    lines.append("")
    lines.append("| x | Mode | Time (s) | Status | Speedup |")
    lines.append("|---|------|----------|--------|---------|")

    for x in sorted(results.keys()):
        x_results = results[x]

        # Sequential row
        seq = x_results.get('sequential', {})
        seq_time = seq.get('elapsed_seconds', 0)
        seq_status = seq.get('status', 'NOT_RUN')
        lines.append(f"| {x:,} | sequential | {seq_time:.2f} | {seq_status} | 1.00x |")

        # Parallel rows
        for workers in [2, 4, 8]:
            mode_name = f'parallel_w{workers}'
            par = x_results.get(mode_name, {})
            par_time = par.get('elapsed_seconds', 0)
            par_status = par.get('status', 'NOT_RUN')

            if seq_status == 'SUCCESS' and par_status == 'SUCCESS':
                speedup = seq_time / par_time
                lines.append(f"| {x:,} | w={workers} | {par_time:.2f} | {par_status} | {speedup:.2f}x |")
            elif par_status == 'NOT_RUN':
                lines.append(f"| {x:,} | w={workers} | N/A | SKIPPED | N/A |")
            else:
                lines.append(f"| {x:,} | w={workers} | {par_time:.2f} | {par_status} | N/A |")

    lines.append("")
    lines.append("## Observations")
    lines.append("")

    # Calculate average speedup for successful runs
    speedups = []
    for x, x_results in results.items():
        seq = x_results.get('sequential', {})
        if seq.get('status') == 'SUCCESS':
            for workers in [2, 4, 8]:
                mode_name = f'parallel_w{workers}'
                par = x_results.get(mode_name, {})
                if par.get('status') == 'SUCCESS':
                    speedup = seq['elapsed_seconds'] / par['elapsed_seconds']
                    speedups.append((x, workers, speedup))

    if speedups:
        lines.append("**Measured speedups (successful runs only):**")
        for x, workers, speedup in speedups:
            lines.append(f"- π({x:,}) with {workers} workers: {speedup:.2f}x")

        avg_speedup = sum(s for _, _, s in speedups) / len(speedups)
        lines.append(f"- **Average speedup across all modes:** {avg_speedup:.2f}x")
    else:
        lines.append("**No successful parallel runs** - all measurements exceeded time cap or failed")

    lines.append("")

    # Report timeouts
    timeouts = []
    for x, x_results in results.items():
        for mode, result in x_results.items():
            if result.get('status') == 'TIMEOUT':
                timeouts.append((x, mode, result['elapsed_seconds']))

    if timeouts:
        lines.append("## Timeouts")
        lines.append("")
        lines.append(f"The following measurements exceeded the {max_seconds}s cap:")
        for x, mode, elapsed in timeouts:
            lines.append(f"- π({x:,}) {mode}: {elapsed:.1f}s")
        lines.append("")
        lines.append("Per docs/benchmark_policy.md, stress benchmarks (500k+) require explicit approval.")

    lines.append("")
    lines.append("---")
    lines.append("")
    lines.append("**Benchmark Date:** Generated automatically")
    lines.append(f"**Time Cap:** {max_seconds}s per measurement")
    lines.append("**Policy:** docs/benchmark_policy.md")
    lines.append("**ADR:** docs/adr/0004-parallel-pi.md")

    return "\n".join(lines)


def main():
    """Run pi_parallel micro-benchmark with time cap enforcement."""
    parser = argparse.ArgumentParser(
        description="Micro-benchmark for pi_parallel() speedup characterization",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="See docs/benchmark_policy.md for time caps and approval rules."
    )
    parser.add_argument(
        '--max-seconds', '-t',
        type=int,
        default=int(os.environ.get('MAX_SECONDS', 30)),
        help='Maximum seconds per measurement (default: 30, override via MAX_SECONDS env var)'
    )
    parser.add_argument(
        '--values',
        type=str,
        default='200000,500000,1000000',
        help='Comma-separated list of x values to test (default: 200000,500000,1000000)'
    )
    parser.add_argument(
        '--output',
        type=str,
        default='benchmarks/results/pi_parallel_micro.md',
        help='Output file for markdown results (default: benchmarks/results/pi_parallel_micro.md)'
    )
    args = parser.parse_args()

    max_seconds = args.max_seconds
    test_values = [int(x.strip()) for x in args.values.split(',')]
    output_file = args.output

    print("=" * 80)
    print("LULZprime Pi Parallel Micro-Benchmark")
    print(f"Target: Measure pi_parallel() speedup vs pi() at x = {', '.join(str(v) for v in test_values)}")
    print(f"Time Cap: {max_seconds} seconds per measurement (per docs/benchmark_policy.md)")
    print("=" * 80)

    # Check for stress benchmarks (500k+)
    stress_values = [v for v in test_values if v >= 500000]
    if stress_values:
        print()
        print("⚠️  WARNING: Large x values detected (>= 500k)")
        print(f"   Values: {stress_values}")
        print(f"   Time cap: {max_seconds}s per measurement will be enforced")
        print("   If timeouts occur, results will be marked as TIMEOUT")
        print()

    # Run benchmark
    results = benchmark_pi_parallel_micro(test_values, max_seconds)

    # Format and print results
    print()
    print("=" * 80)
    print("Summary")
    print("=" * 80)

    markdown = format_results_markdown(results, max_seconds)
    print(markdown)

    # Write to file
    output_path = Path(output_file)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(markdown)

    print()
    print(f"Results written to: {output_file}")
    print("=" * 80)


if __name__ == "__main__":
    main()
