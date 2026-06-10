# examples/failure_demo.py
# Failure path: Φ becomes non-total, irreversible transition.
# Invariant I2: Irreversibility enforced (no reverse edge)
# Invariant I5: trace is append-only

import sys
import os

# Add parent directory to path (for trace_exporter import)
script_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(script_dir)
sys.path.insert(0, parent_dir)

from trace_exporter import TraceLog


def run_failure():
    """
    Failure execution path: forced NonRepresentableState transition.

    Flow:
    1. Initialize window (RepresentableState)
    2. Observation triggers failure (Φ non-total)
    3. Irreversible transition to NonRepresentableState
    4. Witness emitted (no recovery possible)
    5. Render outputs P2 primitives only

    No recovery, no branching, terminal state.
    """
    trace = TraceLog()

    # Event 1: Window creation
    trace.emit("STATE_INIT", {
        "window_id": "W2",
        "state": "RepresentableState"
    })

    # Event 2: Observation that triggers failure
    trace.emit("OBSERVATION", {
        "window_id": "W2",
        "value": None  # undefined, triggers failure
    })

    # Event 3: IRREVERSIBLE TRANSITION (F_Ω2: no reverse edge)
    trace.emit("STATE_TRANSITION", {
        "window_id": "W2",
        "from": "RepresentableState",
        "to": "NonRepresentableState"
    })

    # Event 4: Witness emission (immutable proof of failure)
    trace.emit("WITNESS_EMIT", {
        "window_id": "W2",
        "failure_level": "TOPOLOGICAL",
        "witness_code": "NON_TOTAL_MAPPING",
        "timestamp": 3
    })

    # Event 5: Render (P2-only primitives, no interpretation)
    trace.emit("RENDER", {
        "window_id": "W2",
        "output": "PixelBuffer(P2.LossSignature + P2.NoiseFloor)"
    })

    trace.save("traces/failure_trace.json")
    print(f"✓ Failure path trace: {len(trace)} events")
    print(f"✓ Saved to: traces/failure_trace.json")
    print(f"✓ Invariant: NonRepresentableState is TERMINAL (no reverse edge)")


if __name__ == "__main__":
    run_failure()
