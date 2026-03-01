# Security Policy

## Supported Versions

| Version | Supported          |
|---------|--------------------|
| 1.0.x   | Yes                |
| < 1.0   | No                 |

## Reporting a Vulnerability

If you discover a security vulnerability in this project, please report
it responsibly.

### How to Report

1. **Do not open a public GitHub issue.** Security vulnerabilities must
   be reported privately to avoid exposing users to risk.

2. **Email**: Send a detailed report to the repository owner via the
   contact information on the GitHub profile.

3. **Include**:
   - Description of the vulnerability
   - Steps to reproduce
   - Potential impact
   - Suggested fix (if you have one)

### Response Timeline

- **Acknowledgment**: Within 48 hours of receiving the report
- **Assessment**: Within 7 days, we will assess severity and impact
- **Fix**: Critical vulnerabilities will be patched within 14 days
- **Disclosure**: Public disclosure after the fix is released

### Severity Levels

| Level    | Description                          | Response Time |
|----------|--------------------------------------|---------------|
| Critical | Remote code execution, data breach   | 48 hours      |
| High     | Privilege escalation, secret leak    | 7 days        |
| Medium   | Denial of service, info disclosure   | 14 days       |
| Low      | Minor issues, hardening suggestions  | 30 days       |

## Security Practices

This project follows these security standards:

- **Secret scanning**: detect-secrets is configured in pre-commit hooks
- **Dependency auditing**: Dependencies are reviewed for known vulnerabilities
- **Minimal permissions**: CI workflows use minimal required permissions
- **No credentials in code**: All secrets are managed via environment
  variables or secret managers

## Scope

This security policy covers:
- The `ai-engineering-standards` Python package
- Configuration templates distributed by this project
- CI/CD workflow templates

It does not cover:
- Projects that use these standards (they have their own policies)
- Third-party dependencies (report to their maintainers)
