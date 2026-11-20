"""python -m reviewbot [--base main] [repo] — review the current branch."""

from __future__ import annotations

import argparse
import asyncio
from pathlib import Path

from .agent import run_review


def main() -> None:
    parser = argparse.ArgumentParser(prog="reviewbot")
    parser.add_argument("repo", nargs="?", type=Path, default=Path.cwd())
    parser.add_argument("--base", default="main")
    args = parser.parse_args()
    report = asyncio.run(run_review(args.repo.resolve(), args.base))
    for f in report.findings:
        print(f"{f.path}:{f.line}: [{f.severity}] {f.message}")
    print(f"\n{report.summary}")
    print(f"({report.subtype}, {report.turns} turns, ~${report.cost_usd:.4f})")
    raise SystemExit(1 if any(f.severity in ("major", "critical")
                              for f in report.findings) else 0)


if __name__ == "__main__":
    main()
