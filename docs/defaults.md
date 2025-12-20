# defaults.md
**LULZprime – Development Defaults, Repository Scaffold, and Operational Rules (v0.2.0)**

---

## 0. Purpose and Scope

This document defines the **non-negotiable development defaults** for the LULZprime project as of version **0.2.0** (released December 20, 2025).  
It serves as a **one-stop operational reference** for humans and agentic systems.

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
2. `docs/0.2.0/` (current development manual and version guidance)
3. `docs/0.1.2/` (historical manual for v0.1.2)
4. `docs/defaults.md` (this file)
5. Source code
6. Code comments

Any conflict must be resolved by moving **up** this list.

---

## 2. Repository and Access Defaults

### 2.1 Canonical repository
- **GitHub repository:**  
  `https://github.com/RobLe3/lulzprime`

### 2.2 Canonical user identity
- **Git identity:** `github@roblemumin.com`

### 2.3 Access method
- Repository access is via **SSH**, not HTTPS.
- Local development uses the `git` CLI talking to GitHub over SSH.

Expected remote form:
git@github.com:RobLe3/lulzprime.git

---

## 3. Default Repository Structure (v0.2.0)

lulzprime/  
├── README.md  
├── LICENSE  
├── pyproject.toml  
├── CHANGELOG.md  
├── SECURITY.md  
├── CONTRIBUTING.md  
├── CODEOWNERS  
├── .gitignore  
├── .gitattributes  
├── .editorconfig  
├── .pre-commit-config.yaml  
│  
├── docs/  
│   ├── defaults.md                 # THIS FILE  
│   ├── autostart.md  
│   ├── index.md  
│   ├── milestones.md  
│   ├── todo.md  
│   ├── issues.md  
│   ├── adr/  
│   ├── diagrams/  
│   ├── paper/                      # Canonical location for the OMPC paper  
│   │   └── OMPC_v1.33.7lulz.pdf  
│   ├── 0.1.2/                      # Historical development manual for v0.1.2  
│   │   ├── part_0.md  
│   │   ├── part_1.md  
│   │   ├── part_2.md  
│   │   ├── part_3.md  
│   │   ├── part_4.md  
│   │   ├── part_5.md  
│   │   ├── part_6.md  
│   │   ├── part_7.md  
│   │   ├── part_8.md  
│   │   └── part_9.md  
│   └── 0.2.0/                       # Current development manual and release artifacts  
│       ├── part_0.md  
│       ├── part_1.md  
│       ├── part_2.md  
│       ├── part_3.md  
│       ├── part_4.md  
│       ├── part_5.md  
│       ├── part_6.md  
│       ├── part_7.md  
│       ├── part_8.md  
│       ├── part_9.md  
│       ├── release_notes.md  
│       ├── migration_guide.md      # Guidance for upgrading from v0.1.2  
│       ├── benchmarks_summary.md   # Curated performance results for v0.2.0  
│       └── activation_instructions.md  # Config changes, Meissel-Lehmer activation, etc.  
│  
├── src/  
│   └── lulzprime/  
│       ├── __init__.py  
│       ├── config.py  
│       ├── utils.py  
│       ├── types.py  
│       ├── forecast.py  
│       ├── primality.py  
│       ├── pi.py  
│       ├── lookup.py  
│       ├── resolve.py  
│       ├── simulator.py  
│       ├── gaps.py  
│       ├── diagnostics.py  
│       └── lehmer.py                   # Dedicated Meissel-Lehmer backend module  
│  
├── tests/  
│   ├── test_api_contracts.py  
│   ├── test_resolve.py  
│   ├── test_between.py  
│   ├── test_primality.py  
│   ├── test_pi.py  
│   ├── test_simulator.py  
│   └── fixtures/  
│  
├── benchmarks/  
│   ├── README.md  
│   ├── bench_resolve.py  
│   ├── bench_between.py  
│   └── results/  
│  
└── tools/  
    ├── validate_part_contracts.py  
    ├── smoke_run.py  
    └── release_checklist.md  

**Rules:**
- All importable code lives under `src/lulzprime/`.
- Core tracking files live directly under `docs/`.
- The canonical OMPC paper **must** reside in `docs/paper/`.
- Historical development manual for v0.1.2 is archived in `docs/0.1.2/` (renamed from the original `docs/manual/`).
- Current active development manual (Parts 0–9) and version-specific guidance for v0.2.0 reside in `docs/0.2.0/`.
- Future releases will follow the same pattern (e.g., `docs/0.3.0/` containing the then-current manual).

**v0.2.0 Specific Notes:**
- The original `docs/manual/` has been renamed to `docs/0.1.2/` to preserve the exact v0.1.2 development context as immutable history.
- A new, updated set of Parts 0–9 reflecting v0.2.0 refinements now lives in `docs/0.2.0/`.
- Additional release artifacts (notes, migration, benchmarks) are also in `docs/0.2.0/`.

---

## 4. Files and Artifacts That Must Never Be Committed

### 4.1 Absolute exclusions
The following must **never** be uploaded to the repository:

- SSH keys and certificates: `id_rsa`, `id_ed25519`, `*.pem`, `*.key`, `*.p12`, `*.pfx`
- Secrets and tokens: `.env`, `.env.*`, `*secret*`, `*token*`, `*apikey*`
- Credential caches: `.netrc`, keychains, browser profiles
- Virtual environments: `.venv/`, `venv/`
- Build outputs: `dist/`, `build/`, `*.whl`, `*.egg-info/`
- Coverage and test noise: `.coverage`, `htmlcov/`, `.pytest_cache/`
- IDE and OS artifacts: `.DS_Store`, `Thumbs.db`, `.idea/`, `.vscode/`
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

### 6.1 Historical Manual (v0.1.2)
- Archived in `docs/0.1.2/` (Parts 0–9).
- Treated as immutable unless correcting reproducibility issues.

### 6.2 Current Manual (v0.2.0)
- Active Parts 0–9 live in `docs/0.2.0/`.
- This is the living development manual for ongoing work.

### 6.3 Canonical paper
- Stored in `docs/paper/OMPC_v1.33.7lulz.pdf`.
- Long verbatim excerpts must **not** be copied into docs.
- Docs may summarize and reference, not reproduce.

### 6.4 Diagrams
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

Large artifacts must be generated on demand or stored externally.

---

## 8. Build, Test, and Quality Defaults

- Packaging via `pyproject.toml`
- `src/` layout mandatory
- Tests via `pytest` (target: 200+ passing tests)
- Public API contract tests mandatory
- Performance regressions tracked (benchmarks/results/)
- Meissel-Lehmer π(x) backend enabled by default (`ENABLE_LEHMER_PI = True`)

No merge is acceptable without passing tests.

---

## 9. Branching and Release Discipline

### 9.1 Branches
- `main` is always releasable
- Feature branches: `feat/<topic>`, `fix/<topic>`, `docs/<topic>`

### 9.2 Releases
- Semantic versioning
- Update `CHANGELOG.md`
- Run `tools/release_checklist.md`

---

## 10. Contributor and Agent Expectations

Any contributor or agent must:
- read this file before making changes,
- consult `docs/0.2.0/` for current manual and guidance,
- reference `docs/0.1.2/` only for historical context,
- respect scope and non-goals,
- defer to the paper when uncertain.

Violations invalidate contributions.

---

## 11. Enforcement Rule

This document is **binding**.

If a contribution violates:
- `defaults.md`,
- current version guidance,
- or the canonical paper,

it must be rejected or reverted.

---

## 12. Success Condition

`defaults.md` is considered effective if:
- repository hygiene remains clean,
- no sensitive artifacts leak,
- development remains reproducible,
- historical v0.1.2 manual is preserved in `docs/0.1.2/`,
- current manual and guidance are centralized in `docs/0.2.0/`,
- and the project remains aligned with `OMPC_v1.33.7lulz.pdf`.

End of document.