"""Fail the release if the Git tag and the package version disagree.

Usage: python scripts/check_version.py v0.3.0
"""

import sys
import tomllib
from pathlib import Path


def main(tag: str) -> int:
    project = tomllib.loads(Path("pyproject.toml").read_text(encoding="utf-8"))
    version = project["project"]["version"]
    if tag != f"v{version}":
        print(f"::error::tag {tag} does not match pyproject.toml version {version}")
        return 1
    print(f"tag {tag} matches version {version}")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1]))
