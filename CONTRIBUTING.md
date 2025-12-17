# Contributing to LULZprime

Thank you for considering contributing to LULZprime!

## Before You Start

**REQUIRED READING** (in this order):

1. `docs/autostart.md` - Startup procedure and file parse order
2. `docs/defaults.md` - Repository rules and constraints
3. `docs/manual/part_0.md` - Conceptual framing
4. `docs/manual/part_2.md` - Goals, non-goals, and constraints
5. `docs/manual/part_4.md` - Public API contracts
6. `docs/manual/part_8.md` - Extension rules

**These documents are binding.** Contributions that violate them will be rejected.

## Canonical Reference

The canonical concept source is `paper/OMPC_v1.33.7lulz.pdf`.

**If in doubt, check the paper first.**

## Precedence Order

When there is conflict or uncertainty, resolve by consulting in this order:
1. `paper/OMPC_v1.33.7lulz.pdf`
2. `docs/manual/part_0.md` through `part_9.md`
3. `docs/defaults.md`
4. Source code
5. Code comments

## Contribution Workflow

### 1. Check Existing Work

Before starting:
- Check `docs/issues.md` for known bugs
- Check `docs/todo.md` for planned work
- Check `docs/milestones.md` to avoid duplicate work

### 2. Discuss Major Changes

For significant changes:
- Open an issue first
- Reference relevant manual parts
- Explain goal mapping (G1–G7 from Part 9)
- Wait for approval before implementation

### 3. Development Process

```bash
# Fork and clone
git clone git@github.com:YourUsername/lulzprime.git
cd lulzprime

# Install in development mode
pip install -e ".[dev]"

# Create feature branch
git checkout -b feat/your-feature

# Make changes
# - Follow manual parts 0-9
# - Add tests for new functionality
# - Update relevant tracking files

# Run tests
pytest

# Run code quality checks
black src/ tests/
ruff check src/ tests/
mypy src/

# Commit with descriptive message
git commit -m "feat: Add feature X per Part Y"

# Push and create PR
git push origin feat/your-feature
```

### 4. Pull Request Requirements

Your PR must include:
- Description of changes
- Reference to manual parts followed
- Goal mapping (which of G1-G7 does this address?)
- Test coverage for new code
- Update to relevant tracking file:
  - `docs/issues.md` if fixing a bug
  - `docs/todo.md` if completing planned work
  - `docs/milestones.md` if completing a deliverable
- Confirmation that no forbidden scope was entered

## Code Standards

### Python Style
- Follow PEP 8
- Use `black` for formatting (line length 100)
- Use `ruff` for linting
- Type hints encouraged but not required

### Documentation
- Docstrings for all public functions
- Reference manual parts in module docstrings
- Include examples in docstrings where helpful

### Testing
- All public API functions must have tests
- Tests must verify contracts from Part 4
- Use pytest fixtures for common setups
- Aim for >80% coverage of core modules

## What Can Be Changed

### Allowed (from Part 8, section 8.3):
- New π(x) implementations (behind PrimeCounter interface)
- New primality test backends
- Execution backends (multiprocessing, GPU)
- Table storage backends
- Diagnostics and visualization tools

### Forbidden (from Part 8, section 8.4):
- Modifying public API semantics
- Replacing forecast → correction pipelines with heuristics
- Adding global sieving to core resolution
- Adding AI/ML "prime prediction"
- Adding network calls or remote dependencies
- Making cryptographic claims

## Scope Integrity

From `docs/manual/part_2.md`, section 2.4:

LULZprime must **NOT** claim or implement:
- Cryptographic breaks or shortcuts
- Integer factorization acceleration
- Cryptographic entropy replacement
- Heuristic "prime guessing"
- Probabilistic claims without verification

**These exclusions are permanent and enforceable.**

## Testing Requirements

Before submitting:
- All tests pass: `pytest`
- Code formatted: `black src/ tests/`
- No lint errors: `ruff check src/ tests/`
- Type checking passes: `mypy src/`

## Commit Message Format

Use conventional commits:
- `feat:` New feature
- `fix:` Bug fix
- `docs:` Documentation changes
- `test:` Test additions/changes
- `refactor:` Code refactoring
- `perf:` Performance improvements
- `chore:` Build/tooling changes

Example:
```
feat: Implement Lehmer π(x) algorithm per Part 6

- Adds sublinear prime counting per Part 6 performance model
- Satisfies memory constraint < 25MB
- Tests verify correctness against simple counting
- Maps to goals G2 (hardware efficiency) and G6 (maintainability)
```

## Review Process

Your PR will be reviewed for:
1. Alignment with manual parts
2. API contract compliance
3. Test coverage
4. Code quality
5. Documentation completeness
6. Scope integrity

## Questions?

- Open an issue with label `question`
- Reference specific manual parts in your question
- Be specific about what you've already consulted

## License

By contributing, you agree that your contributions will be licensed under the MIT License.

---

**Remember**: The project succeeds when it remains aligned with the canonical OMPC paper and maintains scope integrity.
