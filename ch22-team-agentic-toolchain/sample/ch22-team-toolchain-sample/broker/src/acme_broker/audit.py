"""One JSON line per tool call: who, what, outcome, how long."""

from __future__ import annotations

import json
import time
from pathlib import Path
from threading import Lock


class AuditLog:
    def __init__(self, path: Path) -> None:
        self.path, self._lock = path, Lock()

    def record(self, user: str, tool: str, target: str, outcome: str,
               started: float) -> None:
        entry = {"ts": round(time.time(), 3), "user": user, "tool": tool,
                 "target": target, "outcome": outcome,
                 "ms": round((time.perf_counter() - started) * 1000, 1)}
        with self._lock, self.path.open("a", encoding="utf-8") as fh:
            fh.write(json.dumps(entry) + "\n")
