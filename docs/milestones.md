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

**Commit/Tag:** e3845c1

---

End of milestones log.


### Scale Characterization v3 (Documentation Accuracy Audit) – 2025-12-17

**Goals:** G6 (Maintainability - accurate documentation)

**Deliverable:**
- Documentation accuracy audit for segmented sieve memory claims
- Corrected all inaccurate memory usage claims (1 MB → 8 MB per segment)
- Established practical limits for segmented sieve (viable up to ~250k indices)
- Verified memory constraint compliance remains satisfied

**Verification:**
- **Documentation Audit Results:**
  - Critical finding: Python list[bool] uses 8 bytes/element (pointer overhead), not 1 byte
  - Measured: 1M element list[bool] = 7.63 MB, not 1 MB as documented
  - Root cause: List stores 8-byte pointers to boolean objects on 64-bit Python
- **Files Corrected:**
  - src/lulzprime/pi.py module docstring
  - src/lulzprime/pi.py:_segmented_sieve() docstring
  - src/lulzprime/pi.py:pi() docstring
  - src/lulzprime/pi.py code comments
  - benchmarks/results/summary.md (added v3 section)
- **Practical Limits Established:**
  - Indices 1-100k: Good (seconds, full sieve)
  - Indices 100k-250k: Acceptable (minutes, segmented sieve)
  - Indices 250k-500k: Impractical (30+ minutes runtime)
  - Indices 500k+: Not viable with current implementation
- **Memory Compliance:** Still satisfied (< 25 MB at all tested indices)

**Test Status:**
- 55/55 tests passing (documentation changes only, no code changes)
- No regressions

**Issue Resolution:**
- ✅ [DOC-INACCURACY] Segmented Sieve Memory Claims Incorrect (docs/issues.md)
- Severity: LOW (documentation only, no functional impact)
- All inaccurate claims corrected

**Status:** Documentation corrected, practical limits documented, audit complete.

**Commit/Tag:** cbd8802

---

### Benchmark Guardrails and Performance Limits – 2025-12-17

**Goals:** G6 (Maintainability - reproducible benchmarking)

**Deliverable:**
- Created benchmark policy framework to prevent accidental long-running benchmarks
- Established mandatory time caps and approval rules for stress benchmarks (500k+)
- Enforced policy in benchmark scripts with stdlib-only timeout guards
- Documented performance limits: 500k+ indices impractical with current implementation

**Verification:**
- **Policy Document:** docs/benchmark_policy.md
  - Default time cap: 60 seconds per index
  - Default benchmark set: 50k, 100k, 250k only
  - Stress benchmarks (500k+) require explicit approval in docs/milestones.md
  - Timeout enforcement mandatory (abort on cap exceeded)
- **Benchmark Script Updates:** benchmarks/bench_scale_characterization.py
  - Added argparse CLI: `--max-seconds` flag, `MAX_SECONDS` env var
  - Stress benchmark check: interactive prompt for 500k+ indices
  - Timeout guard: aborts run if time cap exceeded, records TIMEOUT status
  - Stdlib only: no external dependencies (time, argparse, tracemalloc)
- **Issue Tracking:** docs/issues.md
  - New open issue: [PERFORMANCE] resolve(500,000) exceeds acceptable runtime
  - Severity: MEDIUM, Status: OPEN
  - Evidence: 500k and 1M indices exceeded 30 minutes runtime
  - Proposed remediation: Phase 2 sublinear π(x) (future work)

**Practical Limits Established:**
- **Indices 1-100k:** Good (seconds, full sieve)
- **Indices 100k-250k:** Acceptable (minutes, segmented sieve)
- **Indices 250k-500k:** Impractical (30+ minutes runtime)
- **Indices 500k+:** Not viable with current implementation

**Benchmark Policy Categories:**
1. **Smoke Benchmarks:** 1, 10, 100, 1000 (5s total cap, no approval)
2. **Scale Benchmarks:** 50k, 100k, 250k (60s per index cap, no approval)
3. **Stress Benchmarks:** 500k+ (explicit approval required, documented in milestones)

**Enforcement Mechanism:**
- CLI flags: `--max-seconds N` or `-t N`
- Environment variable: `MAX_SECONDS=N`
- Default: 60 seconds per index
- Timeout guard: checks elapsed time, aborts if exceeded
- Partial results: records TIMEOUT status, marks subsequent indices NOT_RUN

**Goal Alignment:**
- G6 (Maintainability): Reproducible benchmarking with time-bounded execution
- Prevents accidental 30+ minute runs that block development workflow
- Clear approval process for stress benchmarks (500k+)
- Documentation consistency maintained (no conflicting runtime claims)

**Files Modified:**
- docs/benchmark_policy.md: NEW - policy framework
- benchmarks/bench_scale_characterization.py: Added time cap enforcement
- docs/issues.md: Added [PERFORMANCE] issue, fixed stale memory claims
- docs/milestones.md: This entry

**Impact:**
- Development workflow protected from accidental long-running benchmarks
- Clear boundaries: default set (50k/100k/250k) vs stress benchmarks (500k+)
- Practical limits documented and enforced via policy
- Future stress benchmarks require explicit approval and documentation

**Status:** Policy established, enforcement implemented, performance limits documented

**Commit/Tag:** cbdb078

---

### Public API Contract Hardened – 2025-12-17

**Goals:** G6 (Maintainability), G5 (Scope Integrity), G7 (OMPC Alignment)

**Deliverable:**
- Hardened public API contract to prevent misuse and set correct user expectations
- Formalized Tier A/B/C guarantees with explicit NOT-guarantees
- Created comprehensive API contract documentation (docs/api_contract.md)
- Updated README with "What LULZprime Is/Is NOT" sections
- Enhanced all public function docstrings with performance envelopes and constraints

**Verification:**
- **Docstring Updates:** All 7 public functions now have:
  - GUARANTEES section (what IS promised)
  - INPUT CONSTRAINTS section (including practical limits)
  - PERFORMANCE ENVELOPE section (qualitative scaling)
  - DOES NOT GUARANTEE section (explicit non-promises)
  - WARNING sections for critical misuse cases (forecast, simulate)

- **Files Modified:**
  - src/lulzprime/resolve.py (resolve, between, next_prime, prev_prime)
  - src/lulzprime/forecast.py (forecast with NOT EXACT warnings)
  - src/lulzprime/primality.py (is_prime with crypto warnings)
  - src/lulzprime/simulator.py (simulate with CRITICAL MISUSE warnings)

- **README.md Updates:**
  - Added "What LULZprime Is" section (navigation, deterministic, hardware efficient)
  - Added "What LULZprime Is NOT" section (not crypto, not unbounded, not predictor)
  - Added "Practical Index Range" section with Phase 1 performance tiers
  - Improved Quick Start examples with Tier A/B/C annotations
  - All claims aligned with benchmark_policy.md (≤ 250k practical, 500k+ impractical)

- **docs/api_contract.md Created:** NEW comprehensive contract document with:
  - Formalized Tier A (Exact), Tier B (Verified), Tier C (Estimate) definitions
  - Per-function guarantee specifications
  - Misuse cases section with code examples (5 critical misuses documented)
  - Performance expectations table
  - Determinism and reproducibility guarantees
  - Contract violation definitions

**Consistency Verification:**
- ✅ README practical limits match benchmark_policy.md
- ✅ Docstring performance envelopes match api_contract.md
- ✅ Tier A/B/C definitions consistent across all docs
- ✅ No crypto promises anywhere (explicit warnings added)
- ✅ forecast() marked as estimate (NOT exact) in all locations
- ✅ simulate() marked as non-exact with CRITICAL MISUSE warnings
- ✅ No unbounded runtime promises (practical limits documented)

**Misuse Cases Documented:**
1. Using forecast() as exact primes (Tier C misunderstanding)
2. Using simulate() as exact primes (critical simulator misuse)
3. Cryptographic use cases (explicit prohibition + warnings)
4. Unbounded index assumptions (practical limits documented)
5. Security-critical applications (not suitable, use crypto libraries)

**Goal Alignment:**
- G5 (Scope Integrity): Clear boundaries on what LULZprime is/is NOT
- G6 (Maintainability): Consistent, explicit contracts across all documentation
- G7 (OMPC Alignment): Navigation model emphasized, no prediction claims

**Impact:**
- Third-party users cannot accidentally misuse the library
- Explicit performance envelopes prevent unrealistic expectations
- Tier A/B/C system prevents ambiguous correctness claims
- Comprehensive misuse case documentation protects against crypto misuse
- README sets correct expectations before installation

**Test Status:**
- No code changes (documentation only)
- All 55 tests continue to pass (verified in Task 6)

**Status:** Public API contract hardened, usage boundaries explicit, misuse cases documented

**Commit/Tag:** 6fcc6c1

---

### Batch Resolver API with Deterministic Caching – 2025-12-17

**Goals:** G2 (Hardware Efficiency), G3 (Determinism), G6 (Maintainability)

**Deliverable:**
- Implemented batch-friendly API layer for efficient multi-resolution operations
- Added resolve_many() and between_many() with π(x) caching optimization
- Maintained Tier A/B guarantees for all batch operations
- No changes to existing public APIs

**Verification:**
- **New Module:** src/lulzprime/batch.py
  - resolve_many(indices): Tier A exact results with order preservation
  - between_many(ranges): Tier B verified results
  - Internal π(x) caching (no global state, cache per batch execution only)
  - Sorts indices internally to optimize π(x) reuse

- **Files Modified:**
  - src/lulzprime/__init__.py: Added batch exports
  - docs/api_contract.md: Added batch function specifications
  - README.md: Added batch example

- **Tests Added:** tests/test_batch.py (33 new tests)
  - Correctness: verify matches individual resolve() calls
  - Order preservation: results match input order
  - Determinism: same inputs yield same outputs
  - Input validation: bad types, negative indices rejected
  - Duplicates: allowed and handled correctly
  - Batch sizes: small (10), medium (100) tested
  - Edge cases: empty batches, single elements, overlapping ranges

**Batch API Guarantees:**

**resolve_many(indices):**
- Tier A (Exact): Each result is exact p_index
- Deterministic and order-preserving
- Optimization: internally sorts + caches π(x) within batch
- No persistent global state
- Practical limit: ~100 indices per batch

**between_many(ranges):**
- Tier B (Verified): All returned primes verified
- Deterministic and order-preserving
- Each range processed independently
- Practical limit: ~100 ranges per batch

**Optimization Strategy:**
- Sort indices internally to minimize π(x) recomputation
- Simple dict cache for π(x) within single batch execution
- Cache discarded after batch completes (no global state)
- Temporarily patches pi() function during batch execution

**Goal Alignment:**
- G2 (Hardware Efficiency): Batch caching reduces π(x) overhead
- G3 (Determinism): All batch operations deterministic
- G6 (Maintainability): Clean additive API, no changes to existing functions

**Test Status:**
- 88/88 tests passing (55 original + 33 batch = 100% pass rate)
- No regressions in existing tests
- Comprehensive validation of determinism, order preservation, correctness

**Performance Characteristics:**
- Small batches (< 10): similar to loop
- Medium batches (10-100): faster than loop (π(x) caching benefit)
- Speedup depends on index locality (sorted indices share π(x) work)
- Memory: O(batch_size) for results + O(π(x) calls) for cache

**Impact:**
- Day-to-day scripting: batch operations now efficient
- Tier guarantees unchanged: resolve_many() is Tier A exact
- No global caches or persistent state (per Part 6 constraints)
- Clean integration with existing API

**Status:** Batch API implemented, tested, documented, ready for use

**Commit/Tag:** 8943766

---

### Batch Caching Made Side-Effect Free – 2025-12-17

**Goals:** G2 (Hardware Efficiency), G3 (Determinism), G6 (Maintainability)

**Deliverable:**
- Eliminated global monkeypatching from resolve_many() implementation
- Refactored to use dependency injection for π(x) caching
- Preserved all existing behavior and Tier A guarantees
- Made batch operations thread-safe by design

**Problem:**
Previous implementation used temporary global patching:
```python
# OLD - PROBLEMATIC
pi_module.pi = cached_pi  # Global mutation
try:
    result = resolve_internal(index)
finally:
    pi_module.pi = original_pi  # Restore
```

This approach:
- Blocks future parallelism
- Creates hidden side effects
- Not thread-safe
- Violates clean dependency injection principles

**Solution:**
Implemented dependency injection pattern:
1. Added `resolve_internal_with_pi(index, pi_fn)` in lookup.py
2. Modified `_binary_search_pi` to accept pi_fn parameter
3. resolve_many() creates local `cached_pi` closure
4. Passes closure to `resolve_internal_with_pi` (no global mutation)

**Verification:**
- **Files Modified:**
  - src/lulzprime/lookup.py: Added resolve_internal_with_pi() for dependency injection
  - src/lulzprime/batch.py: Removed global patching, uses local closure + injection
  - tests/test_resolve.py: Updated structural test to check new function
  - tests/test_batch.py: Added 3 new tests for global mutation verification
  - docs/api_contract.md: Updated optimization strategy description

- **New Tests Added:** 3 tests in TestResolveManyNoGlobalMutation class
  - test_no_global_pi_mutation: Verifies pi() identity unchanged
  - test_consecutive_calls_no_state: Verifies no leftover state between calls
  - test_sentinel_wrapper_not_leaked: Verifies no wrapper leaks to global scope

- **Test Results:** 91/91 tests passing (88 original + 3 new = 100% pass rate)
  - All existing batch tests pass (determinism, order preservation, correctness)
  - All existing resolve tests pass (Part 5 compliance verified)
  - New tests confirm no global mutation

**Implementation Details:**

**Before (Global Patching):**
```python
def _resolve_with_pi_cache(index, pi_cache):
    original_pi = pi_module.pi
    pi_module.pi = cached_pi  # GLOBAL MUTATION
    try:
        result = resolve_internal(index)
    finally:
        pi_module.pi = original_pi  # Restore
```

**After (Dependency Injection):**
```python
# In resolve_many():
def cached_pi(x: int) -> int:
    """Local closure, no global state."""
    if x not in pi_cache:
        pi_cache[x] = default_pi(x)
    return pi_cache[x]

# Pass to internal resolver
result = resolve_internal_with_pi(index, cached_pi)
```

**Goal Alignment:**
- G2 (Hardware Efficiency): Same π(x) caching efficiency, now thread-safe
- G3 (Determinism): Same deterministic behavior, verified via tests
- G6 (Maintainability): Cleaner dependency injection, enables future parallelism

**Behavioral Guarantees Preserved:**
- ✅ Tier A exact results unchanged
- ✅ Order preservation unchanged
- ✅ Determinism unchanged
- ✅ Performance characteristics unchanged
- ✅ All 88 original tests pass
- ✅ No API changes

**New Capabilities Enabled:**
- Thread-safe batch operations (no shared mutable global state)
- Future parallelization possible (no global locks needed)
- Cleaner testing (can inject mock π(x) for unit tests)
- No hidden side effects

**Impact:**
- Batch caching remains efficient (local closure overhead negligible)
- Code is now thread-safe by design
- Future parallel batch operations possible
- No global state mutation anywhere in codebase
- Clean dependency injection pattern established

**Status:** Global patching eliminated, batch operations thread-safe, all tests pass

**Commit/Tag:** b6c1bd0

---

End of milestones log.

