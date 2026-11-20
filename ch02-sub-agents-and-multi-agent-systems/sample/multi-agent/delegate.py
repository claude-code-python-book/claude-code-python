"""Dynamic orchestration: the orchestrator delegates through a tool."""
from typing import Any

from subagent_lib import run_subagent   # the function from Listing 2-1

SUBAGENTS = {
    "researcher": "You find facts about Python libraries. Be brief and "
                  "say when you are unsure.",
    "coder": "You write small, correct, type-hinted Python functions.",
    "reviewer": "You review Python code for bugs. List problems only.",
}

DELEGATE_TOOL: dict[str, Any] = {
    "name": "delegate",
    "description": "Hand a self-contained task to a specialist sub-agent. "
                   "The sub-agent sees only the task text you write, so "
                   "include everything it needs.",
    "input_schema": {
        "type": "object",
        "properties": {
            "agent": {"type": "string", "enum": list(SUBAGENTS)},
            "task": {"type": "string",
                     "description": "Objective, inputs and output format"},
        },
        "required": ["agent", "task"],
    },
}

def delegate(agent: str, task: str) -> str:
    """The tool's implementation: run the chosen sub-agent, return its answer."""
    return run_subagent(system=SUBAGENTS[agent], task=task)
