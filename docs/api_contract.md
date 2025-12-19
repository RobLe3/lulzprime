# API Contract

**LULZprime – Public API Guarantees, Tiers, and Misuse Cases**

---

## Purpose

This document formalizes the public API contract for LULZprime, defining explicit guarantees, constraints, and boundaries for all exported functions.

It serves as the canonical reference for:
- What each function guarantees (correctness, determinism, performance)
- What each function does NOT guarantee
- Tier classifications (A, B, C)
- Misuse cases that users must avoid

**Canonical references:**
- [OMPC Paper](https://roblemumin.com/library.html) (conceptual foundation)
- `docs/manual/part_4.md` (API specification)
- `docs/manual/part_9.md` (alignment goals)

---

## Guarantee Tiers

LULZprime defines three guarantee tiers to prevent ambiguous correctness claims:

### Tier A (Exact)
- **Definition**: Returns the exact mathematical value by construction
- **Verification**: Proven correct via workflow (forecast → π(x) → primality confirmation)
- **Functions**: `resolve(index)`
- **Promise**: Output is always the exact p_index, never approximate
- **Example**: `resolve(100)` always returns exactly 541 (the 100th prime)

### Tier B (Verified)
- **Definition**: Returns confirmed primes via primality testing
- **Verification**: Each returned value passes deterministic primality test
- **Functions**: `between(x, y)`, `next_prime(n)`, `prev_prime(n)`, `is_prime(n)`
- **Promise**: If returns True or a prime, that value is verified prime (no false positives)
- **Example**: `is_prime(541)` returns True only after deterministic Miller-Rabin verification

### Tier C (Estimate)
- **Definition**: Returns approximate values for navigation, NOT exact truth
- **Verification**: None (estimate only, no correctness guarantee)
- **Functions**: `forecast(index)`
- **Promise**: Fast O(1) approximation, typically within ~1% of true value
- **Warning**: `forecast(index)` may NOT equal `resolve(index)`, may not be prime

---

## Public API Functions

### resolve(index: int) -> int

**Tier**: A (Exact)

**Purpose**: Return the exact nth prime p_index.

**Guarantees:**
- Exact by construction (uses forecast → π(x) → primality-confirmed correction)
- Deterministic (same index always yields same result)
- No hidden network access or precomputation
- Workflow compliance per Part 5 section 5.3

**Input Constraints:**
- index >= 1 (1-based indexing)
- index must be integer
- Practical limit: ≤ ~250,000 (completes within minutes)
- Stress limit: > 500,000 may exceed 30 minutes

**Does NOT Guarantee:**
- Bounded runtime for arbitrary large indices
- Cryptographic properties (not suitable for security)
- Sublinear time complexity (current: O(x log log x) where x ≈ p_index)

---

### forecast(index: int) -> int

**Tier**: C (Estimate)

**Purpose**: Return an analytic estimate for p_index (navigation only).

**Guarantees:**
- Deterministic estimate (same index yields same estimate)
- Fast O(1) computation
- Typically within ~1% of true value for large indices

**Input Constraints:**
- index >= 1
- index must be integer
- No practical upper bound (formula works for arbitrarily large indices)

**Does NOT Guarantee:**
- Exactness (forecast(index) may NOT equal resolve(index))
- Primality (returned value may not be prime)
- Bounded error (relative error varies with index)

**CRITICAL WARNING:**
- Do NOT use `forecast()` as if it returns exact primes
- Use `resolve()` for exact primes
- `forecast()` is for navigation ONLY

---

### between(x: int, y: int) -> list[int]

**Tier**: B (Verified)

**Purpose**: Return all primes in [x, y] via localized primality testing.

**Guarantees:**
- All returned values are verified primes
- Complete (all primes in range returned, none skipped)
- Deterministic (same range yields same list)

**Input Constraints:**
- x <= y (valid range)
- y >= 2 (no primes below 2)
- Practical limit: ranges with < ~10,000 primes complete quickly

**Does NOT Guarantee:**
- Sublinear complexity in range size (linear in candidates tested)
- Bounded runtime for arbitrarily large ranges

---

### next_prime(n: int) -> int

**Tier**: B (Verified)

**Purpose**: Return the smallest prime >= n.

**Guarantees:**
- Returned value is verified prime
- Minimal (smallest prime >= n, not a larger one)
- Deterministic

**Input Constraints:**
- n must be integer
- Practical limit: n < 10^15 (deterministic primality test range)

**Does NOT Guarantee:**
- Bounded runtime (depends on gap to next prime, average ~log n)
- Cryptographic properties

---

### prev_prime(n: int) -> int

**Tier**: B (Verified)

**Purpose**: Return the largest prime <= n.

**Guarantees:**
- Returned value is verified prime
- Maximal (largest prime <= n, not a smaller one)
- Deterministic

**Input Constraints:**
- n >= 2 (no primes below 2)
- n must be integer
- Practical limit: n < 10^15

**Does NOT Guarantee:**
- Bounded runtime (depends on gap to previous prime)
- Cryptographic properties

---

### is_prime(n: int) -> bool

**Tier**: B (Verified)

**Purpose**: Deterministic primality test for n < 2^64.

**Guarantees:**
- Deterministic and correct for n < 2^64 (~1.8 × 10^19)
- No false positives (if True, n is guaranteed prime)
- No false negatives (if n is prime and n < 2^64, returns True)

**Input Constraints:**
- n >= 0
- n must be integer
- Deterministic guarantee valid for n < 2^64

**Does NOT Guarantee:**
- Cryptographic security (not a crypto primitive)
- Constant time execution (timing may leak information)
- Suitability for security-critical applications

**WARNING:**
Not suitable for cryptographic applications. Use established cryptographic libraries for security-sensitive primality testing.

---

### simulate(n_steps, *, seed, diagnostics, ...) -> list[int] | tuple

**Tier**: N/A (Simulation output, not exact primes)

**Purpose**: Generate pseudo-primes for testing and validation.

**Guarantees:**
- Reproducible (same seed yields same sequence)
- Statistically prime-like (reproduces expected density/gaps)
- Fast (no primality testing required)

**Input Constraints:**
- n_steps > 0
- seed must be integer or None

**Does NOT Guarantee:**
- Exactness (simulate(n)[i] may NOT equal resolve(i))
- Primality (returned values may not be prime)
- Cryptographic properties
- Truth generation (output is for validation, not authoritative)

**CRITICAL MISUSE WARNING:**
- DO NOT use `simulate()` output as if it were exact primes
- Use `resolve()` for exact primes
- Use `is_prime()` to verify primality
- Simulation output has NO mathematical guarantee of primality

---

### resolve_many(indices: Iterable[int]) -> list[int]

**Tier**: A (Exact)

**Purpose**: Efficiently resolve multiple prime indices in a single call.

**Guarantees:**
- Tier A (Exact): Each result is exact p_index, same as resolve()
- Deterministic: Same indices always yield same results in same order
- Order preservation: Results match input order exactly
- No global state: π(x) cache exists only during this call

**Input Constraints:**
- Each index must be >= 1 (1-based indexing)
- Each index must be integer
- Duplicates allowed (will compute each independently)
- Practical limit per batch: ~100 indices (to stay within benchmark caps)
- Each index subject to same limits as resolve() (≤ ~250k practical)

**Optimization Strategy:**
- Internally sorts indices to minimize π(x) recomputation
- Caches π(x) results within this single batch execution using local closure
- Dependency injection: passes cached π(x) function to internal resolver
- No global state mutation or monkeypatching
- No persistent cache (cache discarded after return)
- Thread-safe by design (no shared mutable state)
- Speedup depends on index locality (sorted indices share π(x) work)

**Performance Envelope:**
- Small batches (< 10): seconds (similar to loop)
- Medium batches (10-100): faster than loop (π(x) caching benefit)
- Large batches (100+): may exceed benchmark time caps

**Does NOT Guarantee:**
- Bounded runtime for arbitrary large batches
- Parallelization (single-threaded execution)
- Memory efficiency beyond O(batch_size) for results

**Example:**
```python
# Efficient batch resolution
indices = [1, 10, 100, 50, 25]
primes = lulzprime.resolve_many(indices)
# Returns: [2, 29, 541, 229, 97] (order preserved)
```

---

### between_many(ranges: Iterable[tuple[int,int]]) -> list[list[int]]

**Tier**: B (Verified)

**Purpose**: Efficiently query primes in multiple ranges.

**Guarantees:**
- Tier B (Verified): All returned primes are verified
- Deterministic: Same ranges always yield same results
- Order preservation: Results match input range order
- Completeness: All primes in each range returned

**Input Constraints:**
- Each range must be (x, y) tuple with x <= y
- y must be >= 2 for each range
- Practical limit: ranges with < ~10,000 primes each
- Batch size: reasonable number of ranges (< 100)

**Performance Envelope:**
- Linear in total primes returned
- No cross-range optimization (each range independent)

**Does NOT Guarantee:**
- Cross-range optimization or caching
- Parallelization

**Example:**
```python
# Batch range queries
ranges = [(10, 20), (100, 110)]
results = lulzprime.between_many(ranges)
# Returns: [[11, 13, 17, 19], [101, 103, 107, 109]]
```

---

## Misuse Cases

### Critical Misuses (Must Never Occur)

1. **Using forecast() as exact primes:**
   ```python
   # ✗ WRONG: forecast() is estimate only
   primes = [lulzprime.forecast(i) for i in range(1, 101)]

   # ✓ CORRECT: Use resolve() for exact primes
   primes = [lulzprime.resolve(i) for i in range(1, 101)]
   ```

2. **Using simulate() as exact primes:**
   ```python
   # ✗ WRONG: simulate() is not exact
   primes = lulzprime.simulate(100, seed=42)

   # ✓ CORRECT: Use resolve() for exact primes
   primes = [lulzprime.resolve(i) for i in range(1, 101)]
   ```

3. **Cryptographic use cases:**
   ```python
   # ✗ WRONG: Not suitable for cryptographic key generation
   p = lulzprime.resolve(1000)
   q = lulzprime.resolve(1001)
   n = p * q  # DO NOT use for RSA modulus

   # ✓ CORRECT: Use established cryptographic libraries
   from cryptography.hazmat.primitives.asymmetric import rsa
   private_key = rsa.generate_private_key(...)
   ```

4. **Unbounded index assumptions:**
   ```python
   # ✗ WRONG: May exceed practical runtime limits
   p = lulzprime.resolve(1_000_000)  # Impractical (30+ minutes)

   # ✓ CORRECT: Stay within practical limits
   if index <= 250_000:
       p = lulzprime.resolve(index)
   else:
       print("Index exceeds practical limit, see benchmark_policy.md")
   ```

5. **Security-critical applications:**
   ```python
   # ✗ WRONG: Not suitable for security
   if lulzprime.is_prime(candidate):
       use_as_crypto_key(candidate)  # DO NOT

   # ✓ CORRECT: Use cryptographic libraries
   from cryptography.hazmat.primitives.asymmetric import rsa
   # Use established crypto libraries for security
   ```

### Common Misunderstandings

1. **"LULZprime can predict primes"**
   - **FALSE**: LULZprime navigates to primes using analytic forecasting + exact correction
   - It does not "predict" or "guess" primes
   - All exact results (Tier A, B) are verified, not predicted

2. **"forecast() returns primes"**
   - **FALSE**: forecast() returns estimates (Tier C), not exact primes
   - Use resolve() for exact primes

3. **"LULZprime breaks cryptography"**
   - **FALSE**: LULZprime is a navigation toolkit, not a cryptographic attack
   - No factorization shortcuts, no RSA breaks
   - See Part 0 section 0.5 and Part 2 Non-Goals

4. **"All indices work equally fast"**
   - **FALSE**: Performance scales with index size
   - Practical limit: ~250,000 (minutes)
   - Stress limit: 500,000+ (impractical, 30+ minutes)
   - See docs/benchmark_policy.md for measured data

---

## Performance Expectations

### Practical Index Ranges (Phase 1)

| Index Range | Expected Runtime | Use Case |
|-------------|------------------|----------|
| 1 - 1,000 | Milliseconds | Scripting, interactive use |
| 1,000 - 100,000 | Seconds | Batch processing |
| 100,000 - 250,000 | Minutes | Large-scale tasks |
| 500,000+ | Impractical (30+ min) | Future work (Phase 2) |

**Note**: Phase 2 (true sublinear π(x) via Meissel-Lehmer) will improve large-index performance. Current implementation uses segmented sieve (O(x log log x)).

### Optional Parallel Acceleration

**Opt-in parallel π(x) backend available** (added 2025-12-17, ADR 0004):

LULZprime provides an optional `pi_parallel()` function that leverages multi-core CPUs to reduce wall-clock time for large indices:

```python
from lulzprime.pi import pi_parallel

# Use parallel backend for large x
count = pi_parallel(1_000_000, workers=4)  # ~3-5x faster than pi(1_000_000)
```

**Characteristics:**
- **Opt-in only**: Not used by default, must be explicitly called
- **Deterministic**: Bit-identical results to `pi()` for same inputs
- **Multi-core speedup**: 3-5x faster for x >= 1M on 4-8 core CPUs
- **Threshold-based**: Automatically falls back to sequential for x < 1M (avoids overhead)
- **Memory safe**: Bounded memory per worker, same constraints as `pi()`

**Use cases:**
- Large-scale batch processing (resolve_many with pi_fn=pi_parallel)
- Interactive exploration at 500k+ indices (reduces wait time)
- Development workflow where 30+ min is impractical

**Not suitable for:**
- Small x (< 1M): overhead dominates, no benefit
- Security-critical applications: same as `pi()`, not crypto-safe
- True sublinear complexity: still O(x log log x), just parallelized

**Advanced: Wiring pi_parallel into resolution pipeline**

For advanced users who want to use parallel π(x) in the resolution workflow, you can use the internal API with dependency injection:

```python
from lulzprime.lookup import resolve_internal_with_pi
from lulzprime.pi import pi_parallel

# Example 1: Direct resolution with parallel π(x)
# Note: This is internal API, use at your own risk
index = 500_000
prime = resolve_internal_with_pi(index, pi_parallel)  # Uses parallel π(x)

# Example 2: Manual batch with parallel π(x)
# Note: resolve_many() does not currently expose pi_fn parameter
# Advanced users can implement custom batch logic:
from lulzprime.pi import pi_parallel, _simple_sieve
import math

def resolve_many_parallel(indices: list[int], workers: int = 4) -> list[int]:
    """Custom batch resolution using pi_parallel."""
    # Create cached version of pi_parallel
    def cached_pi_parallel(x: int) -> int:
        return pi_parallel(x, workers=workers)

    # Use dependency injection for each index
    return [resolve_internal_with_pi(idx, cached_pi_parallel) for idx in indices]

# Usage
primes = resolve_many_parallel([100_000, 200_000, 300_000], workers=4)
```

**Note:** The above examples use internal APIs (`resolve_internal_with_pi`) which are subject to change. Future enhancement may expose `pi_fn` parameter in public `resolve_many()` API.

**See also:**
- docs/adr/0004-parallel-pi.md for implementation details
- Part 6 section 6.3: Phase 2 sublinear π(x) remains future work

---

## Determinism and Reproducibility

**All Tier A and Tier B functions are deterministic:**
- Same inputs always yield same outputs
- No hidden randomness or network access
- No environment-dependent behavior (except for performance)

**Tier C (forecast) is deterministic:**
- Same index always yields same estimate
- Estimate formula is fixed (refined PNT approximation)

**Simulation (simulate) requires explicit seed for determinism:**
- `simulate(n, seed=42)` is reproducible
- `simulate(n, seed=None)` uses system randomness (non-deterministic)

---

## Contract Violations

**The following behaviors violate the API contract:**

1. **Silent correctness changes**: Changing Tier A/B output without version bump
2. **Hidden precomputation**: Loading large prime tables without user consent
3. **Network access**: Making network requests without explicit documentation
4. **Non-determinism**: Returning different values for same inputs (except simulate with seed=None)
5. **Unbounded blocking**: Hanging indefinitely without progress indication

**If a violation is discovered:**
- File an issue: https://github.com/RobLe3/lulzprime/issues
- Reference: docs/issues.md (BUG or CONSTRAINT-VIOLATION)

---

## References

- **Canonical paper**: [OMPC at roblemumin.com](https://roblemumin.com/library.html)
- **Public API spec**: docs/manual/part_4.md
- **Workflows**: docs/manual/part_5.md
- **Performance constraints**: docs/manual/part_6.md
- **Project goals**: docs/manual/part_9.md
- **Benchmark policy**: docs/benchmark_policy.md
- **Open issues**: docs/issues.md

---

## Success Condition

This API contract is effective if:
- Users understand what each function guarantees and does NOT guarantee
- Misuse cases are clearly documented and avoided
- Tier A/B/C classifications prevent ambiguous correctness claims
- Performance expectations are realistic and documented
- Contract violations are rare and quickly identified

---

**Effective Date:** 2025-12-17
**Version:** v0.1.0-dev
**Policy Owner:** Core Team
**Review Frequency:** After major API changes or performance improvements

---

End of API contract.
