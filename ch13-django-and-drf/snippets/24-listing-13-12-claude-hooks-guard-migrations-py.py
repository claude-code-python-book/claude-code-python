"""PreToolUse hook: ask before Claude edits a migration that is already committed.

A committed migration may have been applied on a colleague's machine, in CI
or in production. Editing it changes history that those databases have
already recorded; the safe change is a new migration.
"""

import json
import re
import subprocess
import sys
from pathlib import Path

MIGRATION = re.compile(r"(^|/)migrations/\d{4}_\w+\.py$")


def is_committed(path: Path, cwd: Path) -> bool:
    """Return True if git tracks the file."""
    result = subprocess.run(
        ["git", "ls-files", "--error-unmatch", str(path)],
        cwd=cwd,
        capture_output=True,
        check=False,
    )
    return result.returncode == 0


def main() -> int:
    """Read the tool call from stdin and print a decision, or nothing."""
    event = json.load(sys.stdin)
    file_path = event.get("tool_input", {}).get("file_path", "")
    cwd = Path(event["cwd"])
    if not MIGRATION.search(file_path.replace("\\", "/")):
        return 0
    if not is_committed(Path(file_path), cwd):
        return 0  # a new migration: fine to write
    output = {
        "hookSpecificOutput": {
            "hookEventName": "PreToolUse",
            "permissionDecision": "ask",
            "permissionDecisionReason": (
                f"{Path(file_path).name} is committed and may already be applied. "
                "Create a new migration instead, unless this one has never "
                "left your machine."
            ),
        }
    }
    print(json.dumps(output))
    return 0


if __name__ == "__main__":
    sys.exit(main())
