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
