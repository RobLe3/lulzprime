Part 0 of 9, Canonical Context and High-Level Abstraction (Agent Primer)
0.1 Canonical reference
* Canonical concept source: OMPC_v1.33.7lulz.pdf
* Absolute rule: This paper is the conceptual ground truth. If any later part, code decision, or agent inference conflicts with the paper, the paper overrides everything.

0.2 What the paper is really about (one level up)
The paper does not claim to generate or predict prime numbers deterministically. Instead, it shows that:
The statistical structure of primes can be navigated efficiently using analytic forecasting + exact correction, without enumerating all primes below a target.
This reframes primes from a brute-force object into a navigable space.

0.3 Core abstraction introduced by OMPC
OMPC introduces three separable ideas:
1. Analytic navigation
    * Use refined Prime Number Theorem approximations to jump close to a desired prime location.
    * This gives a cheap, O(1) estimate for where the target lies.
2. Exact correction
    * Use exact prime counting π(x) and local primality tests to correct the estimate.
    * This guarantees correctness without global sieving.
3. Controlled stochastic modeling (optional)
    * A constrained probabilistic simulator reproduces prime-like statistics using negative feedback.
    * This is for simulation, validation, and insight — not truth generation.
The first two form a deterministic lookup engine. The third provides context, falsifiability, and testing power.

0.4 The key conceptual shift
Traditional thinking:
* “To get big primes, you must generate or sieve everything below them.”
OMPC thinking:
* “You can navigate to primes using math, then verify locally.”
This is analogous to:
* DNS vs brute-force IP scanning
* Binary search vs linear search
* Routing vs flooding

0.5 What lulzprime inherits from the paper
lulzprime inherits only what the paper justifies:
* Forecast → verify → correct pipelines
* Exactness via correction, not guessing
* Efficiency via locality, not enumeration
* Clear falsifiability and diagnostics
* Strict separation between:
    * exact resolution,
    * estimates,
    * simulations
It does not inherit:
* cryptographic claims,
* factorization shortcuts,
* speculative models beyond the paper’s scope.

0.6 Why this part exists (agent guidance)
This part exists so that agents do not misinterpret the project as:
* a prime generator,
* a probabilistic oracle,
* an AI prediction system,
* or a cryptographic attack tool.
Agents must internalize:
* primes are deterministic,
* navigation is analytic,
* correctness comes from verification,
* simulation is explanatory, not authoritative.

0.7 Mental model agents must use
When building or modifying lulzprime, agents must think in this order:
1. Where should the prime roughly be? (analytic forecast)
2. How do I verify and correct efficiently? (π(x), primality)
3. How do I prove I stayed aligned? (diagnostics, falsifiability)
Any deviation from this order is a design error.

0.8 Success condition for Part 0
Part 0 is satisfied if:
* An agent can explain lulzprime’s purpose without mentioning sieving as default.
* An agent can distinguish exact results from estimates and simulations.
* An agent understands why OMPC is the canonical reference.
* An agent will defer to the paper when uncertain.
