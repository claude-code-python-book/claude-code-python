import json
import subprocess
import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).parents[1]
HOOK = ROOT / ".claude" / "hooks" / "check_migration.py"


def run_hook(file_path: Path) -> subprocess.CompletedProcess[str]:
    event = {
        "hook_event_name": "PostToolUse",
        "tool_name": "Write",
        "cwd": str(ROOT),
        "tool_input": {"file_path": str(file_path)},
    }
    return subprocess.run(
        [sys.executable, str(HOOK)],
        input=json.dumps(event),
        capture_output=True,
        text=True,
        check=False,
        env={"CLAUDE_PROJECT_DIR": str(ROOT)},
    )


@pytest.fixture
def versions(tmp_path: Path) -> Path:
    folder = tmp_path / "migrations" / "versions"
    folder.mkdir(parents=True)
    return folder


def test_a_risky_migration_goes_back_to_claude(versions: Path) -> None:
    bad = versions / "0006_index_total.py"
    bad.write_text(
        "from alembic import op\n\n\ndef upgrade():\n"
        '    op.create_index("ix_orders_total", "orders", ["total"])\n'
    )
    result = run_hook(bad)
    assert result.returncode == 2
    assert "MIG001" in result.stderr


def test_a_safe_migration_passes(versions: Path) -> None:
    good = versions / "0006_noop.py"
    good.write_text("def upgrade():\n    pass\n")
    assert run_hook(good).returncode == 0


def test_other_files_are_ignored(tmp_path: Path) -> None:
    other = tmp_path / "loyalty" / "service.py"
    other.parent.mkdir()
    other.write_text("op.drop_table('x')\n")
    assert run_hook(other).returncode == 0
