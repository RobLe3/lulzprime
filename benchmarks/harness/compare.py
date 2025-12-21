#!/usr/bin/env python3
"""
Compare benchmark results from pyperf JSON outputs.

Produces markdown summary with performance deltas between versions.
"""

import json
import sys
from pathlib import Path
from typing import Dict, Optional, Tuple


def load_pyperf_result(json_path: Path) -> Optional[Dict]:
    """Load a pyperf JSON result file."""
    try:
        with open(json_path) as f:
            return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError) as e:
        print(f"Warning: Could not load {json_path}: {e}", file=sys.stderr)
        return None


def extract_mean_time(result: Dict) -> Optional[float]:
    """Extract mean time in seconds from pyperf result."""
    try:
        # pyperf stores mean in 'benchmarks' list
        if "benchmarks" in result and len(result["benchmarks"]) > 0:
            bench = result["benchmarks"][0]
            if "runs" in bench and len(bench["runs"]) > 0:
                # Get mean from runs
                values = []
                for run in bench["runs"]:
                    if "values" in run:
                        values.extend(run["values"])
                if values:
                    return sum(values) / len(values)
        return None
    except (KeyError, TypeError, ZeroDivisionError):
        return None


def format_time(seconds: Optional[float]) -> str:
    """Format time in human-readable units."""
    if seconds is None:
        return "N/A"

    if seconds < 1e-6:
        return f"{seconds * 1e9:.2f} ns"
    elif seconds < 1e-3:
        return f"{seconds * 1e6:.2f} µs"
    elif seconds < 1:
        return f"{seconds * 1e3:.2f} ms"
    else:
        return f"{seconds:.3f} s"


def compute_percent_change(baseline: Optional[float], current: Optional[float]) -> str:
    """Compute percent change from baseline to current."""
    if baseline is None or current is None:
        return "N/A"
    if baseline == 0:
        return "∞"

    change = ((current - baseline) / baseline) * 100
    sign = "+" if change > 0 else ""
    return f"{sign}{change:.1f}%"


def format_speedup(baseline: Optional[float], current: Optional[float]) -> str:
    """Format speedup as '1.5x faster' or '2.0x slower'."""
    if baseline is None or current is None:
        return "N/A"
    if current == 0:
        return "∞x faster"

    ratio = baseline / current
    if ratio >= 1.0:
        return f"{ratio:.2f}x faster"
    else:
        return f"{1/ratio:.2f}x slower"


def compare_versions(
    results_012: Path, results_020: Path, output_md: Path
) -> None:
    """
    Compare v0.1.2 and v0.2.0 benchmark results.

    Args:
        results_012: Directory containing v0.1.2 pyperf JSON files
        results_020: Directory containing v0.2.0 pyperf JSON files
        output_md: Output markdown file
    """
    # Benchmark file patterns to look for
    benchmarks = [
        ("resolve_10000", "resolve(10000)"),
        ("resolve_100000", "resolve(100000)"),
        ("resolve_250000", "resolve(250000)"),
        ("resolve_500000", "resolve(500000)"),
        ("pi_1000000", "pi(1000000)"),
        ("pi_10000000", "pi(10000000)"),
        ("pi_100000000", "pi(100000000)"),
        ("forecast_1000000_r1", "forecast(1000000, refinement=1)"),
        ("forecast_1000000_r2", "forecast(1000000, refinement=2)"),
        ("forecast_100000000_r1", "forecast(100000000, refinement=1)"),
        ("forecast_100000000_r2", "forecast(100000000, refinement=2)"),
        ("forecast_1000000000_r1", "forecast(1000000000, refinement=1)"),
        ("forecast_1000000000_r2", "forecast(1000000000, refinement=2)"),
        ("simulate_10000", "simulate(10000, list)"),
        ("simulate_100000", "simulate(100000, list)"),
        ("simulate_1000000", "simulate(1000000, list)"),
        ("simulate_10000_gen", "simulate(10000, generator)"),
        ("simulate_100000_gen", "simulate(100000, generator)"),
        ("simulate_1000000_gen", "simulate(1000000, generator)"),
    ]

    # Collect results
    results = []
    for file_pattern, label in benchmarks:
        path_012 = results_012 / f"{file_pattern}.json"
        path_020 = results_020 / f"{file_pattern}.json"

        data_012 = load_pyperf_result(path_012)
        data_020 = load_pyperf_result(path_020)

        time_012 = extract_mean_time(data_012) if data_012 else None
        time_020 = extract_mean_time(data_020) if data_020 else None

        results.append((label, time_012, time_020))

    # Generate markdown
    with open(output_md, "w") as f:
        f.write("# lulzprime v0.1.2 vs v0.2.0 Benchmark Comparison\n\n")
        f.write("## Summary\n\n")
        f.write("| Benchmark | v0.1.2 | v0.2.0 | Change | Speedup |\n")
        f.write("|-----------|--------|--------|--------|----------|\n")

        for label, time_012, time_020 in results:
            time_012_str = format_time(time_012)
            time_020_str = format_time(time_020)
            change = compute_percent_change(time_012, time_020)
            speedup = format_speedup(time_012, time_020)

            f.write(f"| {label} | {time_012_str} | {time_020_str} | {change} | {speedup} |\n")

        f.write("\n## Notes\n\n")
        f.write("- Times are mean values across multiple runs\n")
        f.write("- Negative % change indicates v0.2.0 is faster\n")
        f.write("- Speedup shows relative performance (higher is better)\n")
        f.write("- N/A indicates benchmark data not available\n")

    print(f"Comparison written to: {output_md}")


def main():
    """Main entry point."""
    if len(sys.argv) != 4:
        print("Usage: compare.py <v0.1.2_results_dir> <v0.2.0_results_dir> <output.md>")
        print("\nExample:")
        print("  python compare.py results/v0.1.2 results/v0.2.0 summary.md")
        sys.exit(1)

    results_012 = Path(sys.argv[1])
    results_020 = Path(sys.argv[2])
    output_md = Path(sys.argv[3])

    if not results_012.is_dir():
        print(f"Error: {results_012} is not a directory", file=sys.stderr)
        sys.exit(1)

    if not results_020.is_dir():
        print(f"Error: {results_020} is not a directory", file=sys.stderr)
        sys.exit(1)

    compare_versions(results_012, results_020, output_md)


if __name__ == "__main__":
    main()
