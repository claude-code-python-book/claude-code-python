"""PostToolUse hook: check a migration as soon as Claude writes it.

Runs tools/check_migrations.py on the file. Exit code 2 sends the findings
to Claude, which can fix the migration before anyone runs it.
"""

import json
import os
import re
import subprocess
import sys
from pathlib import Path

MIGRATION = re.compile(r"(^|/)migrations/versions/[^/]+\.py$")


def main() -> int:
    """Read the tool call from stdin; exit 2 if the migration has findings."""
    event = json.load(sys.stdin)
    file_path = event.get("tool_input", {}).get("file_path", "")
    if not MIGRATION.search(file_path.replace("\\", "/")):
        return 0
    project = Path(os.environ.get("CLAUDE_PROJECT_DIR", event["cwd"]))
    result = subprocess.run(
        [sys.executable, str(project / "tools" / "check_migrations.py"), file_path],
        capture_output=True,
        text=True,
        check=False,
    )
    if result.returncode == 0:
        return 0
    print(result.stdout.rstrip(), file=sys.stderr)
    print(
        "Fix these, or add '# migration-ok: CODE <reason>' to the line "
        "if the risk is understood and accepted.",
        file=sys.stderr,
    )
    return 2


if __name__ == "__main__":
    sys.exit(main())
