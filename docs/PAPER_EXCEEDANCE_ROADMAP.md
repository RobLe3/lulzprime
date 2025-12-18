# Paper-Exceedance Roadmap

**Date:** 2025-12-18
**Status:** DESIGN ONLY (Phase 5)
**Current State:** Full paper alignment achieved (Python implementation)

---

## Executive Summary

This document outlines paths to **exceed** paper performance targets beyond the current Python implementation. All approaches below are **design-only** and require separate approval before implementation.

**Current Performance (Python):**
- resolve(500k): 73s (Meissel O(x^(2/3)))
- Memory: 1.16 MB
- Python ceiling: ~3× worse than theoretical constant

**Goal:** Exceed Python ceiling and achieve near-theoretical performance.

---

## Path 1: C/Rust Core Port

### Overview
Port Meissel-Lehmer π(x) core to C/Rust with Python bindings.

### Expected Gains
- **Performance:** 10-50× speedup vs current Python
- **resolve(500k):** 73s → 1.5-7s (estimated)
- **Memory:** Comparable or better (native arrays)

### Technical Approach

**Option A: C Extension Module (CPython C API)**
```c
// Minimal example structure
static PyObject* pi_meissel_c(PyObject* self, PyObject* args) {
    unsigned long long x;
    if (!PyArg_ParseTuple(args, "K", &x)) {
        return NULL;
    }

    unsigned long long result = _pi_meissel_impl(x);
    return PyLong_FromUnsignedLongLong(result);
}
```

**Option B: Rust with PyO3 bindings**
```rust
use pyo3::prelude::*;

#[pyfunction]
fn pi_meissel(x: u64) -> PyResult<u64> {
    Ok(pi_meissel_impl(x))
}

#[pymodule]
fn lulzprime_rust(_py: Python, m: &PyModule) -> PyResult<()> {
    m.add_function(wrap_pyfunction!(pi_meissel, m)?)?;
    Ok(())
}
```

### Implementation Steps
1. **Prototype phase:**
   - Port `_pi_meissel()` to C/Rust (pure implementation)
   - Validate correctness against Python oracle (100k, 1M, 10M)
   - Benchmark single-threaded performance

2. **Integration phase:**
   - Create Python bindings (CPython C API or PyO3)
   - Add fallback to Python implementation if C/Rust unavailable
   - Wire into `pi()` dispatch with new `ENABLE_NATIVE_PI` flag

3. **Optimization phase:**
   - Cache-friendly memory layout for φ memoization
   - SIMD vectorization (Path 2)
   - Iterative φ instead of recursive (reduce call overhead)

4. **Validation phase:**
   - Run full test suite (169 tests)
   - Benchmark suite (π-level and resolve-level)
   - Determinism validation
   - Cross-platform testing (Linux, macOS, Windows)

### Complexity
- **High:** Requires C/Rust expertise, build system changes
- **Maintenance:** Two implementations (Python fallback + native)
- **Risk:** Binary distribution complexity (wheels, ABI compatibility)

### Prerequisites
- Approval for native code (security review)
- Build toolchain setup (gcc/clang/rustc)
- CI/CD for cross-platform builds
- Wheel distribution strategy (PyPI, manylinux)

### Expected Timeline
- Prototype: 1-2 weeks
- Integration: 1 week
- Optimization: 1-2 weeks
- Validation: 1 week
- **Total:** 4-6 weeks

---

## Path 2: SIMD Vectorization (φ and P2 loops)

### Overview
Use SIMD (AVX2/AVX-512/NEON) to vectorize tight loops in φ and P2.

### Expected Gains
- **Performance:** 2-8× speedup on top of C/Rust base
- **Best case:** Combined with Path 1: 20-400× vs current Python
- **resolve(500k):** 73s → 0.2-3.5s (estimated)

### Technical Approach

**Vectorized φ sieve marking:**
```c
// Example: AVX2 vectorized sieve (8× uint32 in parallel)
void phi_sieve_avx2(uint32_t* sieve, uint32_t n, uint32_t* primes, uint32_t a) {
    __m256i vec_zero = _mm256_setzero_si256();
    for (uint32_t i = 0; i < a; i++) {
        uint32_t p = primes[i];
        __m256i vec_p = _mm256_set1_epi32(p);

        for (uint32_t j = p; j <= n; j += 8) {
            __m256i vec_vals = _mm256_loadu_si256((__m256i*)&sieve[j]);
            // Mark multiples of p
            // ... (vectorized modulo and marking logic)
        }
    }
}
```

**Vectorized P2 summation:**
```c
// Example: AVX2 parallel sum reduction
uint64_t p2_sum_avx2(uint64_t* terms, size_t count) {
    __m256i vec_sum = _mm256_setzero_si256();

    for (size_t i = 0; i < count; i += 4) {
        __m256i vec_terms = _mm256_loadu_si256((__m256i*)&terms[i]);
        vec_sum = _mm256_add_epi64(vec_sum, vec_terms);
    }

    // Horizontal sum reduction
    return horizontal_sum_avx2(vec_sum);
}
```

### Implementation Steps
1. Profile current bottlenecks (φ vs P2 time breakdown)
2. Prototype vectorized φ sieve marking (inner loop)
3. Prototype vectorized P2 summation
4. Integrate with C/Rust core (Path 1 dependency)
5. Runtime CPU feature detection (AVX2 fallback to scalar)
6. Benchmark and validate correctness

### Complexity
- **Very High:** Requires SIMD expertise, intrinsics knowledge
- **Dependency:** Requires Path 1 (C/Rust core)
- **Portability:** AVX2 (x86-64), NEON (ARM), fallback (scalar)

### Prerequisites
- Path 1 complete (C/Rust core)
- SIMD intrinsics library (compiler support)
- CPU feature detection (runtime dispatch)

### Expected Timeline
- Prototype: 2-3 weeks
- Integration: 1 week
- Optimization: 1-2 weeks
- **Total:** 4-6 weeks (after Path 1)

---

## Path 3: P3 Correction (Algorithmic Upgrade)

### Overview
Add Lehmer P3 correction term for better asymptotic constant.

### Formula
```
π(x) = φ(x, a) + (a - 1) - P2(x, a) - P3(x, a)

where:
  P3(x, a) = sum_{i=a+1}^{b} (π(x / p_i) - (i - 1))
  b = π(x^(1/2))
```

### Expected Gains
- **Performance:** 1.5-3× speedup (better constant, not asymptotic class)
- **Complexity stays:** O(x^(2/3)) but with smaller constant
- **Best with:** Path 1 (C/Rust) or Path 4 (Deleglise-Rivat)

### Technical Approach

**Current (P2 only):**
```python
def _pi_meissel(x):
    # ...
    result = phi_val + (a - 1) - p2
    return result
```

**With P3:**
```python
def _pi_meissel_p3(x):
    # ...
    p3 = _compute_p3(x, a, b)  # New term
    result = phi_val + (a - 1) - p2 - p3
    return result

def _compute_p3(x, a, b):
    """Compute P3 correction term."""
    p3_sum = 0
    for i in range(a + 1, b + 1):
        p_i = get_ith_prime(i)
        pi_term = _pi_meissel_p3(x // p_i)  # Recursive
        p3_sum += (pi_term - (i - 1))
    return p3_sum
```

### Implementation Steps
1. Research P3 formula derivation (Lehmer 1985 paper)
2. Implement `_compute_p3()` function
3. Integrate with existing `_pi_meissel()` (optional flag)
4. Add P3-specific memoization (cache π(x / p_i) calls)
5. Validate correctness (no change to results, only speed)
6. Benchmark and compare to P2-only

### Complexity
- **Medium-High:** Requires careful implementation, recursive calls
- **Risk:** P3 overhead may exceed benefit for small x (crossover point?)
- **Maintenance:** More complex code, harder to verify

### Prerequisites
- Deep understanding of Lehmer algorithm
- Validation strategy (P3 should not change results)
- Benchmark policy update (measure P3 crossover point)

### Expected Timeline
- Research: 1 week
- Implementation: 2 weeks
- Validation: 1 week
- **Total:** 4 weeks

---

## Path 4: Deleglise-Rivat Algorithm

### Overview
Next-generation prime counting with better asymptotic complexity.

### Formula
```
π(x) = φ(x, a) + S1(x, a) + S2(x, a) + S3(x, a)

Complexity: O(x^(2/3) / log^2 x)
  vs Meissel O(x^(2/3))
```

### Expected Gains
- **Asymptotic:** Better scaling for very large x (> 10^12)
- **Practical:** 2-5× at x = 10^9, more at x > 10^12
- **Best for:** Extreme indices (resolve(10M+), research-level)

### Technical Approach

**High-level structure:**
```python
def _pi_deleglise_rivat(x):
    """Deleglise-Rivat algorithm (O(x^(2/3) / log^2 x))."""
    a = pi(x ** (1/3))  # Same as Meissel
    b = pi(x ** (1/2))

    phi_val = phi(x, a)
    s1 = _compute_s1(x, a, b)  # Special leaves (type 1)
    s2 = _compute_s2(x, a, b)  # Special leaves (type 2)
    s3 = _compute_s3(x, a, b)  # Special leaves (type 3)

    return phi_val + s1 + s2 + s3
```

**Differences from Meissel:**
- More refined special leaf classification (S1, S2, S3)
- Better cache locality (wheel structure)
- Asymptotically faster but more complex

### Implementation Steps
1. **Research phase (2-4 weeks):**
   - Study Deleglise-Rivat paper (1996)
   - Study reference implementations (primesieve, etc.)
   - Understand S1/S2/S3 computation

2. **Prototype phase (4-6 weeks):**
   - Implement S1, S2, S3 separately
   - Validate each component against Meissel oracle
   - Integrate into full algorithm

3. **Optimization phase (2-4 weeks):**
   - Cache-friendly memory layout
   - Wheel optimization
   - Parallelization (if applicable)

4. **Validation phase (2 weeks):**
   - Correctness validation (vs Meissel up to 10^9)
   - Performance benchmarking
   - Determine crossover point (when DR beats Meissel)

### Complexity
- **Very High:** Research-level algorithm, complex implementation
- **Risk:** High bug surface area, hard to debug
- **Maintenance:** Requires domain expertise to maintain

### Prerequisites
- Path 1 complete (C/Rust core) - DR too slow in Python
- Deep understanding of analytic number theory
- Extensive validation infrastructure
- Approval for research-level work

### Expected Timeline
- Research: 2-4 weeks
- Prototype: 4-6 weeks
- Optimization: 2-4 weeks
- Validation: 2 weeks
- **Total:** 10-16 weeks (research-level effort)

---

## Path 5: Parallel π(x) (Multi-threaded)

### Overview
Parallelize π(x) computation across multiple CPU cores.

### Expected Gains
- **Performance:** 2-8× speedup (depends on core count)
- **Scalability:** Linear scaling up to ~8 cores, diminishing returns beyond
- **Best with:** Path 1 (C/Rust core) for GIL-free parallelism

### Technical Approach

**Parallel P2 computation:**
```rust
// Example: Rayon parallel iterator (Rust)
use rayon::prelude::*;

fn compute_p2_parallel(x: u64, a: u64, primes: &[u64]) -> u64 {
    primes[a..b]
        .par_iter()
        .enumerate()
        .map(|(j, &p_j)| {
            let i = a + j;
            let count = pi_recursive(x / p_j);
            count - i - 1
        })
        .sum()
}
```

**Parallel φ computation (segmented approach):**
```rust
fn phi_parallel(x: u64, a: u64, primes: &[u64]) -> u64 {
    let segment_size = (x as f64).sqrt() as u64;
    let segments: Vec<_> = (0..x).step_by(segment_size).collect();

    segments.par_iter()
        .map(|&start| phi_segment(start, segment_size, primes, a))
        .sum()
}
```

### Implementation Steps
1. Profile current bottlenecks (identify parallelizable sections)
2. Prototype parallel P2 (simplest target)
3. Add thread pool management (rayon or custom)
4. Add work-stealing scheduler (balance load)
5. Benchmark scaling (1, 2, 4, 8 threads)
6. Integrate with C/Rust core (Path 1 dependency)

### Complexity
- **High:** Requires concurrent programming expertise
- **Dependency:** Path 1 (Python GIL blocks native parallelism)
- **Risk:** Contention on shared φ cache, synchronization overhead

### Prerequisites
- Path 1 complete (C/Rust core for GIL-free parallelism)
- Thread pool library (rayon, OpenMP, etc.)
- Benchmark multi-core performance
- Policy approval for multi-threading

### Expected Timeline
- Prototype: 2 weeks
- Integration: 1 week
- Optimization: 1-2 weeks
- **Total:** 4-5 weeks (after Path 1)

---

## Comparison Matrix

| Path | Expected Speedup | Complexity | Dependencies | Timeline | Risk |
|------|------------------|------------|--------------|----------|------|
| 1. C/Rust Core | 10-50× | High | None | 4-6 weeks | Medium |
| 2. SIMD | 2-8× (on top of Path 1) | Very High | Path 1 | 4-6 weeks | High |
| 3. P3 Correction | 1.5-3× | Medium-High | None | 4 weeks | Medium |
| 4. Deleglise-Rivat | 2-5× (at x > 10^9) | Very High | Path 1 | 10-16 weeks | High |
| 5. Parallel π(x) | 2-8× (on top of Path 1) | High | Path 1 | 4-5 weeks | Medium-High |

---

## Recommended Sequence

### Phase A: Foundation (Path 1)
**Goal:** Get off Python ceiling
1. Port Meissel to C/Rust (10-50× gain)
2. Validate correctness and determinism
3. Benchmark and compare to Python baseline

**Expected:** resolve(500k): 73s → 1.5-7s

### Phase B: Algorithmic Refinement (Path 3)
**Goal:** Better constant factor
1. Add P3 correction (1.5-3× gain on top of Path 1)
2. Determine P3 crossover point
3. Benchmark and validate

**Expected:** resolve(500k): 1.5-7s → 0.5-4s

### Phase C: Parallelism (Path 5)
**Goal:** Scale to multi-core
1. Parallelize P2 and φ computation (2-8× gain)
2. Add thread pool management
3. Benchmark scaling behavior

**Expected:** resolve(500k): 0.5-4s → 0.1-1s

### Phase D: Advanced (Paths 2 or 4, optional)
**Goal:** Research-level optimization
- Path 2 (SIMD): Squeeze out last 2-8× from vectorization
- Path 4 (DR): For extreme indices (10M+), research-level

**Expected:** resolve(500k): 0.1-1s → 0.05-0.2s (SIMD)

---

## Policy Requirements

### Code Approval
- **Native code (C/Rust):** Security review required (memory safety, buffer overflows)
- **Binary distribution:** Wheel building strategy, manylinux compliance
- **Fallback strategy:** Python implementation must remain as fallback

### Testing Requirements
- All 169 tests pass with native code
- Determinism validation (bit-identical across runs)
- Cross-platform testing (Linux, macOS, Windows)
- Benchmark suite (π-level and resolve-level)

### Performance Requirements
- Must exceed Python baseline by ≥5× to justify complexity
- Must maintain Tier A correctness (exact, deterministic)
- Memory constraint: < 25 MB (or document new constraint)

### Maintenance Requirements
- Two implementations maintained (Python + native)
- CI/CD for cross-platform builds
- Documentation for build toolchain setup

---

## Non-Goals (Out of Scope)

1. **GPU acceleration:** π(x) not well-suited for GPU (memory-bound, irregular)
2. **Distributed computing:** Overkill for single-machine problem
3. **Approximate π(x):** Paper requires Tier A exact, no approximations
4. **External dependencies:** Paper constraint (pure implementation)

---

## Conclusion

**Current State:** Full paper alignment achieved (Python implementation)

**Paper-Exceedance Paths:**
1. **Path 1 (C/Rust):** Highest priority, 10-50× gain, feasible
2. **Path 3 (P3):** Medium priority, 1.5-3× gain, refinement
3. **Path 5 (Parallel):** High priority after Path 1, 2-8× gain
4. **Path 2 (SIMD):** Advanced, 2-8× gain, high complexity
5. **Path 4 (DR):** Research-level, for extreme indices only

**Recommended:** Start with Path 1 (C/Rust core) as foundation for all other paths.

**Status:** DESIGN COMPLETE - Implementation requires separate approval

---

**Document Status:** COMPLETE (Phase 5)
**Next Phase:** Phase 6 (Final consolidation)
