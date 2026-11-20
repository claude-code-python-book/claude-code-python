import subprocess
from pathlib import Path

import pytest

BASE = '''def average(xs: list[float]) -> float:
    if not xs:
        return 0.0
    return sum(xs) / len(xs)
'''
FEATURE = '''def average(xs: list[float]) -> float:
    return sum(xs) / len(xs)


def ratio(a: int, b: int) -> float:
    return a / b
'''


def sh(repo: Path, *args: str) -> None:
    subprocess.run(["git", "-C", str(repo), *args], check=True,
                   capture_output=True)


@pytest.fixture
def repo(tmp_path: Path) -> Path:
    """A git repo whose feature branch removes an empty-list guard."""
    sh(tmp_path, "init", "-q", "-b", "main")
    sh(tmp_path, "config", "user.email", "dev@example.com")
    sh(tmp_path, "config", "user.name", "Dev")
    (tmp_path / "stats.py").write_text(BASE)
    sh(tmp_path, "add", ".")
    sh(tmp_path, "commit", "-qm", "base")
    sh(tmp_path, "switch", "-qc", "feature")
    (tmp_path / "stats.py").write_text(FEATURE)
    sh(tmp_path, "commit", "-qam", "simplify average, add ratio")
    (tmp_path / ".env").write_text("API_TOKEN=do-not-read\n")  # untracked
    return tmp_path


@pytest.fixture
def anyio_backend() -> str:
    return "asyncio"
