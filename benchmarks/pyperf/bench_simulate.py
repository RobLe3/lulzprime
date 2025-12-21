#!/usr/bin/env python3
"""
Benchmark simulate() function using pyperf.

Tests prime simulation in both list and generator modes.
"""

import pyperf
from lulzprime import simulate


def bench_simulate_list(loops, n_steps, seed):
    """Benchmark simulate() in list mode."""
    # Sanity check on first run
    if loops == 1:
        result = simulate(n_steps, seed=seed)
        if not isinstance(result, list):
            raise ValueError(f"simulate({n_steps}, seed={seed}) did not return list")
        if len(result) != n_steps:
            raise ValueError(
                f"simulate({n_steps}, seed={seed}) returned {len(result)} steps, "
                f"expected {n_steps}"
            )

    # Actual benchmark loop
    t0 = pyperf.perf_counter()
    for _ in range(loops):
        result = simulate(n_steps, seed=seed)
        # Minimal consumption to ensure list is fully materialized
        _ = len(result)
    return pyperf.perf_counter() - t0


def bench_simulate_generator(loops, n_steps, seed):
    """Benchmark simulate() in generator mode."""
    # Sanity check on first run
    if loops == 1:
        gen = simulate(n_steps, seed=seed, as_generator=True)
        result = list(gen)
        if len(result) != n_steps:
            raise ValueError(
                f"simulate({n_steps}, seed={seed}, as_generator=True) "
                f"yielded {len(result)} steps, expected {n_steps}"
            )

    # Actual benchmark loop
    t0 = pyperf.perf_counter()
    for _ in range(loops):
        gen = simulate(n_steps, seed=seed, as_generator=True)
        # Consume generator with cheap reduction
        count = 0
        last = None
        for value in gen:
            count += 1
            last = value
        # Use values to prevent optimization
        _ = (count, last)
    return pyperf.perf_counter() - t0


def add_cmdline_args(cmd, args):
    """Add custom command-line arguments."""
    cmd.extend(["--n-steps", str(args.n_steps)])
    cmd.extend(["--seed", str(args.seed)])
    if args.generator_mode:
        cmd.append("--generator-mode")


if __name__ == "__main__":
    runner = pyperf.Runner(add_cmdline_args=add_cmdline_args)
    runner.metadata["description"] = "Benchmark simulate() - prime sequence simulation"

    # Add custom arguments
    runner.argparser.add_argument(
        "--n-steps", type=int, default=10000,
        help="Number of simulation steps (default: 10000)"
    )
    runner.argparser.add_argument(
        "--seed", type=int, default=42,
        help="Random seed for reproducibility (default: 42)"
    )
    runner.argparser.add_argument(
        "--generator-mode", action="store_true",
        help="Benchmark generator mode (as_generator=True)"
    )
    args = runner.parse_args()

    # Select appropriate benchmark function
    if args.generator_mode:
        bench_name = f"simulate({args.n_steps}, seed={args.seed}, as_generator=True)"
        runner.bench_time_func(
            bench_name,
            bench_simulate_generator,
            args.n_steps,
            args.seed,
        )
    else:
        bench_name = f"simulate({args.n_steps}, seed={args.seed})"
        runner.bench_time_func(
            bench_name,
            bench_simulate_list,
            args.n_steps,
            args.seed,
        )
