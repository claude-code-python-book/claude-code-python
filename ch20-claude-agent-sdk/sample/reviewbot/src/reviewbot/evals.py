"""Score review findings against labelled cases; optionally run live."""

from __future__ import annotations

import argparse
import asyncio
import subprocess
import tempfile
import tomllib
from dataclasses import dataclass
from pathlib import Path
from typing import Any

from .tools import SEVERITIES, Finding

RANK = {name: i for i, name in enumerate(SEVERITIES)}


@dataclass
class CaseScore:
    name: str
    recall: float
    precision: float


def matches(finding: Finding, path: str, expected: dict[str, Any]) -> bool:
    text = finding.message.lower()
    return (
        finding.path == path
        and abs(finding.line - expected["line"]) <= 3
        and RANK[finding.severity] >= RANK[expected["min_severity"]]
        and any(word in text for word in expected["keywords"])
    )


def score(case: dict[str, Any], findings: list[Finding]) -> CaseScore:
    expected = case["expect"]
    hit = [e for e in expected if any(matches(f, case["path"], e) for f in findings)]
    useful = [f for f in findings if any(matches(f, case["path"], e) for e in expected)]
    return CaseScore(
        case["name"],
        recall=len(hit) / len(expected),
        precision=len(useful) / len(findings) if findings else 1.0,
    )


def load_cases(path: Path) -> list[dict[str, Any]]:
    cases: list[dict[str, Any]] = tomllib.loads(path.read_text("utf-8"))["case"]
    return cases


def build_repo(case: dict[str, Any], root: Path) -> Path:
    def git(*args: str) -> None:
        ident = ["-c", "user.name=eval", "-c", "user.email=eval@example.com"]
        subprocess.run(["git", "-C", str(root), *ident, *args],  # noqa: S603,S607
                       check=True, capture_output=True)

    target = root / case["path"]
    git("init", "-q", "-b", "main")
    target.write_text(case["base"].lstrip())
    git("add", ".")
    git("commit", "-qm", "base")
    git("switch", "-qc", "change")
    target.write_text(case["change"].lstrip())
    git("commit", "-qam", "change")
    return root


async def run_live(cases_file: Path) -> list[CaseScore]:
    from .agent import run_review  # needs ANTHROPIC_API_KEY and spends money

    scores = []
    for case in load_cases(cases_file):
        with tempfile.TemporaryDirectory() as tmp:
            report = await run_review(build_repo(case, Path(tmp)), "main")
        scores.append(score(case, report.findings))
    return scores


def main() -> None:
    parser = argparse.ArgumentParser(description="Run review evals live.")
    parser.add_argument("cases", type=Path)
    parser.add_argument("--min-recall", type=float, default=1.0)
    args = parser.parse_args()
    scores = asyncio.run(run_live(args.cases))
    for s in scores:
        print(f"{s.name:20} recall={s.recall:.2f} precision={s.precision:.2f}")
    if min(s.recall for s in scores) < args.min_recall:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
