# ⚙️ AIS² Invariants (Machine-Checkable Constraints)

**See parent directory for full specification:** `../AIS2_PUBLIC/INVARIANTS.md`

## Core Invariants (Implicit in Day 1 Code)

### I1: Renderer Purity
- No mutable state
- No side effects
- Pure function: PrimitiveSet → PixelBuffer

### I2: State Machine Irreversibility
- DAG structure: RepresentableState → NonRepresentableState (one-way)
- No reverse transitions
- Terminal absorbing state

### I3: Ω-Domain Isolation
- Type-separated: FailureWitness ≠ Observation
- Renderer never sees witness
- OmegaProjectionPolicy enforces boundary

### I4: Primitive Closure
- Fixed set: P0 (4) + P1 (3) + P2 (3) = 10 classes
- No runtime creation
- Immutable

### I5: Trace Append-Only
- Only operation: append
- No deletion, no update, no mutation
- Immutable after export

## Forbidden Edges (Implicit in Architecture)

**F1:** Dashboard → core logic (❌ forbidden)
**F2:** Observational layer → internal state (❌ forbidden)
**F3:** Renderer → witness/observation (❌ forbidden)
**F4:** Trace → semantic interpretation (❌ forbidden)

## Allowed Edges (Implicit in Architecture)

**A1:** Core internal coupling (✔ frozen core only)
**A2:** Examples → core (✔ read-only instantiation)
**A3:** Trace exporter → system output (✔ serialization only)
**A4:** Dashboard → trace JSON (✔ pure function)
**A5:** Docker → all (✔ build-time only)

---

For full machine-checkable specifications, see: `../AIS2_PUBLIC/INVARIANTS.md`
