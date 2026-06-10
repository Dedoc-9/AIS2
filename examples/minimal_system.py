# examples/minimal_system.py
# Minimal deterministic system runner.
# Single execution, no randomness, append-only trace.
# Invariant I2: state transitions valid
# Invariant I5: trace is append-only

import sys
import os

# Add parent directory to path (for trace_exporter import)
script_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(script_dir)
sys.path.insert(0, parent_dir)

from trace_exporter import TraceLog


def run_minimal():
    """
    Minimal deterministic execution path.

    Flow:
    1. Initialize window (RepresentableState)
    2. Emit observation
    3. Projection → PrimitiveSet
    4. Render (PixelBuffer output)

    No branching, no randomness, deterministic order.
    """
    trace = TraceLog()

    # Event 1: Window creation (RepresentableState)
    trace.emit("STATE_INIT", {
        "window_id": "W1",
        "state": "RepresentableState"
    })

    # Event 2: Observation input
    trace.emit("OBSERVATION", {
        "window_id": "W1",
        "value": 42
    })

    # Event 3: Projection (Φ is total, RepresentableState)
    trace.emit("PROJECTION", {
        "window_id": "W1",
        "primitive_set": ["P0.Point", "P0.Edge"]
    })

    # Event 4: Render (pure function)
    trace.emit("RENDER", {
        "window_id": "W1",
        "output": "PixelBuffer(hash=0x1234abcd)"
    })

    trace.save("traces/minimal_trace.json")
    print(f"✓ Minimal system trace: {len(trace)} events")
    print(f"✓ Saved to: traces/minimal_trace.json")


if __name__ == "__main__":
    run_minimal()
