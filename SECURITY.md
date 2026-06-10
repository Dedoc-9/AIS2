# Security Policy

## Reporting Security Vulnerabilities

AIS² is an open-source research system designed for OSDI publication. While we take security seriously, the primary use case is academic research and reproducible systems benchmarking, not production deployment.

### How to Report a Vulnerability

**Do NOT open a public GitHub issue for security vulnerabilities.**

Instead, please email security concerns to: **bigdilly95@gmail.com**

Please include:
- Description of the vulnerability
- Steps to reproduce (if applicable)
- Potential impact
- Suggested fix (if you have one)

We will acknowledge receipt within 48 hours and provide an initial response within 5 business days.

### Vulnerability Handling Process

1. **Receipt** — Acknowledge vulnerability report
2. **Assessment** — Evaluate severity and impact
3. **Fix Development** — Work on a patch (in private fork if needed)
4. **Testing** — Verify the fix preserves system invariants
5. **Disclosure** — Release fix and publish security advisory
6. **Credit** — Acknowledge reporter (with permission)

### Supported Versions

| Version | Supported | Notes |
|---------|-----------|-------|
| 1.0.0   | ✓ Current | Active OSDI submission artifact |
| < 1.0.0 | ✗ No      | Pre-release phases (A–C) not supported |

### Security Considerations

#### What AIS² Protects Against
- **Type-unsafe Ω-domain access** — Enforced via type system, cannot emit Observation(ω)
- **Trace mutation** — Frozen TraceEvent dataclass prevents modification
- **System ← UI coupling** — Graph-form forbidden edges prevent reverse data flow
- **Semantic leakage** — OmegaProjectionPolicy type separation

#### What AIS² Does NOT Provide
- **Cryptographic guarantees** — No cryptographic signing or verification
- **Confidentiality** — Traces are JSON plaintext; no encryption layer
- **Access control** — No built-in authentication or authorization
- **Network security** — Trace export to disk is unprotected
- **Physical security** — Assumes trusted execution environment

#### Threat Model
AIS² assumes:
- **Trusted system** — No malicious instrumentation
- **Untrusted external inputs** — Validates trace payloads (basic type checking)
- **Local execution** — No network communication by default
- **Honest observers** — Dashboard viewers cannot mutate state

### Dependencies

AIS² depends on:
- **Python 3.11+** — Language runtime
- **Streamlit** — Web UI framework
- **NumPy** — Numerical operations (optional)
- **pytest** — Testing framework (dev only)
- **black, ruff, mypy** — Code quality (dev only)

For security concerns in dependencies, check their respective security advisories:
- https://www.python.org/downloads/security/
- https://github.com/streamlit/streamlit/security
- https://github.com/numpy/numpy/security

### Code Integrity

All commits are signed and verified. Verify commit signatures:
```bash
git verify-commit <commit-hash>
```

All releases are tagged and signed:
```bash
git tag -v v1.0.0
```

### Security Scanning

This repository is scanned for vulnerabilities using:
- **GitHub Dependabot** — Automated dependency scanning
- **CodeQL** — Static analysis (via GitHub Security tab)
- **BANDIT** — Python security linter (dev setup)

Enable Dependabot alerts in repository settings to stay informed of new vulnerabilities.

### Responsible Disclosure Timeline

For reported vulnerabilities:
- **Critical** (CVSS 9–10) — Fix within 2 weeks
- **High** (CVSS 7–8.9) — Fix within 4 weeks
- **Medium** (CVSS 4–6.9) — Fix within 8 weeks
- **Low** (CVSS < 4) — Fix within 12 weeks

We request embargo periods of 30 days from fix release before public disclosure.

### Questions?

For security policy questions (not vulnerability reports), please open a GitHub issue with the `[security]` label.

---

**Last Updated**: 2026-06-09 | **Version**: 1.0.0
