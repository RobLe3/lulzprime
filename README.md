# LULZprime

**Prime resolution and navigation library based on OMPC**

LULZprime is a Python library for efficient prime number resolution using analytic forecasting + exact correction, derived from the OMPC approach. It enables fast access to the nth prime and primes in numeric intervals without requiring full enumeration or sieving.

## What LULZprime Is

- **Prime navigator**: Efficiently locates primes using analytic forecasting + exact correction
- **Deterministic resolver**: Same inputs always yield same exact primes (Tier A guarantee)
- **Hardware efficient**: Runs on low-end devices (< 25 MB memory footprint)
- **Practical up to ~250k indices**: Completes within seconds to minutes for typical use cases
- **Well-defined guarantees**: Explicit Tier A/B/C contracts (exact, verified, estimate)

## What LULZprime Is NOT

- **NOT a cryptographic primitive**: Not suitable for security-critical applications
- **NOT suitable for unbounded indices**: Practical limit ~250,000 (indices > 500k impractical)
- **NOT a prime "predictor"**: Uses navigation, not prediction or guessing
- **NOT a factorization tool**: No shortcuts for integer factorization or RSA
- **NOT a replacement for crypto libraries**: Use established cryptographic tools for security

## Practical Index Range

**Current implementation (Phase 1):**
- **Small indices (< 1,000):** milliseconds - excellent for scripting
- **Medium indices (1,000 - 100,000):** seconds - practical for most tasks
- **Large indices (100,000 - 250,000):** minutes - acceptable for batch jobs
- **Stress indices (500,000+):** impractical (30+ minutes) - future work

See `docs/benchmark_policy.md` for measured performance data.

## Installation

```bash
pip install lulzprime
```

Or install from source:

```bash
git clone git@github.com:RobLe3/lulzprime.git
cd lulzprime
pip install -e .
```

## Quick Start

```python
import lulzprime

# Example 1: Get the exact 100th prime (Tier A: Exact)
p_100 = lulzprime.resolve(100)
print(f"The 100th prime is {p_100}")  # Output: 541 (exact, deterministic)

# Example 2: Get all primes in a range (Tier B: Verified)
primes = lulzprime.between(10, 30)
print(f"Primes from 10 to 30: {primes}")
# Output: [11, 13, 17, 19, 23, 29] (all verified primes)

# Example 3: Check primality (Tier B: Verified, deterministic for n < 2^64)
print(lulzprime.is_prime(541))  # True
print(lulzprime.is_prime(540))  # False

# Example 4: Navigate primes (Tier B: Verified)
next_p = lulzprime.next_prime(100)   # 101 (smallest prime >= 100)
prev_p = lulzprime.prev_prime(100)   # 97 (largest prime <= 100)

# Example 5: Estimate for navigation (Tier C: Estimate only, NOT exact)
estimate = lulzprime.forecast(100)   # ~540-545 (approximate, not exact)
# ⚠️  Use resolve() for exact primes, forecast() is for navigation only
```

## Public API

- **`resolve(index)`** → Returns the exact p_index (Tier A: Exact)
- **`forecast(index)`** → Returns an analytic estimate for p_index (Tier C: Estimate)
- **`between(x, y)`** → Returns all primes in [x, y] (Tier B: Verified)
- **`next_prime(n)`** → Returns smallest prime >= n (Tier B: Verified)
- **`prev_prime(n)`** → Returns largest prime <= n (Tier B: Verified)
- **`is_prime(n)`** → Primality predicate (Tier B: Verified)
- **`simulate(...)`** → OMPC simulator for pseudo-prime sequences (optional mode)

See `docs/manual/part_4.md` for complete API contracts.

## Core Concepts

LULZprime inherits from the OMPC approach:

1. **Analytic navigation**: Use refined Prime Number Theorem approximations to jump close to desired prime locations (O(1) estimates)
2. **Exact correction**: Use prime counting π(x) and primality tests to correct estimates and guarantee correctness
3. **Controlled stochastic modeling**: Optional simulator for validation and testing (not for truth generation)

This reframes primes from a brute-force enumeration problem into a navigable space.

**Canonical reference**: `paper/OMPC_v1.33.7lulz.pdf`

## Documentation

- **Quick start**: This README
- **Development manual**: `docs/manual/part_0.md` through `part_9.md`
- **API contracts**: `docs/manual/part_4.md`
- **Workflows**: `docs/manual/part_5.md`
- **Developer guide**: `docs/autostart.md` and `docs/defaults.md`
- **Canonical paper**: `paper/OMPC_v1.33.7lulz.pdf`

## Development

### Setup

```bash
# Clone repository
git clone git@github.com:RobLe3/lulzprime.git
cd lulzprime

# Install in development mode with dev dependencies
pip install -e ".[dev]"

# Run tests
pytest

# Run tests with coverage
pytest --cov=lulzprime --cov-report=html
```

### Project Structure

```
lulzprime/
├── src/lulzprime/      # Source code
├── tests/              # Test suite
├── docs/               # Documentation
│   ├── manual/         # Development manual (Parts 0-9)
│   ├── milestones.md   # Completed deliverables
│   ├── todo.md         # Planned work
│   └── issues.md       # Bugs and corrections
├── paper/              # Canonical OMPC paper
└── benchmarks/         # Performance benchmarks
```

### Contributing

See `CONTRIBUTING.md` for contribution guidelines.

**Important**: Before contributing, read:
1. `docs/autostart.md` - Startup procedure and parse order
2. `docs/defaults.md` - Repository rules and constraints
3. `docs/manual/part_0.md` through `part_9.md` - Development manual

## Non-Goals

LULZprime explicitly does **NOT** claim or implement:
- Factorization acceleration
- Cryptographic breaks (RSA/ECC/discrete log)
- "Predicting primes" as deterministic truth
- Replacement for cryptographic entropy sources

This library is an efficiency and navigation toolkit, consistent with the paper's scope.

## License

MIT License - See `LICENSE` file for details.

## Citation

If you use LULZprime in academic work, please cite the canonical OMPC paper:
```
[Citation details from paper/OMPC_v1.33.7lulz.pdf]
```

## Support

- **Issues**: https://github.com/RobLe3/lulzprime/issues
- **Documentation**: https://github.com/RobLe3/lulzprime/tree/main/docs
- **Repository**: https://github.com/RobLe3/lulzprime

---

**Status**: Alpha development (v0.1.0-dev)

Generated with documentation-first development approach.
