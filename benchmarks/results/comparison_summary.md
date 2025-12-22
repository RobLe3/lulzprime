# lulzprime v0.1.2 vs v0.2.0 Benchmark Results

## Performance Comparison

| Benchmark | v0.1.2 | v0.2.0 | Improvement |
|-----------|--------|--------|-------------|
| resolve(10000) | 368 ms | 399 ms | 1.1x slower |
| resolve(100000) | 7.49 s | 1.73 s | 4.3x faster |
| resolve(250000) | 14.85 s | 4.48 s | 3.3x faster |
| resolve(500000) | 35.77 s | 6.30 s | 5.7x faster |
| pi(1000000) | 173 ms | 49 ms | 3.6x faster |
| pi(10000000) | 1.91 s | 326 ms | 5.9x faster |
| pi(100000000) | 26.05 s | 2.72 s | 9.6x faster |
| forecast(10^6, r=1) | 983.5 ns | 606.6 ns | 1.6x faster |
| forecast(10^6, r=2) | — | 750.3 ns | v0.2.0 only |
| forecast(10^8, r=1) | 1.02 µs | 551.3 ns | 1.9x faster |
| forecast(10^8, r=2) | — | 610.7 ns | v0.2.0 only |
| forecast(10^9, r=1) | 1.00 µs | 532.7 ns | 1.9x faster |
| forecast(10^9, r=2) | — | 637.3 ns | v0.2.0 only |
| simulate(10000) | 744 ms | 797 ms | 1.1x slower |
| simulate(100000) | 7.39 s | 7.83 s | 1.1x slower |
| simulate(1000000) | 70.81 s | N/A | N/A |

## Key Findings

### Dramatic Performance Improvements

**pi(10^8): 9.6x faster** (26.05 s → 2.72 s)
- Enabled Meissel-Lehmer algorithm: O(x^(2/3)) vs O(x log log x)

**resolve(500000): 5.7x faster** (35.77 s → 6.30 s)

### New Features in v0.2.0

- **forecast() refinement levels**: Optional refinement_level parameter (1 or 2)
- **Generator mode**: as_generator parameter for simulate() - O(1) memory streaming
- **Meissel-Lehmer pi()**: ENABLE_LEHMER_PI=True by default

### Notes

- All times are mean values from pyperf statistical benchmarking
- v0.1.2 lacks refinement_level and as_generator parameters
- forecast() is O(1) in both versions (sub-microsecond)
- Some v0.2.0 benchmarks incomplete due to time constraints
