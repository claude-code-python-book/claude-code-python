"""Offline tests for Chapter 1: the tools, the loop and explore.py, with a fake API."""
import importlib
import runpy
import sys
from pathlib import Path

import fake_anthropic as fa
import pytest

HERE = Path(__file__).resolve().parent.parent
DEMO = HERE / "demo_project"


@pytest.fixture
def agent(monkeypatch):
    venv_file = DEMO / ".venv" / "lib" / "ignored.py"   # must never be listed
    venv_file.parent.mkdir(parents=True, exist_ok=True)
    venv_file.write_text("# TODO: hidden in .venv\n")
    monkeypatch.setattr(sys, "argv", ["agent.py", str(DEMO)])
    sys.modules.pop("agent", None)
    fa.CALLS.clear()
    return importlib.import_module("agent")


def test_list_python_files_skips_venv(agent):
    assert agent.list_python_files(".").splitlines() == [
        "billing/tax.py", "orders/service.py"]


def test_read_file_numbers_lines(agent):
    assert agent.read_file("billing/tax.py").startswith("   1: RATE = 0.2")


def test_paths_outside_the_project_are_refused(agent):
    with pytest.raises(ValueError, match="outside the project"):
        agent.read_file("../agent.py")


def test_agent_loop_runs_tools_and_returns_the_report(agent, capsys):
    replies = iter([
        fa.Response([fa.thinking("I'll list the files."),
                     fa.tool_use("list_python_files", {"directory": "."}, "t1")],
                    "tool_use"),
        fa.Response([fa.tool_use("read_file", {"path": "orders/service.py"}, "t2"),
                     fa.tool_use("read_file", {"path": "billing/tax.py"}, "t3")],
                    "tool_use"),
        fa.Response([fa.text("## TODO report\n- orders/service.py line 5")]),
    ])
    fa.SCRIPT = lambda kwargs: next(replies)
    report = agent.run_agent("Find every TODO")
    assert report.startswith("## TODO report")
    # every call sends the tools, the system prompt and adaptive thinking
    assert all(c["tools"] == agent.TOOL_SCHEMAS and c["thinking"] == agent.THINKING
               for c in fa.CALLS)
    # the second call carries the tool result, matched by tool_use_id
    results = fa.CALLS[1]["messages"][-1]["content"]
    assert results[0]["tool_use_id"] == "t1" and "orders/service.py" in results[0]["content"]
    # both read_file results come back together in one user message
    third = fa.CALLS[2]["messages"][-1]["content"]
    assert [r["tool_use_id"] for r in third] == ["t2", "t3"]
    out = capsys.readouterr().out
    assert "[step 1]  list_python_files({'directory': '.'})" in out
    assert "[thinking] I'll list the files." in out


def test_tool_errors_go_back_to_the_model(agent):
    result = agent.run_tool("read_file", {"path": "../x"}, "t9")
    assert result["is_error"] is True and "outside the project" in result["content"]


def test_step_limit_stops_a_runaway_loop(agent):
    fa.SCRIPT = lambda kwargs: fa.Response(
        [fa.tool_use("list_python_files", {}, "t")], "tool_use")
    with pytest.raises(RuntimeError, match="within 10 steps"):
        agent.run_agent("loop forever")


def test_a_cut_off_reply_is_an_error(agent):
    fa.SCRIPT = lambda kwargs: fa.Response([fa.text("...")], "max_tokens")
    with pytest.raises(RuntimeError, match="cut off"):
        agent.run_agent("x")


def test_explore_prints_one_round(monkeypatch, capsys):
    monkeypatch.setattr(sys, "argv", ["explore.py", str(DEMO)])
    for name in ("agent", "explore"):
        sys.modules.pop(name, None)
    replies = iter([
        fa.Response([fa.thinking("I'll start by listing the Python files."),
                     fa.tool_use("list_python_files", {"directory": "."}, "toolu_1")],
                    "tool_use"),
        fa.Response([fa.tool_use("read_file", {"path": "orders/service.py"}, "toolu_2")],
                    "tool_use"),
    ])
    fa.SCRIPT = lambda kwargs: next(replies)
    runpy.run_path(str(HERE / "explore.py"), run_name="__main__")
    out = capsys.readouterr().out
    assert "stop_reason: tool_use" in out
    assert "  tool_use : list_python_files {'directory': '.'} id = toolu_1" in out
    assert "--- second call ---" in out


def test_chatbot_prints_only_text(capsys):
    fa.SCRIPT = lambda kwargs: fa.Response([fa.thinking("hm"), fa.text("A generator...")])
    runpy.run_path(str(HERE / "chatbot.py"))
    assert capsys.readouterr().out == "A generator...\n"


def test_tool_schema_matches_the_book(capsys):
    runpy.run_path(str(HERE / "tool_schema.py"))
    out = capsys.readouterr().out
    assert "'required': ['order_id']" in out and "'include_items': {'type': 'boolean'}" in out
