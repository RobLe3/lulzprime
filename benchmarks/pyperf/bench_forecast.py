#!/usr/bin/env python3
"""
Benchmark forecast() function using pyperf.

Tests prime approximation at various upper bounds and refinement levels.
"""

import pyperf
from lulzprime import forecast


def bench_forecast(loops, n, refinement_level):
    """Benchmark forecast(n, refinement_level) for given upper bound."""
    # Sanity check on first run
    if loops == 1:
        result = forecast(n, refinement_level=refinement_level)
        if n == 1000000 and refinement_level == 2:
            # forecast returns float approximation, should be close to pi(1e6) = 78498
            # Allow reasonable tolerance for approximation
            if not (70000 < result < 85000):
                raise ValueError(
                    f"forecast({n}, refinement_level={refinement_level}) = {result}, "
                    f"expected ~78498"
                )

    # Actual benchmark loop
    t0 = pyperf.perf_counter()
    for _ in range(loops):
        forecast(n, refinement_level=refinement_level)
    return pyperf.perf_counter() - t0


def add_cmdline_args(cmd, args):
    """Add custom command-line arguments."""
    cmd.extend(["--upper-bound", str(args.upper_bound)])
    cmd.extend(["--refinement-level", str(args.refinement_level)])


if __name__ == "__main__":
    runner = pyperf.Runner(add_cmdline_args=add_cmdline_args)
    runner.metadata["description"] = "Benchmark forecast() - prime approximation"

    # Add custom arguments
    runner.argparser.add_argument(
        "--upper-bound", type=int, default=1000000,
        help="Upper bound for forecast(n) (default: 1000000)"
    )
    runner.argparser.add_argument(
        "--refinement-level", type=int, default=2,
        help="Refinement level (1 or 2, default: 2)"
    )
    args = runner.parse_args()

    # Run benchmark
    runner.bench_time_func(
        f"forecast({args.upper_bound}, refinement_level={args.refinement_level})",
        bench_forecast,
        args.upper_bound,
        args.refinement_level,
    )
