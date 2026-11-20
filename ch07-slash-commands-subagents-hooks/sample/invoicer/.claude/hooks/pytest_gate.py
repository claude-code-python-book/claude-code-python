"""Stop hook: keep Claude working while the fast test suite fails.

Runs only when Python files have uncommitted changes. Blocks the stop
once; if the tests still fail after that retry, lets Claude stop and
warns the user instead of looping.
"""

import json
import os
import subprocess
import sys
from pathlib import Path

PYTEST = ["uv", "run", "--quiet", "pytest", "-q", "-x", "-m", "not slow"]
PASSED, NO_TESTS = 0, 5  # pytest exit codes that count as success


def python_changed(project: Path) -> bool:
    """True if git reports changed or new .py files (or git is unusable)."""
    try:
        status = subprocess.run(
            ["git", "status", "--porcelain", "--untracked-files=all", "--", "*.py"],
            cwd=project,
            capture_output=True,
            text=True,
            timeout=30,
            check=True,
        )
    except (OSError, subprocess.SubprocessError):
        return True  # not a git repository: run the tests to be safe
    return bool(status.stdout.strip())


def main() -> int:
    event = json.load(sys.stdin)
    project = Path(os.environ.get("CLAUDE_PROJECT_DIR", event["cwd"]))
    if not python_changed(project):
        return 0

    try:
        result = subprocess.run(
            PYTEST, cwd=project, capture_output=True, text=True, timeout=280
        )
    except (OSError, subprocess.TimeoutExpired) as exc:
        print(json.dumps({"systemMessage": f"pytest gate skipped: {exc}"}))
        return 0
    if result.returncode in (PASSED, NO_TESTS):
        return 0

    if event.get("stop_hook_active"):
        # Claude already had one try after a block. Don't loop: tell the user.
        message = "Tests still fail after Claude's retry. Run: uv run pytest -q"
        print(json.dumps({"systemMessage": message}))
        return 0

    tail = "\n".join((result.stdout + result.stderr).strip().splitlines()[-30:])
    print(f"The test suite fails:\n{tail}", file=sys.stderr)
    print("Fix the code or the tests before you finish.", file=sys.stderr)
    return 2


if __name__ == "__main__":
    sys.exit(main())
