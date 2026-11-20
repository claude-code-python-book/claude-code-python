"""Guard rails between an HTTP endpoint and the review agent."""

from __future__ import annotations

import asyncio
import os
from collections.abc import Awaitable, Callable
from pathlib import Path

from .agent import ReviewReport, run_review

Runner = Callable[[Path, str], Awaitable[ReviewReport]]


class UnknownRepoError(LookupError):
    pass


class BudgetExhaustedError(RuntimeError):
    pass


class ReviewService:
    def __init__(
        self, repos: dict[str, Path], *, max_concurrent: int = 2,
        timeout_s: float = 600, budget_usd: float = 20.0,
        runner: Runner = run_review,
    ) -> None:
        self.repos = repos
        self.timeout_s = timeout_s
        self.budget_usd = budget_usd
        self.spent_usd = 0.0
        self._slots = asyncio.Semaphore(max_concurrent)  # one CLI process each
        self._runner = runner

    @classmethod
    def from_env(cls) -> ReviewService:
        # REVIEWBOT_REPOS="payments=/srv/repos/payments,web=/srv/repos/web"
        pairs = os.environ.get("REVIEWBOT_REPOS", "").split(",")
        repos = {k: Path(v) for k, _, v in (p.partition("=") for p in pairs) if v}
        return cls(repos, budget_usd=float(os.environ.get("REVIEWBOT_BUDGET", 20)))

    async def review(self, repo: str, base: str) -> ReviewReport:
        path = self.repos.get(repo)          # never a client-supplied path
        if path is None:
            raise UnknownRepoError(repo)
        if self.spent_usd >= self.budget_usd:
            raise BudgetExhaustedError(f"spent ${self.spent_usd:.2f}")
        async with self._slots:
            async with asyncio.timeout(self.timeout_s):
                report = await self._runner(path, base)
        self.spent_usd += report.cost_usd
        return report
