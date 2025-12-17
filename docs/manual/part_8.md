Part 8 of 9, Extension Rules and Third-Party Contributions
8.1 Canonical reference
* Canonical concept source: OMPC_v1.33.7lulz.pdf
* Rule: Extensions must not alter or contradict the mechanisms, scope, or claims defined in the paper.

8.2 Purpose of this part
This part defines where creativity is allowed and where it is forbidden, so the project remains stable, auditable, and aligned even when extended by third parties or agentic systems.

8.3 Allowed extension zones (explicitly permitted)
Extensions are allowed only in the following areas:
1. π(x) backends
    * New prime-counting implementations may be added.
    * Must satisfy the PrimeCounter interface.
    * Must clearly state correctness bounds and tested ranges.
2. Primality testing backends
    * Additional primality tests may be added.
    * Must document guarantee tier (deterministic range or probabilistic).
    * Must not weaken guarantees of public API functions.
3. Execution backends
    * Multiprocessing, GPU, or distributed executors.
    * Must be optional and isolated from core modules.
    * Must preserve determinism where applicable.
4. Table storage backends
    * New storage formats (binary, sqlite, parquet, etc.).
    * Must not affect correctness or resolution logic.
5. Diagnostics and visualization
    * Additional diagnostics, plotting, or reporting layers.
    * Must be strictly observational.

8.4 Forbidden extension zones (hard bans)
The following are not allowed:
* Modifying the semantics of public API functions.
* Replacing forecast → correction pipelines with heuristic shortcuts.
* Introducing global sieving into core resolution paths.
* Adding AI, ML, or heuristic “prime prediction.”
* Adding network calls or remote dependencies.
* Making cryptographic claims beyond those explicitly denied in the paper.
Violations invalidate the extension.

8.5 Extension integration rules
* All extensions must live outside core modules.
* Core modules must not import optional extensions.
* Extensions must register via explicit hooks or factories.
* No monkey-patching of core functions.

8.6 Versioning and compatibility rules
* Core API changes require a documented version bump.
* Extensions must declare compatibility with core versions.
* Deprecated APIs must remain available for at least one minor release cycle.

8.7 Review and validation requirements
Every extension must provide:
* a short scope declaration,
* a list of modified or extended interfaces,
* verification evidence that core guarantees still hold.
Extensions without validation are unsupported.

8.8 Agentic development constraints
For agent-driven extensions:
* Agents may not invent new public API endpoints.
* Agents must pass all Part 7 self-check markers.
* Agents must fail closed when uncertain.

8.9 Success definition (for this part)
This part is satisfied if:
* Third parties can extend the system without breaking it.
* Core logic remains untouched and auditable.
* Creativity is channeled into safe, bounded areas.
* Long-term maintainability is preserved.
