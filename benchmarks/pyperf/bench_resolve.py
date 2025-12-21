#!/usr/bin/env python3
"""
Benchmark resolve() function using pyperf.

Tests exact prime resolution at various index sizes.
"""

import pyperf
from lulzprime import resolve


def bench_resolve(loops, n):
    """Benchmark resolve(n) for given index."""
    # Sanity check on first run
    if loops == 1:
        result = resolve(n)
        if n == 100000:
            expected = 1299709
            if result != expected:
                raise ValueError(f"resolve({n}) = {result}, expected {expected}")

    # Actual benchmark loop
    t0 = pyperf.perf_counter()
    for _ in range(loops):
        resolve(n)
    return pyperf.perf_counter() - t0


def add_cmdline_args(cmd, args):
    """Add custom command-line arguments."""
    cmd.extend(["--index", str(args.index)])


if __name__ == "__main__":
    runner = pyperf.Runner(add_cmdline_args=add_cmdline_args)
    runner.metadata["description"] = "Benchmark resolve() - exact nth prime resolution"

    # Add custom argument for index
    runner.argparser.add_argument(
        "--index", type=int, default=10000,
        help="Prime index to resolve (default: 10000)"
    )
    args = runner.parse_args()

    # Run benchmark
    runner.bench_time_func(
        f"resolve({args.index})",
        bench_resolve,
        args.index,
    )
