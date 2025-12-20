# Changelog

All notable changes to LULZprime will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

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
