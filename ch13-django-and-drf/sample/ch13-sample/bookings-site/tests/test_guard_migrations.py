"""The migrations hook, run the way Claude Code runs it: JSON on stdin."""

import json
import subprocess
import sys
from pathlib import Path

import pytest

HOOK = Path(__file__).parent.parent / ".claude/hooks/guard_migrations.py"


@pytest.fixture
def repo(tmp_path: Path) -> Path:
    """A git repository with one committed migration."""
    migrations = tmp_path / "bookings/migrations"
    migrations.mkdir(parents=True)
    (migrations / "0001_btree_gist.py").write_text("# applied everywhere\n")
    git = ["git", "-c", "user.name=t", "-c", "user.email=t@example.com"]
    subprocess.run([*git, "init", "-q"], cwd=tmp_path, check=True)
    subprocess.run([*git, "add", "."], cwd=tmp_path, check=True)
    subprocess.run([*git, "commit", "-qm", "first"], cwd=tmp_path, check=True)
    return tmp_path


def run_hook(repo: Path, file_path: str) -> str:
    event = {
        "hook_event_name": "PreToolUse",
        "tool_name": "Edit",
        "tool_input": {"file_path": str(repo / file_path)},
        "cwd": str(repo),
    }
    result = subprocess.run(
        [sys.executable, str(HOOK)],
        input=json.dumps(event),
        capture_output=True,
        text=True,
        check=True,
    )
    return result.stdout


def test_editing_a_committed_migration_asks_first(repo: Path) -> None:
    decision = json.loads(run_hook(repo, "bookings/migrations/0001_btree_gist.py"))
    output = decision["hookSpecificOutput"]
    assert output["permissionDecision"] == "ask"
    assert "0001_btree_gist.py is committed" in output["permissionDecisionReason"]


@pytest.mark.parametrize(
    "file_path",
    [
        "bookings/migrations/0002_new.py",  # not committed yet
        "bookings/migrations/__init__.py",  # not a migration
        "bookings/models.py",  # not in migrations/
    ],
)
def test_other_files_get_no_opinion(repo: Path, file_path: str) -> None:
    assert run_hook(repo, file_path) == ""
