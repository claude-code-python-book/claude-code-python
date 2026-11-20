"""Cost ledger, the HTTP service guard rails, schemas, and eval scoring."""

import asyncio
from pathlib import Path

import pytest
from claude_agent_sdk import AssistantMessage, ResultMessage, TextBlock

from reviewbot.agent import ReviewReport
from reviewbot.cost import CostLedger
from reviewbot.evals import build_repo, load_cases, score
from reviewbot.schemas import ReviewRequest, ReviewResponse
from reviewbot.service import BudgetExhaustedError, ReviewService, UnknownRepoError
from reviewbot.tools import Finding

CASES = Path(__file__).parent.parent / "evals" / "cases.toml"


def step(msg_id: str, tokens: int) -> AssistantMessage:
    return AssistantMessage(content=[TextBlock("...")], model="m",
                            message_id=msg_id,
                            usage={"input_tokens": tokens, "output_tokens": 1})


def done(cost: float) -> ResultMessage:
    return ResultMessage(subtype="success", duration_ms=1, duration_api_ms=1,
                         is_error=False, num_turns=2, session_id="s",
                         total_cost_usd=cost,
                         usage={"output_tokens": 300,
                                "cache_read_input_tokens": 900})


def test_ledger_counts_each_api_response_once() -> None:
    ledger = CostLedger()
    for msg in [step("a", 1000), step("a", 1000), step("b", 1500), done(0.02)]:
        ledger.observe(msg)
    assert (ledger.input_tokens, ledger.output_tokens) == (2500, 300)
    assert ledger.cost_usd == pytest.approx(0.02) and ledger.runs == 1


def report(cost: float = 0.10) -> ReviewReport:
    return ReviewReport([Finding("a.py", 1, "major", "bug")], "summary",
                        "success", cost, 3, "s")


@pytest.mark.anyio
async def test_service_limits_concurrency() -> None:
    running = peak = 0

    async def runner(path: Path, base: str) -> ReviewReport:
        nonlocal running, peak
        running += 1
        peak = max(peak, running)
        await asyncio.sleep(0.02)
        running -= 1
        return report()

    svc = ReviewService({"web": Path("/srv/web")}, max_concurrent=2,
                        runner=runner)
    await asyncio.gather(*(svc.review("web", "main") for _ in range(5)))
    assert peak == 2
    assert svc.spent_usd == pytest.approx(0.50)


@pytest.mark.anyio
async def test_service_rejects_unknown_repo_and_spent_budget() -> None:
    async def runner(path: Path, base: str) -> ReviewReport:
        return report(cost=1.0)

    svc = ReviewService({"web": Path("/srv/web")}, budget_usd=1.0, runner=runner)
    with pytest.raises(UnknownRepoError):
        await svc.review("../../etc", "main")
    await svc.review("web", "main")
    with pytest.raises(BudgetExhaustedError):
        await svc.review("web", "main")


@pytest.mark.anyio
async def test_service_times_out() -> None:
    async def runner(path: Path, base: str) -> ReviewReport:
        await asyncio.sleep(1)
        return report()

    svc = ReviewService({"web": Path("/srv/web")}, timeout_s=0.05, runner=runner)
    with pytest.raises(TimeoutError):
        await svc.review("web", "main")


def test_schemas_validate_and_serialise() -> None:
    with pytest.raises(ValueError):
        ReviewRequest(repo="web", base="--upload-pack=x")
    body = ReviewResponse.from_report(report(0.123456)).model_dump()
    assert body["cost_usd"] == 0.1235 and body["findings"][0]["path"] == "a.py"


def test_eval_scoring() -> None:
    case = load_cases(CASES)[0]
    good = Finding("stats.py", 2, "major", "Raises ZeroDivisionError on empty list")
    weak = Finding("stats.py", 2, "minor", "empty list not handled")
    noise = Finding("stats.py", 1, "info", "Consider a docstring")
    assert score(case, [good, noise]).recall == 1.0
    assert score(case, [good, noise]).precision == 0.5
    assert score(case, [weak]).recall == 0.0        # severity too low


def test_eval_fixture_repo_has_the_change(tmp_path: Path) -> None:
    case = load_cases(CASES)[1]
    repo = build_repo(case, tmp_path)
    assert "shell=True" in (repo / "deploy.py").read_text()
