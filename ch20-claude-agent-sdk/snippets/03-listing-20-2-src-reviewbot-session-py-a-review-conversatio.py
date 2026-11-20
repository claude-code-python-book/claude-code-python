async def ask(client: ClaudeSDKClient, prompt: str, deadline_s: float) -> str:
    """Send one turn; interrupt it if it runs past the deadline."""
    await client.query(prompt)
    watchdog = asyncio.create_task(_interrupt_after(client, deadline_s))
    answer = ""
    try:
        # Drain the whole response, even after an interrupt, so the
        # next turn starts from a clean stream.
        async for message in client.receive_response():
            if isinstance(message, ResultMessage):
                answer = message.result or f"[{message.subtype}]"
    finally:
        watchdog.cancel()
    return answer


async def _interrupt_after(client: ClaudeSDKClient, seconds: float) -> None:
    await asyncio.sleep(seconds)
    await client.interrupt()


async def review_chat(
    repo: Path, questions: list[str], *, deadline_s: float = 300,
    transport: Transport | None = None,
) -> list[str]:
    state = ReviewState(repo=repo, base="main")
    options = build_options(state, AuditLog())
    async with ClaudeSDKClient(options=options, transport=transport) as client:
        answers = [await ask(client, q, deadline_s) for q in questions]
    return answers
