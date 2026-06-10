# trace_exporter.py
# Append-only event log. No mutation, no deletion, no update semantics.
# Invariant I5: Trace is immutable after export.

import json
from dataclasses import dataclass, asdict
from typing import Any, Dict, List


@dataclass(frozen=True)
class TraceEvent:
    """Immutable trace event. Frozen to prevent mutation."""
    event_type: str
    timestamp: int
    payload: Dict[str, Any]


class TraceLog:
    """
    Append-only event log (Invariant I5).

    Contract:
    - Only operation: append (emit)
    - No deletion, no update, no mutation
    - Export is final snapshot (immutable)
    """

    def __init__(self):
        self._events: List[TraceEvent] = []
        self._t = 0

    def emit(self, event_type: str, payload: Dict[str, Any]):
        """
        Emit immutable event to log.

        Invariant I1: timestamps strictly increasing
        Invariant I5: append-only semantics
        """
        self._events.append(
            TraceEvent(
                event_type=event_type,
                timestamp=self._t,
                payload=payload,
            )
        )
        self._t += 1

    def export_json(self) -> str:
        """
        Export full trace as JSON string.
        No interpretation, no branching logic.
        """
        return json.dumps([asdict(e) for e in self._events], indent=2)

    def save(self, path: str):
        """
        Write trace to file (final, immutable snapshot).
        """
        with open(path, "w") as f:
            f.write(self.export_json())

    def __len__(self):
        return len(self._events)
