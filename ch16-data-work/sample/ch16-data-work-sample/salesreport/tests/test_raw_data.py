"""Raw exports are evidence: prove they were never modified."""

import hashlib
from pathlib import Path

RAW = Path(__file__).parents[1] / "data/raw"


def test_raw_files_match_their_manifest() -> None:
    lines = (RAW / "MANIFEST.sha256").read_text().splitlines()
    assert lines, "empty manifest"
    for line in lines:
        digest, name = line.split()
        actual = hashlib.sha256((RAW / name).read_bytes()).hexdigest()
        assert actual == digest, f"{name} has changed"
