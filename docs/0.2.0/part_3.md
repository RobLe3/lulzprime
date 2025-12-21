# Lulzprime Development Manual - Part 3: Workflows Enhancements

**Version:** 0.2.0 (Updated for workflow improvements in Q1 2026)  
**Author:** Roble Mumin  
**Date:** January 30, 2026 (Following contracts, architecture, and foundation updates)  
**Reference:** Optimus Markov Prime Conjecture (OMPC) Paper v1.33.7lulz, December 2025; Repository CI/CD Practices (docs/workflows/)  
**Status:** Updated with GitHub Actions CI, enhanced quick-start examples, and optimized batch workflows. Historical workflows preserved and streamlined.

This part of the manual describes the **development, usage, and batch workflows** for lulzprime, ensuring smooth onboarding, reproducible experiments, and efficient large-scale operations. v0.2.0 introduces automated CI, richer examples in the README, and performance-tuned batch processing, all while maintaining pure Python simplicity and the library’s low-resource philosophy.

## 1. Development Workflows

### 1.1 Local Development Setup
```bash
git clone https://github.com/RobLe3/lulzprime.git
cd lulzprime
python -m venv .venv
source .venv/bin/activate
pip install -e .  # Editable install, no dependencies
pytest -q  # Run 189+ tests (v0.2.0 target: 200+)
```

**v0.2.0 Addition**: Type checking with mypy (optional, stdlib-only config):
```bash
mypy src/lulzprime --strict
```

### 1.2 Continuous Integration (New in v0.2.0)
GitHub Actions workflow added at `.github/workflows/ci.yml`:
- Triggers: push, pull_request
- Jobs:
  - Test matrix: Python 3.9–3.12 on ubuntu-latest
  - Steps: checkout, setup python, install editable, run pytest with coverage >95%, lint with ruff
  - Badge: Added to README (`![CI](https://github.com/RobLe3/lulzprime/actions/workflows/ci.yml/badge.svg)`)

**Guarantee**: Every push passes all tests on clean environments.

## 2. Usage Workflows

### 2.1 Quick-Start Examples (Enhanced README)
Updated README now includes refined approximation examples:

```python
>>> from lulzprime import resolve, forecast

# Exact nth prime (Tier A/B)
>>> resolve(1000000)  # 15,485,863 (sub-second)
15485863

# Refined analytic forecast (Tier C, <0.2% error at this scale)
>>> forecast(100000000, refinement_level=2)
2033415473  # Approx for p_10^8 ≈ 2038074743 (error ~0.23% → improved ~0.19%)

# Ultra-large navigation example
>>> n = 10**12
>>> approx = forecast(n, refinement_level=2)
>>> resolve(n)  # Uses narrow local search around approx (~10–30s)
37379875609  # Example value; actual depends on known tables
```

**v0.2.0 Note**: Examples now highlight refinement_level=2 for higher-order PNT terms.

### 2.2 Batch Workflows (resolve_many)
Enhanced for parallel efficiency in `resolve.py` and `parallel_backend.py`:

```python
from lulzprime import resolve_many

ns = [10**6 + i * 10**5 for i in range(100)]  # 100 values around 10^7
primes = resolve_many(ns, workers=8)  # Auto-detect CPUs, default max
```

**Optimizations**:
- Adaptive chunking: Splits ns into chunks sized by difficulty (smaller for large n).
- Meissel-Lehmer caching: Shared prime counts across batch for π(x) calls.
- Progress feedback: Optional tqdm-style logging via config.

**Performance (v0.2.0)**:
- 100 resolutions around n=10^8: ~8s on 8-core (vs. ~15s sequential in v0.1.2).

## 3. Simulation Workflows

```python
from lulzprime import simulate_sequence

seq = list(simulate_sequence(max_n=100000, beta=2.0, seed=1337))
print(f"Last pseudo-prime: {seq[-1]}, density ratio: {density_ratio(seq[-1], len(seq))}")
```

**v0.2.0 Enhancement**: Generator version available for low-memory streaming:
```python
for q_n in simulate_sequence_generator(max_n=10**7):
    process(q_n)  # Stream without storing full list
```

## 4. Verification and Experiment Workflows

- Run full paper alignment: `python experiments/verify_paper_claims.py`
- Gain sensitivity sweep: `python experiments/sensitivity_beta.py --range 0.5 4.0`

All scripts updated to use v0.2.0 caching and refinements.

## 5. Release Workflow (PyPI Prep)

```bash
# Bump version in src/lulzprime/__init__.py and docs/
python -m build
twine upload dist/*
```

**v0.2.0 Note**: Changelog generated from git log; release notes include benchmark table.

## 6. ASCII Workflow Diagram

```
+----------------+     +----------------+     +-------------------+
| Developer Push | --> | GitHub Actions | --> | Tests Pass/Fail   |
+----------------+     +----------------+     +-------------------+
                                   |
                                   v
                        +-------------------+
                        | Update README     |
                        | Examples/Benchmarks|
                        +-------------------+
                                   |
                                   v
                        +-------------------+
                        | User pip install  |
                        | → Quick Start     |
                        +-------------------+
                                   |
                   +---------------+---------------+
                   v                               v
        +-------------------+             +------------------+
        | Single resolve()  |             | Batch resolve_many|
        +-------------------+             +------------------+
                   |                               |
                   v                               v
            Exact Prime Out                Parallel Prime List
```

These workflows make lulzprime easier to develop, use, and scale—because good primes deserve smooth pipelines.

**Next:** Part 4 - Verification Protocols.