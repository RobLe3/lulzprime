> ⚠️ **Status: Historical / Archived**
>
> This document reflects the development process used while LULZprime was actively evolving.
> The project is now a completed, reference-grade implementation.
> This file is retained for context and provenance only.

Part 5 of 9, Internal Execution Chains and Workflows
5.1 Canonical reference
* Canonical concept source: OMPC_v1.33.7lulz.pdf
* Rule: Core workflows must follow the paper’s “forecast → verify/correct” approach and OMPC feedback definitions where used.

5.2 Workflow, forecast(index)
Intent: Provide an analytic jump point for p_index (estimate only).
Steps:
1. Validate index >= 1.
2. For small index, return from a small hardcoded list.
3. For larger index, compute refined estimate:
    * q_hat = n * (log n + log log n - 1) (integer truncated).
4. Return q_hat.
Output class: Tier C (Estimate).

5.3 Workflow, resolve(index)
Intent: Return the exact p_index efficiently without full sieving.
Canonical chain: forecast → bracket → π(x) refinement → deterministic correction → verify
Steps:
1. Validate index >= 1.
2. guess = forecast(index).
3. Choose an initial lower bound lo near the guess (conservative window), ensuring lo >= 2.
4. Choose an upper bound hi that is guaranteed to contain p_index (use known analytic upper bound strategy).
5. If pi(lo) > index, widen lo downwards (fallback to 2).
6. Binary search on [lo, hi] to find minimal x with pi(x) >= index.
7. Let x be that minimal value.
8. Deterministic correction:
    * If x not prime, step to previous prime.
    * While pi(x) > index, step backward prime-by-prime.
    * While pi(x) < index, step forward prime-by-prime.
9. Return x.
Output class: Tier A (Exact).

5.4 Workflow, between(x, y)
Intent: Return primes in [x, y] using localized testing.
Steps:
1. Validate x <= y, clamp x to at least 2.
2. Start at p = next_prime(x).
3. While p <= y:
    * append p (or yield in generator variant),
    * set p = next_prime(p + 1).
4. Return list.
Output class: Tier B (Verified).

5.5 Workflow, next_prime(n) and prev_prime(n)
Intent: Local navigation primitives.
next_prime steps:
1. If n <= 2, return 2.
2. If even, increment to next odd.
3. Loop: test primality, if not, add 2.
prev_prime steps:
1. If n < 2, raise.
2. If n == 2, return 2.
3. If even, decrement to odd.
4. Loop: test primality, if not, subtract 2, stop if below 2.
Output class: Tier B (Verified).

5.6 Workflow, is_prime(n)
Intent: Provide a fast, reliable primality predicate for the library’s guarantee scope.
Steps:
1. Handle small n and small primes.
2. Fast small-prime divisibility checks.
3. Run deterministic Miller–Rabin for 64-bit range (fixed bases), as in the paper’s reference approach.
Output class: Tier B (Verified within stated range).

5.7 Workflow, simulate(n_steps, ...)
Intent: Generate pseudo-primes q_n using OMPC negative feedback control. Not a claim of exact primes.
Canonical chain: gap model → density ratio w → tilted sampling → update q
Steps:
1. Validate n_steps > 0.
2. Initialize q_1 (default 2 or warm-start per configuration).
3. Prepare gap distribution P0(g) from gaps.py (empirical or provided).
4. For each step n:
    * compute w(q_n) = (q_n / log q_n) / n (density ratio),
    * compute beta_n via annealing schedule if enabled,
    * sample gap g ~ P(g|w) using log-weight tilt:
        * log P(g|w) = log P0(g) + beta*(1-w)*log g + C,
    * set q_{n+1} = q_n + g.
5. If diagnostics enabled, record sparse checkpoints including pi(q_n)/n where configured.
6. Return sequence, plus diagnostics if requested.
Output class: Simulation output (non-exact), validated via diagnostics.

5.8 Workflow invariants (must remain true)
* resolve() must never depend on OMPC simulation to be correct.
* forecast() must be callable without any precompute.
* Simulation must be reproducible with fixed seeds.
* Diagnostics must never change results, only observe them.

5.9 Success definition (for this part)
This part is satisfied if:
* Each public function has one canonical internal chain.
* Chains match the paper’s described mechanisms and scope.
* Implementations can be verified against these workflows without ambiguity.
