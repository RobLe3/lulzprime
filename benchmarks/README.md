# Benchmarks

Performance benchmarks for LULZprime.

## Purpose

Benchmarks verify performance claims from `docs/manual/part_6.md` and track regression thresholds from `docs/manual/part_9.md`.

## Benchmark Files

- `bench_resolve.py` - Benchmark resolve() performance
- `bench_between.py` - Benchmark between() range resolution
- `results/` - Benchmark results (not committed, generated locally)

## Running Benchmarks

```bash
# Run specific benchmark
python benchmarks/bench_resolve.py

# Compare results
python benchmarks/bench_resolve.py --compare results/baseline.json
```

## Performance Constraints

From Part 6, section 6.3:

- `forecast()` → O(1)
- `π(x)` → sublinear (Lehmer-style), bounded memory
- `resolve()` → dominated by small number of π(x) calls + primality checks
- `between()` → linear in number of primes returned, not range width

## Memory Constraints

From Part 2, section 2.5:

- Core functionality target: < 25 MB resident memory

## Reporting

Benchmark results should include:
- Operation tested
- Input characteristics (index range, values)
- Time statistics (mean, median, p95, p99)
- Memory usage
- Comparison to thresholds

Store results in `results/` directory with timestamps.

**Do not commit large benchmark data files** (per `docs/defaults.md` section 4).
