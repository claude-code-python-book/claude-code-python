from collections.abc import Callable
from pathlib import Path
from subprocess import CompletedProcess

RunHook = Callable[..., CompletedProcess[str]]


MESSY = "import sys\nimport os\ndef area(w,h):\n    return w*h\n"
TIDY = "def area(w, h):\n    return w * h\n"


def edit_event(path: Path) -> dict[str, object]:
    return {
        "hook_event_name": "PostToolUse",
        "tool_name": "Edit",
        "tool_input": {"file_path": str(path)},
    }


def test_fixes_and_formats(run_hook: RunHook, project: Path) -> None:
    target = project / "geometry.py"
    target.write_text(MESSY)
    result = run_hook("format_python.py", **edit_event(target))
    assert result.returncode == 0, result.stderr
    assert target.read_text() == TIDY  # unused imports removed, formatted


def test_reports_unfixable_errors(run_hook: RunHook, project: Path) -> None:
    target = project / "broken.py"
    target.write_text("def total():\n    return subtotal * 2\n")
    result = run_hook("format_python.py", **edit_event(target))
    assert result.returncode == 2
    assert "F821" in result.stderr  # undefined name `subtotal`


def test_ignores_other_files(run_hook: RunHook, project: Path) -> None:
    notes = project / "notes.md"
    notes.write_text("import os\n")
    result = run_hook("format_python.py", **edit_event(notes))
    assert result.returncode == 0
    assert notes.read_text() == "import os\n"


def test_ignores_files_outside_project(run_hook: RunHook, tmp_path: Path) -> None:
    outside = tmp_path / "elsewhere.py"
    outside.write_text(MESSY)
    result = run_hook("format_python.py", **edit_event(outside))
    assert result.returncode == 0
    assert outside.read_text() == MESSY
