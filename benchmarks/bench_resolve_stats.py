#!/usr/bin/env python3
"""
Diagnostic benchmark for resolve() internal operations.

Measures pi(x) calls, binary search iterations, and correction steps
to identify performance bottlenecks in the resolution pipeline.

This is pure measurement - no algorithmic changes.

See docs/manual/part_5.md for resolution pipeline.
See docs/benchmark_policy.md for time caps and approval rules.
"""

import sys
import time
import argparse
import os
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from lulzprime.diagnostics import ResolveStats
from lulzprime.lookup import resolve_internal_with_pi
from lulzprime.pi import pi


def benchmark_resolve_stats(index: int, max_seconds: int = 60) -> dict:
    """
    Benchmark resolve() with internal statistics tracking.

    Args:
        index: Prime index to resolve
        max_seconds: Maximum seconds allowed for this index

    Returns:
        Dictionary with timing and internal metrics
    """
    stats = ResolveStats()

    start = time.perf_counter()
    result = resolve_internal_with_pi(index, pi, stats)
    elapsed = time.perf_counter() - start

    # Check timeout
    if elapsed > max_seconds:
        return {
            'index': index,
            'status': 'TIMEOUT',
            'elapsed_seconds': elapsed,
            'max_seconds': max_seconds,
        }

    # Success - return full stats
    return {
        'index': index,
        'status': 'SUCCESS',
        'result': result,
        'elapsed_seconds': elapsed,
        'pi_calls': stats.pi_calls,
        'binary_search_iterations': stats.binary_search_iterations,
        'correction_backward_steps': stats.correction_backward_steps,
        'correction_forward_steps': stats.correction_forward_steps,
        'forecast_value': stats.forecast_value,
    }


def format_results_as_markdown(results: list[dict], max_seconds: int) -> str:
    """
    Format benchmark results as markdown for docs.

    Args:
        results: List of benchmark result dictionaries
        max_seconds: Time cap used for benchmarks

    Returns:
        Markdown-formatted string
    """
    lines = []
    lines.append("# Resolve() Diagnostic Statistics")
    lines.append("")
    lines.append("**Purpose:** Measure internal operations of resolve() to identify bottlenecks")
    lines.append("")
    lines.append("## Methodology")
    lines.append("")
    lines.append("- **Function:** `resolve_internal_with_pi(index, pi, stats)`")
    lines.append("- **Instrumentation:** ResolveStats dataclass (see diagnostics.py)")
    lines.append("- **Time cap:** {} seconds per index (default)".format(max_seconds))
    lines.append("- **Policy:** docs/benchmark_policy.md")
    lines.append("")
    lines.append("## Metrics Tracked")
    lines.append("")
    lines.append("- **pi_calls:** Number of π(x) function calls during resolution")
    lines.append("- **binary_search_iterations:** Number of binary search iterations")
    lines.append("- **correction_backward_steps:** Backward correction steps (pi(x) > index)")
    lines.append("- **correction_forward_steps:** Forward correction steps (pi(x) < index)")
    lines.append("- **forecast_value:** Initial forecast estimate")
    lines.append("")
    lines.append("## Results")
    lines.append("")
    lines.append("| Index | Status | Time (s) | π(x) Calls | Binary Iters | Backward | Forward | Forecast |")
    lines.append("|-------|--------|----------|------------|--------------|----------|---------|----------|")

    for r in results:
        if r['status'] == 'TIMEOUT':
            lines.append(f"| {r['index']:,} | TIMEOUT | {r['elapsed_seconds']:.1f} | N/A | N/A | N/A | N/A | N/A |")
        else:
            lines.append(
                f"| {r['index']:,} | {r['status']} | {r['elapsed_seconds']:.2f} | "
                f"{r['pi_calls']} | {r['binary_search_iterations']} | "
                f"{r['correction_backward_steps']} | {r['correction_forward_steps']} | "
                f"{r['forecast_value']:,} |"
            )

    lines.append("")
    lines.append("## Analysis")
    lines.append("")

    successful = [r for r in results if r['status'] == 'SUCCESS']
    if successful:
        lines.append("**Observations:**")
        lines.append("")
        for r in successful:
            total_ops = (r['pi_calls'] +
                        r['binary_search_iterations'] +
                        r['correction_backward_steps'] +
                        r['correction_forward_steps'])
            pi_pct = (r['pi_calls'] / total_ops * 100) if total_ops > 0 else 0
            lines.append(f"- **Index {r['index']:,}:**")
            lines.append(f"  - π(x) calls: {r['pi_calls']} ({pi_pct:.1f}% of total operations)")
            lines.append(f"  - Binary search iterations: {r['binary_search_iterations']}")
            lines.append(f"  - Correction steps: {r['correction_backward_steps']} backward, {r['correction_forward_steps']} forward")
            lines.append(f"  - Total time: {r['elapsed_seconds']:.2f}s")
            lines.append("")

        avg_pi_calls = sum(r['pi_calls'] for r in successful) / len(successful)
        avg_time = sum(r['elapsed_seconds'] for r in successful) / len(successful)
        lines.append(f"**Averages across {len(successful)} successful runs:**")
        lines.append(f"- π(x) calls per resolve: {avg_pi_calls:.1f}")
        lines.append(f"- Time per resolve: {avg_time:.2f}s")
        lines.append("")

    timeouts = [r for r in results if r['status'] == 'TIMEOUT']
    if timeouts:
        lines.append("**Timeouts:**")
        lines.append("")
        for r in timeouts:
            lines.append(f"- Index {r['index']:,}: exceeded {r['max_seconds']}s cap ({r['elapsed_seconds']:.1f}s)")
        lines.append("")

    lines.append("---")
    lines.append("")
    lines.append("**Benchmark Date:** " + time.strftime("%Y-%m-%d %H:%M:%S"))
    lines.append(f"**Time Cap:** {max_seconds}s per index")
    lines.append("**Policy:** docs/benchmark_policy.md")
    lines.append("**Implementation:** src/lulzprime/lookup.py")
    lines.append("")

    return "\n".join(lines)


def main():
    """Run diagnostic benchmarks with time cap enforcement."""
    # Parse command line arguments
    parser = argparse.ArgumentParser(
        description="Diagnostic benchmark for LULZprime resolve() internals",
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
    parser.add_argument(
        '--output', '-o',
        type=str,
        default='benchmarks/results/resolve_stats.md',
        help='Output file for markdown results (default: benchmarks/results/resolve_stats.md)'
    )
    args = parser.parse_args()

    max_seconds = args.max_seconds
    test_indices = [int(x.strip()) for x in args.indices.split(',')]
    output_file = args.output

    print("=" * 80)
    print("LULZprime Resolve() Diagnostic Benchmark")
    print(f"Target: Measure internal operations at indices: {', '.join(str(i) for i in test_indices)}")
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

    for index in test_indices:
        print(f"Benchmarking resolve({index:,}) with stats...", flush=True)

        try:
            result = benchmark_resolve_stats(index, max_seconds=max_seconds)
            results.append(result)

            if result['status'] == 'TIMEOUT':
                print(f"  ⏱ TIMEOUT: Exceeded {max_seconds} second cap after {result['elapsed_seconds']:.1f} seconds")
                print(f"  ⚠️  Stopping benchmark run per docs/benchmark_policy.md")
                print(f"  Remaining indices not tested.")
                print()
                break

            # Success - print details
            print(f"  ✓ p_{index:,} = {result['result']:,}")
            print(f"    Time: {result['elapsed_seconds']:.2f}s")
            print(f"    π(x) calls: {result['pi_calls']}")
            print(f"    Binary search iterations: {result['binary_search_iterations']}")
            print(f"    Correction steps: {result['correction_backward_steps']} backward, {result['correction_forward_steps']} forward")
            print(f"    Forecast: {result['forecast_value']:,}")
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

    successful = [r for r in results if r['status'] == 'SUCCESS']
    if successful:
        print(f"{'Index':<12} {'Status':<12} {'Time (s)':<12} {'π(x) Calls':<12} {'Binary Iters':<12}")
        print("-" * 80)
        for r in successful:
            print(f"{r['index']:<12,} {r['status']:<12} {r['elapsed_seconds']:<12.2f} "
                  f"{r['pi_calls']:<12} {r['binary_search_iterations']:<12}")
        print()

    timeouts = [r for r in results if r['status'] == 'TIMEOUT']
    if timeouts:
        print("⏱ TIMEOUTS DETECTED:")
        for t in timeouts:
            print(f"   Index {t['index']:,}: exceeded {max_seconds}s cap ({t['elapsed_seconds']:.1f}s)")
        print()

    # Generate markdown output
    markdown = format_results_as_markdown(results, max_seconds)

    output_path = Path(output_file)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(markdown)

    print(f"✓ Results written to {output_file}")
    print("=" * 80)

    return results


if __name__ == "__main__":
    main()
