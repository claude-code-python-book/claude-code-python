"""Keep the CLAUDE.md files short and pointing at things that exist."""

import re
import tomllib
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
MAX_LINES = 80
FILES = sorted(p for p in ROOT.rglob("CLAUDE.md") if ".venv" not in p.parts)

FENCE = re.compile(r"^```.*?^```", re.MULTILINE | re.DOTALL)
CODE_SPAN = re.compile(r"`([^`\n]+)`")
IMPORT = re.compile(r"(?<!\S)@([\w./~-]+)")


def test_claude_md_files_stay_short() -> None:
    for path in FILES:
        count = len(path.read_text().splitlines())
        assert count <= MAX_LINES, f"{path.relative_to(ROOT)}: {count} lines"


def test_paths_in_code_spans_exist() -> None:
    for path in FILES:
        for span in CODE_SPAN.findall(path.read_text()):
            for token in span.split():
                if token.startswith("/"):
                    continue  # a slash command such as /code-review
                token = token.split("::")[0].lstrip("@")
                if "/" in token and not re.search(r"[*<>{}$:]", token):
                    assert (ROOT / token).exists(), f"{path.name}: no {token}"


def test_imports_resolve() -> None:
    for path in FILES:
        prose = CODE_SPAN.sub("", FENCE.sub("", path.read_text()))
        for target in IMPORT.findall(prose):
            resolved = Path(target).expanduser()
            if not resolved.is_absolute():
                resolved = path.parent / resolved
            assert resolved.exists(), f"{path.name} imports missing @{target}"


def test_uv_run_tools_are_dev_dependencies() -> None:
    pyproject = tomllib.loads((ROOT / "pyproject.toml").read_text())
    dev = pyproject["dependency-groups"]["dev"]
    declared = {re.split(r"[<>=!~;\[ ]", spec)[0] for spec in dev}
    own_scripts = set(pyproject["project"].get("scripts", {}))
    used = set(re.findall(r"uv run (\w[\w-]*)", (ROOT / "CLAUDE.md").read_text()))
    missing = used - declared - own_scripts - {"python"}
    assert not missing, f"CLAUDE.md runs tools not in the dev group: {missing}"
