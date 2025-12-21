#!/usr/bin/env python3
"""
Benchmark pi() function using pyperf.

Tests prime counting function at various upper bounds.
"""

import pyperf
from lulzprime.pi import pi


def bench_pi(loops, x):
    """Benchmark pi(x) for given upper bound."""
    # Sanity check on first run
    if loops == 1:
        result = pi(x)
        if x == 1000000:
            expected = 78498
            if result != expected:
                raise ValueError(f"pi({x}) = {result}, expected {expected}")

    # Actual benchmark loop
    t0 = pyperf.perf_counter()
    for _ in range(loops):
        pi(x)
    return pyperf.perf_counter() - t0


def add_cmdline_args(cmd, args):
    """Add custom command-line arguments."""
    cmd.extend(["--upper-bound", str(args.upper_bound)])


if __name__ == "__main__":
    runner = pyperf.Runner(add_cmdline_args=add_cmdline_args)
    runner.metadata["description"] = "Benchmark pi() - prime counting function"

    # Add custom argument for upper bound
    runner.argparser.add_argument(
        "--upper-bound", type=int, default=1000000,
        help="Upper bound for pi(x) (default: 1000000)"
    )
    args = runner.parse_args()

    # Run benchmark
    runner.bench_time_func(
        f"pi({args.upper_bound})",
        bench_pi,
        args.upper_bound,
    )
