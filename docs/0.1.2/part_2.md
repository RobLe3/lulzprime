> ⚠️ **Status: Historical / Archived**
>
> This document reflects the development process used while LULZprime was actively evolving.
> The project is now a completed, reference-grade implementation.
> This file is retained for context and provenance only.

Part 2 of 9, Goals, Non-Goals, and Constraints
2.1 Canonical reference
* Canonical concept source: OMPC_v1.33.7lulz.pdf
* Rule: If goals or constraints are ambiguous, defer to the paper.

2.2 Primary goals (must-haves)
1. Hardware efficiency first
    * Must run efficiently on low-end devices (old laptops, SBCs, small VPS).
    * Minimal RAM footprint, no large precomputed tables by default.
2. Fast prime resolution
    * Enable near-O(1) amortized nth-prime lookup via forecast → correction.
    * Avoid full sieving for point queries.
3. Deterministic and reproducible
    * Same inputs yield same outputs.
    * All stochastic components must accept explicit seeds.
4. Script-ready usability
    * One-line calls for common tasks.
    * No mandatory configuration or warm-up steps.
5. Scalable by design
    * Same primitives must scale to batch jobs, multiprocessing, and clusters.
    * Parallelism optional, never required.

2.3 Secondary goals (nice-to-haves)
* Support bulk prime table generation by index or range.
* Allow optional GPU / distributed backends without touching core logic.
* Provide diagnostic hooks for performance and convergence validation.
* Enable educational and exploratory use without extra tooling.

2.4 Explicit non-goals (hard exclusions)
The library must not:
* Claim cryptographic breaks or shortcuts.
* Accelerate integer factorization.
* Replace cryptographic entropy sources.
* Introduce AI-driven or heuristic “prime guessing.”
* Hide correctness behind probabilistic claims without verification.
These exclusions are permanent and enforceable.

2.5 Performance constraints
* Memory: Prefer < 25 MB for core functionality.
* CPU: Single-core friendly, predictable execution.
* I/O: No network dependency.
* Startup: No long initialization phase required.

2.6 Architectural constraints
* Clear separation between:
    * public API,
    * core math logic,
    * optional scale/backends.
* No cross-layer coupling.
* Extensions must be additive, not intrusive.

2.7 Behavioral constraints for agentic development
* No new public functions without specification in Part 4.
* No algorithmic deviation from OMPC principles without explicit approval.
* Optimization must not change numerical meaning or guarantees.
* “Clever” improvements that violate constraints are invalid by default.

2.8 Success definition (for this part)
This part is satisfied if:
* All later design decisions can be checked against these goals.
* Violations are detectable by inspection or automated tests.
* The system remains aligned with the paper’s scope and intent.
