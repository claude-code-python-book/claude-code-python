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
