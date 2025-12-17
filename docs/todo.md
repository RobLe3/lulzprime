# todo.md
**LULZprime – Planned Work and Open Tasks**

---

## Purpose

This file records planned work that is not started or not assigned to an active effort.

Each todo item must reference:
- The manual part(s) it relates to
- The target module(s)
- The success criterion (what "done" means)

---

## Todo Item Format

```
## [Task Title]

**Related Parts:** Part X, Part Y

**Target Modules:** module.py

**Success Criterion:**
- Specific, measurable completion criteria

**Priority:** [High/Medium/Low]
```

---

## Open Tasks

### Phase 1: Implement Segmented Sieve π(x) (Memory Constraint Fix)

**Related Parts:** Part 2 (section 2.5), Part 4, Part 5, Part 6 (sections 6.3, 6.4)

**Target Modules:** src/lulzprime/pi.py, tests/test_pi.py

**Related Issue:** docs/issues.md [CONSTRAINT-VIOLATION] Memory Exceeds 25MB Limit at Large Indices

**Related ADR:** docs/adr/0002-memory-bounded-pi.md (Option C - Phase 1)

**Success Criterion:**
- Implement segmented sieve with fixed memory window (1M elements ≈ 125 KB)
- Memory usage < 25 MB for all indices up to 1M+ (resolves constraint violation)
- Threshold-based dispatch: simple sieve for x < 100k, segmented for x ≥ 100k
- Time complexity: O(x log log x) (same asymptotic as current)
- Space complexity: O(segment_size + sqrt(x)) ≈ O(1) for fixed segment size
- All existing tests continue to pass (52/52)
- Deterministic, exact counting maintained (Tier A guarantees)
- No public API changes
- No workflow changes (Part 5 section 5.3 compliance maintained)

**Dependency-Ordered Implementation Steps:**
1. Implement `_segmented_sieve(x, segment_size=1_000_000)` in src/lulzprime/pi.py
2. Modify `pi(x)` to dispatch based on threshold (x < 100k vs x ≥ 100k)
3. Add correctness tests in tests/test_pi.py:
   - test_pi_segmented_correctness (verify against known π(x) values)
   - test_pi_segmented_vs_simple (property test for x < 10^6)
   - test_pi_segment_boundaries (edge cases)
   - test_pi_threshold_dispatch (verify algorithm selection)
4. Add memory compliance tests in tests/test_memory_compliance.py (NEW):
   - test_resolve_memory_250k (assert < 25 MB)
   - test_resolve_memory_500k (assert < 25 MB)
   - test_resolve_memory_1M (assert < 25 MB)
5. Rerun scale characterization benchmarks:
   - python benchmarks/bench_scale_characterization.py
   - Verify all indices 50k/100k/250k/500k/1M use < 25 MB
6. Update documentation:
   - docs/issues.md: Add "Proposed remediation" section
   - benchmarks/results/summary.md: Update with new memory measurements
   - docs/milestones.md: Add milestone when complete
7. Commit and push

**Priority:** HIGH (blocks production use at large indices, violates Part 6 constraint)

**Expected Effort:** 2-4 hours

**Expected Memory at Key Indices:**
- resolve(250,000): ~150 KB (down from 42.71 MB) ✓
- resolve(500,000): ~170 KB ✓
- resolve(1,000,000): ~190 KB ✓

---

### Phase 2: Implement True Sublinear π(x) Backend (Lehmer-style)

**Related Parts:** Part 4, Part 5, Part 6 (section 6.3)

**Target Modules:** src/lulzprime/pi.py

**Related ADR:** docs/adr/0002-memory-bounded-pi.md (Option C - Phase 2)

**Dependency:** Requires Phase 1 (segmented sieve) completion

**Success Criterion:**
- π(x) uses true sublinear algorithm (Meissel-Lehmer or equivalent)
- Time complexity: O(x^(2/3)) or better (true sublinear, not O(x log log x))
- Space complexity: O(x^(1/3)) or less (sublinear memory)
- Cross-validated against segmented sieve for correctness (x < 10^7)
- Maintains deterministic behavior and Tier A guarantees
- Memory usage bounded per Part 2 constraints (< 25 MB)
- All existing tests continue to pass
- Performance improvement measurable via benchmarks for x > 10^7
- No public API changes
- Hybrid approach: use segmented sieve for x < 10^6, Lehmer for x ≥ 10^6

**Priority:** Medium (optimization, not constraint violation fix)

**Expected Effort:** 20-40 hours (research + implementation + validation)

**Current State:**
- π(x) uses Sieve of Eratosthenes: O(x log log x) time, O(x) space
- Phase 1 will use segmented sieve: O(x log log x) time, O(1) space
- Both are optimized linear, not true sublinear
- Phase 1 satisfies Part 2/Part 6 memory constraints
- Phase 2 achieves Part 6 section 6.3 asymptotic complexity target

**Why This Matters:**
- Part 6 section 6.3 specifies "π(x) → sublinear (Lehmer-style), bounded memory"
- Phase 1 satisfies memory constraint but not asymptotic complexity target
- True sublinear methods enable better scaling for very large x (> 10^7)
- Completes full alignment with Part 6 performance model

**Notes:**
- Keep Phase 1 segmented sieve as fallback/validation baseline
- Lehmer-style algorithms are complex - extensive literature review required
- Reference implementations: primesieve, SymPy, Kim Walisch's primecount
- Ensure π(x) interface remains unchanged
- Consider Deleglise-Rivat variant for practical performance

---

End of todo list.
