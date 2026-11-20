"""Call the tool handlers directly: they are plain async functions."""

from pathlib import Path

import pytest

from reviewbot.tools import ReviewState, review_tools


def handlers(repo: Path) -> tuple[ReviewState, dict]:
    state = ReviewState(repo=repo, base="main")
    return state, {t.name: t.handler for t in review_tools(state)}


def body(result: dict) -> str:
    return result["content"][0]["text"]


@pytest.mark.anyio
async def test_changed_files_lists_branch_changes(repo: Path) -> None:
    _, tools = handlers(repo)
    assert body(await tools["changed_files"]({})) == "stats.py"


@pytest.mark.anyio
async def test_file_diff_shows_removed_guard(repo: Path) -> None:
    _, tools = handlers(repo)
    diff = body(await tools["file_diff"]({"path": "stats.py"}))
    assert "-    if not xs:" in diff
    assert "+def ratio(a: int, b: int) -> float:" in diff


@pytest.mark.anyio
@pytest.mark.parametrize("bad", ["../outside.py", "/etc/passwd", "--output=x"])
async def test_file_diff_refuses_unsafe_paths(repo: Path, bad: str) -> None:
    _, tools = handlers(repo)
    result = await tools["file_diff"]({"path": bad})
    assert result["is_error"] is True


@pytest.mark.anyio
async def test_record_finding_appends(repo: Path) -> None:
    state, tools = handlers(repo)
    result = await tools["record_finding"]({
        "path": "stats.py", "line": 2, "severity": "major", "message": "x"})
    assert body(result) == "Recorded finding #1"
    assert state.findings[0].severity == "major"


@pytest.mark.anyio
async def test_changed_files_reports_git_errors(repo: Path) -> None:
    state, tools = handlers(repo)
    state.base = "no-such-branch"
    result = await tools["changed_files"]({})
    assert result["is_error"] is True
    assert "git diff failed" in body(result)
