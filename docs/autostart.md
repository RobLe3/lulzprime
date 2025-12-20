# autostart.md
**LULZprime – Agent / Developer Startup Order, Consultation Priority, and Tracking Files (v0.2.0)**

---

## 0. Purpose

This document defines the **startup procedure** for humans and agentic systems working on LULZprime as of version **0.2.0** (released December 20, 2025).

It answers:
- which files must be parsed first,
- which references override others when uncertainty occurs,
- where progress is recorded,
- where open work is tracked,
- where bugs and corrections are tracked,
- and in what order these files are read and updated.

This file is a **runbook**, the first operational entry point after cloning the repo.

---

## 1. Canonical Precedence (Always Applies)

When there is any conflict or uncertainty, resolve by consulting sources in this order:

1. The canonical OMPC paper located at `docs/paper/OMPC_v1.33.7lulz.pdf`  
   **Rule: If in doubt, consult the paper first.**  
2. `docs/0.2.0/` (current active development manual Parts 0–9 and version-specific guidance)  
3. `docs/0.1.2/` (historical manual for v0.1.2)  
4. `docs/defaults.md`  
5. Source code under `src/lulzprime/`  
6. Code comments

If the local copy of the paper is not decisive, cross-reference the online source at `https://roblemumin.com/library.html`.

---

## 2. Required Development Tracking Files

The following tracking files are mandatory and live directly in `docs/`:

- `docs/milestones.md`  
  Records **completed, verified, and accepted** achievements and deliverables.

- `docs/todo.md`  
  Records **planned work** that is identified but not yet started or actively in progress.

- `docs/issues.md`  
  Records **bugs, regressions, constraint violations, workflow deviations, performance regressions, and spec ambiguities**.

These three files are the operational memory of the project.  
They must remain short, current, structured, and reflect the state of v0.2.0.

---

## 3. One-Time Setup Parse Order (Fresh Clone)

On a fresh clone of v0.2.0, parse in this order:

1. `docs/defaults.md`  
   Establishes repo rules, structure, and hygiene.

2. `docs/autostart.md` (this file)  
   Establishes startup and tracking procedures.

3. The canonical paper: `docs/paper/OMPC_v1.33.7lulz.pdf`  
   Review core conjecture, equations, and claims.

4. `docs/0.2.0/` folder contents  
   - First: `part_0.md` through `part_9.md` (current active development manual)  
   - Then: `release_notes.md`, `migration_guide.md`, `benchmarks_summary.md`, `activation_instructions.md` (version-specific guidance)

5. `docs/0.1.2/` folder contents (optional but recommended for context)  
   Historical Parts 0–9 from the v0.1.2 development cycle.

6. `docs/milestones.md`  
   Review completed work and v0.2.0 deliverables.

7. `docs/issues.md`  
   Confirm no open critical issues.

8. `docs/todo.md`  
   Review any remaining planned work.

9. Only then, parse code:  
   `src/lulzprime/__init__.py` and relevant modules.

If any required file is missing or outdated, stop and repair before proceeding.

---

## 4. Normal Daily Parse Order (Routine Work on v0.2.0+)

At the start of any session:

1. `docs/defaults.md`  
2. `docs/autostart.md` (this file)  
3. The canonical paper: `docs/paper/OMPC_v1.33.7lulz.pdf` (quick scan of relevant sections if needed)  
4. `docs/0.2.0/part_0.md` (concept refresh)  
5. `docs/0.2.0/part_2.md` (constraints)  
6. `docs/0.2.0/part_4.md` (public API contracts)  
7. `docs/0.2.0/part_6.md` (forecasting and π(x) backends)  
8. `docs/0.2.0/part_9.md` (alignment and verification)

Then consult current state:
9. `docs/issues.md` → Address any open items first (bugs/regressions take priority)  
10. `docs/todo.md` → Select next planned task  
11. `docs/milestones.md` → Avoid duplicating completed work

Only then proceed to code changes.

---

## 5. “If in Doubt” Consultation Order

When uncertain about correctness, scope, or intent:

1. The canonical paper: `docs/paper/OMPC_v1.33.7lulz.pdf`  
2. `docs/0.2.0/` (current manual Parts 0–9)  
3. `docs/0.1.2/` (historical context only)  
4. `docs/defaults.md`  
5. Existing tests under `tests/`  
6. If still uncertain → create entry in `docs/issues.md` labeled `SPEC-AMBIGUITY` and stop change.

---

## 6. Update Rules for Tracking Files (v0.2.0)

### 6.1 `docs/issues.md`
Update **immediately** when:
- A test fails
- A regression is detected
- A constraint is violated (e.g., memory >25 MB)
- Performance falls below v0.2.0 benchmarks
- A scope boundary is crossed
- Spec ambiguity arises

Issues must be triaged before starting new features.

### 6.2 `docs/todo.md`
Update when:
- New enhancement is proposed and accepted
- Work is deferred
- Future optimization is identified

Each item must reference:
- Related manual part(s) in `docs/0.2.0/`
- Target module(s)
- Measurable success criterion

### 6.3 `docs/milestones.md`
Update **only** when:
- A deliverable is fully complete
- All tests and verification pass
- Benchmarks confirm no regression
- Alignment with OMPC paper is maintained

Milestones must include:
- Summary
- Goal mapping
- Verification evidence (tests/benchmarks)
- Commit/tag reference

---

## 7. Mandatory Triggers for Re-Reading Files

### 7.1 Before changing public API
Read: `docs/paper/OMPC_v1.33.7lulz.pdf`, `docs/0.2.0/part_4.md`, `docs/0.2.0/part_9.md` → Log as `API-CHANGE-PROPOSAL` in `issues.md`.

### 7.2 Before performance work
Read: `docs/paper/OMPC_v1.33.7lulz.pdf` (pages 8–9), `docs/0.2.0/part_2.md`, `docs/0.2.0/part_6.md`, `docs/0.2.0/part_9.md`.

### 7.3 Before modifying π(x) or forecast backends
Read: `docs/paper/OMPC_v1.33.7lulz.pdf` (pages 6–9), `docs/0.2.0/part_6.md`, historical notes in `docs/0.1.2/` if needed.

### 7.4 Before simulator changes
Read: `docs/paper/OMPC_v1.33.7lulz.pdf` (pages 6–7), `docs/0.2.0/part_5.md`, historical convergence fixes in `docs/issues.md` or `docs/0.1.2/`.

---

## 8. Required End-of-Work Session Procedure

At session end:

1. Run full test suite.
2. If failures: update `docs/issues.md`.
3. If incomplete tasks: update `docs/todo.md`.
4. If deliverable complete and verified: update `docs/milestones.md`.
5. Confirm no forbidden artifacts (per `defaults.md`).
6. Commit with message referencing relevant issue/todo/milestone.

---

## 9. File Locations (Single Source of Truth – v0.2.0)

- Canonical paper: `docs/paper/OMPC_v1.33.7lulz.pdf`
- Current manual & guidance: `docs/0.2.0/` (Parts 0–9 + release artifacts)
- Historical manual: `docs/0.1.2/` (Parts 0–9 from v0.1.2)
- Repo defaults: `docs/defaults.md`
- Startup/runbook: `docs/autostart.md` (this file)
- Tracking:
  - `docs/milestones.md`
  - `docs/todo.md`
  - `docs/issues.md`
- Code: `src/lulzprime/`
- Tests: `tests/`

---

## 10. Success Condition (v0.2.0)

This process is successful if:
- references are consulted in correct order (paper first),
- scope drift is prevented,
- corrections are captured immediately,
- milestones reflect verified v0.2.0 deliverables,
- historical v0.1.2 context is preserved but not active,
- and development remains aligned with the canonical OMPC reference in `docs/paper/`.

End of document.