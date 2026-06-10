# ❄️ AIS² FREEZE CONTRACT

This file is a boundary contract between frozen semantics and allowed-to-evolve layers.

**See parent directory for full specification:** `../AIS2_PUBLIC/FREEZE.md`

## Key Rules (Summary)

**Frozen (no modifications):**
- phase_c/ (state machine, projection logic)
- validator/ (invariant checkers)
- All core semantics defined in submission

**Allowed to evolve:**
- dashboard/ (UI/UX)
- examples/ (demo scripts)
- trace_exporter/ (serialization)
- docker/ (reproducibility)

**Never:**
- Semantics changes after freeze
- New primitives at runtime
- State mutations from UI
- Bidirectional coupling (UI → core)

---

For full details, see: `../AIS2_PUBLIC/FREEZE.md`
