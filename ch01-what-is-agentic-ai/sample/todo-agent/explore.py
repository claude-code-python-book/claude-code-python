"""Steps 4 and 5: one round of the agent loop, done by hand.

Run it with:  uv run python explore.py ./src
"""
from typing import Any

from agent import (
    MAX_TOKENS,
    MODEL,
    SYSTEM_PROMPT,
    THINKING,
    TOOL_SCHEMAS,
    TOOLS,
    client,
)

def ask_claude(messages: list[dict[str, Any]]) -> Any:
    """Send the conversation so far, with the tool menu, to Claude."""
    return client.messages.create(
        model=MODEL,
        max_tokens=MAX_TOKENS,
        thinking=THINKING,
        system=SYSTEM_PROMPT,
        tools=TOOL_SCHEMAS,
        messages=messages,
    )

def show(response: Any) -> None:
    """Print what Claude sent back, block by block."""
    print("stop_reason:", response.stop_reason)
    for block in response.content:
        if block.type == "thinking":
            print("  thinking :", block.thinking.strip()[:80] or "(hidden)")
        elif block.type == "text":
            print("  text     :", block.text)
        elif block.type == "tool_use":
            print("  tool_use :", block.name, block.input, "id =", block.id)

# --- Step 4: make one call and look at the reply ---------------------
messages: list[dict[str, Any]] = [
    {"role": "user", "content": "Find every TODO or FIXME comment in "
                                "this project and summarize each one."}
]
response = ask_claude(messages)
show(response)

# --- Step 5: run the tools Claude asked for, send the results back ---
messages.append({"role": "assistant", "content": response.content})

results = []
for block in response.content:
    if block.type == "tool_use":
        output = TOOLS[block.name](**block.input)      # we do the work
        results.append({
            "type": "tool_result",
            "tool_use_id": block.id,                   # match the request
            "content": output,
        })
messages.append({"role": "user", "content": results})

print("\n--- second call ---")
show(ask_claude(messages))
