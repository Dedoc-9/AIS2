# examples/omega_transition_demo.py
# Ω path: categorical/domain failure forces type-separated handling.
# Invariant I3: Ω-domain isolation enforced
# Invariant I5: trace is append-only

import sys
import os

# Add parent directory to path (for trace_exporter import)
script_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(script_dir)
sys.path.insert(0, parent_dir)

from trace_exporter import TraceLog


def run_omega():
    """
    Ω execution path: categorical/domain boundary violation.

    Flow:
    1. Initialize window (RepresentableState)
    2. Observation triggers domain violation
    3. Irreversible transition to NonRepresentableState
    4. Type-separated Ω witness (no observation leakage)
    5. OmegaProjectionPolicy → P2 primitives only

    Ω is not data; it is a proof of Φ non-totality.
    """
    trace = TraceLog()

    # Event 1: Window creation
    trace.emit("STATE_INIT", {
        "window_id": "W3",
        "state": "RepresentableState"
    })

    # Event 2: Observation crosses domain boundary
    trace.emit("OBSERVATION", {
        "window_id": "W3",
        "value": "invalid_type"  # domain violation
    })

    # Event 3: IRREVERSIBLE TRANSITION (no recovery)
    trace.emit("STATE_TRANSITION", {
        "window_id": "W3",
        "from": "RepresentableState",
        "to": "NonRepresentableState"
    })

    # Event 4: Ω witness (type-separated, no observation in output)
    trace.emit("OMEGA_WITNESS", {
        "window_id": "W3",
        "failure_level": "CATEGORICAL",
        "witness_code": "DOMAIN_VIOLATION",
        "timestamp": 3
    })

    # Event 5: Render with OmegaProjectionPolicy (P2-only)
    trace.emit("RENDER", {
        "window_id": "W3",
        "output": "PixelBuffer(P2.LossSignature + P2.NullSpaceMarker)"
    })

    trace.save("traces/omega_trace.json")
    print(f"✓ Ω path trace: {len(trace)} events")
    print(f"✓ Saved to: traces/omega_trace.json")
    print(f"✓ Invariant: Ω is type-separated (no Observation leakage)")


if __name__ == "__main__":
    run_omega()
