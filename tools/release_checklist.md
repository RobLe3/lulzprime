# Release Checklist

Pre-release verification checklist for LULZprime releases.

## Pre-Release Verification

### 1. Documentation Review
- [ ] All manual parts (0-9) are current
- [ ] `docs/milestones.md` updated with new deliverables
- [ ] `docs/todo.md` cleared of completed items
- [ ] `docs/issues.md` has no critical open issues
- [ ] `CHANGELOG.md` updated with all changes
- [ ] `README.md` version references updated

### 2. Code Quality
- [ ] All tests pass: `pytest`
- [ ] Test coverage > 80%: `pytest --cov`
- [ ] No lint errors: `ruff check src/ tests/`
- [ ] Code formatted: `black --check src/ tests/`
- [ ] Type checking passes: `mypy src/`
- [ ] No TODO/FIXME in production code

### 3. API Contract Verification (Part 4)
- [ ] All public API functions tested
- [ ] Input validation works correctly
- [ ] Guarantee tiers verified (A, B, C)
- [ ] Determinism confirmed
- [ ] No silent behavior changes

### 4. Workflow Verification (Part 5)
- [ ] `resolve()` follows forecast → π(x) → correction chain
- [ ] `between()` uses localized testing
- [ ] `simulate()` reproducible with seeds
- [ ] All workflows match manual specifications

### 5. Performance Verification (Part 6)
- [ ] Core memory usage < 25 MB verified
- [ ] Benchmarks run without regression
- [ ] Performance matches documented complexity claims
- [ ] No unbounded memory growth

### 6. Constraint Compliance (Part 2)
- [ ] No network dependencies
- [ ] Hardware efficiency maintained
- [ ] Determinism preserved
- [ ] No cryptographic claims introduced
- [ ] Scope integrity maintained

### 7. Diagnostics and Self-Checks (Part 7)
- [ ] Resolution verification passes
- [ ] Range verification passes
- [ ] Simulator diagnostics show convergence
- [ ] No silent failures

### 8. Extension Compliance (Part 8)
- [ ] No forbidden modifications made
- [ ] Extensions properly isolated
- [ ] Core modules untouched by optional features

### 9. Alignment Measurement (Part 9)
- [ ] Goal mapping complete (G1-G7)
- [ ] Verification evidence documented
- [ ] Known limitations listed
- [ ] OMPC alignment confirmed

### 10. Package Build
- [ ] `pyproject.toml` version updated
- [ ] `src/lulzprime/__init__.py` version matches
- [ ] Package builds: `python -m build`
- [ ] Package installs cleanly in fresh venv
- [ ] Import works: `python -c "import lulzprime; print(lulzprime.__version__)"`

### 11. Git and Repository
- [ ] All changes committed
- [ ] No uncommitted tracking files
- [ ] No secrets or forbidden artifacts (check `.gitignore`)
- [ ] Tag created: `git tag v<version>`
- [ ] Tag pushed: `git push origin v<version>`

### 12. GitHub Release
- [ ] GitHub release created from tag
- [ ] Release notes from `CHANGELOG.md` included
- [ ] Goal mapping included in release notes
- [ ] Known limitations documented

### 13. Post-Release
- [ ] Verify package on PyPI
- [ ] Test installation: `pip install lulzprime==<version>`
- [ ] Update `docs/milestones.md` with release milestone
- [ ] Announce release (if applicable)

## Version Bump Checklist

Files to update when bumping version:
- [ ] `pyproject.toml` - `[project] version`
- [ ] `src/lulzprime/__init__.py` - `__version__`
- [ ] `CHANGELOG.md` - Add new version section
- [ ] `README.md` - Update status badge (if applicable)

## Rollback Procedure

If critical issues found post-release:
1. Yank release on PyPI
2. Create hotfix branch
3. Fix issue
4. Follow checklist for patch release
5. Document in `docs/issues.md`

## Contact

Release manager: github@roblemumin.com
