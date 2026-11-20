"""The smallest possible sub-agent: a fresh conversation with its own job."""
import sys
from pathlib import Path

import anthropic

MODEL = "claude-sonnet-5-5"  # check the Models page for current IDs
client = anthropic.Anthropic()

def run_subagent(system: str, task: str) -> str:
    """Run one focused agent in a brand-new context and return its answer."""
    response = client.messages.create(
        model=MODEL,
        max_tokens=16000,      # a ceiling; thinking counts toward it
        system=system,                                   # its own role
        messages=[{"role": "user", "content": task}],    # its own context
    )
    return "".join(b.text for b in response.content if b.type == "text")

# The main program (the "orchestrator") delegates one job to a sub-agent.
source = Path(sys.argv[1]).read_text(encoding="utf-8")
summary = run_subagent(
    system="You summarize Python modules for a code reviewer. "
           "Reply with at most five short bullet points.",
    task=f"Summarize what this module does:\n\n{source}",
)
print(summary)   # only the short summary comes back, not the whole file
