# Benchmarks

Performance benchmarks for LULZprime.

## Purpose

Benchmarks verify performance claims from `docs/manual/part_6.md` and track regression thresholds from `docs/manual/part_9.md`.

## Directory Structure

```
benchmarks/
├── harness/              # Benchmark orchestration and analysis
│   ├── env_info.py       # Environment metadata capture
│   ├── compare.py        # Compare results across versions
│   └── run_all.sh        # Run complete benchmark suite
├── pyperf/               # pyperf benchmark scripts
│   ├── bench_resolve.py  # Benchmark resolve(n) - exact nth prime
│   ├── bench_pi.py       # Benchmark pi(x) - prime counting
│   ├── bench_forecast.py # Benchmark forecast(n) - approximation
│   └── bench_simulate.py # Benchmark simulate(N) - prime simulation
├── results/              # Benchmark results (not committed, generated locally)
└── README.md             # This file
```

## Quick Start

### Running All Benchmarks

```bash
# Run complete benchmark suite
./benchmarks/harness/run_all.sh

# Results will be saved to: benchmarks/results/<timestamp>_<hostname>/
```

### Running Individual Benchmarks

```bash
# Benchmark resolve(n) for various indices
python3 benchmarks/pyperf/bench_resolve.py --index 100000

# Benchmark pi(x) for various upper bounds
python3 benchmarks/pyperf/bench_pi.py --upper-bound 1000000

# Benchmark forecast(n) with refinement levels
python3 benchmarks/pyperf/bench_forecast.py --upper-bound 100000000 --refinement-level 2

# Benchmark simulate(N) in list mode
python3 benchmarks/pyperf/bench_simulate.py --n-steps 100000 --seed 42

# Benchmark simulate(N) in generator mode
python3 benchmarks/pyperf/bench_simulate.py --n-steps 100000 --seed 42 --generator-mode
```

## Version Comparison Workflow

To compare performance between lulzprime versions (e.g., v0.1.2 vs v0.2.0):

### 1. Set Up Isolated Environments

```bash
# Create venv for v0.1.2
python3 -m venv .venv-0.1.2
source .venv-0.1.2/bin/activate
pip install lulzprime==0.1.2 pyperf
deactivate

# Create venv for v0.2.0
python3 -m venv .venv-0.2.0
source .venv-0.2.0/bin/activate
pip install lulzprime==0.2.0 pyperf
deactivate
```

### 2. Run Benchmarks for Each Version

```bash
# Run v0.1.2 benchmarks
source .venv-0.1.2/bin/activate
./benchmarks/harness/run_all.sh benchmarks/results/v0.1.2
deactivate

# Run v0.2.0 benchmarks
source .venv-0.2.0/bin/activate
./benchmarks/harness/run_all.sh benchmarks/results/v0.2.0
deactivate
```

### 3. Generate Comparison Report

```bash
python3 benchmarks/harness/compare.py \
    benchmarks/results/v0.1.2 \
    benchmarks/results/v0.2.0 \
    benchmarks/results/comparison_summary.md

# View the report
cat benchmarks/results/comparison_summary.md
```

## Benchmark Coverage

### Core Functions (Tier A & B)

- **`resolve(n)`**: Exact nth prime resolution
  - Indices: 10^4, 10^5, 2.5×10^5, 5×10^5
  - Sanity check: resolve(100000) = 1299709

- **`pi(x)`**: Prime counting function
  - Upper bounds: 10^6, 10^7, 10^8
  - Sanity check: pi(1000000) = 78498

### Approximation Functions (Tier C)

- **`forecast(n, refinement_level)`**: Prime approximation
  - Upper bounds: 10^6, 10^8, 10^9
  - Refinement levels: 1, 2
  - Expected: <0.2% error for n ≥ 10^8 with refinement_level=2

- **`simulate(N, seed)`**: Prime sequence simulation
  - Step counts: 10^4, 10^5, 10^6
  - Modes: list (default), generator (as_generator=True)
  - Seed: 42 (for reproducibility)

## External Library Comparisons (Optional)

To compare lulzprime with external libraries:

```bash
# Install optional comparison libraries
pip install primesieve sympy prime-sieve

# Run benchmarks with same parameters
# (Results labeled separately as "external" comparisons)
```

**Note**: External library comparisons are best-effort and kept separate from apples-to-apples lulzprime version comparisons.

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
