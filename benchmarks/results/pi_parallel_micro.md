# Pi Parallel Micro-Benchmark Results

**Benchmark Policy Compliance:** Time cap enforced at 30s per measurement

## Methodology

- **Sequential baseline:** `pi(x)` (single-threaded segmented sieve)
- **Parallel modes:** `pi_parallel(x, workers=k)` for k in {2, 4, 8}
- **Time cap:** Each measurement limited to 30 seconds (default)
- **Timeout handling:** TIMEOUT = measurement exceeded cap, skipped
- **Correctness:** All parallel results verified against sequential

## Results

| x | Mode | Time (s) | Status | Speedup |
|---|------|----------|--------|---------|
| 200,000 | sequential | 0.03 | SUCCESS | 1.00x |
| 200,000 | w=2 | 0.03 | SUCCESS | 0.95x |
| 200,000 | w=4 | 0.03 | SUCCESS | 1.01x |
| 200,000 | w=8 | 0.03 | SUCCESS | 0.98x |
| 500,000 | sequential | 0.09 | SUCCESS | 1.00x |
| 500,000 | w=2 | 0.09 | SUCCESS | 0.98x |
| 500,000 | w=4 | 0.09 | SUCCESS | 1.00x |
| 500,000 | w=8 | 0.09 | SUCCESS | 1.00x |
| 1,000,000 | sequential | 0.19 | SUCCESS | 1.00x |
| 1,000,000 | w=2 | 0.33 | SUCCESS | 0.58x |
| 1,000,000 | w=4 | 0.32 | SUCCESS | 0.60x |
| 1,000,000 | w=8 | 0.56 | SUCCESS | 0.34x |

## Observations

**Measured speedups (successful runs only):**
- π(200,000) with 2 workers: 0.95x
- π(200,000) with 4 workers: 1.01x
- π(200,000) with 8 workers: 0.98x
- π(500,000) with 2 workers: 0.98x
- π(500,000) with 4 workers: 1.00x
- π(500,000) with 8 workers: 1.00x
- π(1,000,000) with 2 workers: 0.58x
- π(1,000,000) with 4 workers: 0.60x
- π(1,000,000) with 8 workers: 0.34x
- **Average speedup across all modes:** 0.83x


---

**Benchmark Date:** Generated automatically
**Time Cap:** 30s per measurement
**Policy:** docs/benchmark_policy.md
**ADR:** docs/adr/0004-parallel-pi.md