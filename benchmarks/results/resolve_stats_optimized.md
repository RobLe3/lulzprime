# Resolve() Diagnostic Statistics

**Purpose:** Measure internal operations of resolve() to identify bottlenecks

## Methodology

- **Function:** `resolve_internal_with_pi(index, pi, stats)`
- **Instrumentation:** ResolveStats dataclass (see diagnostics.py)
- **Time cap:** 60 seconds per index (default)
- **Policy:** docs/benchmark_policy.md

## Metrics Tracked

- **pi_calls:** Number of π(x) function calls during resolution
- **binary_search_iterations:** Number of binary search iterations
- **correction_backward_steps:** Backward correction steps (pi(x) > index)
- **correction_forward_steps:** Forward correction steps (pi(x) < index)
- **forecast_value:** Initial forecast estimate

## Results

| Index | Status | Time (s) | π(x) Calls | Binary Iters | Backward | Forward | Forecast |
|-------|--------|----------|------------|--------------|----------|---------|----------|
| 50,000 | SUCCESS | 2.05 | 21 | 16 | 0 | 0 | 610,057 |
| 100,000 | SUCCESS | 4.72 | 22 | 17 | 0 | 0 | 1,295,639 |
| 250,000 | SUCCESS | 14.10 | 23 | 18 | 0 | 0 | 3,487,316 |

## Analysis

**Observations:**

- **Index 50,000:**
  - π(x) calls: 21 (56.8% of total operations)
  - Binary search iterations: 16
  - Correction steps: 0 backward, 0 forward
  - Total time: 2.05s

- **Index 100,000:**
  - π(x) calls: 22 (56.4% of total operations)
  - Binary search iterations: 17
  - Correction steps: 0 backward, 0 forward
  - Total time: 4.72s

- **Index 250,000:**
  - π(x) calls: 23 (56.1% of total operations)
  - Binary search iterations: 18
  - Correction steps: 0 backward, 0 forward
  - Total time: 14.10s

**Averages across 3 successful runs:**
- π(x) calls per resolve: 22.0
- Time per resolve: 6.96s

---

**Benchmark Date:** 2025-12-17 23:20:40
**Time Cap:** 60s per index
**Policy:** docs/benchmark_policy.md
**Implementation:** src/lulzprime/lookup.py
