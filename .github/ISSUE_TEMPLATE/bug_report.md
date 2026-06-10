---
name: Bug Report
about: Report a bug or unexpected behavior
title: "[BUG] "
labels: bug
assignees: ''

---

## Description

**Summary**: Brief description of the bug

**Expected behavior**: What should happen?

**Actual behavior**: What actually happens?

---

## Steps to Reproduce

1. Step 1
2. Step 2
3. Step 3

---

## Environment

- **Python version**: (e.g., 3.11.2)
- **OS**: (e.g., Linux, macOS, Windows)
- **AIS² version**: (e.g., 1.0.0)
- **Installation method**: (e.g., `pip install -e .`, Docker, git clone)

### Reproduce Command

```bash
# Exact command(s) to reproduce the bug
python examples/minimal_system.py
```

### Error Output

```
# Paste full error message, traceback, or log output
Traceback (most recent call last):
  ...
```

---

## Root Cause Analysis

**Do you know what's causing this?** (if applicable)

---

## Impact

- [ ] Determinism is broken (traces are non-identical)
- [ ] Type safety is compromised (Ω-domain access leaks)
- [ ] System integrity is affected (reverse edges or mutations)
- [ ] Documentation is misleading
- [ ] Other (please specify):

---

## Proposed Solution

(Optional) If you have a fix in mind, describe it here.

---

## Additional Context

Add any other context, screenshots, or configuration details.

### Related Issues

- Closes #___ (if applicable)
- Related to #___ (if applicable)

---

## Checklist

- [ ] I have verified this is a reproducible issue (not a user error)
- [ ] I have searched existing issues and this is not a duplicate
- [ ] I have provided sufficient detail to reproduce the bug
- [ ] I have provided my environment details
- [ ] I have checked the documentation and TROUBLESHOOTING guide

---

**Thank you for reporting this bug!** The AIS² team will investigate and respond promptly.
