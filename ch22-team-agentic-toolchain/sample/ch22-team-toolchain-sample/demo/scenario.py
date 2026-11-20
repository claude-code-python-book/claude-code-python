"""Drive the running demo broker as three developers, then report on the audit log."""

import asyncio
import sys
from pathlib import Path

import httpx2
from mcp.client import Client
from mcp.client.streamable_http import streamable_http_client

DEMO = Path(sys.argv[1])
URL = "http://127.0.0.1:8772/mcp"
PLAN = [  # (developer, tool, arguments, repeat)
    ("alice", "get_issue", {"key": "PAY-142"}, 6),
    ("alice", "search_issues", {"query": "refund"}, 3),
    ("alice", "comment_on_issue", {"key": "PAY-142", "body": "PR #88 opened"}, 1),
    ("bob", "get_issue", {"key": "WEB-7"}, 4),
    ("bob", "get_issue", {"key": "PAY-142"}, 1),          # no access upstream
    ("bob", "comment_on_issue", {"key": "WEB-7", "body": "done"}, 1),  # read scope
    ("carol", "get_issue", {"key": "WEB-7"}, 2),           # never registered
]


async def main() -> None:
    for who, tool, args, times in PLAN:
        token = (DEMO / f"{who}.jwt").read_text()
        async with httpx2.AsyncClient(headers={"Authorization": f"Bearer {token}"},
                                      timeout=30) as http:
            async with Client(streamable_http_client(URL, http_client=http)) as c:
                for _ in range(times):
                    await c.call_tool(tool, args)


asyncio.run(main())
