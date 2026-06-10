# Contributing to AIS²

## Overview

AIS² is a sealed reference core for OSDI research. This document outlines contribution guidelines, boundaries, and expectations.

## Key Principle

**AIS² System Specification is Frozen**

The core system (phase_c/, validator/, FREEZE.md, INVARIANTS.md) is architecturally complete and locked. Contributions must not alter:
- System semantics
- Execution model
- Trace format
- Invariant definitions (I1–I5, F1–F4, A1–A5)
- Renderer contract

## What CAN Be Modified

- **Implementation fidelity** — bug fixes, refactoring (type annotations, naming, style)
- **Documentation clarity** — typos, reorganization, better examples (no semantic changes)
- **Test coverage** — additional test cases, test infrastructure
- **Performance optimization** — internal speedups, memory efficiency (preserving behavior)
- **Visualization/UI** — improvements to dashboard, new visualization modes

## What CANNOT Be Modified

- **phase_c/state_machine.py** — state machine logic (frozen by FREEZE.md)
- **validator/validator.py** — validator rules (frozen by INVARIANTS.md)
- **Trace format** — event schema, ordering, immutability semantics
- **System boundaries** — AIS²/MCL separation, UI/system coupling rules
- **License** — MIT license terms remain unchanged

## Contribution Workflow

### 1. Fork and Clone

```bash
git clone https://github.com/Dedoc-9/AIS2.git
cd AIS2
```

### 2. Create a Feature Branch

```bash
git checkout -b feature/your-feature-name
```

### 3. Install Development Environment

```bash
pip install -r requirements.txt
pip install -e ".[dev]"
```

### 4. Make Changes

Follow the coding guidelines:
- Write deterministic code (same input → same output)
- Run tests frequently: `pytest tests/ -v`
- Run linters: `black . && ruff check .`
- Run type checks: `mypy phase_c validator trace_exporter`

### 5. Verify Determinism

```bash
# Run twice and verify output is identical
python examples/minimal_system.py
md5sum traces/minimal_trace.json > /tmp/hash1
python examples/minimal_system.py
md5sum traces/minimal_trace.json > /tmp/hash2
diff /tmp/hash1 /tmp/hash2  # Must match exactly
```

### 6. Commit and Push

```bash
git add .
git commit -m "Description of changes"
git push origin feature/your-feature-name
```

### 7. Submit Pull Request

When submitting a PR:
- Reference any related issues
- Describe why the change is needed
- Verify all CI checks pass
- Request review from @Dedoc-9

## Code Style

- **Python**: Follow PEP 8, formatted with `black`
- **Linting**: Use `ruff` for style enforcement
- **Type hints**: Encouraged; use `mypy` for checking
- **Documentation**: Docstrings for all public functions and classes

## Testing

**All contributions must include tests.**

- Unit tests: `tests/unit/`
- Integration tests: `tests/integration/`
- Invariant tests: `tests/invariants/` (verify I1–I5)

Run tests:
```bash
pytest tests/ -v --cov=phase_c --cov=validator
```

## Determinism Requirements

**Any modification must preserve determinism:**

1. Same inputs → same trace (byte-identical)
2. No randomness without fixed seed
3. No external state dependency
4. No timing-dependent behavior

Verify:
```bash
python examples/minimal_system.py
python examples/failure_demo.py
python examples/omega_transition_demo.py
```

All three should produce identical traces on repeated runs.

## Documentation

If your changes affect user-facing behavior:
- Update README.md
- Update AIS2_USER_GUIDE.md
- Update relevant spec files (if applicable)

## Questions & Discussion

- **Architecture questions** → Open an issue with `[architecture]` label
- **Bug reports** → Open an issue with `[bug]` label
- **Feature requests** → Open an issue with `[feature]` label
- **Design discussions** → Open an issue with `[discussion]` label

## Licensing

By contributing to AIS², you agree that your contributions will be licensed under the MIT License.

## Code of Conduct

- Be respectful and constructive
- Focus on technical substance, not personalities
- Assume good intent
- Address disagreements through discussion and data

---

**Thank you for contributing to AIS²!**
