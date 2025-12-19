> ⚠️ **Status: Historical / Archived**
>
> This document reflects the development process used while LULZprime was actively evolving.
> The project is now a completed, reference-grade implementation.
> This file is retained for context and provenance only.

Part 7 of 9, Diagnostics, Verification, and Self-Checks
7.1 Canonical reference
* Canonical concept source: OMPC_v1.33.7lulz.pdf
* Rule: Diagnostics and verification mechanisms must mirror the falsifiability philosophy and measurable criteria defined in the paper.

7.2 Purpose of diagnostics
Diagnostics exist to:
* verify correctness claims,
* detect drift or instability,
* prevent silent regressions,
* support agentic self-verification.
Diagnostics must observe only. They must never alter computational results.

7.3 Mandatory verification classes
A. Resolution verification (Tier A)
Applies to resolve():
* Verify pi(result) == index.
* Verify is_prime(result) == True.
* Any failure is a hard error.
B. Range verification (Tier B)
Applies to between(), next_prime(), prev_prime():
* Each returned value must satisfy is_prime(p).
* Ordering must be strictly increasing.
* No duplicates allowed.
C. Forecast sanity (Tier C)
Applies to forecast():
* Used only as an estimate.
* Optional check: abs(pi(forecast(n)) - n) / n < ε (configurable, non-fatal).

7.4 OMPC simulator diagnostics
For simulate() runs, the following diagnostics must be available:
* Density alignment: track pi(q_n) / n.
* Convergence: verify pi(q_n) / n → 1 as n grows.
* Drift detection: flag monotonic deviation beyond threshold.
* Reproducibility: identical output for fixed seed and parameters.
These checks reflect the paper’s verification gates and failure modes.

7.5 Logging and observability rules
* Diagnostics output must be structured (tuples, dicts, or records).
* No implicit printing.
* Diagnostics may be sampled (sparse checkpoints) to control overhead.
* Logging must be disableable with zero cost when off.

7.6 Regression test requirements
Every public function must have:
* correctness tests (exactness or verification tier),
* boundary tests (small inputs, limits),
* reproducibility tests (where applicable).
Regression tests must fail fast and loudly.

7.7 Agentic self-check markers
For agent-driven development, the following self-checks are mandatory:
* API drift check: public functions match Part 4 exactly.
* Workflow conformance: internal execution chains match Part 5.
* Constraint compliance: no forbidden dependencies or behaviors from Part 2.
* Canonical alignment: no logic contradicts the paper.
Violation of any marker invalidates the change.

7.8 Failure handling rules
* No silent fallback to slower or different algorithms.
* No partial success returns.
* All verification failures raise explicit, typed errors.

7.9 Success definition (for this part)
This part is satisfied if:
* All correctness claims are mechanically verifiable.
* Simulation behavior is falsifiable and observable.
* Agents can detect drift, regression, or scope violations automatically.
* The system remains aligned with OMPC verification philosophy.
