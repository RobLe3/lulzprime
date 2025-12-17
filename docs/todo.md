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

### Implement True Sublinear π(x) Backend (Lehmer-style)

**Related Parts:** Part 4, Part 5, Part 6

**Target Modules:** src/lulzprime/pi.py

**Success Criterion:**
- π(x) uses true sublinear algorithm (Lehmer, Meissel-Lehmer, or equivalent)
- Time complexity: O(x^(2/3)) or better (not O(x log log x))
- Space complexity: bounded, ideally O(x^(1/3)) or less
- Maintains deterministic behavior and correctness
- Memory usage bounded per Part 2 constraints (< 25 MB)
- All existing tests continue to pass
- Performance improvement measurable via benchmarks for x > 10^6
- No public API changes

**Priority:** Medium

**Current State:**
- π(x) uses Sieve of Eratosthenes: O(x log log x) time, O(x) space
- This is optimized linear, not sublinear
- Achieved 20x speedup over original O(n) primality-test counting
- Satisfies Part 2 memory constraints for typical usage (x ≤ 10^6)

**Why This Matters:**
- Part 6 section 6.3 specifies "π(x) → sublinear (Lehmer-style), bounded memory"
- Current implementation is a pragmatic optimization but doesn't meet spec
- True sublinear methods required for very large x (> 10^7) with bounded memory

**Notes:**
- Keep existing sieve-based implementation as fallback for small x
- Lehmer-style algorithms are complex - consult paper and literature
- Ensure PrimeCounter interface remains unchanged
- Consider hybrid: sieve for small x, Lehmer for large x

---

End of todo list.
