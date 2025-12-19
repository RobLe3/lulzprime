> ⚠️ **Status: Historical / Archived**
>
> This document reflects the development process used while LULZprime was actively evolving.
> The project is now a completed, reference-grade implementation.
> This file is retained for context and provenance only.

Part 6 of 9, Performance, Hardware, and Scaling Model
6.1 Canonical reference
* Canonical concept source: OMPC_v1.33.7lulz.pdf
* Rule: Performance claims and scaling behavior must remain consistent with the paper’s verified benchmarks and scope.

6.2 Hardware baseline targets
Minimum target (must work):
* Single-core CPU
* ≤ 4 GB RAM
* No GPU
* No network access
Expected behavior:
* resolve(n) usable for large n without sieving
* Stable execution time without memory spikes
* Deterministic results

6.3 Core performance model (low-end devices)
Design principles:
* Avoid O(n) or O(n log log n) memory growth.
* Favor O(1) arithmetic, logarithms, and bounded loops.
* Use localized primality tests instead of global enumeration.
Core costs:
* forecast() → O(1)
* π(x) → sublinear (Lehmer-style), bounded memory
* resolve() → dominated by a small number of π(x) calls and primality checks
* between() → linear in number of primes returned, not range width
This matches the paper’s “jump-and-adjust” efficiency claims.

6.4 Memory constraints
* No mandatory prime tables.
* Optional π(x) cache size must be configurable.
* Simulator must operate in streaming mode, not retain full history unless requested.
Target memory envelope (core):
* < 25 MB resident set for typical usage.

6.5 Scaling model, CPU (multiprocessing)
Scaling is horizontal, not algorithmic mutation.
Allowed strategies:
* Parallelize independent resolve(n) calls.
* Split large between(x, y) queries into subranges.
* Batch simulation runs with independent seeds.
Constraints:
* No shared mutable state between workers.
* Deterministic ordering required for reproducibility.

6.6 Scaling model, GPU and accelerators (optional)
GPU usage is non-core and must obey these rules:
* No GPU dependency in core modules.
* GPU acceleration limited to:
    * bulk primality testing,
    * large batch verification,
    * optional table generation backends.
* GPU code must be pluggable and ignorable.
The paper does not assume or require GPU computation.

6.7 Large table generation modes
Two supported conceptual modes:
1. Index-based tables
    * Generate many p_n via parallel resolve(n) calls.
    * Efficient for sparse or very large indices.
2. Range-based tables
    * Optional segmented sieve backend.
    * Used only when dense ranges are explicitly requested.
The default mode remains resolution, not enumeration.

6.8 Energy efficiency principles
* Prefer fewer arithmetic operations over memory access.
* Avoid cache-thrashing data structures.
* Keep hot loops branch-light.
* No speculative computation.
Energy efficiency is treated as a first-class design constraint, consistent with the paper’s stated impact goals.

6.9 Success definition (for this part)
This part is satisfied if:
* Core functionality runs acceptably on low-end hardware.
* Scaling paths do not alter correctness guarantees.
* High-end acceleration remains optional and isolated.
* Performance claims remain testable and falsifiable against the paper’s benchmarks.
