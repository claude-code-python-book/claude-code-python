import json
from collections.abc import Callable
from pathlib import Path
from subprocess import CompletedProcess

RunHook = Callable[..., CompletedProcess[str]]


STOP = {"hook_event_name": "Stop", "stop_hook_active": False}


def write_test(project: Path, body: str) -> None:
    (project / "test_sample.py").write_text(f"def test_sample():\n    {body}\n")


def test_allows_stop_when_tests_pass(run_hook: RunHook, project: Path) -> None:
    write_test(project, "assert 1 + 1 == 2")
    result = run_hook("pytest_gate.py", **STOP)
    assert result.returncode == 0
    assert result.stdout == ""


def test_blocks_stop_when_tests_fail(run_hook: RunHook, project: Path) -> None:
    write_test(project, "assert 1 + 1 == 3")
    result = run_hook("pytest_gate.py", **STOP)
    assert result.returncode == 2
    assert "FAILED test_sample.py::test_sample" in result.stderr


def test_warns_instead_of_looping(run_hook: RunHook, project: Path) -> None:
    write_test(project, "assert 1 + 1 == 3")
    result = run_hook("pytest_gate.py", **{**STOP, "stop_hook_active": True})
    assert result.returncode == 0
    assert "still fail" in json.loads(result.stdout)["systemMessage"]


def test_skips_when_no_python_changed(run_hook: RunHook, project: Path) -> None:
    (project / "README.md").write_text("# Notes\n")
    result = run_hook("pytest_gate.py", **STOP)
    assert result.returncode == 0
    assert result.stdout == result.stderr == ""
