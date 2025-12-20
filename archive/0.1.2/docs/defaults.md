> ⚠️ **Status: Historical / Archived**
>
> This document reflects the development process used while LULZprime was actively evolving.
> The project is now a completed, reference-grade implementation.
> This file is retained for context and provenance only.

# defaults.md
**LULZprime – Development Defaults, Repository Scaffold, and Operational Rules**

---

## 0. Purpose and Scope

This document defines the **non-negotiable development defaults** for the LULZprime project.  
It serves as a **one-stop operational reference** for humans and agentic systems involved in development.

It specifies:
- repository structure and layout,
- development and contribution rules,
- forbidden files and artifacts,
- documentation handling,
- verification and hygiene expectations,
- and canonical references.

This document is **binding**, not advisory.

---

## 1. Canonical References and Precedence

### 1.1 Canonical concept source
- **Primary reference:** `https://roblemumin.com/library.html`
- **Rule:** *If in doubt, check the paper.*

### 1.2 Precedence order (highest to lowest)
1. `https://roblemumin.com/library.html`
2. `docs/manual/part_0.md` through `part_9.md`
3. `docs/defaults.md` (this file)
4. Source code
5. Code comments

Any conflict must be resolved by moving **up** this list.

---

## 2. Repository and Access Defaults

### 2.1 Canonical repository
- **GitHub repository:**  
  `https://github.com/RobLe3/lulzprime`

### 2.2 Canonical user identity
- **Git identity:** `github@roblemumin.com`

### 2.3 Access method
- Repository access is assumed via **SSH**, not HTTPS.
- Local development uses the `git` CLI talking to GitHub over SSH.

Expected remote form:
git@github.com:RobLe3/lulzprime.git
---

## 3. Default Repository Structure

lulzprime/ ├── README.md ├── LICENSE ├── pyproject.toml ├── CHANGELOG.md ├── SECURITY.md ├── CONTRIBUTING.md ├── CODEOWNERS ├── .gitignore ├── .gitattributes ├── .editorconfig ├── .pre-commit-config.yaml │ ├── docs/ │ ├── defaults.md # THIS FILE │ ├── index.md │ ├── manual/ │ │ ├── part_0.md │ │ ├── part_1.md │ │ ├── part_2.md │ │ ├── part_3.md │ │ ├── part_4.md │ │ ├── part_5.md │ │ ├── part_6.md │ │ ├── part_7.md │ │ ├── part_8.md │ │ └── part_9.md │ ├── adr/ │ └── diagrams/ │ ├── paper/ │ └── OMPC_v1.33.7lulz.pdf │ ├── src/ │ └── lulzprime/ │ ├── init.py │ ├── resolve.py │ ├── forecast.py │ ├── lookup.py │ ├── pi.py │ ├── primality.py │ ├── simulator.py │ ├── gaps.py │ ├── diagnostics.py │ ├── config.py │ ├── utils.py │ └── types.py │ ├── tests/ │ ├── test_api_contracts.py │ ├── test_resolve.py │ ├── test_between.py │ ├── test_primality.py │ ├── test_pi.py │ ├── test_simulator.py │ └── fixtures/ │ ├── benchmarks/ │ ├── README.md │ ├── bench_resolve.py │ ├── bench_between.py │ └── results/ │ └── tools/ ├── validate_part_contracts.py ├── smoke_run.py └── release_checklist.md
Rules:
- All importable code lives under `src/lulzprime/`.
- Documentation lives under `docs/`.
- The paper lives under `paper/`.

---

## 4. Files and Artifacts That Must Never Be Committed

### 4.1 Absolute exclusions
The following must **never** be uploaded to the repository:

- SSH keys and certificates:  
  `id_rsa`, `id_ed25519`, `*.pem`, `*.key`, `*.p12`, `*.pfx`
- Secrets and tokens:  
  `.env`, `.env.*`, `*secret*`, `*token*`, `*apikey*`
- Credential caches:  
  `.netrc`, keychains, browser profiles
- Virtual environments:  
  `.venv/`, `venv/`
- Build outputs:  
  `dist/`, `build/`, `*.whl`, `*.egg-info/`
- Coverage and test noise:  
  `.coverage`, `htmlcov/`, `.pytest_cache/`
- IDE and OS artifacts:  
  `.DS_Store`, `Thumbs.db`, `.idea/`, `.vscode/`
- Large generated prime tables
- Raw benchmark dumps or massive data files
- Agent logs containing internal system prompts or traces

If a file *might* contain secrets, it is treated as secret.

---

## 5. Default `.gitignore` Expectations

At minimum, `.gitignore` must cover:
- Python caches and bytecode
- Virtual environments
- Build artifacts
- Test and coverage artifacts
- OS and editor noise
- Environment files

The project favors **explicit ignores over accidental leaks**.

---

## 6. Documentation Handling Rules

### 6.1 Manual
- The development manual is split into Parts 0–9.
- Files live under `docs/manual/`.
- Each part is versioned, short, and scoped.

### 6.2 Canonical paper
- `https://roblemumin.com/library.html` must exist in the repo.
- Long verbatim excerpts must **not** be copied into docs.
- Docs may summarize and reference, not reproduce.

### 6.3 Diagrams
- Store diagram **sources**, not massive rendered exports.
- Prefer Mermaid, SVG source, or draw.io XML.

---

## 7. Development Artifacts Policy

### 7.1 Allowed
- Small benchmark summaries in markdown
- Small JSON fixtures for tests
- Architecture Decision Records (ADRs)
- Release notes and changelog entries

### 7.2 Disallowed by default
- Multi-GB data artifacts
- Full prime tables
- Scratch notebooks without curation

Large artifacts must be:
- generated on demand, or
- stored externally and documented.

---

## 8. Build, Test, and Quality Defaults

- Packaging via `pyproject.toml`
- `src/` layout is mandatory
- Tests via `pytest`
- Public API contract tests are mandatory
- Performance regressions are tracked (see Part 9)

No merge is acceptable without passing tests.

---

## 9. Branching and Release Discipline

### 9.1 Branches
- `main` is always releasable
- Feature branches:  
  `feat/<topic>`, `fix/<topic>`, `docs/<topic>`

### 9.2 Releases
- Semantic versioning
- Update `CHANGELOG.md`
- Run `tools/release_checklist.md`

---

## 10. Contributor and Agent Expectations

Any contributor or agent must:
- read this file before making changes,
- follow Parts 0–9 of the manual,
- respect scope and non-goals,
- defer to the paper when uncertain.

Violations invalidate contributions.

---

## 11. Enforcement Rule

This document is **binding**.

If a contribution violates:
- `defaults.md`,
- the manual,
- or the canonical paper,

it must be rejected or reverted.

---

## 12. Success Condition

`defaults.md` is considered effective if:
- repository hygiene remains clean,
- no sensitive artifacts leak,
- development remains reproducible,
- agentic systems stay within scope,
- and the project remains aligned with  
  `OMPC_v1.33.7lulz.pdf`.

End of document.
