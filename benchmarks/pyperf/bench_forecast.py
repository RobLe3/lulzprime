#!/usr/bin/env python3
"""
Benchmark forecast() function using pyperf.

Tests prime approximation at various upper bounds and refinement levels.
"""

import pyperf
from lulzprime import forecast


def bench_forecast(loops, n, refinement_level):
    """Benchmark forecast(n, refinement_level) for given upper bound."""
    # Detect if forecast() supports refinement_level parameter (v0.2.0+)
    # v0.1.2 only has forecast(index), v0.2.0+ has forecast(index, refinement_level=1)
    try:
        # Try v0.2.0+ API first
        test_result = forecast(n, refinement_level=refinement_level)
        supports_refinement = True
    except TypeError:
        # Fall back to v0.1.2 API (no refinement_level)
        test_result = forecast(n)
        supports_refinement = False
        if refinement_level != 1:
            # v0.1.2 doesn't support refinement levels, skip this benchmark
            raise ValueError(
                f"forecast() in this version doesn't support refinement_level parameter. "
                f"Requested refinement_level={refinement_level}, but only default is available."
            )

    # Sanity check on first run
    if loops == 1:
        if n == 100000:
            # forecast(100000) approximates the 100,000th prime ≈ 1,299,709
            # Allow reasonable tolerance for approximation
            if not (1250000 < test_result < 1350000):
                raise ValueError(
                    f"forecast({n}) = {test_result}, expected ~1,299,709"
                )

    # Actual benchmark loop
    t0 = pyperf.perf_counter()
    if supports_refinement:
        for _ in range(loops):
            forecast(n, refinement_level=refinement_level)
    else:
        for _ in range(loops):
            forecast(n)
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
