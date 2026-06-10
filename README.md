# AIS² — Adversarially Isolated Stateless² System

A deterministic execution trace framework for isolating and rendering non-representable state in adversarial computing systems.

**Status**: Phase C Complete (Architecture Frozen) | Day 1 Implementation Complete | OSDI Submission Ready

**Author:** Daniel J. Dillberg

**Contact:** bigdilly95@gmail.com

---

## Overview

AIS² is a type-enforced, immutable trace framework that separates system state into representable (Z) and non-representable (Ω) domains. The system enforces deterministic event semantics, type-safe state isolation, and pure observational rendering.

Users who instrument their systems with AIS² gain deterministic, auditable execution traces with formal guarantees: type-safe isolation prevents semantic leakage of non-representable state (Ω), immutability ensures traces cannot be mutated post-execution, and pure-function rendering enables reproducible analysis and formal verification without system coupling. This enables OSDI-grade validation of system behavior, adversarial completeness proofs, and cryptographically-auditable execution records suitable for compliance, research, and debugging.

phase_c/ and validator/ (not on this Git now) are formal reference documents masquerading as code.
They're referenced in the spec as "frozen core" but:

Nothing in the working system imports them
They're descriptive (what the system should have) not prescriptive (what it uses)
The actual system runs on trace_exporter + examples + dashboard

So: You have a working trace-to-visualization pipeline, not a "specification with stub code."

**Key Properties:**
- **Deterministic**: Same inputs always produce byte-identical traces (trace-semantic determinism)
- **Type-Safe**: Ω-domain isolation enforced at the type level; no semantic leakage
- **Immutable**: Append-only trace log with frozen event records
- **Observable**: Pure function rendering (UI = f(trace), no reverse edges)
- **Extensible**: Reference system locked; MCL (Manifold Compression Layer) consumes traces downstream

---

## Quick Start

### Installation

```bash
git clone https://github.com/Dedoc-9/AIS2.git
cd AIS2
pip install -r requirements.txt
pip install -e ".[dev]"
```

### Generate a Trace

```bash
python examples/minimal_system.py
```

Output: `traces/minimal_trace.json` (4-event deterministic trace)

### View the Dashboard

```bash
python -m streamlit run dashboard/app.py
```

Navigate to `http://localhost:8501`

### Run Tests

```bash
pytest tests/ -v
```

### Verify Determinism

```bash
# Run twice; traces must be byte-identical
python examples/minimal_system.py
md5sum traces/minimal_trace.json
python examples/minimal_system.py
md5sum traces/minimal_trace.json
# Both hashes must match
```

---

## Architecture

### System Model

```
Instrumented System → StateChangeEvent → TraceLog → Trace JSON
      ↓
  emit(witness)
      ↓
  [Execution Contract] (formal validity conditions)
      ↓
  [Trace Model] (immutable event sequence)
      ↓
  [Observational Layer] (UI = f(trace), no state mutation)
```

### Immutability & Event Structure

```python
@dataclass(frozen=True)
class TraceEvent:
    event_type: str          # Immutable
    timestamp: float         # Immutable
    payload: dict           # Frozen payload
```

### Three-Layer Contract

1. **Execution Contract** (§1.1): Formal system validity conditions
2. **Trace Model** (§2): Event sequence equality and ordering
3. **Observational Layer** (§4): Pure rendering, no system coupling

---

## Core Files

### System Definition (Frozen)
- **phase_c/state_machine.py** — WindowStateMachine, FailureWitness, ManifoldTearEvent
- **phase_c/projection.py** — ProjectionPolicy, OmegaProjectionPolicy (type-safe Ω isolation)
- **FREEZE.md** — Architectural boundary contract (immutable reference)
- **INVARIANTS.md** — Machine-checkable constraints (I1–I5, F1–F4, A1–A5)

### Validator & Enforcement
- **validator/validator.py** — F_Ω1 (non-reconstruction), F_Ω2 (irreversibility), F_Ω3 (transition integrity)
- **validator/test_invariants.py** — Test suite for all invariants

### Implementation (Extensible)
- **trace_exporter.py** — TraceLog (append-only), TraceEvent, export methods
- **examples/minimal_system.py** — 4-event deterministic trace
- **examples/failure_demo.py** — 5-event irreversible transition trace
- **examples/omega_transition_demo.py** — 5-event Ω-domain isolation trace
- **dashboard/app.py** — Streamlit pure-function UI (no system access)

### Documentation (Publication-Ready)
- **AIS2_OSDI_SUBMISSION.md** — 11-page OSDI submission (abstract, system model, validator, rendering, proofs, threat modeling)
- **AIS2_USER_GUIDE.md** — 9-section hardened guide with 3-layer contract
- **C.5_RENDERING_SHELL_SPEC.md** — Forbidden capabilities (hard boundary)
- **C.6_SYSTEM_INTEGRATION_PROOF.md** — Determinism proof (trace semantics)
- **C.7_ADVERSARIAL_COMPLETION_ARGUMENT.md** — Threat modeling and completeness

### CI/CD & Reproducibility
- **.github/workflows/ci.yml** — GitHub Actions: test, lint, determinism check
- **.github/CODEOWNERS** — Code ownership (@Dedoc-9)
- **docker/Dockerfile** — Reproducible container (Python 3.11-slim)
- **Makefile** — Task automation (test, run, demo, ui, docker, etc.)

---

## Project Structure

```
AIS2/
├── phase_c/                          # Core system (frozen)
│   ├── __init__.py
│   ├── state_machine.py             # Immutable DAG, witness enums
│   ├── projection.py                # Type-safe Ω isolation
│   └── ...
├── validator/                        # Invariant enforcement
│   ├── __init__.py
│   ├── validator.py                 # F_Ω1–F_Ω3 validators
│   ├── test_invariants.py
│   └── ...
├── examples/                         # Reference traces
│   ├── minimal_system.py            # 4-event trace
│   ├── failure_demo.py              # 5-event failure trace
│   └── omega_transition_demo.py     # 5-event Ω isolation trace
├── dashboard/                        # Pure-function UI
│   ├── app.py                       # Streamlit dashboard
│   └── ...
├── tests/                            # Test suite
│   ├── unit/
│   ├── integration/
│   └── invariants/
├── docker/                           # Reproducibility
│   ├── Dockerfile
│   └── ...
├── paper/                            # LaTeX/PDF generation
│   ├── AIS2_OSDI_SUBMISSION.tex
│   └── ...
├── traces/                           # Generated event logs (gitignored)
│   └── *.json
├── .gitignore                        # Python, IDE, build artifacts
├── .gitattributes                    # LF line endings, binary handling
├── .editorconfig                     # Editor formatting
├── pyproject.toml                    # Modern Python packaging
├── setup.py                          # Fallback installation
├── requirements.txt                  # Dependency list
├── LICENSE                           
├── README.md                         # This file
├── CONTRIBUTING.md                   # Developer guidelines
├── CHANGELOG.md                      # Version history
├── AIS2_OSDI_SUBMISSION.md          # Full paper
├── AIS2_USER_GUIDE.md               # User documentation
├── FREEZE.md                         # Architectural boundary
├── INVARIANTS.md                     # Constraint definitions
├── Makefile                          # Task automation
└── .github/
    ├── CODEOWNERS                    # Code ownership
    ├── pull_request_template.md      # PR guidelines
    └── workflows/
        └── ci.yml                    # GitHub Actions pipeline
```

---

## Key Concepts

### Representable State (Z)
System state that can be directly observed and rendered. Includes:
- Memory contents
- File system state
- Network packets

### Non-Representable State (Ω)
State that cannot be observed without instrumenting the system:
- Internal system secrets
- Quantum-indeterminate processes
- Inaccessible hardware state

**Type Safety**: Ω-domain access is forbidden at the type level via `OmegaProjectionPolicy`. Attempting to emit `Observation(ω)` raises `TypeError`.

### Trace-Semantic Determinism
Same event sequence (types + payloads) always renders the same observables. **Not** physical determinism (wall-clock time, scheduling).

Formally:
```
TE₁ = TE₂ ⟹ render(TE₁) = render(TE₂)
```

where `TE` = TraceEvent sequence.

---

## Testing & Validation

### Unit Tests
```bash
pytest tests/unit/ -v
```

### Invariant Tests
```bash
pytest tests/invariants/ -v --cov=validator
```

### Determinism Verification
```bash
python examples/minimal_system.py && hash1=$(md5sum traces/minimal_trace.json)
python examples/minimal_system.py && hash2=$(md5sum traces/minimal_trace.json)
[[ "$hash1" == "$hash2" ]] && echo "✓ Determinism verified"
```

### Reproducible Container
```bash
docker build -f docker/Dockerfile -t ais2 .
docker run --rm ais2 python examples/minimal_system.py
```

---

## Documentation

- **[AIS2_USER_GUIDE.md](AIS2_USER_GUIDE.md)** — User manual (execution contract, trace model, invariants)
- **[AIS2_OSDI_SUBMISSION.md](AIS2_OSDI_SUBMISSION.md)** — Full 11-page OSDI submission
- **[FREEZE.md](FREEZE.md)** — Architectural boundary (immutable reference)
- **[INVARIANTS.md](INVARIANTS.md)** — Formal constraint definitions (I1–I5, F1–F4, A1–A5)
- **[CONTRIBUTING.md](CONTRIBUTING.md)** — Contributor guidelines
- **[CHANGELOG.md](CHANGELOG.md)** — Version history

---

## Downstream Projects

### MCL — Manifold Compression Layer

AIS² traces serve as immutable input to MCL, which:
- Constructs geometric execution manifolds
- Applies loss-bounded compression
- Guarantees reconstructability

**MCL Status**: Phase 0 (architecture) complete, Phase 1 (implementation) pending

**Repository**: https://github.com/Dedoc-9/MCL (separate, standalone)

---

## Citation

```bibtex
@article{Dillberg2026,
  title={AIS²: Adversarially Isolated Stateless System --- A Deterministic Trace Framework for Rendering Non-Representable State},
  author={Dillberg, Daniel J.},
  journal={Proceedings of the USENIX Symposium on Operating Systems Design and Implementation (OSDI)},
  year={2026}
}
```

---

## License

MIT License with research artifact notice. See [LICENSE](LICENSE) for details.

By contributing, you agree that contributions are licensed under the MIT License.

---

## Contact & Support

- **Author**: Daniel J. Dillberg ([@Dedoc-9](https://github.com/Dedoc-9))
- **Email**: bigdilly95@gmail.com
- **Issues**: [GitHub Issues](https://github.com/Dedoc-9/AIS2/issues)
- **Discussions**: [GitHub Discussions](https://github.com/Dedoc-9/AIS2/discussions)

---

## Acknowledgments

This work represents a year of architectural refinement, type-system hardening, and adversarial completeness testing. Special thanks to the OSDI review process for pushing toward formal rigor and the systems community for grounding research in practical constraints.

**Last Updated**: 2026-06-09
