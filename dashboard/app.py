# dashboard/app.py
# Streamlit observational trace viewer.
# Pure function over trace JSON (no system access, no state mutation).
# Invariant F1: UI → system (forbidden)
# Invariant I1–I5: rendered directly from trace

import streamlit as st
import json
import os


def load_trace(path: str):
    """Load JSON trace file (read-only)."""
    if not os.path.exists(path):
        st.error(f"Trace file not found: {path}")
        return []
    with open(path, "r") as f:
        return json.load(f)


def render_event_log(trace):
    """
    Render append-only event log.
    No filtering, no reordering, no mutation.
    """
    st.subheader("Event Log (Append-Only, No Mutation)")
    for i, event in enumerate(trace):
        st.text(f"[{event['timestamp']}] {event['event_type']}: {event['payload']}")


def render_window_snapshots(trace):
    """
    Render window state snapshots at each event.
    Static view (no animation, no interpolation).
    """
    st.subheader("Window Snapshots (State at Each Event)")
    windows = {}
    for event in trace:
        window_id = event["payload"].get("window_id", "unknown")
        if window_id not in windows:
            windows[window_id] = []
        windows[window_id].append(event)

    for window_id, events in windows.items():
        with st.expander(f"Window {window_id}"):
            for event in events:
                st.write(f"State: {event['payload'].get('state', 'unknown')}")


def render_primitive_inspector(trace):
    """
    Group primitives by type (P0, P1, P2).
    No interpretation, no semantics.
    """
    st.subheader("Primitive Inspector")
    primitives = {"P0": [], "P1": [], "P2": []}
    for event in trace:
        prim_set = event["payload"].get("primitive_set", [])
        for p in prim_set:
            if p.startswith("P0"):
                primitives["P0"].append(p)
            elif p.startswith("P1"):
                primitives["P1"].append(p)
            elif p.startswith("P2"):
                primitives["P2"].append(p)
    st.json(primitives)


def main():
    st.set_page_config(layout="wide")
    st.title("AIS² Trace Dashboard (Observational Only)")

    st.sidebar.title("Trace Loader")
    trace_path = st.sidebar.text_input(
        "Trace file path",
        "traces/minimal_trace.json"
    )

    # Load and display
    trace = load_trace(trace_path)
    if trace:
        st.success(f"✓ Loaded {len(trace)} events")

        col1, col2 = st.columns([1, 1])

        with col1:
            render_event_log(trace)

        with col2:
            render_window_snapshots(trace)

        render_primitive_inspector(trace)

        st.divider()
        st.info("Dashboard is observational only: pure function over trace JSON. No system access, no state mutation.")
    else:
        st.warning("No trace loaded.")


if __name__ == "__main__":
    main()
