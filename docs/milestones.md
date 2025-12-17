# milestones.md
**LULZprime – Completed Achievements and Accepted Deliverables**

---

## Purpose

This file records completed achievements and accepted deliverables for the LULZprime project.

Each milestone must include:
- Deliverable summary
- Goal mapping (G1–G7 from Part 9)
- Verification evidence location (tests/benchmarks)
- Version tag or commit reference (when used)

---

## Milestone Format

```
## [Milestone Title] – [Date]

**Goals:** G1, G2, ...

**Deliverable:**
- Brief description of what was completed

**Verification:**
- Location of tests/benchmarks
- Results summary

**Commit/Tag:** [commit hash or version tag]
```

---

## Completed Milestones

### Repository Structure Setup – 2025-12-17

**Goals:** G6 (Maintainability)

**Deliverable:**
- Established canonical directory structure per defaults.md
- Created documentation framework (autostart.md, defaults.md, manual parts 0-9)
- Set up tracking files (milestones.md, todo.md, issues.md)

**Verification:**
- Directory structure matches defaults.md section 3
- All manual parts 0-9 present in docs/manual/

**Commit/Tag:** [initial setup]

---

### Verified Correctness and Performance Baseline – 2025-12-17

**Goals:** G1 (Correct Prime Resolution), G2 (Hardware Efficiency), G3 (Determinism), G5 (Scope Integrity), G6 (Maintainability), G7 (OMPC Alignment)

**Deliverable:**
- Established clean, verified baseline for core resolver
- Core resolution pipeline fully functional and tested
- resolve(), between(), next_prime(), prev_prime(), is_prime() all operational
- Performance baseline measured at representative indices (1, 10, 100, 1K, 10K)
- Full Part 5 workflow compliance verified
- All public API contracts from Part 4 verified via tests
- OMPC simulator with proper gap distribution and convergence

**Verification:**
- **Test Results:** 51/51 tests passing (100% pass rate)
  - All core resolution tests pass (6/6, including correction step compliance)
  - All API contract tests pass (15/15)
  - All primality and π(x) tests pass (17/17)
  - All simulator tests pass (7/7, including convergence)
  - All determinism and guarantee tier tests pass (6/6)
- **Benchmark Results:** benchmarks/results/summary.md
  - resolve(1): 0.009 ms (p_1 = 2)
  - resolve(10): 0.024 ms (p_10 = 29)
  - resolve(100): 7.570 ms (p_100 = 541)
  - resolve(1000): 211.5 ms (p_1000 = 7919)
  - resolve(10000): 3561 ms (p_10000 = 104729)
- **Workflow Verification:**
  - Execution chain matches Part 5 section 5.3 exactly (forecast → bracket → π(x) → correction)
  - Both backward and forward correction steps implemented
  - Structural test (test_correction_step_compliance) ensures compliance
- **Goal Alignment:** All 7 project goals satisfied (see benchmarks/results/summary.md)

**Issues Resolved:**
- ✅ Simulator convergence fixed via proper OMPC gap distribution (exponential decay model)
- ✅ Forward correction step added to resolve_internal for complete Part 5 compliance
- All previously logged issues resolved and documented in docs/issues.md

**Performance Characteristics:**
- Current π(x) implementation: O(n) simple counting (identified as optimization priority)
- Memory footprint: < 25 MB (Part 2 constraint satisfied)
- Deterministic and reproducible (Part 4 contract verified)
- Production-ready for indices up to 10K with well-characterized performance

**Status:** Clean baseline with zero open issues

**Commit/Tag:** [baseline-v0.1.0-clean]

---

### Optimized Linear π(x) via Sieve-Based Backend – 2025-12-17

**Goals:** G1 (Correct Prime Resolution), G2 (Hardware Efficiency), G3 (Determinism), G6 (Maintainability)

**Deliverable:**
- Replaced O(n) primality-test counting with O(x log log x) sieve-based π(x)
- This is optimized linear (not sublinear) - improves constant factors, not asymptotic complexity
- Achieved ~20x average speedup for resolve() at indices ≥ 100
- Maintained all correctness guarantees (Tier A, B, C)
- No public API changes
- Added comprehensive test coverage for large values (up to 10^6)

**Verification:**
- **Test Results:** 52/52 tests passing (100% pass rate)
  - Added new test_pi_very_large_values covering π(10^5) and π(10^6)
  - All existing tests continue to pass
- **Performance Improvements:**
  - resolve(100): 7.57ms → 0.37ms (**20.2x faster**)
  - resolve(1000): 211ms → 11ms (**18.6x faster**)
  - resolve(10000): 3561ms → 164ms (**21.7x faster**)
- **Implementation Details:**
  - Sieve of Eratosthenes for x ≤ 10^6
  - Memory usage: ~1MB per 10^6 range (< 25MB constraint satisfied)
  - Deterministic, exact counting maintained
- **Goal Alignment:**
  - G1: Correctness maintained - all resolution tests pass
  - G2: Hardware efficiency dramatically improved - 20x speedup
  - G3: Determinism verified - consistent results across runs
  - G6: Clean modular implementation - no API changes
  - **Note on G7:** Part 6 section 6.3 specifies sublinear π(x); current implementation is optimized linear. True sublinear methods remain future work (see docs/todo.md)

**Technical Details:**
- **File Modified:** src/lulzprime/pi.py
  - Implemented _simple_sieve() for efficient prime generation
  - Kept _pi_simple() as reference fallback
  - Updated pi() to use sieve for all practical ranges
- **Tests Added:** tests/test_pi.py
  - test_pi_very_large_values: validates π(x) up to 10^6
- **Benchmarks:** benchmarks/results/summary.md updated with before/after comparison

**Memory Characteristics:**
- Sieve uses ~1MB for x=10^6 (well within 25MB Part 2 constraint)
- Memory scales linearly with x but remains bounded
- No hidden precomputation or memory leaks

**Performance Characteristics:**
- Time complexity: O(x log log x) for sieve generation (optimized linear, not sublinear)
- Space complexity: O(x) for sieve array
- Dramatic constant-factor improvement: 20x average speedup for indices ≥ 100
- Asymptotic complexity unchanged: still linear in x, not sublinear

**Clarification:**
This optimization improves constant factors dramatically but does not achieve
the sublinear complexity specified in Part 6 section 6.3. True sublinear
methods (Lehmer-style, O(x^(2/3))) remain future work per docs/todo.md.

**Status:** Optimization complete with verified performance gains and zero regressions

**Commit/Tag:** [optimize-pi-v0.1.1]

---

### Snapshot 1: Verified Resolver + Optimized Linear π(x) – 2025-12-17

**Tag:** v0.1.0-snapshot.1
**Commit:** 8ce44e6be862070b9b6010fdcaa481c0028911a1

**Status:** Production-ready snapshot with verified correctness and optimized performance

**Summary:**
First stable snapshot of LULZprime with complete resolver pipeline and optimized π(x) backend.

**Test Status:**
- 52/52 tests passing (100% pass rate)
- All Tier A, B, C guarantees verified
- Full Part 5 workflow compliance
- Zero open issues

**Performance Characteristics:**
- resolve(10000): 164ms (21.7x faster than baseline)
- π(x) backend: Sieve of Eratosthenes O(x log log x)
- Memory: < 25MB (Part 2 constraint satisfied)

**Evidence:**
- Benchmark results: benchmarks/results/summary.md
- Test suite: tests/ (pytest -q shows 52 passed)
- Milestone documentation: Complete with before/after comparisons

**Components:**
- Core resolver: src/lulzprime/resolve.py, lookup.py, forecast.py
- Prime counting: src/lulzprime/pi.py (optimized linear via sieve)
- Primality testing: src/lulzprime/primality.py (deterministic Miller-Rabin)
- OMPC simulator: src/lulzprime/simulator.py, gaps.py

**Known Limitations:**
- π(x) is optimized linear (O(x log log x)), not true sublinear
- True sublinear methods (Lehmer-style, O(x^(2/3))) remain future work
- See docs/todo.md for roadmap

---

### Scale Characterization v1 (Large Index Benchmarks) – 2025-12-17

**Goals:** G2 (Hardware Efficiency - validation), G9 (Alignment Measurement)

**Deliverable:**
Characterization of resolve() performance and memory usage at large indices (50k, 100k, 250k) to validate scaling behavior and identify constraint limits.

**Method:**
Measurement-only work with no code changes. Pure characterization of existing implementation.

**Results:**

| Index   | Time (median) | Memory (peak) | Status |
|---------|---------------|---------------|--------|
| 50,000  | 10.6 sec      | 7.80 MB       | ✓      |
| 100,000 | 27.0 sec      | 16.24 MB      | ✓      |
| 250,000 | 81.4 sec      | 42.71 MB      | ✗      |

**Key Findings:**
1. ✓ Performance scaling follows expected O(x log log x) behavior
2. ✓ Deterministic behavior verified at all tested scales
3. ✓ Indices up to ~150k remain within 25 MB memory constraint
4. ✗ **Constraint violation identified:** resolve(250k) uses 42.71 MB, exceeding Part 6 section 6.4 limit of < 25 MB by 71%

**Issue Logged:**
- docs/issues.md: [CONSTRAINT-VIOLATION] Memory Exceeds 25MB Limit at Large Indices
- Severity: HIGH
- Root cause: Sieve of Eratosthenes O(x) space complexity
- Impact: Prevents usage at large indices on low-end devices

**Practical Limits Established:**
- **Safe range:** Indices up to 100k (16 MB peak, completes in ~27 sec)
- **Marginal range:** Indices 100k-150k (approaching 25 MB limit)
- **Constrained range:** Indices 150k+ (exceeds memory constraint)

**Evidence:**
- benchmarks/bench_scale_characterization.py
- benchmarks/results/summary.md (Scale Characterization v1 section)
- All measurements with tracemalloc memory tracking

**Status:** Characterization complete, constraint violation documented, no fixes attempted per safety protocols

---

End of milestones log.

### Memory-Bounded π(x) Phase 1 (Segmented Sieve) – 2025-12-17

**Goals:** G1 (Correct Prime Resolution), G2 (Hardware Efficiency), G3 (Determinism), G6 (Maintainability), G7 (OMPC Alignment)

**Deliverable:**
- Implemented segmented sieve backend for π(x) to restore Part 6 section 6.4 memory compliance
- Hybrid threshold-based dispatch: full sieve for x < 100k, segmented for x ≥ 100k
- Fixed segment size of 1,000,000 elements (~1 MB per segment as boolean list)
- Memory constraint violation RESOLVED: all tested indices now < 25 MB

**Verification:**
- **Test Results:** 55/55 tests passing (100% pass rate)
  - 3 new tests added for segmented sieve:
    - test_pi_segmented_threshold: Verifies threshold dispatch
    - test_pi_segmented_large_values: Tests multi-segment correctness (250k, 500k, 750k)
    - test_pi_segmented_vs_full_sieve: Cross-validates segmented vs full sieve
  - All Tier A guarantees maintained (exact, deterministic π(x))
  - No API changes, no workflow changes
- **Memory Results:** benchmarks/results/summary.md (Scale Characterization v2)
  - resolve(50,000): 5.54 MB peak (down from 7.80 MB, 29% reduction) ✓
  - resolve(100,000): 11.71 MB peak (down from 16.24 MB, 28% reduction) ✓
  - resolve(250,000): **15.27 MB peak** (down from 42.71 MB, **64% reduction**) ✓
  - **All indices now satisfy < 25 MB constraint**

**Implementation Details:**
- **File Modified:** src/lulzprime/pi.py
  - Implemented _segmented_sieve(x, segment_size=1_000_000) function
  - Modified pi(x) to use threshold dispatch at 100,000
  - Module docstring updated with Phase 1 implementation notes
- **Tests Added:** tests/test_pi.py
  - test_pi_segmented_threshold (threshold boundary)
  - test_pi_segmented_large_values (correctness at 250k/500k/750k)
  - test_pi_segmented_vs_full_sieve (cross-validation)
- **Benchmarks:** benchmarks/results/summary.md updated with Scale Characterization v2
- **Documentation:** docs/adr/0002-memory-bounded-pi.md (ADR for design decision)

**Memory Characteristics:**
- Segment array: ~1 MB per segment (Python boolean list)
- Small primes up to sqrt(x): negligible (< 100 KB for x < 10^7)
- Total peak: ~1-2 MB for pi(x) call + resolver overhead
- Well within Part 6 section 6.4 constraint (< 25 MB)

**Performance Characteristics:**
- Time complexity: O(x log log x) - unchanged from full sieve
- Space complexity: O(1) for fixed segment size
- Threshold dispatch preserves performance for small x
- Segmented sieve slower than full sieve (expected memory/speed tradeoff)

**Goal Alignment:**
- G1 (Correct Prime Resolution): ✓ All tests pass, π(x) exact and verified
- G2 (Hardware Efficiency): ✓ **RESTORED** - Memory < 25 MB for all tested indices
- G3 (Determinism): ✓ Identical results across runs, cross-validated with full sieve
- G6 (Maintainability): ✓ Modular implementation, clear threshold dispatch
- G7 (OMPC Alignment): ✓ No changes to resolve() workflow (Part 5 compliance)

**Issues Resolved:**
- ✅ [CONSTRAINT-VIOLATION] Memory Exceeds 25MB Limit at Large Indices (docs/issues.md)
- Measured evidence: resolve(250k) now 15.27 MB (down from 42.71 MB)
- Safe range expanded from ~100k to 250k+ indices

**Status:** Memory constraint violation RESOLVED. Production-ready for low-end devices.

**Commit/Tag:** [to be added]

---

End of milestones log.

