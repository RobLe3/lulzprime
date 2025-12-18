# PyPI Release Checklist

This checklist covers the steps to release a new version of lulzprime to PyPI.

## Pre-Release Checklist

### 1. Version Bump

- [ ] Update version in `pyproject.toml`
- [ ] Update version in `src/lulzprime/__init__.py`
- [ ] Ensure versions match exactly

### 2. Documentation Review

- [ ] Update `README.md` if needed
- [ ] Update `CHANGELOG.md` (create if missing) with release notes
- [ ] Review `docs/` for outdated claims or performance numbers
- [ ] Verify all code examples in README work

### 3. Testing

- [ ] Run full test suite: `pytest`
- [ ] Verify all 169 tests pass
- [ ] Run tests with multiple Python versions (3.10, 3.11, 3.12)
- [ ] Check code formatting: `black --check src/ tests/`
- [ ] Run linter: `ruff check src/ tests/`
- [ ] Optional: Run type checker: `mypy src/`

### 4. Build Verification

- [ ] Clean previous builds: `rm -rf dist/ build/ *.egg-info`
- [ ] Build packages: `python -m build`
- [ ] Verify both `sdist` and `wheel` created in `dist/`
- [ ] Check build output for warnings

### 5. Package Verification

- [ ] Run `twine check dist/*`
- [ ] Verify no errors in package metadata
- [ ] Install in fresh venv and test:
  ```bash
  python -m venv .test-venv
  source .test-venv/bin/activate
  pip install dist/lulzprime-*.whl
  python -c "import lulzprime; print(lulzprime.__version__)"
  python -c "import lulzprime; print(lulzprime.resolve(100))"  # Should output 541
  deactivate
  rm -rf .test-venv
  ```

### 6. Git Hygiene

- [ ] Ensure all changes committed
- [ ] Ensure working tree clean: `git status`
- [ ] Push all commits to remote: `git push origin main`
- [ ] Verify CI passes (GitHub Actions)

## Release Process

### 7. Create Git Tag

```bash
# Tag the release
git tag -a v0.1.0 -m "Release v0.1.0: Full paper alignment achieved"

# Push tag to remote
git push origin v0.1.0
```

### 8. Upload to Test PyPI (Recommended First)

```bash
# Upload to Test PyPI first
twine upload --repository testpypi dist/*

# Test installation from Test PyPI
pip install --index-url https://test.pypi.org/simple/ --no-deps lulzprime

# Verify it works
python -c "import lulzprime; print(lulzprime.__version__)"
```

### 9. Upload to Production PyPI

```bash
# Upload to production PyPI
twine upload dist/*

# This will prompt for PyPI credentials
# Alternative: Use API token (recommended)
# Set in ~/.pypirc or use:
# twine upload dist/* -u __token__ -p pypi-YOUR_TOKEN_HERE
```

### 10. Verify Release

```bash
# Wait ~5 minutes for PyPI to update
# Install from PyPI
pip install lulzprime

# Verify version
python -c "import lulzprime; print(lulzprime.__version__)"

# Run smoke test
python -c "import lulzprime; assert lulzprime.resolve(100) == 541"
```

## Post-Release Checklist

### 11. GitHub Release

- [ ] Go to https://github.com/RobLe3/lulzprime/releases
- [ ] Create new release from tag v0.1.0
- [ ] Add release notes (from CHANGELOG.md)
- [ ] Attach `dist/` files if desired
- [ ] Publish release

### 12. Documentation Updates

- [ ] Verify PyPI page looks correct
- [ ] Update any external documentation links
- [ ] Update installation instructions if needed

### 13. Announce

- [ ] Optional: Announce on social media, forums, etc.
- [ ] Optional: Submit to relevant lists (Python Weekly, etc.)

## Rollback Procedure

If issues are discovered after release:

1. **Yank the release on PyPI** (does not delete, marks as unstable):
   ```bash
   # NOT RECOMMENDED unless critical security issue
   ```

2. **Release a patch version**:
   - Fix the issue
   - Bump to v0.1.1
   - Follow release process again

3. **Document the issue**:
   - Add to CHANGELOG.md
   - Update GitHub release notes

## Common Issues

### Build Fails

- Check `pyproject.toml` syntax
- Ensure all source files included
- Check `MANIFEST.in` if using custom includes

### Twine Upload Fails

- Verify PyPI credentials
- Check for name conflicts
- Ensure version doesn't already exist

### Import Fails After Install

- Verify `src/` layout correct
- Check `__init__.py` exports
- Ensure dependencies listed in `pyproject.toml`

## Version Numbering

Follow SemVer (Semantic Versioning):

- **Major (1.0.0)**: Breaking API changes
- **Minor (0.1.0)**: New features, backward compatible
- **Patch (0.1.1)**: Bug fixes, backward compatible

Current version scheme:
- `0.1.0` - Initial stable release (full paper alignment)
- `0.1.1` - Patch fixes
- `0.2.0` - New features (e.g., Meissel default enabled)
- `1.0.0` - API stable, production ready

## Credentials Setup

### PyPI API Token (Recommended)

1. Go to https://pypi.org/manage/account/token/
2. Create token with scope "Entire account" or specific project
3. Save token securely
4. Configure `~/.pypirc`:
   ```ini
   [pypi]
   username = __token__
   password = pypi-YOUR_TOKEN_HERE
   ```

### Test PyPI Token

1. Go to https://test.pypi.org/manage/account/token/
2. Create token
3. Configure `~/.pypirc`:
   ```ini
   [testpypi]
   repository = https://test.pypi.org/legacy/
   username = __token__
   password = pypi-YOUR_TEST_TOKEN_HERE
   ```

## Quick Reference Commands

```bash
# Full release workflow
rm -rf dist/ build/ *.egg-info
python -m build
twine check dist/*
twine upload --repository testpypi dist/*  # Test first
twine upload dist/*  # Production
git tag -a v0.1.0 -m "Release v0.1.0"
git push origin v0.1.0
```

## Support

For issues with the release process:
- PyPI help: https://pypi.org/help/
- Twine docs: https://twine.readthedocs.io/
- Python packaging: https://packaging.python.org/
