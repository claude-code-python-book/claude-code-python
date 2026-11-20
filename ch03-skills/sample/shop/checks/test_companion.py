"""Checks that the Chapter 3 scripts print exactly what the chapter shows.

Run from the chapter folder:  uv run pytest checks -q
"""
import json
import re
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SKILL = ROOT / ".claude/skills/writing-pytest-tests"
EXPECTED = json.loads((Path(__file__).parent / "expected.json").read_text())  # from the book


def run(*args: str) -> subprocess.CompletedProcess[str]:
    return subprocess.run([sys.executable, *args], cwd=ROOT, capture_output=True,
                          text=True)


def book_block(start: str) -> str:
    return EXPECTED[start]


def test_list_functions_maps_pricing() -> None:
    r = run(str(SKILL / "scripts/list_functions.py"), "src/shop/pricing.py")
    assert r.returncode == 0
    entries = {e["name"]: e for e in json.loads(r.stdout)}
    assert list(entries) == ["apply_discount", "parse_quantity", "Cart.add", "Cart.total"]
    assert entries["parse_quantity"]["raises"] == ["ValueError"]
    assert entries["Cart.total"]["raises"] == []
    assert entries["apply_discount"]["signature"] == (
        "def apply_discount(price: float, percent: float) -> float")


def test_list_functions_explains_bad_input() -> None:
    r = run(str(SKILL / "scripts/list_functions.py"), "src/shop/missing.py")
    assert r.returncode == 1 and "does not exist" in r.stderr


def test_check_tests_passes_the_good_file() -> None:
    r = run(str(SKILL / "scripts/check_tests.py"), "tests/test_pricing.py")
    assert r.returncode == 0
    assert r.stdout == "OK: 9 tests in tests/test_pricing.py, no problems found\n"


def test_check_tests_output_on_the_bad_file_matches_the_book() -> None:
    r = run(str(SKILL / "scripts/check_tests.py"), "examples/test_bad.py")
    assert r.returncode == 1
    expected = book_block("examples/test_bad.py:")
    assert r.stdout == expected
    assert r.stdout.startswith("examples/test_bad.py: 6 problems in 3 tests")


def test_the_good_tests_pass() -> None:
    r = subprocess.run([sys.executable, "-m", "pytest", "-q", "-p", "no:cacheprovider",
                        "tests/test_pricing.py"], cwd=ROOT, capture_output=True, text=True)
    assert "17 passed" in r.stdout


def test_validate_skill_on_the_two_skills() -> None:
    r = run("validate_skill.py", ".claude/skills/writing-pytest-tests",
            ".claude/skills/python-house-style")
    assert r.returncode == 0
    assert r.stdout == "OK: writing-pytest-tests\nOK: python-house-style\n"


def test_validate_skill_on_the_bad_skill_matches_the_book() -> None:
    r = run("validate_skill.py", "examples/bad-skill/helper")
    assert r.returncode == 1
    expected = book_block("FAIL: helper")
    assert r.stdout == expected
    assert r.stdout.count("error:") == 4 and r.stdout.count("warning:") == 4


def test_every_pattern_in_patterns_md_runs(tmp_path: Path) -> None:
    text = (SKILL / "references/patterns.md").read_text()
    codes = re.findall(r"```python\n(.*?)```", text, re.S)
    assert len(codes) == 6
    for i, code in enumerate(codes, 1):
        (tmp_path / f"test_pattern_{i}.py").write_text(code)
    r = subprocess.run([sys.executable, "-m", "pytest", "-q", "-p", "no:cacheprovider",
                        str(tmp_path)], cwd=ROOT, capture_output=True, text=True,
                       env={"PYTHONPATH": str(ROOT / "src"), "PATH": "/usr/bin:/bin"})
    assert "6 passed" in r.stdout, r.stdout + r.stderr
