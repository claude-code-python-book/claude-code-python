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
