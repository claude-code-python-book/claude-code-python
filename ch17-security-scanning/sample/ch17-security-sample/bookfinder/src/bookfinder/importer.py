"""Import a catalogue file (YAML) and cache it (JSON, never pickle)."""

import json
import subprocess
from pathlib import Path
from typing import Any

import yaml


def load_catalogue(text: str) -> list[dict[str, Any]]:
    """Parse a YAML catalogue. safe_load builds only plain data types."""
    data = yaml.safe_load(text)
    if not isinstance(data, list):
        raise ValueError("catalogue must be a list of books")
    return data


def save_cache(books: list[dict[str, Any]], path: Path) -> None:
    """Cache parsed books as JSON, which cannot carry code."""
    path.write_text(json.dumps(books))


def load_cache(path: Path) -> list[dict[str, Any]]:
    """Read the cache back."""
    books: list[dict[str, Any]] = json.loads(path.read_text())
    return books


def count_lines(path: Path) -> int:
    """Count lines with wc, passing the file name as one argument, no shell."""
    result = subprocess.run(  # noqa: S603 - fixed program, argument list, no shell
        ["wc", "-l", "--", str(path)],  # noqa: S607 - wc is found on PATH
        capture_output=True,
        text=True,
        check=True,
        timeout=10,
    )
    return int(result.stdout.split()[0])
