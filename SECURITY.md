# SECURITY.md

## Security Policy

### Supported Versions

| Version | Supported |
|---------|-----------|
| 1.0.x   | ✅ Yes    |
| < 1.0   | ❌ No     |

### Reporting a Vulnerability

We take the security of Hermes Kill seriously. If you believe you've found a security vulnerability, please report it to us as described below.

**Please do NOT report security vulnerabilities through public GitHub issues.**

Instead, please report them via email to:
- lirugang123@qq.com

### What to Include

Your report should include:

1. Description of the vulnerability
2. Steps to reproduce
3. Potential impact
4. Suggested fix (if any)

### Response Time

We aim to respond to security reports within 48 hours.

### Disclosure Policy

We follow a coordinated disclosure process:

1. Report is received and acknowledged
2. Vulnerability is validated
3. Fix is developed and tested
4. Release is prepared
5. Public disclosure after fix is available

## Security Measures

This project implements:

- Input validation and sanitization
- Rate limiting
- Timeout controls
- Secure HTTP handling
- Dependency scanning

## Dependencies

We regularly update dependencies to address security vulnerabilities. Run:

```bash
pip audit
```

to check for known vulnerabilities.
