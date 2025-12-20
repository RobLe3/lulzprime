> ⚠️ **Status: Historical / Archived**
>
> This document reflects the development process used while LULZprime was actively evolving.
> The project is now a completed, reference-grade implementation.
> This file is retained for context and provenance only.

Part 3 of 9, High-Level Architecture Blueprint
3.1 Canonical reference
* Canonical concept source: OMPC_v1.33.7lulz.pdf
* Rule: Architecture must not contradict the paper’s scope or mechanisms.

3.2 Architectural overview
lulzprime is structured as a layered, modular system with a strict separation between:
* Public API (stable, minimal),
* Core computation (forecast, counting, verification),
* Optional scale components (batching, parallelism, storage).
No layer may bypass another.

3.3 Module layout and responsibilities
lulzprime/
├── __init__.py        # Public API re-exports only
├── resolve.py         # User-facing resolution functions
├── forecast.py        # Analytic estimators (PNT-based)
├── lookup.py          # Jump-adjust pipelines
├── pi.py              # Prime counting backends (π(x))
├── primality.py       # Primality testing utilities
├── simulator.py       # OMPC simulator (optional mode)
├── gaps.py            # Gap distributions for simulation
├── diagnostics.py     # Verification and convergence checks
├── config.py          # Defaults and tunables
├── utils.py           # Shared helpers

3.4 Public API boundary
Only the following are considered public:
* resolve(n)
* between(x, y)
* forecast(n)
* next_prime(n)
* prev_prime(n)
* is_prime(n)
* simulate(...)
Everything else is internal and may change without notice.

3.5 Core tier (mandatory)
Always available, single-thread friendly:
* forecast.py
* lookup.py
* pi.py
* primality.py
* resolve.py
No optional dependencies allowed here.

3.6 Scale tier (optional)
May be added later without modifying core:
* batch generation
* multiprocessing
* GPU / distributed executors
* persistent prime tables
These must live outside core modules and use defined interfaces only.

3.7 Dependency direction rules
* resolve.py may call forecast, lookup, primality, pi
* lookup.py may call forecast, pi, primality
* forecast.py must not call anything else
* simulator.py must not call resolve or lookup
* diagnostics.py may observe, never mutate
Violations are design errors.

3.8 Extensibility boundaries
* New π(x) methods go into pi.py behind a common interface.
* New primality tests go into primality.py.
* New simulators must live beside simulator.py, not replace it.
* No extension may alter public API semantics.

3.9 Success definition (for this part)
This part is satisfied if:
* Every function has exactly one home.
* The public API remains small and stable.
* Core functionality remains usable on low-end hardware.
* Optional scale features can be added without refactoring the core.
