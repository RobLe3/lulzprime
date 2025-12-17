# Security Policy

## Scope

LULZprime is a mathematical library for prime number resolution and navigation. It is **not** a cryptographic library and makes no cryptographic claims.

## Non-Cryptographic Scope

From `docs/manual/part_1.md` section 1.6 and `docs/manual/part_2.md` section 2.4:

LULZprime explicitly does **NOT** claim or implement:
- Cryptographic breaks (RSA, ECC, discrete log)
- Factorization acceleration
- Cryptographic entropy generation
- Key generation or management
- Any cryptographic primitives

**This library should not be used for cryptographic purposes.**

## Supported Versions

| Version | Supported          |
| ------- | ------------------ |
| 0.1.x   | :white_check_mark: |

## Reporting a Vulnerability

If you discover a security vulnerability in LULZprime:

### What to Report

**Report if:**
- Input validation bypass leading to undefined behavior
- Memory safety issues (overflow, buffer issues)
- Denial of service vulnerabilities
- Code injection possibilities
- Dependency vulnerabilities

**Do NOT report:**
- "Cryptographic vulnerabilities" (this is not a crypto library)
- Claims that primes can be "predicted" (not the library's purpose)
- Performance as a "security issue" (performance is tracked separately)

### How to Report

1. **Do NOT open a public issue**
2. Email: github@roblemumin.com
3. Include:
   - Description of the vulnerability
   - Steps to reproduce
   - Impact assessment
   - Suggested fix (if any)

### Response Timeline

- **Initial response**: Within 7 days
- **Fix timeline**: Depends on severity
  - Critical: Within 30 days
  - High: Within 60 days
  - Medium: Within 90 days
  - Low: Best effort

### Disclosure Policy

- We follow coordinated disclosure
- Security fixes will be released as patch versions
- Credits given to reporters (unless they prefer anonymity)
- CVEs assigned for significant vulnerabilities

## Security Best Practices for Users

### Input Validation

LULZprime validates inputs per `docs/manual/part_4.md` section 4.5:
- Index values must be >= 1
- Range bounds must satisfy x <= y and y >= 2
- All inputs must be integers

**Do not bypass these validations** in your code.

### Determinism

LULZprime is deterministic (Part 4, section 4.3):
- Same inputs always yield same outputs
- Simulation requires explicit seeds for reproducibility

**Do not use simulation output as cryptographic randomness.**

### Resource Limits

From `docs/manual/part_2.md` section 2.5:
- Memory target: < 25 MB for core functionality
- No network access (ever)

If you encounter unbounded memory growth or network access attempts, report as a bug.

### Dependencies

LULZprime has **zero runtime dependencies** (core library).

Development dependencies are listed in `pyproject.toml` and should be kept minimal.

## Known Limitations

From `docs/manual/part_6.md`:

1. **Performance**: Resolution performance is optimized for efficiency, not constant-time operation
2. **Integer size**: Primality testing guarantees are stated per implementation (currently deterministic for 64-bit)
3. **Simulation**: Pseudo-prime simulation is NOT a source of true primes

These are **design choices**, not vulnerabilities.

## Security Audit History

| Date | Auditor | Scope | Status |
|------|---------|-------|--------|
| TBD  | TBD     | TBD   | TBD    |

## Contact

- Security issues: github@roblemumin.com
- General issues: https://github.com/RobLe3/lulzprime/issues

---

**Remember**: LULZprime is a mathematical tool, not a security tool. Use appropriate cryptographic libraries for cryptographic purposes.
