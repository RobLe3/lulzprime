# Lulzprime Development Manual - Part 2: Contracts and Guarantees

**Version:** 0.2.0 (Updated for refined guarantees in Q1 2026)  
**Author:** Roble Mumin  
**Date:** January 25, 2026 (Following architecture optimizations and foundation updates)  
**Reference:** Optimus Markov Prime Conjecture (OMPC) Paper v1.33.7lulz, December 2025; Archived API Contracts from v0.1.2 (docs/manual/part_4.md integration)  
**Status:** Updated with strengthened API contracts, refined error bounds for ultra-large n, and explicit Tier guarantees. Historical contracts preserved and extended.

This part of the manual defines the **contracts and guarantees** provided by the lulzprime library, ensuring users and developers understand the reliability, exactness, and performance expectations of each function. In v0.2.0, contracts have been strengthened to reflect refined asymptotic approximations and handling of ultra-large indices (n > 10^15), while maintaining backward compatibility. All public APIs remain unchanged, with added documentation for new optional parameters and tighter bounds.

Contracts are categorized into three **Tiers** (as established in v0.1.2 and refined here):

- **Tier A: Exact** – Deterministic, mathematically proven correct results.
- **Tier B: Verified** – Probabilistic with verification to deterministic bounds (e.g., primality testing).
- **Tier C: Estimate** – Analytic approximation with bounded error (suitable for navigation/forecasting).

## 1. Core Guarantee Principles

- **Exactness Priority**: For accessible n (up to ~10^8–10^9 on consumer hardware), functions default to Tier A.
- **Scalability**: For larger n, fall back gracefully to Tier B/C with explicit warnings.
- **Purity and Determinism**: No randomness in final outputs for resolution functions; simulations are reproducible with fixed seeds.
- **Error Handling**: Invalid inputs (e.g., n < 1, non-integer) raise `ValueError` with clear messages.

**v0.2.0 Refinements**:
- Tightened Tier C relative error guarantees to <0.2% for n ≥ 10^8 (previously ~0.23–0.29%).
- Added support for n > 10^15 in Tier C with sub-0.1% projected errors.
- Explicit contracts for new caching behaviors (no side effects beyond performance).

## 2. Public API Contracts

### 2.1 resolve(n: int, mode: str = 'auto') -> int
**Description**: Returns the exact nth prime p_n.

**Contracts**:
- **Tier A (Exact)**: Guaranteed for n ≤ 10^8 (verified against known tables); uses Meissel-Lehmer π(x) + localized correction.
- **Tier B (Verified)**: For 10^8 < n ≤ 10^12, combines forecast with extensive Miller-Rabin witnesses (deterministic up to 10^18 bounds).
- **Tier C Fallback**: Not used; raises error if exactness cannot be verified.
- **Input**: n ≥ 1 (n=1 → 2).
- **Time**: Sub-second for n < 10^9; ~10–60s for n ~10^12 (improved ~20% in v0.2.0 via caching).
- **Raises**: ValueError for invalid n; RuntimeError if verification fails (rare).

**v0.2.0 Update**: Added 'auto' mode refines search window to ±0.1% of forecast.

### 2.2 forecast(n: int, refinement_level: int = 1) -> int
**Description**: Returns analytic approximation q̂(n) using refined PNT.

**Contracts**:
- **Tier C (Estimate)**: Relative error <0.3% for n ≥ 10^6; <0.2% for n ≥ 10^8 (v0.2.0 refinement).
- Formula: n * (log n + log log n - 1 + (log log n - 2)/log n * (refinement_level > 1)).
- **Input**: n ≥ 10 (warm-start recommended).
- **Time**: O(1), <1ms.
- **Use Case**: Navigation aid for resolve(); enables "jump and adjust" strategy (OMPC paper page 8).

**v0.2.0 Update**: refinement_level=2 adds higher-order terms; error bounds explicitly documented.

### 2.3 simulate(n: int, beta: float = 2.0, seed: Optional[int] = None) -> List[int]
**Description**: Generates pseudo-prime sequence using OMPC Markov model.

**Contracts**:
- **Tier C (Statistical)**: Sequence reproduces prime statistics (gaps, density) within 1σ variance.
- Reproducible with seed.
- Density ratio w → 1 ± 0.05 for large n.
- **Memory**: O(n) but generator variant available.
- **No Exactness Guarantee**: For statistical studies only.

**v0.2.0 Update**: Default beta=2.0 tuned for stability; annealing prep noted.

### 2.4 Other Functions (primality.is_prime, parallel_backend.resolve_many, etc.)
- **is_prime(x: int)**: Tier B – Deterministic for x < 2^64; probabilistic beyond with high confidence.
- **resolve_many(ns: List[int])**: Applies resolve() in parallel; maintains individual contracts.

## 3. Input Validation and Error Handling (v0.2.0 Enhanced)

All public functions now include:
```python
from typing import Optional

def _validate_n(n: int, min_n: int = 1) -> None:
    if not isinstance(n, int) or n < min_n:
        raise ValueError(f"n must be integer >= {min_n}, got {n!r}")
```

**Guarantee**: Clear, consistent errors; no silent failures.

## 4. Performance and Resource Contracts

- **Memory**: <50 MB peak for n=10^8 operations (reduced in v0.2.0).
- **CPU**: Single-threaded by default; multiprocessing safe.
- **Scalability**: Practical up to n=10^15+ via Tier C guidance.

## 5. Alignment with OMPC Paper

Contracts directly support paper claims (pages 8–9): Forecast errors enable narrow local tests, yielding 100–1,500× speedups. Full validation in `PAPER_ALIGNMENT_STATUS.md`.

These contracts ensure lulzprime is reliable for both research and production—exact where possible, transparent where approximate. Keep trusting the process, but verify the lulz.

**Next:** Part 3 - Workflows Enhancements.