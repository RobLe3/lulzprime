# ADR 0004: Parallel π(x) Implementation

**Date:** 2025-12-17
**Status:** PROPOSED
**Decision Maker:** Core Team
**Related Issues:** docs/issues.md [PERFORMANCE] resolve(500,000) exceeds acceptable runtime

---

## Context and Problem Statement

Scale characterization benchmarks reveal that resolve(500,000) and resolve(1,000,000) exceed 30 minutes runtime, making these indices impractical for development workflow and routine testing.

**Measured Behavior:**
- resolve(250,000): Minutes (acceptable, within constraints)
- resolve(500,000): 30+ minutes (impractical, exceeds benchmark policy caps)
- resolve(1,000,000): 30+ minutes (impractical)

**Root Cause:**
The current π(x) implementation uses segmented sieve with O(x log log x) time complexity. While memory-compliant (< 25 MB per ADR 0002), this remains linear in x and does not leverage multi-core CPUs for parallel processing.

**Constraint References:**
- docs/benchmark_policy.md: Default time cap is 60 seconds per index
- docs/issues.md: 500k+ indices documented as impractical with current implementation
- Part 6 section 6.3: Target is true sublinear π(x) (O(x^(2/3))) - not yet implemented

**Business Impact:**
- Blocks development workflow for indices beyond 250k
- Prevents routine testing at stress benchmark levels (500k+)
- Multi-core CPUs are common but remain unutilized
- Phase 2 (true sublinear Lehmer-style π(x)) remains future work (20-40 hour effort)

**Opportunity:**
Implement opt-in parallel π(x) backend that leverages multi-core CPUs to reduce wall-clock time for large indices, providing practical improvement while Phase 2 sublinear implementation remains scheduled.

---

## Decision Drivers

1. **Must preserve determinism** - Same inputs must yield same outputs regardless of parallelism
2. **Must preserve Tier A guarantees** - Exact, verified π(x) counting
3. **Must be opt-in** - Default behavior unchanged, no automatic parallelization
4. **Must maintain memory compliance** - No regression beyond < 25 MB constraint
5. **Must be safe with dependency injection** - Works with batch API's pi_fn pattern
6. **Must provide clear failure modes** - Fallback to single-core if parallelization fails
7. **No external dependencies** - Use stdlib only (multiprocessing module)

---

## Option A: Threading (concurrent.futures.ThreadPoolExecutor)

### Description
Use Python's threading to parallelize segment processing across multiple threads.

### Expected Complexity
- Same algorithmic complexity: O(x log log x)
- Wall-clock speedup: ~1x (negligible due to GIL)

### Pros
- Simpler than multiprocessing (shared memory)
- No serialization overhead
- Lower process creation overhead

### Cons
- **GIL bottleneck**: Python's Global Interpreter Lock prevents true parallelism for CPU-bound work
- **No speedup expected**: Sieve marking is CPU-bound, GIL limits to single-core performance
- **Misleading API**: Would imply parallelism but deliver sequential performance

### Risk Level
LOW (implementation simple) but **HIGH (zero benefit due to GIL)**

---

## Option B: Multiprocessing (concurrent.futures.ProcessPoolExecutor)

### Description
Use Python's multiprocessing to parallelize segment processing across multiple processes, each with independent GIL.

### Algorithm Overview
```python
def pi_parallel(x: int, workers: int | None = None) -> int:
    """
    Count primes <= x using parallel segmented sieve.

    Strategy:
    1. Generate small primes up to sqrt(x) (sequential, small cost)
    2. Divide range [sqrt(x), x] into disjoint segments
    3. Process each segment in parallel (independent workers)
    4. Aggregate counts in deterministic order (segment order)

    Determinism:
    - Segment boundaries are deterministic (fixed by x and worker count)
    - Each segment is independent (no shared mutable state)
    - Aggregation is ordered (sum segments in ascending order)
    - Result is bit-identical to sequential for same x
    """
    if workers is None:
        workers = min(os.cpu_count() or 1, 8)

    # Small primes (sequential)
    sqrt_x = int(math.sqrt(x))
    small_primes = _simple_sieve(sqrt_x)
    count = len(small_primes)

    if x <= sqrt_x:
        return count

    # Divide range into segments
    segments = _create_segment_ranges(sqrt_x + 1, x, workers)

    # Process segments in parallel
    with ProcessPoolExecutor(max_workers=workers) as executor:
        # Each worker counts primes in its segment using small_primes
        segment_counts = executor.map(
            _count_segment_primes,
            segments,
            [small_primes] * len(segments)
        )

    # Aggregate in deterministic order (segment order preserved by map)
    count += sum(segment_counts)

    return count
```

### Expected Complexity
- **Time (wall-clock):** O(x log log x / workers) - linear speedup with worker count
- **Time (CPU total):** O(x log log x) - same total work as sequential
- **Space:** O(segment_size + sqrt(x)) per worker - bounded by segment size

### Expected Speedup
| Workers | Expected Speedup | resolve(500k) Time | resolve(1M) Time |
|---------|------------------|-------------------|------------------|
| 1 (seq) | 1x               | 30+ min           | 30+ min          |
| 2       | ~1.8x            | ~17 min           | ~17 min          |
| 4       | ~3.2x            | ~9 min            | ~9 min           |
| 8       | ~5.5x            | ~5 min            | ~5 min           |

Note: Speedup is sublinear due to:
- Small primes generation overhead (sequential)
- Process creation overhead
- Segment aggregation overhead
- Diminishing returns as overhead dominates

### Determinism Guarantee
**Critical requirement:** Results must be bit-identical to sequential for same inputs.

**How determinism is ensured:**
1. **Segment boundaries are deterministic:** Fixed by x and worker count
2. **Each segment is independent:** No shared mutable state between workers
3. **Aggregation order is fixed:** Sum segments in ascending segment_start order
4. **No floating-point arithmetic:** All operations use exact integer math
5. **No random decisions:** Segment allocation is deterministic

**Validation:**
- Property test: `pi_parallel(x, workers=W) == pi(x)` for all x and W
- Determinism test: Multiple runs of `pi_parallel(x, workers=W, seed=S)` yield identical results

### Impact on resolve() Workflow
- **No automatic usage:** pi_parallel() is opt-in only
- **No changes to resolve():** Default pi() remains unchanged
- **Safe with dependency injection:** Can pass pi_parallel as pi_fn to resolve_internal_with_pi()
- **Fallback available:** If parallelization fails, fall back to sequential pi()

### Implementation Changes Required
- **src/lulzprime/pi.py:**
  - Add `pi_parallel(x, workers=None)` function
  - Add `_count_segment_primes(segment, small_primes)` worker function
  - Add `_create_segment_ranges(start, end, num_segments)` helper
- **src/lulzprime/config.py:**
  - Add `ENABLE_PARALLEL_PI = False` (opt-in flag)
  - Add `PARALLEL_PI_WORKERS = min(os.cpu_count() or 1, 8)` (default worker count)
- **No changes to public API:** pi_parallel() is a new optional function

### Risks and Mitigations

**Risks:**
1. **Process creation overhead for small x:** Multiprocessing has startup cost
   - **Mitigation:** Use threshold (e.g., only parallelize for x >= 1M)
2. **Serialization overhead for small_primes:** Must pickle small_primes list
   - **Mitigation:** Small primes list is small (< 1 MB for x < 100M)
3. **Non-determinism if aggregation is unordered:** Sum order matters for floating-point
   - **Mitigation:** Use integer-only math, preserve segment order in aggregation
4. **Worker spawn failures on some platforms:** May fail on restricted environments
   - **Mitigation:** Wrap in try/except, fallback to sequential pi()
5. **Memory multiplication:** Each worker holds segment + small_primes
   - **Mitigation:** Limit workers to 8, segment size remains bounded

**Risk Level:** MEDIUM

### Test Plan
1. **Correctness Tests:**
   - Property test: `pi_parallel(x, workers=W) == pi(x)` for x in [1e5, 1e6, 1e7]
   - Edge cases: x < 2, x = 2, x = sqrt threshold
2. **Determinism Tests:**
   - Multiple runs of `pi_parallel(x, workers=W)` yield identical results
   - Different worker counts yield identical results (just different wall time)
3. **Input Validation Tests:**
   - workers <= 0 raises ValueError
   - workers = None uses default (cpu_count)
   - x < 0 raises ValueError (same as pi())
4. **Fallback Tests:**
   - If ProcessPoolExecutor fails, fallback to sequential pi()
   - Verify fallback preserves correctness
5. **Performance Validation (NO LONG BENCHMARKS):**
   - Smoke test: pi_parallel(100_000, workers=2) completes within seconds
   - No formal benchmarking beyond smoke tests (per benchmark_policy.md)

### Implementation Effort
- **Estimated effort:** 3-5 hours
- **Files modified:**
  - src/lulzprime/pi.py: Add pi_parallel() and helpers (~100 LOC)
  - src/lulzprime/config.py: Add config flags (~5 LOC)
  - tests/test_pi.py: Add 8-10 new tests (~150 LOC)
- **No external dependencies:** Uses stdlib multiprocessing only

---

## Option C: Hybrid (Parallel for Large x, Sequential for Small x)

### Description
Combine Options A and B: Use sequential pi() for small x (< 1M), parallel pi_parallel() for large x (>= 1M).

### Rationale
- Process creation overhead dominates for small x (< 1M)
- Parallelism only beneficial when segment work >> overhead
- Threshold at 1M balances overhead vs speedup

### Implementation
```python
def pi_parallel(x: int, workers: int | None = None, threshold: int = 1_000_000) -> int:
    """Parallel π(x) with automatic fallback to sequential for small x."""
    if x < threshold:
        # Small x: overhead dominates, use sequential
        return pi(x)

    # Large x: parallelism beneficial
    return _pi_parallel_impl(x, workers)
```

### Pros
- Avoids overhead for small x
- Preserves fast path for common use cases
- Automatically falls back when parallelism not beneficial

### Cons
- Adds complexity (threshold decision)
- Threshold may need tuning for different hardware

### Risk Level
LOW (builds on Option B with simple threshold check)

---

## Decision Matrix

| Criteria                          | Option A (Threading) | Option B (Multiprocessing) | Option C (Hybrid) |
|-----------------------------------|---------------------|---------------------------|-------------------|
| True parallelism (multi-core)     | ✗ No (GIL)          | ✓ Yes                     | ✓ Yes             |
| Expected speedup at 500k          | ~1x (no benefit)    | ~3-5x (4-8 workers)       | ~3-5x (4-8 workers) |
| Determinism guarantee             | ✓ Yes               | ✓ Yes                     | ✓ Yes             |
| Memory compliance                 | ✓ Yes               | ✓ Yes (bounded)           | ✓ Yes             |
| Implementation risk               | ✓ Low               | ~ Medium                  | ~ Medium          |
| No external dependencies          | ✓ Yes               | ✓ Yes                     | ✓ Yes             |
| Overhead for small x              | ✓ Low               | ✗ High                    | ✓ Low (threshold) |
| Useful for resolve(500k+)         | ✗ No                | ✓ Yes                     | ✓ Yes             |

---

## Recommended Decision: **Option C (Hybrid Parallel π(x))**

### Primary Recommendation: Implement multiprocessing with threshold

**Rationale:**
1. **True multi-core parallelism:** Only multiprocessing bypasses GIL for CPU-bound work
2. **Practical speedup:** 3-5x faster for large indices (500k+), bringing 30+ min down to ~5-10 min
3. **Opt-in design:** Default pi() unchanged, no automatic parallelization
4. **Deterministic:** Segment boundaries and aggregation order are fixed
5. **Memory safe:** Bounded segment size prevents memory explosion
6. **No external deps:** Uses stdlib multiprocessing only
7. **Threshold optimization:** Avoids overhead for small x where parallelism not beneficial

**Why not Option A:**
- Threading provides zero benefit for CPU-bound sieve work due to GIL
- Would mislead users about parallelism without delivering speedup

**Why not Option B alone:**
- Process creation overhead hurts small x performance
- Hybrid (Option C) provides same benefit with better small-x behavior

### Failure Modes and Fallback

**Explicit failure modes:**
1. **Process spawn failure:** Platform doesn't support multiprocessing
   - **Fallback:** Catch exception, use sequential pi()
2. **Worker crash:** Segment processing raises exception
   - **Fallback:** Catch exception, use sequential pi()
3. **Timeout (optional):** Workers hang indefinitely
   - **Fallback:** ProcessPoolExecutor timeout, use sequential pi()

**Fallback guarantee:**
- If pi_parallel() fails for any reason, fall back to sequential pi()
- User-visible error message logged (optional, not required)
- Result correctness always preserved

---

## Implementation Plan

### Step 1: Implement pi_parallel() in pi.py
- **File:** src/lulzprime/pi.py
- **Changes:**
  - Add `pi_parallel(x, workers=None)` function
  - Add `_create_segment_ranges(start, end, num_workers)` helper
  - Add `_count_segment_primes(segment_start, segment_end, small_primes)` worker
  - Implement threshold check (x < 1M → use sequential pi())
  - Implement try/except fallback to pi() if parallelization fails
- **Expected LOC:** ~120 new lines

### Step 2: Wire configuration in config.py
- **File:** src/lulzprime/config.py
- **Changes:**
  - Add `ENABLE_PARALLEL_PI = False` (opt-in flag, not used yet)
  - Add `PARALLEL_PI_WORKERS = min(os.cpu_count() or 1, 8)` (default)
  - Add `PARALLEL_PI_THRESHOLD = 1_000_000` (minimum x for parallelism)
- **Expected LOC:** ~10 new lines
- **Note:** These config options are for future use, not wired into resolve() yet

### Step 3: Add correctness and determinism tests
- **File:** tests/test_pi.py
- **Tests:**
  - `test_pi_parallel_correctness_small`: Verify pi_parallel(1e5) == pi(1e5)
  - `test_pi_parallel_correctness_large`: Verify pi_parallel(1e6) == pi(1e6)
  - `test_pi_parallel_determinism`: Multiple runs yield same result
  - `test_pi_parallel_workers`: Different worker counts yield same result
  - `test_pi_parallel_threshold`: x < threshold uses sequential path
  - `test_pi_parallel_invalid_workers`: workers <= 0 raises ValueError
  - `test_pi_parallel_fallback`: If multiprocessing fails, fallback works
  - `test_pi_parallel_edge_cases`: x < 2, x = 2, etc.
- **Expected LOC:** ~150 new test lines
- **Time cap compliance:** All tests complete within seconds (no stress benchmarks)

### Step 4: Update documentation
- **File:** docs/api_contract.md
  - Add section on optional parallel acceleration
  - Note: opt-in only, not used by default
  - Mention determinism guarantee
- **File:** README.md (if exists, otherwise skip)
  - Add short note on enabling parallel π(x)
  - Example usage: `pi_parallel(1_000_000, workers=4)`

### Step 5: Run tests
- **Command:** `pytest -q`
- **Expected:** All tests pass (91+ existing + ~8 new = 99+ tests)
- **Time cap:** Test suite completes within normal time (< 60 seconds)

### Step 6: Commit and push
- **Commit message:** "Add opt-in parallel π(x) backend (multiprocessing)"
- **Update:** docs/milestones.md with implementation details
- **Verify:** No breaking changes, all existing tests pass

---

## Consequences

### Positive
- **Faster wall-time for large indices:** 3-5x speedup for 500k+ indices
- **Practical 500k+ resolution:** Brings 30+ min down to ~5-10 min (usable)
- **Multi-core utilization:** Leverages commonly available multi-core CPUs
- **Opt-in design:** No breaking changes, no automatic behavior change
- **Deterministic:** Same correctness and reproducibility guarantees as sequential
- **No external deps:** Uses stdlib only

### Negative
- **Increased code complexity:** ~120 LOC for parallel implementation
- **Process overhead for small x:** Mitigated by threshold, but adds branch
- **Platform dependency:** multiprocessing behavior varies (Windows vs Unix)
- **Memory multiplication:** Workers each hold segment + small_primes (bounded)

### Neutral
- **Not true sublinear:** Still O(x log log x), just parallelized
- **Phase 2 (Lehmer) remains future work:** This is a wall-time optimization, not algorithmic improvement
- **Opt-in means manual invocation:** Users must explicitly call pi_parallel()

---

## Validation

### Pre-Implementation Validation
- [x] Reviewed docs/issues.md (PERFORMANCE issue at 500k)
- [x] Reviewed docs/benchmark_policy.md (time cap requirements)
- [x] Reviewed existing pi() implementation (segmented sieve)
- [x] Reviewed dependency injection pattern (batch API uses pi_fn)

### Post-Implementation Validation (Checklist)
- [ ] All tests pass (pytest -q shows 100% pass rate)
- [ ] pi_parallel(x) == pi(x) for tested x values (correctness)
- [ ] Determinism verified (multiple runs, different worker counts)
- [ ] Fallback tested (multiprocessing failure gracefully handled)
- [ ] No breaking changes (existing API unchanged)
- [ ] Documentation updated (api_contract.md, README if exists)
- [ ] Committed and pushed to main

---

## References

- **Issue:** docs/issues.md - [PERFORMANCE] resolve(500,000) exceeds acceptable runtime
- **Benchmark Policy:** docs/benchmark_policy.md (time caps, stress benchmark approval)
- **ADR 0002:** docs/adr/0002-memory-bounded-pi.md (memory-bounded π(x) implementation)
- **Constraints:** docs/manual/part_6.md (section 6.3 sublinear target, section 6.4 memory)
- **API Contract:** docs/api_contract.md (performance expectations)
- **Canonical Reference:** paper/OMPC_v1.33.7lulz.pdf

---

**End of ADR 0004**
