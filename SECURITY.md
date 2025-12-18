# Security Policy

## Supported Versions

| Version | Supported          |
| ------- | ------------------ |
| 0.1.x   | :white_check_mark: |

## Reporting a Vulnerability

If you discover a security vulnerability in lulzprime, please report it by:

1. **Do NOT** open a public GitHub issue for security vulnerabilities
2. Email: github@roblemumin.com with subject line "SECURITY: lulzprime vulnerability"
3. Include:
   - Description of the vulnerability
   - Steps to reproduce
   - Potential impact
   - Suggested fix (if available)

## Response Timeline

- **Initial Response:** Within 48 hours
- **Status Update:** Within 7 days
- **Fix Timeline:** Depends on severity (critical issues prioritized)

## Security Considerations

This library is designed for:
- Deterministic prime number resolution
- Educational and research purposes
- Non-cryptographic applications

**Not suitable for:**
- Cryptographic key generation
- Security-sensitive applications requiring cryptographic randomness
- Production systems requiring security guarantees

## Scope

Security reports should focus on:
- Input validation bypasses leading to crashes or incorrect results
- Denial of service vulnerabilities
- Memory safety issues (if C/Rust extensions are added in the future)

Out of scope:
- Performance issues (file as regular issue)
- Feature requests (file as regular issue)
- Theoretical algorithmic complexity concerns (file as regular issue)
