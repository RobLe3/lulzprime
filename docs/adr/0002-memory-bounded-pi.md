# ADR 0002: Memory-Bounded π(x) Implementation

**Date:** 2025-12-17
**Status:** PROPOSED
**Decision Maker:** Core Team
**Related Issues:** docs/issues.md [CONSTRAINT-VIOLATION] Memory Exceeds 25MB Limit at Large Indices

---

## Context and Problem Statement

Scale characterization benchmarks (benchmarks/bench_scale_characterization.py) reveal that the current π(x) implementation violates Part 6 section 6.4 memory constraint at large indices.

**Measured Behavior:**
- resolve(50,000): 7.80 MB peak ✓ (within constraint)
- resolve(100,000): 16.24 MB peak ✓ (within constraint)
- resolve(250,000): **42.71 MB peak** ✗ (exceeds 25 MB limit by 71%)

**Root Cause:**
The current π(x) implementation uses Sieve of Eratosthenes with O(x) space complexity. For large prime values (e.g., p_250000 = 3,497,861), memory usage scales linearly with x, violating the < 25 MB constraint.

**Constraint Reference:**
- Part 2 section 2.5: "Memory: Prefer < 25 MB for core functionality"
- Part 6 section 6.4: "Target memory envelope (core): < 25 MB resident set for typical usage"
- Part 6 section 6.2: "Must work on ≤ 4 GB RAM, single-core CPU, no GPU"

**Business Impact:**
- Prevents usage on low-end devices (SBCs, old laptops, small VPS) at large indices
- Violates stated design constraint for hardware efficiency (G2)
- Blocks production deployment for indices > 150k

---

## Decision Drivers

1. **Must satisfy Part 6 memory constraint** (< 25 MB) for indices up to at least 250k
2. **Must maintain Tier A guarantees** (exact, deterministic π(x))
3. **Must not change public API** (Part 4 contracts)
4. **Must not change resolve() workflow** (Part 5 section 5.3 compliance)
5. **Minimize implementation risk** and time to remediation
6. **Maintain alignment with OMPC principles** (G7)

---

## Option A: Segmented Sieve π(x) (RECOMMENDED)

### Description
Implement segmented sieve algorithm for π(x) with fixed memory window. Instead of creating a full sieve array of size x, process primes in fixed-size segments (e.g., 1M elements = ~125 KB per segment).

### Algorithm Overview
```
pi_segmented(x):
    if x < 2: return 0

    # Small primes generated once (< 125 KB for sqrt(x) up to ~16M)
    small_primes = simple_sieve(sqrt(x))

    count = len(small_primes)
    segment_size = 1_000_000  # Fixed memory window

    # Process range [sqrt(x), x] in segments
    for segment_start in range(sqrt(x), x, segment_size):
        segment_end = min(segment_start + segment_size, x)
        segment = create_segment(segment_start, segment_end)

        # Sieve segment using small_primes
        for p in small_primes:
            mark_multiples_in_segment(segment, p, segment_start)

        count += count_primes_in_segment(segment)

    return count
```

### Expected Complexity
- **Time:** O(x log log x) - same asymptotic complexity as current implementation
- **Space:** O(segment_size + sqrt(x)) ≈ O(1) for fixed segment size
  - Segment array: 1M elements = ~125 KB
  - Small primes: sqrt(x) / ln(sqrt(x)) primes ≈ ~100 KB for x = 10^7
  - **Total peak memory: ~250 KB** (well within 25 MB constraint)

### Expected Peak Memory Behavior
| Index   | p_n Value  | Segment Memory | Small Primes | Total  | Status |
|---------|------------|----------------|--------------|--------|--------|
| 50,000  | 611,953    | 125 KB         | 11 KB        | 136 KB | ✓      |
| 100,000 | 1,299,709  | 125 KB         | 17 KB        | 142 KB | ✓      |
| 250,000 | 3,497,861  | 125 KB         | 29 KB        | 154 KB | ✓      |
| 500,000 | 7,368,787  | 125 KB         | 42 KB        | 167 KB | ✓      |
| 1,000,000 | 15,485,863 | 125 KB       | 61 KB        | 186 KB | ✓      |

Memory usage becomes **constant** regardless of index.

### Impact on resolve() Workflow
- **No changes** to Part 5 section 5.3 execution chain
- π(x) interface remains identical (same input/output contract)
- Deterministic correction steps unchanged
- All existing tests continue to pass

### Implementation Changes Required
- Modify `src/lulzprime/pi.py:pi()` to use segmented sieve for x > threshold (e.g., 100k)
- Keep simple sieve for small x (< 100k) to avoid overhead
- Add `_segmented_sieve()` helper function
- No changes to public API

### Risks and Mitigations

**Risks:**
1. **Performance regression at small x**: Segmented sieve has overhead
   - **Mitigation:** Use threshold-based dispatch (simple sieve for x < 100k, segmented for x ≥ 100k)
2. **Implementation complexity**: Segment boundary handling
   - **Mitigation:** Extensive unit tests for boundary cases, reuse proven segmented sieve algorithms
3. **Off-by-one errors in segment counting**
   - **Mitigation:** Property-based testing, verify against known π(x) values

**Risk Level:** LOW to MEDIUM

### Test Plan
1. **Correctness Tests:**
   - Verify π(x) matches known values for x = 10^3, 10^4, 10^5, 10^6, 10^7
   - Test segment boundaries (powers of 2, segment_size ± 1)
   - Property test: π(x_segmented) == π(x_simple) for x < 10^6
2. **Memory Tests:**
   - Benchmark memory usage for resolve(50k, 100k, 250k, 500k, 1M)
   - Assert peak memory < 25 MB for all tested indices
   - Use tracemalloc for precise measurement
3. **Performance Tests:**
   - Benchmark time for resolve(10k, 100k, 250k) before/after
   - Allow up to 2x slowdown for indices > 100k (acceptable for memory compliance)
   - Ensure no regression for indices < 100k (threshold dispatch)
4. **Integration Tests:**
   - All existing tests continue to pass (52/52)
   - Determinism: Same inputs yield same outputs
   - Workflow compliance: Part 5 section 5.3 verified

### Implementation Effort
- **Estimated effort:** 2-4 hours
- **Files modified:** src/lulzprime/pi.py (single module)
- **Tests added:** 5-10 new tests in tests/test_pi.py
- **Benchmarks:** Rerun bench_scale_characterization.py

---

## Option B: True Sublinear π(x) (Lehmer-Style)

### Description
Implement true sublinear prime counting using Meissel-Lehmer algorithm or variants. This is the target specified in Part 6 section 6.3.

### Algorithm Overview
Uses combinatorial methods to count primes without explicit enumeration:
- Inclusion-exclusion over small primes
- Recursive structure with memoization
- O(x^(2/3)) time, O(x^(1/3)) space

### Expected Complexity
- **Time:** O(x^(2/3)) - true sublinear (better asymptotic than segmented sieve)
- **Space:** O(x^(1/3)) - sublinear memory growth
  - For x = 3,497,861 (p_250000): ~152 memory units
  - For x = 15,485,863 (p_1M): ~250 memory units

### Expected Peak Memory Behavior
Significantly better than both current sieve and segmented sieve for very large x (> 10^7), but overhead may be higher for moderate x due to memoization structures.

### Impact on resolve() Workflow
- No changes to Part 5 section 5.3 execution chain
- π(x) interface remains identical
- Deterministic correction unchanged

### Implementation Changes Required
- Complete rewrite of src/lulzprime/pi.py
- Implement Meissel-Lehmer algorithm with:
  - Phi function (combinatorial counting)
  - P2 and P3 correction terms
  - Memoization structures
- Significantly more complex than segmented sieve

### Risks and Mitigations

**Risks:**
1. **High implementation complexity**: Lehmer algorithm is subtle and error-prone
   - **Mitigation:** Extensive literature review, reference implementation analysis
2. **Correctness risk**: Easy to introduce off-by-one errors in combinatorial terms
   - **Mitigation:** Exhaustive testing against known π(x) values, cross-validation with sieve
3. **Performance regression for small x**: Higher overhead than sieve for x < 10^6
   - **Mitigation:** Hybrid approach with sieve fallback for small x
4. **Longer development time**: 5-10x more complex than segmented sieve
   - **Mitigation:** Schedule as future work, not immediate remediation

**Risk Level:** HIGH

### Test Plan
Same as Option A, plus:
- Cross-validation against segmented sieve for x < 10^7
- Extensive property-based testing for combinatorial correctness
- Performance profiling to validate O(x^(2/3)) scaling

### Implementation Effort
- **Estimated effort:** 20-40 hours (research + implementation + validation)
- **Files modified:** src/lulzprime/pi.py (major rewrite)
- **Tests added:** 20+ new tests for Lehmer-specific logic
- **Risk:** High - defers constraint violation fix

---

## Option C: Hybrid Approach (Segmented Now, Lehmer Later)

### Description
Implement segmented sieve (Option A) immediately to restore memory compliance, then implement Lehmer-style sublinear π(x) (Option B) as future enhancement.

### Rationale
- **Short-term:** Restore < 25 MB compliance within hours (low risk)
- **Long-term:** Achieve Part 6 section 6.3 sublinear target (high value)
- **Incremental:** Each step is independently valuable and testable

### Implementation Phases
1. **Phase 1 (Immediate):** Segmented sieve
   - Restore memory compliance
   - Maintain all guarantees
   - Low implementation risk
2. **Phase 2 (Future):** Lehmer-style sublinear
   - Improve asymptotic complexity
   - Further reduce memory for very large x (> 10^7)
   - Research and validation time allocated properly

### Impact on resolve() Workflow
- Phase 1: No changes
- Phase 2: No changes (π(x) interface unchanged)

### Risks and Mitigations
- **Risk:** Potential duplication of effort
  - **Mitigation:** Segmented sieve is simpler, serves as validation baseline for Lehmer
- **Risk:** Phase 2 may never happen
  - **Mitigation:** Phase 1 alone satisfies all Part 6 constraints; Phase 2 is optimization, not requirement

**Risk Level:** LOW

### Test Plan
- Phase 1: Same as Option A
- Phase 2: Same as Option B, with regression tests ensuring Phase 1 remains as fallback

### Implementation Effort
- **Phase 1:** 2-4 hours (same as Option A)
- **Phase 2:** 20-40 hours (same as Option B, but lower pressure)

---

## Decision Matrix

| Criteria                          | Option A (Segmented) | Option B (Lehmer) | Option C (Hybrid) |
|-----------------------------------|---------------------|-------------------|-------------------|
| Restores < 25 MB compliance       | ✓ Yes               | ✓ Yes             | ✓ Yes             |
| Maintains Tier A guarantees       | ✓ Yes               | ✓ Yes             | ✓ Yes             |
| No public API changes             | ✓ Yes               | ✓ Yes             | ✓ Yes             |
| Implementation risk               | ✓ Low               | ✗ High            | ✓ Low (Phase 1)   |
| Time to remediation               | ✓ 2-4 hours         | ✗ 20-40 hours     | ✓ 2-4 hours       |
| Asymptotic complexity improvement | ~ Same O(x log log x) | ✓ O(x^(2/3))    | ✓ Both (eventual) |
| Aligns with Part 6 section 6.3    | ~ Partial           | ✓ Full            | ✓ Full (eventual) |
| Memory at p_250000                | ✓ ~150 KB           | ✓ ~20 KB          | ✓ ~150 KB (Phase 1) |
| Memory at p_10M                   | ✓ ~200 KB           | ✓ ~50 KB          | ✓ ~200 KB → ~50 KB |

---

## Recommended Decision: **Option C (Hybrid Approach)**

### Primary Recommendation: Implement Segmented Sieve Immediately (Phase 1)

**Rationale:**
1. **Constraint compliance:** Restores < 25 MB memory limit for indices up to 1M+
2. **Low risk:** Well-understood algorithm with straightforward implementation
3. **Fast remediation:** Unblocks production use at large indices within hours
4. **Maintains all guarantees:** No regression in correctness, determinism, or workflow
5. **Provides validation baseline:** Segmented sieve output validates future Lehmer implementation
6. **Aligned with Part 6:** Satisfies section 6.4 memory constraint (< 25 MB)

**Why not Option B alone:**
- High implementation risk for immediate remediation
- 20-40 hour effort delays constraint violation fix
- Can be pursued as enhancement after compliance restored

**Why not Option A alone:**
- Doesn't close gap to Part 6 section 6.3 sublinear target
- Hybrid approach provides both short-term fix and long-term alignment

### Secondary Recommendation: Schedule Lehmer Implementation (Phase 2)

Add to docs/todo.md as future work with:
- Dependency: Requires Phase 1 completion
- Success criterion: O(x^(2/3)) time, O(x^(1/3)) space, cross-validated against segmented sieve
- Priority: Medium (optimization, not constraint violation)

---

## Implementation Plan (Phase 1: Segmented Sieve)

### Step 1: Implement segmented sieve backend
- **File:** src/lulzprime/pi.py
- **Changes:**
  - Add `_segmented_sieve(x, segment_size=1_000_000)` function
  - Modify `pi(x)` to dispatch based on threshold:
    - x < 100,000: Use existing `_simple_sieve()` (no overhead)
    - x ≥ 100,000: Use `_segmented_sieve()` (bounded memory)
  - Keep `_pi_simple()` as reference fallback for testing
- **Expected lines of code:** ~80-120 new lines

### Step 2: Add correctness tests
- **File:** tests/test_pi.py
- **Tests:**
  - test_pi_segmented_correctness: Verify against known π(x) values (10^3 to 10^7)
  - test_pi_segmented_vs_simple: Property test for x < 10^6
  - test_pi_segment_boundaries: Edge cases at segment boundaries
  - test_pi_threshold_dispatch: Verify correct algorithm selection

### Step 3: Add memory compliance tests
- **File:** tests/test_memory_compliance.py (NEW)
- **Tests:**
  - test_resolve_memory_250k: Assert resolve(250000) uses < 25 MB
  - test_resolve_memory_500k: Assert resolve(500000) uses < 25 MB
  - test_resolve_memory_1M: Assert resolve(1000000) uses < 25 MB

### Step 4: Rerun scale characterization benchmarks
- **Command:** python benchmarks/bench_scale_characterization.py
- **Expected Results:**
  - resolve(50,000): < 1 MB peak ✓
  - resolve(100,000): < 1 MB peak ✓
  - resolve(250,000): < 1 MB peak ✓ (down from 42.71 MB)
  - resolve(500,000): < 1 MB peak ✓
  - resolve(1,000,000): < 2 MB peak ✓

### Step 5: Update documentation
- **Files:**
  - docs/issues.md: Add "Proposed remediation" section with link to this ADR
  - docs/todo.md: Update with Phase 1 tasks completed, add Phase 2 tasks
  - benchmarks/results/summary.md: Update with new memory measurements
  - docs/milestones.md: Add milestone when Phase 1 complete

### Step 6: Commit and verify
- Run full test suite: pytest -q (expect 52+ tests passing)
- Verify no API changes: Public interface unchanged
- Verify workflow compliance: Part 5 section 5.3 execution chain unchanged
- Commit with message: "Fix memory constraint violation via segmented sieve"

---

## Consequences

### Positive
- **Immediate compliance:** Restores < 25 MB constraint for all practical indices
- **Unblocks production:** Enables deployment on low-end devices at large indices
- **Low risk:** Well-tested algorithm with clear correctness properties
- **No breaking changes:** Public API and workflow unchanged
- **Provides baseline:** Segmented sieve validates future Lehmer implementation
- **G2 satisfied:** Hardware efficiency goal restored

### Negative
- **Not true sublinear:** Still O(x log log x) time (Part 6 section 6.3 target is O(x^(2/3)))
- **Two-phase approach:** Requires future work to fully close spec gap
- **Slight performance overhead:** Threshold dispatch adds branch (negligible)

### Neutral
- **Code complexity:** Modest increase (~100 LOC) in pi.py
- **Test surface:** Adds 5-10 new tests (improves coverage)
- **Memory vs time tradeoff:** Bounded memory may be slightly slower for very small x (mitigated by threshold)

---

## Validation

### Pre-Implementation Validation
- [x] Reviewed Part 2, Part 6 constraints
- [x] Reviewed Part 5 workflow compliance requirements
- [x] Reviewed benchmark evidence (bench_scale_characterization.py results)
- [x] Reviewed existing π(x) implementation (src/lulzprime/pi.py)

### Post-Implementation Validation (Checklist)
- [ ] All tests pass (pytest -q shows 100% pass rate)
- [ ] Memory compliance verified at indices 50k, 100k, 250k, 500k, 1M (all < 25 MB)
- [ ] No public API changes (Part 4 contracts unchanged)
- [ ] No workflow changes (Part 5 section 5.3 compliance maintained)
- [ ] Performance acceptable (no regression for x < 100k, acceptable slowdown for x ≥ 100k)
- [ ] Documentation updated (issues.md, todo.md, summary.md, milestones.md)
- [ ] Committed and pushed to main

---

## References

- **Issue:** docs/issues.md - [CONSTRAINT-VIOLATION] Memory Exceeds 25MB Limit at Large Indices
- **Benchmark Evidence:** benchmarks/bench_scale_characterization.py, benchmarks/results/summary.md
- **Constraints:** docs/manual/part_2.md (section 2.5), docs/manual/part_6.md (sections 6.3, 6.4)
- **Workflow:** docs/manual/part_5.md (section 5.3)
- **Goals:** docs/manual/part_9.md (G2 Hardware Efficiency, G7 OMPC Alignment)
- **Canonical Reference:** paper/OMPC_v1.33.7lulz.pdf

---

**End of ADR 0002**
