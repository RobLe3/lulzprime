# LULZprime Documentation

Welcome to the LULZprime documentation.

## Quick Links

- **Getting Started**: See [README.md](../README.md)
- **Developer Onboarding**: Start with [autostart.md](autostart.md)
- **Repository Rules**: Read [defaults.md](defaults.md)
- **Manual**: [Part 0](manual/part_0.md) through [Part 9](manual/part_9.md)
- **API Reference**: [Part 4](manual/part_4.md)
- **Canonical Paper**: [paper/OMPC_v1.33.7lulz.pdf](../paper/OMPC_v1.33.7lulz.pdf)

## Documentation Structure

### For Users
- **README.md** - Quick start and overview
- **manual/part_4.md** - Public API contracts

### For Developers
1. **autostart.md** - Required reading, startup procedure
2. **defaults.md** - Repository rules and constraints
3. **manual/part_0.md to part_9.md** - Complete development manual
4. **CONTRIBUTING.md** - Contribution guidelines

### Project Tracking
- **milestones.md** - Completed deliverables
- **todo.md** - Planned work
- **issues.md** - Bugs and corrections

## Manual Overview

The development manual consists of 10 parts:

- **Part 0**: Canonical context and high-level abstraction (agent primer)
- **Part 1**: Concept and origin, canonical reference
- **Part 2**: Goals, non-goals, and constraints
- **Part 3**: High-level architecture blueprint
- **Part 4**: Public API and interface contracts
- **Part 5**: Internal execution chains and workflows
- **Part 6**: Performance, hardware, and scaling model
- **Part 7**: Diagnostics, verification, and self-checks
- **Part 8**: Extension rules and third-party contributions
- **Part 9**: Verification, project goals, and deliverable alignment measurement

## Precedence Order

When there is any conflict or uncertainty, consult sources in this order:

1. `paper/OMPC_v1.33.7lulz.pdf`
2. `manual/part_0.md` through `part_9.md`
3. `defaults.md`
4. Source code
5. Code comments

**Rule: If in doubt, check the paper first.**

## Key Principles

1. **Hardware efficiency first** - Must run on low-end devices
2. **Deterministic and reproducible** - Same inputs yield same outputs
3. **Scope integrity** - No cryptographic claims or factorization shortcuts
4. **Maintainability** - Modular, testable, replaceable components
5. **OMPC alignment** - Behavior consistent with canonical paper

## Contributing

See [CONTRIBUTING.md](../CONTRIBUTING.md) for detailed guidelines.

**Required reading before contributing:**
- autostart.md
- defaults.md
- manual/part_0.md, part_2.md, part_4.md, part_8.md

## Support

- Issues: https://github.com/RobLe3/lulzprime/issues
- Repository: https://github.com/RobLe3/lulzprime
- Email: github@roblemumin.com
