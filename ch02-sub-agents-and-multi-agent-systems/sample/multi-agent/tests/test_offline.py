"""Offline tests for Chapter 2: sub-agents, delegation and the pipeline, with a fake API."""
import asyncio
import json
import runpy
import sys
from pathlib import Path

import fake_anthropic as fa

HERE = Path(__file__).resolve().parent.parent


def test_subagent_basic_sends_a_fresh_context(monkeypatch, capsys, tmp_path):
    src = tmp_path / "m.py"
    src.write_text("def f(): pass\n")
    monkeypatch.setattr(sys, "argv", ["subagent_basic.py", str(src)])
    fa.CALLS.clear()
    fa.SCRIPT = lambda kwargs: fa.Response([fa.text("- defines f")])
    runpy.run_path(str(HERE / "subagent_basic.py"))
    call = fa.CALLS[0]
    assert len(call["messages"]) == 1 and "def f(): pass" in call["messages"][0]["content"]
    assert "five short bullet points" in call["system"]
    assert capsys.readouterr().out == "- defines f\n"


def test_delegate_runs_the_chosen_specialist():
    sys.path.insert(0, str(HERE))
    import delegate
    fa.CALLS.clear()
    fa.SCRIPT = lambda kwargs: fa.Response([fa.text("def add(a: int, b: int) -> int: ...")])
    assert delegate.delegate("coder", "write add").startswith("def add")
    assert fa.CALLS[0]["system"] == delegate.SUBAGENTS["coder"]
    assert delegate.DELEGATE_TOOL["input_schema"]["properties"]["agent"]["enum"] == [
        "researcher", "coder", "reviewer"]


def test_parallel_review_keeps_input_order(monkeypatch, capsys, tmp_path):
    src = tmp_path / "m.py"
    src.write_text("x = 1\n")
    monkeypatch.setattr(sys, "argv", ["parallel_review.py", str(src)])

    def script(kwargs):
        aspect = kwargs["system"].split(" for ")[1].split(" ")[0]
        return fa.Response([fa.text(f"no {aspect} issues")])
    fa.SCRIPT = script
    runpy.run_path(str(HERE / "parallel_review.py"))
    out = capsys.readouterr().out
    assert out.index("=== security ===") < out.index("=== performance ===") < out.index(
        "=== readability ===")
    assert "no performance issues" in out


def test_pipeline_plans_writes_reviews_and_fixes(capsys):
    sys.path.insert(0, str(HERE))
    import pipeline
    outline = [{"title": t, "brief": "b"} for t in ("What the GIL is",
                                                    "Threads and CPU-bound work",
                                                    "What to use instead")]
    rounds = {"review": 0}

    def script(kwargs):
        system = kwargs["system"]
        if system == pipeline.PLANNER:
            return fa.Response([fa.text("Here you go: " + json.dumps(outline))])
        if system == pipeline.WRITER:
            draft = "fixed" if "Reviewer feedback" in kwargs["messages"][0]["content"] else "draft"
            return fa.Response([fa.text(f"{draft}\n```python\nprint('hi')\n```")])
        # reviewer: first call uses the tool, then answers
        last = kwargs["messages"][-1]
        if last["role"] == "user" and isinstance(last["content"], str):
            return fa.Response([fa.tool_use("check_python", {"code": "print('hi'"}, "c1")],
                               "tool_use")
        rounds["review"] += 1
        verdict = ({"approved": False, "feedback": {"Threads and CPU-bound work": "more"}}
                   if rounds["review"] == 1 else {"approved": True})
        return fa.Response([fa.text(json.dumps(verdict))])
    fa.SCRIPT = script
    article = asyncio.run(pipeline.run_pipeline("How Python's GIL affects threads"))
    assert article.startswith("# How Python's GIL affects threads")
    assert article.index("## What the GIL is") < article.index("## What to use instead")
    assert "fixed" in article.split("## Threads and CPU-bound work")[1].split("##")[0]
    out = capsys.readouterr().out
    assert "reviewer (round 2)" in out and "approved: True" in out
    assert pipeline.check_python("print('hi'") .startswith("SyntaxError on line 1")


def test_parse_json_skips_prose_and_wrong_types():
    sys.path.insert(0, str(HERE))
    import pipeline
    assert pipeline.parse_json('ok {"a": 1} then [1, 2]', list) == [1, 2]
