> ⚠️ **Status: Historical / Archived**
>
> This document reflects the development process used while LULZprime was actively evolving.
> The project is now a completed, reference-grade implementation.
> This file is retained for context and provenance only.

Part 4 of 9, Public API and Interface Contracts
4.1 Canonical reference
* Canonical concept source: OMPC_v1.33.7lulz.pdf
* Rule: Public API must stay consistent with OMPC scope, forecast → verify → correct.

4.2 Public API surface
Only these symbols are exported from lulzprime.__init__:
Prime resolution
* resolve(index: int) -> int Returns the exact p_index using forecast + π(x) refinement + primality-confirmed correction.
* forecast(index: int) -> int Returns an analytic estimate for p_index. Not guaranteed exact.
Range resolution
* between(x: int, y: int) -> list[int] Returns all primes in [x, y] via localized primality testing.
Local navigation
* next_prime(n: int) -> int Returns the smallest prime >= n.
* prev_prime(n: int) -> int Returns the largest prime <= n (error if none).
Primality predicate
* is_prime(n: int) -> bool Returns True if n is prime within the supported guarantee tier (see 4.4).
OMPC simulator (optional mode)
* simulate(n_steps: int, *, seed: int | None = None, diagnostics: bool = False, **params) -> list[int] | tuple[list[int], list[tuple]] Returns pseudo-primes q_n, optionally with diagnostics checkpoints.

4.3 Contract rules (global)
1. No silent behavior changes. If defaults change, bump minor version and document.
2. Determinism by default. For simulation, determinism requires explicit seed.
3. No hidden heavy precompute. Any warm-start step must be explicit and measurable.
4. No network access. Ever.
5. Errors are explicit. No “best effort” returning wrong primes.

4.4 Guarantee tiers
To prevent ambiguous correctness claims, lulzprime defines guarantee tiers:
* Tier A (Exact): resolve() returns the exact p_n by construction (π(x) + correction + primality confirmation).
* Tier B (Verified): between(), next_prime(), prev_prime() return exact primes because they confirm via primality testing.
* Tier C (Estimate): forecast() is an estimate only, used for navigation.
If a call cannot satisfy its tier, it must raise an error.

4.5 Input validation contracts
* All public functions validate types and bounds.
* index must be >= 1.
* between(x, y) requires x <= y and y >= 2.
* prev_prime(n) raises if n < 2.

4.6 Stability promises
* The names and signatures in 4.2 are stable for v0.1 through v1.0 unless explicitly deprecated.
* Internal modules may change without notice, as long as 4.2 behavior remains unchanged.

4.7 Internal interface contracts (non-public, but fixed for maintainability)
These are internal “protocol boundaries” that future contributors must obey.
PrimeCounter (π(x) backend)
* pi(x: int) -> int (exact where implemented)
* Must be monotone and correct for tested ranges.
PrimalityTester
* is_prime(n: int) -> bool
* Guarantee scope must be stated (e.g., deterministic for 64-bit, probable for big ints).
ResolverPipeline (resolve chain)
* resolve(index: int) -> int
* Must follow: forecast → bracket → refine with π(x) → correct with primality.
No component may bypass this chain.

4.8 Success definition (for this part)
This part is satisfied if:
* All public functions are fully specified.
* Correctness guarantees are unambiguous.
* Agents cannot invent new public functions without violating this part.
* Implementation can evolve without breaking the public contract.
