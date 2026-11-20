"""A minimal agent that finds TODO comments in a Python project.

Run it with:  uv run python agent.py ./src
Needs:        uv add anthropic   and   ANTHROPIC_API_KEY set
"""
import sys
import textwrap
from collections.abc import Callable
from pathlib import Path
from typing import Any

import anthropic

MODEL = "claude-sonnet-5-5"   # check the Models page for current IDs
MAX_TOKENS = 16000            # a ceiling, not a cost: thinking counts too
MAX_STEPS = 10                # hard stop: never let the loop run forever
THINKING = {"type": "adaptive", "display": "summarized"}  # show reasoning

client = anthropic.Anthropic()   # reads ANTHROPIC_API_KEY from the env
ROOT = Path(sys.argv[1] if len(sys.argv) > 1 else ".").resolve()
SKIP_DIRS = {".venv", "venv", ".git", "__pycache__", "node_modules"}

# --- Tools: ordinary Python functions --------------------------------
def _safe_path(relative: str) -> Path:
    """Resolve a path and refuse anything outside the project root."""
    path = (ROOT / relative).resolve()
    if not path.is_relative_to(ROOT):
        raise ValueError(f"{relative} is outside the project")
    return path

def list_python_files(directory: str = ".") -> str:
    """List .py files under a directory, relative to the project root."""
    base = _safe_path(directory)
    files = sorted(
        p.relative_to(ROOT).as_posix()
        for p in base.rglob("*.py")
        if not SKIP_DIRS.intersection(p.relative_to(ROOT).parts)
    )
    return "\n".join(files) or "(no Python files found)"

def read_file(path: str) -> str:
    """Return a file's contents with line numbers."""
    lines = _safe_path(path).read_text(encoding="utf-8").splitlines()
    numbered = "\n".join(f"{n:>4}: {line}" for n, line in enumerate(lines, 1))
    return numbered or "(empty file)"

TOOLS: dict[str, Callable[..., str]] = {
    "list_python_files": list_python_files,
    "read_file": read_file,
}

TOOL_SCHEMAS: list[dict[str, Any]] = [
    {
        "name": "list_python_files",
        "description": "List all .py files under a directory of the project.",
        "input_schema": {
            "type": "object",
            "properties": {
                "directory": {"type": "string",
                              "description": "Relative path, e.g. 'src'"},
            },
            "required": [],
        },
    },
    {
        "name": "read_file",
        "description": "Read one file. Lines are prefixed with numbers.",
        "input_schema": {
            "type": "object",
            "properties": {"path": {"type": "string"}},
            "required": ["path"],
        },
    },
]

SYSTEM_PROMPT = (
    "You are a code-auditing agent. Use the tools to inspect the project. "
    "Only report what you actually read in a file. When you are done, "
    "answer with a short Markdown report and stop calling tools."
)

# --- The agent loop ---------------------------------------------------
def text_of(response: Any) -> str:
    """Join the text blocks of a response into one string."""
    return "".join(b.text for b in response.content if b.type == "text")

def show_reasoning(response: Any) -> None:
    """Print Claude's thinking summaries and any text, shortened."""
    for block in response.content:
        if block.type == "thinking" and block.thinking.strip():
            print("[thinking]", textwrap.shorten(block.thinking, 150))
        elif block.type == "text" and block.text.strip():
            print("[claude]  ", textwrap.shorten(block.text, 150))

def run_tool(name: str, args: dict[str, Any], tool_use_id: str) -> dict:
    """Execute one tool call and wrap the outcome as a tool_result block."""
    try:
        output = TOOLS[name](**args)
        return {"type": "tool_result", "tool_use_id": tool_use_id,
                "content": output}
    except Exception as exc:  # report errors back to the model
        return {"type": "tool_result", "tool_use_id": tool_use_id,
                "content": f"{type(exc).__name__}: {exc}", "is_error": True}

def run_agent(goal: str) -> str:
    # 1. Memory starts with the goal.
    messages: list[dict[str, Any]] = [{"role": "user", "content": goal}]

    for step in range(1, MAX_STEPS + 1):
        # 2. Think: send everything so far and let Claude decide.
        response = client.messages.create(
            model=MODEL,
            max_tokens=MAX_TOKENS,
            thinking=THINKING,
            system=SYSTEM_PROMPT,
            tools=TOOL_SCHEMAS,
            messages=messages,
        )
        # 3. Remember: Claude's reply goes into the history, unchanged.
        messages.append({"role": "assistant", "content": response.content})

        # 4. Check: is Claude finished, cut off, or asking for tools?
        if response.stop_reason == "max_tokens":
            raise RuntimeError("Claude's reply was cut off; raise MAX_TOKENS")
        if response.stop_reason != "tool_use":       # normally "end_turn"
            return text_of(response)
        show_reasoning(response)

        # 5. Act: run every tool Claude asked for.
        results = []
        for block in response.content:
            if block.type == "tool_use":
                print(f"[step {step}]  {block.name}({block.input})")
                results.append(run_tool(block.name, block.input, block.id))

        # 6. Observe: all results go back together in one user message.
        messages.append({"role": "user", "content": results})

    raise RuntimeError(f"Agent did not finish within {MAX_STEPS} steps")

if __name__ == "__main__":
    report = run_agent(
        "Find every TODO or FIXME comment in this project. Group them by "
        "file, include the line number, and add a one-line summary of "
        "what each one asks for."
    )
    print(report)
