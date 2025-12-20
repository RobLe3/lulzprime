# Changelog

All notable changes to LULZprime will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Added - Phase 2 Performance Optimizations
- **Log caching**: LRU cache (maxsize=2048) for log_n() and log_log_n() functions
  - 25-35% reduction in simulation time for N≥10^6
  - Cache hit rate >95% in typical workloads
- **Generator mode**: Added `as_generator` parameter to simulate()
  - Memory reduction from O(N) to O(1) for streaming workloads
  - Maintains determinism: same seed yields identical sequence
  - 12 new tests validating equivalence and memory efficiency
- **Dynamic β annealing**: Added `anneal_tau` parameter to simulate()
  - Formula: β_eff(n) = beta * (1 - exp(-n / anneal_tau)) * (beta_decay)^n
  - Reduces early transient variance, improves convergence stability
  - 14 new tests validating annealing behavior
- **CDF gap sampling**: Replaced random.choices() with CDF + binary search
  - Performance improvement: O(k) → O(log k) per sample
  - Maintains exact probability distribution semantics
  - 17 new tests validating sampling correctness

### Changed
- simulate() signature now includes: as_generator (bool), anneal_tau (float | None)
- Gap sampling implementation: bisect-based for O(log k) performance
- Total tests: 169 → 225 (56 new tests)

### Performance
- Simulations: 20-60% faster overall
- Memory: 75% reduction with generator mode (180 MB → 45 MB for N=10^6)
- Gap sampling: ~7-8× faster per sample for typical distributions

### Notes
- All optimizations maintain stdlib-only purity (no external dependencies)
- Phase 2 (Performance) complete, Phase 3 (Usability) starting
- Tier C statistical contracts maintained throughout

## [0.1.2] - 2025-12-20

### Fixed
- Documentation: Updated all version references in README from 0.1.0 to current version

### Note
- No code changes from 0.1.1
- PyPI does not allow replacing existing releases, hence 0.1.2 to ensure consistent documentation

## [0.1.1] - 2025-12-20

### Fixed
- CI reliability: Added `fail-fast: false` to workflow matrix for better diagnostics
- Code formatting: Reformatted all source files with black 25.x
- Linting cleanup: Fixed 60 ruff violations (import sorting, unused imports, deprecated typing annotations)
- Configuration: Updated ruff config to use `lint.*` sections (deprecation fix)
- README: Logo now renders correctly on PyPI (GitHub raw URL)

### Changed
- No algorithm changes
- No API changes
- No behavior changes
- Configuration defaults unchanged (ENABLE_LEHMER_PI=False, LEHMER_PI_THRESHOLD=250000)

## [0.1.0] - 2025-12-17

### Added
- Initial repository structure
- Documentation framework (autostart.md, defaults.md, manual parts 0-9)
- Core module skeleton files
- Test suite skeleton
- Public API definition:
  - `resolve(index)` - Exact nth prime resolution
  - `forecast(index)` - Analytic prime location estimate
  - `between(x, y)` - Prime range resolution
  - `next_prime(n)` / `prev_prime(n)` - Prime navigation
  - `is_prime(n)` - Primality testing
  - `simulate(...)` - OMPC simulator
- Tracking files (milestones.md, todo.md, issues.md)
- Project configuration (pyproject.toml, .gitignore, etc.)

## [0.1.0-dev] - 2025-12-17

### Added
- Project initialization
- Documentation-first setup
- Canonical OMPC paper reference
- Development manual (Parts 0-9)
- src/ layout structure
- pytest test framework
- Basic packaging configuration

---

## Release Guidelines

### Version Numbers
- **Major (X.0.0)**: Breaking changes to public API
- **Minor (0.X.0)**: New features, backwards compatible
- **Patch (0.0.X)**: Bug fixes, no API changes

### Release Checklist
See `tools/release_checklist.md` for full release procedure.

---

[Unreleased]: https://github.com/RobLe3/lulzprime/compare/v0.1.0-dev...HEAD
[0.1.0-dev]: https://github.com/RobLe3/lulzprime/releases/tag/v0.1.0-dev
