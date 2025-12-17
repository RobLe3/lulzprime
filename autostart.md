# autostart.md  
**LULZprime – Agent / Developer Startup Order, Consultation Priority, and Tracking Files**

---

## 0. Purpose

This document defines the **startup procedure** for humans and agentic systems working on LULZprime.

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

1. `paper/OMPC_v1.33.7lulz.pdf`  
2. `docs/manual/part_0.md` … `docs/manual/part_9.md`  
3. `docs/defaults.md`  
4. Source code under `src/lulzprime/`  
5. Code comments

Rule: **If in doubt, check the paper first.**  
If the paper is not decisive, consult the manual next.

---

## 2. Required Development Tracking Files

The following tracking files are mandatory and live in `docs/`:

- `docs/milestones.md`  
  Records completed achievements and accepted deliverables.

- `docs/todo.md`  
  Records planned work that is not started or not assigned to an active effort.

- `docs/issues.md`  
  Records bugs, regressions, required corrections, and deviations from the manual/spec.

These three files are the operational memory of the project.  
They must stay short, current, and structured.

---

## 3. One-Time Setup Parse Order (Fresh Clone)

On a fresh clone, the required parse order is:

1. `docs/defaults.md`  
   Establishes repo rules, what must never be committed, and overall scaffolding.

2. `docs/manual/part_0.md`  
   Establishes the conceptual framing and how to interpret OMPC vs implementation.

3. `docs/manual/part_1.md`  
4. `docs/manual/part_2.md`  
5. `docs/manual/part_3.md`  
6. `docs/manual/part_4.md`  
7. `docs/manual/part_5.md`  
8. `docs/manual/part_6.md`  
9. `docs/manual/part_7.md`  
10. `docs/manual/part_8.md`  
11. `docs/manual/part_9.md`  

12. `docs/milestones.md`  
13. `docs/todo.md`  
14. `docs/issues.md`

15. Only then, parse code:  
   `src/lulzprime/__init__.py` and relevant modules.

If any manual files are missing, the startup must stop and the gap must be repaired first.

---

## 4. Normal Daily Parse Order (Routine Work)

At the start of any development session, parse in this order:

1. `docs/defaults.md`  
2. `docs/manual/part_0.md`  
3. `docs/manual/part_2.md` (goals and constraints refresh)  
4. `docs/manual/part_4.md` (public API contract)  
5. `docs/manual/part_5.md` (execution chains)  
6. `docs/manual/part_7.md` (verification/self-check markers)  
7. `docs/manual/part_9.md` (alignment measurement methods)

Then consult current state:
8. `docs/issues.md` (bugs/corrections first)  
9. `docs/todo.md` (planned work)  
10. `docs/milestones.md` (ensure no duplicate work)

Then proceed into code changes.

---

## 5. “If in Doubt” Consultation Order (Decision Procedure)

When an agent or developer is uncertain about correctness, scope, or intent:

1. Consult `paper/OMPC_v1.33.7lulz.pdf`  
2. Consult `docs/manual/part_0.md` (concept primer)  
3. Consult `docs/manual/part_2.md` (constraints)  
4. Consult `docs/manual/part_4.md` (API contract)  
5. Consult `docs/manual/part_5.md` (workflow)  
6. Consult `docs/manual/part_8.md` (extension boundaries)  
7. Consult `docs/defaults.md` (repo policy)  
8. Consult existing tests under `tests/`  
9. Only then consider proposing a change

If uncertainty remains after step 7, the correct action is:
- create an entry in `docs/issues.md` labeled `SPEC-AMBIGUITY`,
- include the exact question, impacted files, and what was consulted,
- and stop that change until resolved.

---

## 6. Update Rules for Tracking Files

### 6.1 `docs/issues.md` (bugs, regressions, corrections)
Update **immediately** when:
- a test fails,
- a workflow deviates from Part 5,
- a constraint is violated,
- performance regresses beyond thresholds,
- a scope boundary is accidentally crossed.

This file is consulted **before** starting new features.  
Issues must be triaged before expanding scope.

### 6.2 `docs/todo.md` (planned work)
Update when:
- a task is identified but not started,
- a future enhancement is proposed,
- work is deferred intentionally.

Todo items must reference:
- the manual part(s) they relate to,
- the target module(s),
- and the success criterion (what “done” means).

### 6.3 `docs/milestones.md` (accepted achievements)
Update only when:
- work is complete,
- tests and verification pass,
- alignment checks in Part 9 are satisfied,
- and scope integrity is maintained.

Milestones must include:
- deliverable summary,
- goal mapping (G1–G7 from Part 9),
- verification evidence location (tests/benchmarks),
- version tag or commit reference (when used).

---

## 7. When Each File Must Be Read (Mandatory Triggers)

### 7.1 Before any change to public API
Read:
- `docs/manual/part_4.md`
- `docs/manual/part_7.md`
- `docs/manual/part_9.md`
Then log intended changes into `docs/issues.md` as `API-CHANGE-PROPOSAL`.

### 7.2 Before any performance optimization
Read:
- `docs/manual/part_2.md`
- `docs/manual/part_6.md`
- `docs/manual/part_9.md`
Then ensure performance regression thresholds remain satisfied.

### 7.3 Before any parallelism / scaling work
Read:
- `docs/manual/part_6.md`
- `docs/manual/part_8.md`
Then ensure it remains optional and does not couple into core.

### 7.4 Before any change to resolver workflow
Read:
- `paper/OMPC_v1.33.7lulz.pdf`
- `docs/manual/part_5.md`
- `docs/manual/part_7.md`
Any workflow change must be logged as `WORKFLOW-CHANGE` in `docs/issues.md`.

---

## 8. Required End-of-Work Session Procedure

At the end of any work session:

1. Run tests.
2. If failures exist: update `docs/issues.md` first.
3. If tasks remain: update `docs/todo.md`.
4. If a deliverable is complete and verified: update `docs/milestones.md`.
5. Confirm no forbidden artifacts exist (per `docs/defaults.md`).
6. Commit with a message referencing issues/todo entries when applicable.

---

## 9. File Locations (Single Source of Truth)

- Canonical paper:  
  `paper/OMPC_v1.33.7lulz.pdf`

- Manual:  
  `docs/manual/part_0.md` … `docs/manual/part_9.md`

- Repo defaults and hygiene rules:  
  `docs/defaults.md`

- Tracking files:  
  `docs/milestones.md`  
  `docs/todo.md`  
  `docs/issues.md`

- Code:  
  `src/lulzprime/`

- Tests:  
  `tests/`

---

## 10. Success Condition

This autostart process is successful if:
- agents and humans consult the right references in the right order,
- scope drift is prevented,
- corrections are captured immediately,
- milestones reflect verified deliverables,
- and development remains aligned with the canonical OMPC reference.

End of document.
