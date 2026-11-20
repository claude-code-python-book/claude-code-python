"""run_subagent from Listing 2-1, as an importable module (used by delegate.py)."""
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

