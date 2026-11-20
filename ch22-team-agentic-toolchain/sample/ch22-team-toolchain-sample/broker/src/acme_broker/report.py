"""Summarise the broker's audit log: adoption, friction and reliability.

    python -m acme_broker.report /var/log/acme-broker/audit.jsonl
"""

from __future__ import annotations

import json
import statistics
import sys
from collections import Counter, defaultdict
from datetime import UTC, datetime
from pathlib import Path
from typing import Any


def load(path: Path) -> list[dict[str, Any]]:
    return [json.loads(line) for line in path.read_text().splitlines() if line]


def summarise(entries: list[dict[str, Any]]) -> dict[str, Any]:
    weeks: dict[str, set[str]] = defaultdict(set)
    for e in entries:
        year, week, _ = datetime.fromtimestamp(e["ts"], UTC).isocalendar()
        weeks[f"{year}-W{week:02d}"].add(e["user"])
    outcomes = Counter(e["outcome"] for e in entries)
    ok_ms = sorted(e["ms"] for e in entries if e["outcome"] == "ok")
    return {
        "calls": len(entries),
        "weekly_active_users": {w: len(u) for w, u in sorted(weeks.items())},
        "calls_by_tool": dict(Counter(e["tool"] for e in entries).most_common()),
        "outcomes": dict(outcomes.most_common()),
        "success_rate": round(outcomes["ok"] / len(entries), 3) if entries else 0.0,
        "p50_ms": round(statistics.median(ok_ms), 1) if ok_ms else None,
        "p95_ms": ok_ms[int(0.95 * (len(ok_ms) - 1))] if ok_ms else None,
        "needs_onboarding": sorted({e["user"] for e in entries
                                    if e["outcome"] == "no_credential"}),
    }


if __name__ == "__main__":
    for name, value in summarise(load(Path(sys.argv[1]))).items():
        print(f"{name:<20} {json.dumps(value)}")
