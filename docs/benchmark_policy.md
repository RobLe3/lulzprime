# Benchmark Policy

**LULZprime – Benchmark Execution Rules and Time Caps**

---

## Purpose

This document defines mandatory rules for running benchmarks in the LULZprime project to prevent accidental long-running operations and ensure reproducible, time-bounded testing.

---

## Benchmark Categories

### 1. Smoke Benchmarks
- **Purpose:** Quick verification that code runs correctly
- **Scope:** Indices 1, 10, 100, 1000
- **Time Cap:** 5 seconds total
- **Frequency:** Run after every code change
- **Approval:** None required

### 2. Scale Benchmarks
- **Purpose:** Characterize performance at representative scales
- **Scope:** Indices 50,000, 100,000, 250,000
- **Time Cap:** 60 seconds per index (180 seconds total)
- **Frequency:** Run after performance-affecting changes
- **Approval:** None required (within default set)

### 3. Stress Benchmarks
- **Purpose:** Test extreme limits and identify failure modes
- **Scope:** Indices 500,000+
- **Time Cap:** Must be explicitly defined per session
- **Frequency:** Only when approved
- **Approval:** **REQUIRED** - must be documented in docs/milestones.md for that session

---

## Mandatory Time Caps

### Default Per-Run Wall-Time Cap
**60 seconds per index**

Any benchmark run that exceeds this cap must:
1. Be aborted immediately
2. Record result as TIMEOUT
3. Not continue to higher indices
4. Log the timeout in benchmark output

### Override Rules
Time caps can only be overridden when:
1. Explicit approval is documented in docs/milestones.md for the current session
2. The milestone entry specifies:
   - Which indices will be tested
   - Expected maximum runtime
   - Justification for exceeding default cap
3. The benchmark script accepts MAX_SECONDS via CLI flag or environment variable

Example milestone approval:
```markdown
### Stress Benchmark Approval – 2025-12-17
**Indices:** 500,000, 1,000,000
**Max Runtime:** 600 seconds per index (10 minutes)
**Justification:** Characterizing Phase 2 sublinear π(x) implementation
**Approval:** [core team member]
```

---

## Default Benchmark Set

**The default scale benchmark set is:**
- Index 50,000
- Index 100,000
- Index 250,000

These three indices:
- Complete within 60 seconds each with current implementation
- Provide adequate scale characterization
- Cover the transition from full sieve to segmented sieve (threshold at 100k)
- Are well within memory constraints (all < 25 MB)

**Indices beyond 250,000 are NOT in the default set** due to excessive runtime (> 30 minutes observed for 500k).

---

## Enforcement in Benchmark Scripts

All benchmark scripts under `benchmarks/` must:

1. **Accept time cap parameter:**
   - CLI flag: `--max-seconds N` or `-t N`
   - Environment variable: `MAX_SECONDS=N`
   - Default: 60 seconds per index

2. **Implement timeout guard:**
   - Use stdlib only (no external dependencies)
   - Check elapsed time before each index
   - Abort if cap exceeded
   - Print clear TIMEOUT message

3. **Report timeouts explicitly:**
   ```
   Benchmarking resolve(500,000)...
   ⏱ TIMEOUT: Exceeded 60 second cap after 60.2 seconds
   ⚠ Stopping benchmark run. Remaining indices not tested.
   ```

4. **Record partial results:**
   - Indices completed before timeout: report normally
   - Timed-out index: mark as TIMEOUT in output
   - Subsequent indices: mark as NOT_RUN

---

## Benchmark Execution Workflow

### Before Running Benchmarks:

1. **Check time budget:**
   - Default set (50k, 100k, 250k): ~3 minutes expected
   - Custom indices: estimate based on scale characterization data

2. **Check approval:**
   - Default set: No approval needed
   - Stress benchmarks (500k+): Verify approval in docs/milestones.md

3. **Set time cap:**
   - Use default (60s) for routine benchmarks
   - Set explicit cap only if approved

### During Benchmark Run:

1. Monitor wall-clock time
2. Abort if cap exceeded
3. Record timeout clearly

### After Benchmark Run:

1. Record results in benchmarks/results/summary.md
2. Note any timeouts
3. Update docs/milestones.md if new characterization data obtained

---

## Rationale

**Why 60 seconds per index?**
- Balances thorough testing with developer productivity
- Prevents accidental 30+ minute runs
- Allows 3x safety margin for typical indices (250k completes in ~20s)
- Long enough for representative measurement, short enough to catch runaway processes

**Why explicit approval for 500k+?**
- Current implementation: resolve(500k) > 30 minutes (observed timeout)
- Excessive runtime blocks development workflow
- Phase 2 (sublinear π(x)) needed for practical 500k+ support
- Approval ensures intentional decision with documented justification

**Why default set of 50k/100k/250k?**
- 50k: Tests lower end of scale (full sieve at threshold)
- 100k: Tests threshold boundary (full → segmented transition)
- 250k: Tests upper limit of practical range (segmented sieve)
- All three complete within time budget
- All three satisfy memory constraint (< 25 MB)

---

## Examples

### Valid: Default Scale Benchmark
```bash
$ python benchmarks/bench_scale_characterization.py
# Uses default indices: 50k, 100k, 250k
# Uses default cap: 60s per index
# No approval needed
```

### Valid: Custom Time Cap (Within Default Set)
```bash
$ python benchmarks/bench_scale_characterization.py --max-seconds 120
# Uses default indices: 50k, 100k, 250k
# Uses custom cap: 120s per index
# No approval needed (indices within default set)
```

### Invalid: Stress Benchmark Without Approval
```bash
$ python benchmarks/bench_stress.py --indices 500000,1000000
# ERROR: Stress benchmarks (500k+) require explicit approval
# See docs/benchmark_policy.md section on approval rules
# Approval must be documented in docs/milestones.md
```

### Valid: Approved Stress Benchmark
```bash
# After adding approval to docs/milestones.md:
$ python benchmarks/bench_stress.py --indices 500000 --max-seconds 600
# Uses approved index: 500k
# Uses approved cap: 600s
# Approval documented in milestones.md
```

---

## Policy Updates

This policy may be updated when:
1. Phase 2 (sublinear π(x)) is implemented and 500k+ becomes practical
2. Performance improvements change runtime characteristics
3. New benchmark categories are needed

All policy updates must be approved and documented in git history.

---

## Enforcement

**Violations of this policy:**
- Running 500k+ benchmarks without approval
- Exceeding time caps without abort
- Not recording timeouts

**Are not acceptable** and must be corrected before committing results.

---

## References

- Scale Characterization v1: benchmarks/results/summary.md (baseline measurements)
- Scale Characterization v2: benchmarks/results/summary.md (Phase 1 segmented sieve)
- Scale Characterization v3: benchmarks/results/summary.md (practical limits established)
- Part 6 section 6.4: Memory constraints (< 25 MB)
- Part 2 section 2.5: Performance constraints

---

**Effective Date:** 2025-12-17
**Policy Owner:** Core Team
**Review Frequency:** After major performance changes (Phase 2, optimizations, etc.)

---

End of benchmark policy.
