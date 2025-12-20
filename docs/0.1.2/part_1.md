> ⚠️ **Status: Historical / Archived**
>
> This document reflects the development process used while LULZprime was actively evolving.
> The project is now a completed, reference-grade implementation.
> This file is retained for context and provenance only.

Part 1 of 9, Concept and Origin, Canonical Reference
1.1 Canonical reference rule
* Canonical concept source: OMPC_v1.33.7lulz.pdf
* If in doubt, check the paper. When any design, naming, or behavior is ambiguous, the paper is the source of truth. Code and comments must conform to it.
1.2 What lulzprime is
lulzprime is a Python library for prime resolving and prime navigation, meaning fast access to:
* the nth prime p_n (index-based resolution),
* primes in a numeric interval [x, y] (range-based resolution),
* prime candidates near a target (neighborhood resolution), using analytic forecasting + localized verification, derived from OMPC.
1.3 What lulzprime is derived from
The library is derived from the OMPC approach described in the paper:
* analytic forecast for the location of p_n (refined PNT approximation),
* exact refinement via prime counting π(x) and correction,
* localized primality testing rather than global sieving,
* optional OMPC simulator using negative feedback on density ratio w(q_n) for generating prime-like sequences.
1.4 The problem lulzprime solves
Provide a hardware-efficient and script-friendly way to resolve primes without:
* precomputing huge prime tables,
* running full sieves for point lookups,
* writing ad-hoc, error-prone primality loops.
1.5 Primary outcomes
* Resolve: quickly compute p_n with forecast → correction → verification.
* Range query: list primes in [x, y] using localized testing.
* Batch mode: scale the same primitives to build tables or serve many queries.
* Simulation mode: generate pseudo-prime sequences for testing and analysis (not as truth, as a controlled stochastic surrogate).
1.6 Non-goals and explicit non-claims
lulzprime must not claim or implement:
* factorization acceleration,
* cryptographic breaks (RSA/ECC/discrete log),
* “predicting primes” as deterministic truth,
* replacing cryptographic entropy requirements. It is an efficiency and navigation toolkit, consistent with the paper’s scope.
1.7 Terminology used across the manual
* p_n: true nth prime.
* π(x): prime counting function.
* forecast(n): analytic estimator for p_n used as a jump point.
* resolve(n): exact p_n recovery pipeline (forecast + π(x) + correction + primality confirmation).
* between(x, y): primes in an interval via localized verification.
* OMPC simulator: stochastic generator of q_n (pseudo-primes) governed by density feedback w(q_n) (optional mode).
