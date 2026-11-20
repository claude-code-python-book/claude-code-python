"""A multi-agent content pipeline: plan -> write in parallel -> review -> fix.

Run it with:  uv run python pipeline.py "How Python's GIL affects threads"
Needs:        uv add anthropic   and   ANTHROPIC_API_KEY set
"""
import asyncio
import json
import sys
import time
from collections.abc import Callable
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

import anthropic

MODEL = "claude-sonnet-5-5"   # check the Models page for current IDs
MAX_TOKENS = 16000            # a ceiling per reply; thinking counts toward it
MAX_REVISIONS = 1             # how many times the writers may fix their work
client = anthropic.AsyncAnthropic()

# --- Shared state: one place that every step reads and writes ----------
@dataclass
class PipelineState:
    topic: str
    outline: list[dict[str, str]] = field(default_factory=list)
    sections: dict[str, str] = field(default_factory=dict)
    review: dict[str, Any] = field(default_factory=dict)
    log: list[str] = field(default_factory=list)
    tokens: int = 0

# --- A tool for the reviewer: check Python syntax without running it ---
def check_python(code: str) -> str:
    """Compile a snippet to find syntax errors. The code is never run."""
    try:
        compile(code, "<snippet>", "exec")
        return "OK: no syntax errors"
    except SyntaxError as exc:
        return f"SyntaxError on line {exc.lineno}: {exc.msg}"

CHECK_PYTHON_SCHEMA = {
    "name": "check_python",
    "description": "Check one Python code block for syntax errors. "
                   "Pass only the code, without the ``` fences.",
    "input_schema": {
        "type": "object",
        "properties": {"code": {"type": "string"}},
        "required": ["code"],
    },
}
Tools = dict[str, tuple[Callable[..., str], dict[str, Any]]]

# --- One reusable sub-agent: Chapter 1's loop, made async --------------
async def run_subagent(state: PipelineState, name: str, system: str,
                       task: str, tools: Tools | None = None,
                       max_steps: int = 8) -> str:
    """Run one agent in its own fresh context and return its final text."""
    tools = tools or {}
    messages: list[dict[str, Any]] = [{"role": "user", "content": task}]
    started = time.perf_counter()

    for _ in range(max_steps):
        request: dict[str, Any] = {"model": MODEL, "max_tokens": MAX_TOKENS,
                                   "system": system, "messages": messages}
        if tools:
            request["tools"] = [schema for _, schema in tools.values()]
        response = await client.messages.create(**request)
        state.tokens += response.usage.input_tokens + response.usage.output_tokens
        messages.append({"role": "assistant", "content": response.content})

        if response.stop_reason != "tool_use":          # this agent is done
            state.log.append(f"{name:<28} {time.perf_counter() - started:5.1f}s")
            return "".join(b.text for b in response.content if b.type == "text")

        results = []
        for block in response.content:
            if block.type == "tool_use":
                function, _ = tools[block.name]
                try:
                    output, failed = function(**block.input), False
                except Exception as exc:
                    output, failed = f"{type(exc).__name__}: {exc}", True
                results.append({"type": "tool_result", "tool_use_id": block.id,
                                "content": output, "is_error": failed})
        messages.append({"role": "user", "content": results})

    raise RuntimeError(f"{name} did not finish within {max_steps} steps")

def parse_json(text: str, expected: type) -> Any:
    """Return the first JSON list or dict (as expected) found in a reply."""
    decoder = json.JSONDecoder()
    for start, char in enumerate(text):
        if char in "[{":
            try:
                value, _ = decoder.raw_decode(text, start)
            except json.JSONDecodeError:
                continue
            if isinstance(value, expected):
                return value
    raise ValueError(f"No JSON {expected.__name__} in reply: {text[:80]!r}")

# --- The three specialist roles ----------------------------------------
PLANNER = ("You plan short technical articles for Python developers. "
           "Reply with JSON only, no other text.")
WRITER = ("You write ONE section of a technical article for Python "
          "developers, in plain, friendly English (150-250 words). "
          "Include exactly one short Python example in a ```python block. "
          "Do not repeat the section title. Write only your section.")
REVIEWER = ("You are a strict technical reviewer. Use the check_python tool "
            "on every Python code block before you decide. Reply with JSON "
            'only: {"approved": true or false, "feedback": {"<exact section '
            'title>": "what to fix"}}. Leave out sections that are fine.')

async def write_section(state: PipelineState, item: dict[str, str],
                        feedback: str = "") -> None:
    """Writer sub-agent: sees only its own section, never the others."""
    task = (f"Article topic: {state.topic}\n"
            f"Your section: {item['title']}\n"
            f"It must cover: {item['brief']}")
    if feedback:
        task += (f"\n\nYour previous draft:\n{state.sections[item['title']]}"
                 f"\n\nReviewer feedback to fix:\n{feedback}")
    text = await run_subagent(state, f"writer: {item['title'][:20]}",
                              WRITER, task)
    state.sections[item["title"]] = text.strip()

def assemble(state: PipelineState) -> str:
    """Join the sections in the planned order."""
    parts = [f"# {state.topic}"]
    for item in state.outline:
        parts.append(f"## {item['title']}\n\n{state.sections.get(item['title'], '')}")
    return "\n\n".join(parts) + "\n"

# --- The orchestrator: plain Python that decides the order -------------
async def run_pipeline(topic: str) -> str:
    state = PipelineState(topic=topic)

    # Step 1 - plan: one agent turns the topic into an outline.
    plan = await run_subagent(
        state, "planner", PLANNER,
        f"Plan an article on: {topic}\nReturn a JSON list of exactly three "
        'objects, each with "title" and "brief" (one sentence on what the '
        "section must cover).")
    state.outline = parse_json(plan, list)

    # Step 2 - write: one writer per section, all at the same time.
    await asyncio.gather(*(write_section(state, item) for item in state.outline))

    # Step 3 - review, then fix and review again (at most MAX_REVISIONS times).
    reviewer_tools: Tools = {"check_python": (check_python, CHECK_PYTHON_SCHEMA)}
    for attempt in range(MAX_REVISIONS + 1):
        reply = await run_subagent(state, f"reviewer (round {attempt + 1})",
                                   REVIEWER, f"Review this article:\n\n{assemble(state)}",
                                   tools=reviewer_tools)
        state.review = parse_json(reply, dict)
        if state.review.get("approved") or attempt == MAX_REVISIONS:
            break
        fixes = state.review.get("feedback", {})
        await asyncio.gather(*(write_section(state, item, fixes[item["title"]])
                               for item in state.outline if item["title"] in fixes))

    # Observability: what ran, how long it took, and what it cost.
    for line in state.log:
        print("  ", line)
    print(f"   approved: {state.review.get('approved')}   "
          f"total tokens: {state.tokens:,}")
    return assemble(state)

if __name__ == "__main__":
    topic = " ".join(sys.argv[1:]) or "How Python's GIL affects threads"
    article = asyncio.run(run_pipeline(topic))
    Path("article.md").write_text(article, encoding="utf-8")
    print("Saved article.md")
