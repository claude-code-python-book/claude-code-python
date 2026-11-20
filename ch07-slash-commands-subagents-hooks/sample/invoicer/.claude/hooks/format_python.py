"""PostToolUse hook: run Ruff on a Python file after Claude edits it.

Fixes what Ruff can fix, formats the file, and reports any lint errors
that remain back to Claude by exiting with status 2.
"""

import json
import os
import subprocess
import sys
from pathlib import Path

RUFF = ["uv", "run", "--quiet", "ruff"]


def ruff(*args: str, cwd: Path) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        [*RUFF, *args], cwd=cwd, capture_output=True, text=True, timeout=50
    )


def main() -> int:
    event = json.load(sys.stdin)
    project = Path(os.environ.get("CLAUDE_PROJECT_DIR", event["cwd"])).resolve()
    path = Path(event.get("tool_input", {}).get("file_path", "")).resolve()

    # Only Python files inside this project; skip .venv and the like.
    if path.suffix not in {".py", ".pyi"} or not path.is_file():
        return 0
    if not path.is_relative_to(project) or ".venv" in path.parts:
        return 0

    try:
        ruff("check", "--fix", "--quiet", str(path), cwd=project)
        ruff("format", "--quiet", str(path), cwd=project)
        result = ruff(
            "check", "--no-fix", "--output-format=concise", str(path), cwd=project
        )
    except (OSError, subprocess.TimeoutExpired) as exc:
        print(f"format_python hook could not run Ruff: {exc}", file=sys.stderr)
        return 1  # a non-blocking error: Claude carries on

    if result.returncode == 1:  # lint errors Ruff could not fix
        print(result.stdout.strip(), file=sys.stderr)
        print("Fix these Ruff errors in the file you just edited.", file=sys.stderr)
        return 2
    if result.returncode != 0:  # Ruff itself failed, e.g. bad config
        print(result.stderr.strip(), file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
