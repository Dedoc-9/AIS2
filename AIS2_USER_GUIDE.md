# AIS² User Guide: Formal System Specification

**Version:** 1.0  
**Audience:** System integrators, researchers, OSDI reviewers  
**Status:** Operational

---

## Core System Definition

```
AIS² = (Instrumented System → Event Trace → Pure Observation Layer)
```

**Scope:** Systems that explicitly emit structured events; no implicit introspection or external observation.

---

## 1. Execution Contract: Instrumented System Definition

### 1.1 System Validity

A system S is **AIS²-compatible** iff:

```
S is valid ⇔ ∃ TraceLog such that:
  S executes AND S calls TraceLog.emit(event_type, payload)
```

**Hard constraints:**
- Events are the only observable output channel
- No implicit introspection or external observation
- No hidden execution channels outside TraceLog
- Instrumentation is mandatory, not optional

### 1.2 Allowed System Operations

**A system MAY:**
- Emit events via TraceLog
- Compute internal state deterministically
- Transform inputs based on explicit logic
- Store ephemeral local variables

**A system MUST NOT:**
- Modify events after emission
- Read from dashboard or UI
- Depend on uncontrolled external state
- Expose non-event output channels

### 1.3 Determinism (Instrumentation-Relative)

**Definition:**

```
Same input + same instrumentation ⇒ identical emitted event sequence
```

**What this means:**
- Event types, payload fields, and ordering are deterministic
- Execution is reproducible given identical code and inputs

**What this does NOT mean:**
- Physical timing determinism
- Hardware-level reproducibility
- Wall-clock timestamp determinism

**Determinism is relative to instrumentation.** If your system uses external randomness (not instrumentation), traces will differ. This is expected and correct.

---

---

## 2. Trace Model: What Is Recorded

### 2.1 Event Definition

Each event has this structure:

```json
{
  "event_type": "string",
  "timestamp": "integer",
  "payload": "object"
}
```

**Constraints:**
- Immutable after emission
- Append-only ordering
- Globally ordered within trace (index 0, 1, 2, ..., n)

### 2.2 Trace Definition

A trace T is:

```
T = [event₀, event₁, event₂, ..., eventₙ]

∀ i < j ⇒ index(eventᵢ) < index(eventⱼ)
No deletion, no mutation, no reordering
```

### 2.3 Trace Equality (Formal Definition)

Two traces T₁ and T₂ are equal iff:

```
T₁ ≡ T₂ ⇔
  same event type sequence
  AND same payload fields (field-wise equality)
  AND same causal ordering

Optional: timestamps excluded from equality
  (e.g., wall-clock times may differ but not affect equality)
```

### 2.4 Trace Completeness (Relative, Not Absolute)

**Definition:**

```
Trace completeness = completeness relative to emitted events
```

**What this means:**
- Events in the trace are complete records of what was emitted
- Trace is complete with respect to instrumentation coverage

**What this does NOT mean:**
- Complete record of all system behavior
- Complete record of internal state
- Complete record of execution reality

**Key insight:** Traces are only as complete as the instrumentation. If you don't emit an event, it won't appear in the trace. This is by design.

---

## 3. Observational Layer: UI Contract

### 3.1 Core Property

The dashboard is a **pure function over traces:**

```
UI_state = f(trace_json)
```

Where:
- f is deterministic
- f is side-effect free
- f has no external dependencies

### 3.2 UI Restrictions

**UI MUST NOT:**
- Modify traces (no event injection, deletion, or mutation)
- Request system execution or control
- Alter event ordering or meaning
- Inject replay commands into the system

**UI MAY ONLY:**
- Display events
- Filter or group (visual representation only)
- Render summaries (derived views, not semantic changes)

### 3.3 System/UI Separation (Graph Form)

**Allowed data flow:**

```
System → TraceLog → TraceFile → UI
```

**Forbidden edges:**

```
UI → System        ❌
UI → TraceLog      ❌
UI → Execution     ❌
```

This separation is **not optional**—it is enforced by architecture.

---

## 4. Compatible System Class

A system is AIS²-compatible iff it satisfies **all** of:

1. **Explicit event emission** — System calls TraceLog.emit()
2. **Trace-semantic determinism** — Same inputs → same emitted events
3. **No hidden channels** — No execution paths outside TraceLog
4. **No external state dependency** — No uncontrolled randomness affecting trace

If any condition fails, the system is not compatible with AIS².

---

## 5. Core Invariants (Formal)

### I1 — Append-Only
```
Events only grow, never change.
∀ trace: only operation is append(event)
No delete, no update, no mutation
```

### I2 — Event Immutability
```
Once emitted, events are frozen.
@dataclass(frozen=True) is the enforcing mechanism
```

### I3 — Pure UI
```
UI cannot influence system execution.
No edge exists: UI → System
```

### I4 — Instrumentation-Deterministic Execution
```
Same input + same instrumentation → identical trace
(modulo optional timestamp fields)
```

### I5 — No Reverse Edges
```
System graph is forward-only.
No path exists from observation back into execution.
```

---

## 6. What AIS² Is NOT

### Hard Boundaries (Non-Negotiable)

AIS² **cannot and will not:**

- **Trace arbitrary systems** — Systems must explicitly call `TraceLog.emit()`. No implicit introspection.
- **Observe non-instrumented code** — If instrumentation is absent, observation is impossible.
- **Support live debugging** — AIS² is post-hoc trace inspection only. No memory inspection, breakpoints, or execution control.
- **Reconstruct hidden state** — Only emitted events are observable. Internal state not logged is not recoverable.
- **Accept UI control of execution** — The dashboard is read-only by design. No event injection or execution modification.
- **Claim universality** — AIS² applies only to systems meeting the Compatible System Class definition (§4).

### Non-Goals (Explicitly Out of Scope)

- Real-time monitoring
- Interactive debugging
- Arbitrary program introspection
- Closed-system reverse engineering
- Inference of unrecorded behavior

---

## 3. How to Use AIS²

### Minimal Workflow

1. **Define a system that emits events**
   ```python
   from trace_exporter import TraceLog
   
   trace = TraceLog()
   trace.emit("INIT", {"state": "ready"})
   trace.emit("STEP", {"value": 42})
   trace.save("output.json")
   ```

2. **Verify determinism** — Run the same system twice, compare trace files. Must be identical.

3. **Load trace in dashboard**
   ```bash
   streamlit run dashboard/app.py
   # Load: output.json
   ```

4. **Inspect events** — View append-only log, verify event structure, check invariants.

### Example: Minimal System

```python
# example_system.py
from trace_exporter import TraceLog

def main():
    trace = TraceLog()
    
    # Event 1: Initialization
    trace.emit("WINDOW_CREATED", {"id": "W1"})
    
    # Event 2: Observation
    trace.emit("OBSERVATION", {"value": 100})
    
    # Event 3: Processing
    trace.emit("PROCESS", {"result": "success"})
    
    # Event 4: Output
    trace.emit("OUTPUT", {"type": "result"})
    
    trace.save("example_trace.json")

if __name__ == "__main__":
    main()
```

**Expected output:**
```json
[
  {"event_type": "WINDOW_CREATED", "timestamp": 0, "payload": {...}},
  {"event_type": "OBSERVATION", "timestamp": 1, "payload": {...}},
  {"event_type": "PROCESS", "timestamp": 2, "payload": {...}},
  {"event_type": "OUTPUT", "timestamp": 3, "payload": {...}}
]
```

---

## 4. Integration Model

### How External Systems Become Compatible

**Requirement:** Your system must emit structured events to a `TraceLog` instance.

**Three integration patterns:**

**Pattern A: Native Integration**
```python
# Your system calls TraceLog directly
from trace_exporter import TraceLog

class MySystem:
    def __init__(self):
        self.trace = TraceLog()
    
    def step(self, input_data):
        self.trace.emit("STEP", {"input": input_data})
        result = self.compute(input_data)
        self.trace.emit("RESULT", {"output": result})
        return result
    
    def save_trace(self, path):
        self.trace.save(path)
```

**Pattern B: Wrapper/Adapter**
```python
# You wrap an existing system to emit events
from trace_exporter import TraceLog

class SystemAdapter:
    def __init__(self, legacy_system):
        self.system = legacy_system
        self.trace = TraceLog()
    
    def execute(self, input_data):
        self.trace.emit("EXECUTE_START", {"input": input_data})
        result = self.system.process(input_data)
        self.trace.emit("EXECUTE_END", {"output": result})
        return result
```

**Pattern C: Instrumented Hooks**
```python
# You add instrumentation points to an existing system
def instrumented_function(x):
    trace.emit("FUNC_ENTER", {"x": x})
    result = original_function(x)
    trace.emit("FUNC_EXIT", {"result": result})
    return result
```

### Constraints on Integration

- **System must be deterministic** — Same input, same execution path, same trace
- **Events must be immutable** — Once emitted, events cannot be modified, deleted, or reordered
- **Trace must be self-contained** — All information necessary to understand execution must be in the trace

---

## 5. Core Invariants (Enforceable Rules)

These are **structural constraints** enforced by design, not aspirational guidelines.

### I1: Trace is Append-Only
```
∀ trace: only operation is append(event)
No delete, no update, no mutation
Enforcement: TraceLog has one public method: emit()
```

**Verification:** Timestamps must be strictly increasing (0, 1, 2, ...).

### I2: No Event Mutation or Deletion
```
∀ event ∈ trace: event is immutable
No event can be modified after emission
Enforcement: TraceEvent is @dataclass(frozen=True)
```

**Verification:** Trace file size increases monotonically with each emit.

### I3: UI is Pure Function Over Trace
```
UI_state = f(trace_json)
No state coupling back into system
Dashboard has no method to modify execution
Enforcement: Dashboard reads trace_file only
```

**Verification:** Dashboard cannot call any system APIs.

### I4: Execution is Deterministic Under Config
```
config_A + system_code_A → trace_X
config_A + system_code_A → trace_X (identical)
Enforcement: No randomness, no timestamps from system clock, no external state
```

**Verification:** Run system twice with same config, compare traces (must be byte-identical).

### I5: No Reverse Influence (UI → System)
```
system execution is independent of UI state
UI cannot modify, replay, or control execution
Enforcement: No event-injection API, no execution hooks from dashboard
```

**Verification:** Closing dashboard does not affect system; UI state has no side effects.

---

## 6. Mental Model

### Analogy: Flight Data Recorder for Software

Think of AIS² like an airplane's flight data recorder:

- **System** = aircraft engine and instrumentation
- **TraceLog** = data recording device (immutable, append-only)
- **Trace file** = recorded flight log (deterministic, reproducible)
- **Dashboard** = playback/inspection tool (read-only viewer)

Just as a flight recorder:
- Records what actually happened (not predictions)
- Cannot be modified after recording
- Cannot control the aircraft during replay
- Provides complete reproducibility

AIS² does the same for software execution: it records what happened, preserves it immutably, and provides read-only inspection.

---

## 7. Common Misconceptions (Corrected)

### ❌ "AIS² can run any program and trace it"
**Correction:** AIS² requires the system to emit events. If your system doesn't call `TraceLog.emit()`, there is nothing to trace. You must instrument your system.

### ❌ "AIS² is a live debugger"
**Correction:** AIS² is a post-hoc log viewer. It does not support breakpoints, step-through debugging, or runtime inspection. It records execution, not controls it.

### ❌ "AIS² can infer what a system did from its output"
**Correction:** AIS² records only what the system explicitly logged. Hidden state, internal computations not emitted, and undocumented behavior are not observable.

### ❌ "I can modify the trace and replay different execution paths"
**Correction:** The trace is immutable and append-only. You cannot modify events, delete them, or inject new ones. The trace is what actually happened, not a scenario generator.

### ❌ "The dashboard can control system behavior"
**Correction:** The dashboard is read-only. It displays the trace; it cannot modify, pause, or control execution. All control must come from the system itself.

### ❌ "AIS² works with any programming language"
**Correction:** AIS² works with any language that can emit to a TraceLog instance (or compatible JSON interface). The system must be explicitly instrumented.

---

## 8. Core Workflow: Step by Step

### Example: Tracing a State Machine

**System definition:**
```python
# state_machine.py
from trace_exporter import TraceLog

class StateMachine:
    def __init__(self):
        self.trace = TraceLog()
        self.state = "INIT"
    
    def transition(self, event):
        self.trace.emit("TRANSITION_START", {
            "from": self.state,
            "event": event
        })
        
        if self.state == "INIT" and event == "start":
            self.state = "RUNNING"
        elif self.state == "RUNNING" and event == "stop":
            self.state = "STOPPED"
        
        self.trace.emit("TRANSITION_END", {
            "to": self.state,
            "success": True
        })
    
    def save_trace(self, path):
        self.trace.save(path)

# Execution
sm = StateMachine()
sm.transition("start")
sm.transition("stop")
sm.save_trace("state_machine_trace.json")
```

**View the trace:**
```bash
python -m streamlit run dashboard/app.py
# In sidebar: state_machine_trace.json
```

**What you see:**
- Event log (TRANSITION_START, TRANSITION_END)
- State snapshots (INIT → RUNNING → STOPPED)
- Window state changes (if any)

---

## 9. Determinism Verification

**Definition (Instrumentation-Relative):**

```
Same input + same instrumentation ⇒ identical emitted event sequence
```

**Verification protocol:**

```bash
# Run 1
python system.py > trace_run1.json

# Run 2 (identical conditions)
python system.py > trace_run2.json

# Compare (event sequence, payloads)
diff <(jq '.[] | {type, payload}' trace_run1.json) \
     <(jq '.[] | {type, payload}' trace_run2.json)
# Should be identical (timestamps may differ if excluded from schema)
```

**What causes non-determinism:**

1. **Uncontrolled randomness** — `random.random()`, UUID generation
2. **External state** — File reads, network calls, environment variables
3. **Hidden concurrency** — Race conditions, thread scheduling
4. **Instrumentation gaps** — Missing events that affect trace

**What does NOT cause non-determinism (acceptable):**

- Wall-clock timestamps (if excluded from equality)
- System clock time (if not emitted)
- Memory addresses (if not emitted)

**Key principle:** Determinism is relative to **what you emit**. If you emit wall-clock timestamps, traces will differ. If you don't emit them (or exclude them from equality), traces will be identical.

---

## 10. Limitations (By Design)

These are **intentional constraints**, not bugs:

- **No live inspection** — Tracing is post-execution only
- **No performance optimization** — Every emit is a log entry; there is no filtering or compression
- **No execution control** — You cannot pause, resume, or modify execution from traces
- **No state inference** — Only explicitly emitted events are visible
- **No arbitrary system support** — Only systems designed to emit events are compatible
- **No concurrency guarantees** — Thread-safe tracing requires explicit synchronization in your system

These limitations are **features**—they enforce the isolation and immutability properties that make AIS² trustworthy.

---

## 11. Getting Started

### Minimum Viable Example

```bash
# 1. Create a system that emits events
echo '
from trace_exporter import TraceLog

trace = TraceLog()
trace.emit("START", {"id": "test"})
trace.emit("END", {"id": "test"})
trace.save("test_trace.json")
' > test_system.py

# 2. Run it
python test_system.py

# 3. View the trace
python -m streamlit run dashboard/app.py
# Load: test_trace.json
```

### Next Steps

1. **Instrument your own system** — Add `TraceLog.emit()` calls to your code
2. **Verify determinism** — Run twice, compare traces
3. **Load in dashboard** — Inspect events visually
4. **Validate invariants** — Use `tests/invariant_test_harness.py`

---

## 12. Support & Feedback

**This is a research artifact.** No production SLA or long-term support guaranteed.

**Questions about scope?**
- Read §2 (What AIS² Is NOT)
- Check §7 (Common Misconceptions)

**Issues with your system?**
- Verify determinism (§9)
- Check that all relevant events are emitted
- Ensure trace JSON is valid

**OSDI reviewers:**
- This guide defines the operational boundaries
- §5 lists all enforceable invariants
- §9 specifies determinism verification
- All claims are scope-bounded and verifiable

---

**End of User Guide**
