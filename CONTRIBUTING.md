# Contributing to lulzprime

Thank you for considering contributing to lulzprime!

## Development Setup

### Prerequisites

- Python >=3.10
- pip
- git

### Local Development

1. **Clone the repository:**
   ```bash
   git clone https://github.com/RobLe3/lulzprime.git
   cd lulzprime
   ```

2. **Create a virtual environment:**
   ```bash
   python -m venv .venv
   source .venv/bin/activate  # On Windows: .venv\Scripts\activate
   ```

3. **Install dev dependencies:**
   ```bash
   pip install -e ".[dev]"
   ```

4. **Run tests:**
   ```bash
   pytest
   ```

## Running Tests

```bash
# Quick test run
pytest -q

# With coverage
pytest --cov=src/lulzprime --cov-report=html

# Specific test file
pytest tests/test_resolve.py

# Run with PYTHONPATH set
PYTHONPATH=src:$PYTHONPATH pytest
```

## Code Style

This project uses:
- **black** for code formatting (line length: 100)
- **ruff** for linting
- **mypy** for type checking (optional, not strict)

```bash
# Format code
black src/ tests/

# Lint
ruff check src/ tests/

# Type check
mypy src/
```

## Testing Guidelines

- All new features must include tests
- Maintain 100% test pass rate (currently 169/169)
- Do not add long-running tests to the main test suite
- Benchmarks should be in `benchmarks/` or `experiments/`, not `tests/`
- Use policy-compliant test indices (see `docs/benchmark_policy.md`)

## Contribution Guidelines

### Before Submitting

1. Ensure all tests pass: `pytest`
2. Format code: `black src/ tests/`
3. Check linting: `ruff check src/ tests/`
4. Update documentation if needed

### Pull Request Process

1. Fork the repository
2. Create a feature branch: `git checkout -b feature/my-feature`
3. Make your changes
4. Add tests for new functionality
5. Ensure all tests pass
6. Commit with clear messages
7. Push to your fork
8. Open a pull request

### Commit Message Format

```
Brief summary (50 chars or less)

Detailed explanation if needed:
- What changed
- Why it changed
- Impact on existing functionality

Refs: #issue-number (if applicable)
```

## What to Contribute

### Welcome Contributions

- Bug fixes
- Documentation improvements
- Test coverage improvements
- Performance optimizations (with benchmarks)
- Examples and tutorials

### Requires Discussion First

- New public API functions
- Breaking changes to existing behavior
- Large-scale refactoring
- New algorithm implementations

Please open an issue first to discuss these types of changes.

## Performance Changes

If proposing performance improvements:

1. Include before/after benchmarks
2. Verify correctness (all tests pass)
3. Verify determinism (results unchanged)
4. Document complexity changes
5. Explain trade-offs (memory vs time, etc.)

## Documentation

- Public API must be documented
- Use docstrings with examples
- Update `docs/` if behavior changes
- Keep README.md accurate

## Questions?

- Open an issue for questions
- Check existing docs in `docs/`
- Review ADRs in `docs/adr/` for design decisions

## Code of Conduct

Be respectful and professional in all interactions.

## License

By contributing, you agree that your contributions will be licensed under the MIT License.
