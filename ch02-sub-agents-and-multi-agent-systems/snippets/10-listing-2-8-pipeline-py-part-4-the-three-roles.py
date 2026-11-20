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
