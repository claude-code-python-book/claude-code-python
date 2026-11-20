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
