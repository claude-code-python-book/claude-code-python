"""Let Claude use a local MCP server's tools through the Messages API.

Run it with:  uv run api_bridge.py "Which customer has spent the most?"
Needs:        uv add anthropic "mcp[cli]", ANTHROPIC_API_KEY, SHOP_DB_URL
"""
import asyncio
import os
import sys
from typing import Any

import anthropic
from mcp import Client, StdioServerParameters

MODEL = "claude-sonnet-5-5"
SERVER = StdioServerParameters(
    command=sys.executable,
    args=["pg_server.py"],
    env={"SHOP_DB_URL": os.environ["SHOP_DB_URL"]},  # pass only what it needs
)
claude = anthropic.AsyncAnthropic()

async def ask(question: str) -> str:
    async with Client(SERVER) as mcp_client:
        listed = await mcp_client.list_tools()
        tools = [{"name": t.name, "description": t.description or "",
                  "input_schema": t.input_schema} for t in listed.tools]
        messages: list[dict[str, Any]] = [{"role": "user", "content": question}]

        for _ in range(10):                                  # step limit
            reply = await claude.messages.create(
                model=MODEL, max_tokens=16000, tools=tools, messages=messages)
            messages.append({"role": "assistant", "content": reply.content})
            if reply.stop_reason != "tool_use":
                return "".join(b.text for b in reply.content if b.type == "text")

            results = []
            for block in reply.content:
                if block.type == "tool_use":                 # MCP does the work
                    out = await mcp_client.call_tool(block.name, block.input)
                    text = "".join(c.text for c in out.content if c.type == "text")
                    results.append({"type": "tool_result", "tool_use_id": block.id,
                                    "content": text, "is_error": out.is_error})
            messages.append({"role": "user", "content": results})
    raise RuntimeError("No answer within 10 steps")

if __name__ == "__main__":
    question = " ".join(sys.argv[1:]) or "Which customer has spent the most?"
    print(asyncio.run(ask(question)))
