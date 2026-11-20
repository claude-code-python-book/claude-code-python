"""Builders for the JSON frames the CLI sends, used to script FakeCLI."""

from __future__ import annotations

import itertools
from typing import Any

from mcp.types import LATEST_PROTOCOL_VERSION

SESSION = "sess-0001"
_ids = itertools.count(1)


def _rid() -> str:
    return f"cli_req_{next(_ids)}"


def init_frame(tools: list[str]) -> dict[str, Any]:
    return {"type": "system", "subtype": "init", "session_id": SESSION,
            "tools": tools, "mcp_servers": [{"name": "review",
                                             "status": "connected"}]}


def assistant(content: list[dict[str, Any]], msg_id: str,
              usage: dict[str, int] | None = None) -> dict[str, Any]:
    return {"type": "assistant", "session_id": SESSION,
            "parent_tool_use_id": None,
            "message": {"id": msg_id, "type": "message", "role": "assistant",
                        "model": "claude-sonnet-5-5", "content": content,
                        "stop_reason": "tool_use",
                        "usage": usage or {"input_tokens": 1000,
                                           "output_tokens": 1}}}


def text_block(text: str) -> dict[str, Any]:
    return {"type": "text", "text": text}


def tool_use(tool_id: str, name: str, args: dict[str, Any]) -> dict[str, Any]:
    return {"type": "tool_use", "id": tool_id, "name": name, "input": args}


def tool_result(tool_id: str, text: str, is_error: bool = False) -> dict[str, Any]:
    return {"type": "user", "session_id": SESSION, "parent_tool_use_id": None,
            "message": {"role": "user", "content": [
                {"type": "tool_result", "tool_use_id": tool_id,
                 "content": text, "is_error": is_error}]}}


def control(request: dict[str, Any], request_id: str | None = None) -> dict[str, Any]:
    return {"type": "control_request", "request_id": request_id or _rid(),
            "request": request}


def hook(callback_id: str, event: str, tool: str, args: dict[str, Any],
         tool_id: str, request_id: str | None = None) -> dict[str, Any]:
    return control({"subtype": "hook_callback", "callback_id": callback_id,
                    "tool_use_id": tool_id,
                    "input": {"hook_event_name": event, "session_id": SESSION,
                              "cwd": "/repo", "tool_name": tool,
                              "tool_input": args}}, request_id)


def permission(tool: str, args: dict[str, Any], tool_id: str,
               request_id: str | None = None) -> dict[str, Any]:
    return control({"subtype": "can_use_tool", "tool_name": tool,
                    "input": args, "tool_use_id": tool_id,
                    "permission_suggestions": []}, request_id)


def mcp(server: str, message: dict[str, Any],
        request_id: str | None = None) -> dict[str, Any]:
    return control({"subtype": "mcp_message", "server_name": server,
                    "message": message}, request_id)


def mcp_handshake(server: str) -> list[dict[str, Any]]:
    return [
        mcp(server, {"jsonrpc": "2.0", "id": 0, "method": "initialize",
                     "params": {"protocolVersion": LATEST_PROTOCOL_VERSION,
                                "capabilities": {},
                                "clientInfo": {"name": "fake-cli",
                                               "version": "0"}}}),
        mcp(server, {"jsonrpc": "2.0",
                     "method": "notifications/initialized"}),
    ]


def mcp_call(server: str, rpc_id: int, tool: str, args: dict[str, Any],
             request_id: str | None = None) -> dict[str, Any]:
    return mcp(server, {"jsonrpc": "2.0", "id": rpc_id, "method": "tools/call",
                        "params": {"name": tool, "arguments": args}},
               request_id)


def result(text: str, *, subtype: str = "success", turns: int = 1,
           cost: float = 0.0123, is_error: bool = False) -> dict[str, Any]:
    return {"type": "result", "subtype": subtype, "is_error": is_error,
            "duration_ms": 4200, "duration_api_ms": 3900,
            "num_turns": turns, "session_id": SESSION, "result": text,
            "total_cost_usd": cost,
            "usage": {"input_tokens": 5200, "output_tokens": 640,
                      "cache_read_input_tokens": 3100},
            "modelUsage": {"claude-sonnet-5-5": {
                "inputTokens": 5200, "outputTokens": 640,
                "costUSD": cost}}}
