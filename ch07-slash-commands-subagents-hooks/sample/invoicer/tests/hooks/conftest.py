"""Fixtures for testing the hook scripts in .claude/hooks.

Each test runs a hook the way Claude Code does: as a child process with
the event JSON on stdin. A stand-in `uv` on PATH runs the tools
directly, so the tests need no network and never touch a lock file.
"""

import json
import os
import subprocess
import sys
from collections.abc import Callable
from pathlib import Path
from typing import Any

import pytest

HOOKS = Path(__file__).resolve().parents[2] / ".claude" / "hooks"

FAKE_UV = f"""#!{sys.executable}
import os, shutil, sys
args = sys.argv[2:]  # drop "run"
while args[0].startswith("-"):
    args.pop(0)  # drop options such as --quiet
exe = shutil.which(args[0])
cmd = [exe, *args[1:]] if exe else [sys.executable, "-m", *args]
os.execv(cmd[0], cmd)
"""

RUFF_CONFIG = '[tool.ruff.lint]\nselect = ["E", "F", "I"]\n'


@pytest.fixture
def project(tmp_path: Path) -> Path:
    """A small Git project with a Ruff configuration."""
    root = tmp_path / "project"
    root.mkdir()
    (root / "pyproject.toml").write_text(RUFF_CONFIG)
    subprocess.run(["git", "init", "-q"], cwd=root, check=True)
    return root


@pytest.fixture
def run_hook(
    project: Path, tmp_path: Path
) -> Callable[..., subprocess.CompletedProcess[str]]:
    """Return a function that runs a hook script with an event on stdin."""
    bin_dir = tmp_path / "bin"
    bin_dir.mkdir()
    (bin_dir / "uv").write_text(FAKE_UV)
    (bin_dir / "uv").chmod(0o755)
    env = {
        **os.environ,
        "PATH": f"{bin_dir}{os.pathsep}{os.environ['PATH']}",
        "CLAUDE_PROJECT_DIR": str(project),
    }

    def run(script: str, **event: Any) -> subprocess.CompletedProcess[str]:
        event = {"cwd": str(project), **event}
        return subprocess.run(
            [sys.executable, str(HOOKS / script)],
            input=json.dumps(event),
            capture_output=True,
            text=True,
            env=env,
            timeout=120,
        )

    return run
