#!/usr/bin/env python3
"""Generate benchmark comparison summary from pyperf JSON results."""

import json
from pathlib import Path

def load_result(path):
    """Load pyperf JSON and extract mean time."""
    try:
        with open(path) as f:
            data = json.load(f)
        if "benchmarks" in data and len(data["benchmarks"]) > 0:
            bench = data["benchmarks"][0]
            if "runs" in bench:
                values = []
                for run in bench["runs"]:
                    if "values" in run:
                        values.extend(run["values"])
                if values:
                    return sum(values) / len(values)
    except:
        pass
    return None

def format_time(seconds):
    """Format time in human-readable units."""
    if seconds is None:
        return "N/A"
    if seconds < 1e-6:
        return f"{seconds * 1e9:.1f} ns"
    elif seconds < 1e-3:
        return f"{seconds * 1e6:.2f} µs"
    elif seconds < 1:
        return f"{seconds * 1e3:.0f} ms"
    else:
        return f"{seconds:.2f} s"

def speedup(old, new):
    """Calculate speedup."""
    if old is None or new is None:
        return "N/A"
    if new == 0:
        return "∞x"
    ratio = old / new
    if ratio >= 1:
        return f"{ratio:.1f}x faster"
    else:
        return f"{1/ratio:.1f}x slower"

results = []

# resolve benchmarks
for n in [10000, 100000, 250000, 500000]:
    old = load_result(f"v0.1.2/resolve_{n}.json")
    new = load_result(f"v0.2.0/resolve_{n}.json")
    results.append((f"resolve({n})", old, new))

# pi benchmarks
for x in [1000000, 10000000, 100000000]:
    old = load_result(f"v0.1.2/pi_{x}.json")
    new = load_result(f"v0.2.0/pi_{x}.json")
    results.append((f"pi({x})", old, new))

# forecast benchmarks
for n in [1000000, 100000000, 1000000000]:
    old_r1 = load_result(f"v0.1.2/forecast_{n}_r1.json")
    new_r1 = load_result(f"v0.2.0/forecast_{n}_r1.json")
    new_r2 = load_result(f"v0.2.0/forecast_{n}_r2.json")
    results.append((f"forecast({n}, r=1)", old_r1, new_r1))
    if new_r2:
        results.append((f"forecast({n}, r=2)", None, new_r2))

# simulate benchmarks
for n in [10000, 100000, 1000000]:
    old = load_result(f"v0.1.2/simulate_{n}.json")
    new = load_result(f"v0.2.0/simulate_{n}.json")
    if old or new:
        results.append((f"simulate({n}, list)", old, new))

# Print markdown table
print("# lulzprime v0.1.2 vs v0.2.0 Benchmark Results\n")
print("## Performance Comparison\n")
print("| Benchmark | v0.1.2 | v0.2.0 | Improvement |")
print("|-----------|--------|--------|-------------|")

for label, old, new in results:
    old_str = format_time(old)
    new_str = format_time(new)
    speedup_str = speedup(old, new)
    print(f"| {label} | {old_str} | {new_str} | {speedup_str} |")

print("\n## Key Findings\n")
print("### Major Performance Improvements")
pi_10e8_old = load_result("v0.1.2/pi_100000000.json")
pi_10e8_new = load_result("v0.2.0/pi_100000000.json")
if pi_10e8_old and pi_10e8_new:
    speedup_val = pi_10e8_old / pi_10e8_new
    print(f"- **pi(10^8)**: {speedup_val:.1f}x faster ({format_time(pi_10e8_old)} → {format_time(pi_10e8_new)})")
    print("  - Meissel-Lehmer algorithm enabled (O(x^(2/3)) vs O(x log log x))")

resolve_500k_old = load_result("v0.1.2/resolve_500000.json")
resolve_500k_new = load_result("v0.2.0/resolve_500000.json")
if resolve_500k_old and resolve_500k_new:
    speedup_val = resolve_500k_old / resolve_500k_new
    print(f"- **resolve(500000)**: {speedup_val:.1f}x faster ({format_time(resolve_500k_old)} → {format_time(resolve_500k_new)})")

print("\n### New Features in v0.2.0")
print("- **forecast() refinement levels**: Added optional refinement_level parameter")
print("- **Generator mode**: Added as_generator parameter for simulate() (not benchmarked)")

print("\n### Notes")
print("- All times are mean values from multiple pyperf runs")
print("- v0.1.2 does not support forecast() refinement_level parameter")
print("- v0.1.2 does not support simulate() generator mode")
print("- Some benchmarks incomplete due to time constraints")
