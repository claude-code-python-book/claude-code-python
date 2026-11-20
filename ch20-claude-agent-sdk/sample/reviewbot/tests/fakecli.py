"""A scripted stand-in for the Claude Code CLI, for offline agent tests.

The SDK talks to the CLI over JSON lines. FakeCLI plays the CLI's side
from a script: one list of frames per user turn. Frames with type
"control_request" are sent to the SDK and FakeCLI waits for the SDK's
answer, so your real hooks, permission callback, and in-process MCP
tools run. Everything else is replayed as-is.

Transport is a low-level SDK interface that may change between releases;
keep this file small and pin the SDK version your tests run against.
"""

from __future__ import annotations

import asyncio
import json
from collections import deque
from typing import Any

from claude_agent_sdk import ProcessError, Transport

Frame = dict[str, Any]


class FakeCLI(Transport):
    def __init__(self, turns: list[list[Frame]], *, exit_code: int = 0) -> None:
        """exit_code != 0: the CLI exits with it after the last turn."""
        self.turns = deque(turns)
        self.exit_code = exit_code
        self.sent: list[Frame] = []            # every frame the SDK wrote
        self.answers: dict[str, Frame] = {}    # SDK replies, by request_id
        self.init_request: Frame | None = None
        self._out: asyncio.Queue[Frame | None] = asyncio.Queue()
        self._waiting: dict[str, asyncio.Event] = {}
        self._tasks: set[asyncio.Task[None]] = set()
        self._ready = False

    async def connect(self) -> None:
        self._ready = True

    def is_ready(self) -> bool:
        return self._ready

    async def write(self, data: str) -> None:
        msg = json.loads(data)
        self.sent.append(msg)
        if msg["type"] == "control_request":       # SDK -> CLI request
            if msg["request"]["subtype"] == "initialize":
                self.init_request = msg["request"]
            await self._out.put({"type": "control_response", "response": {
                "subtype": "success", "request_id": msg["request_id"],
                "response": {}}})
        elif msg["type"] == "control_response":    # SDK answers our request
            reply = msg["response"]
            self.answers[reply["request_id"]] = reply
            self._waiting.pop(reply["request_id"], asyncio.Event()).set()
        elif msg["type"] == "user":                # a new turn starts
            task = asyncio.create_task(self._play(self.turns.popleft()))
            self._tasks.add(task)
            task.add_done_callback(self._tasks.discard)

    async def _play(self, frames: list[Frame]) -> None:
        for frame in frames:
            if frame["type"] == "_pause":              # test-only: stall
                await asyncio.sleep(frame["seconds"])
            elif frame["type"] == "control_request":
                done = self._waiting[frame["request_id"]] = asyncio.Event()
                await self._out.put(frame)
                await asyncio.wait_for(done.wait(), timeout=5)
            else:
                await self._out.put(frame)
        if self.exit_code and not self.turns:      # the process dies
            await self._out.put(None)

    def read_messages(self):  # noqa: ANN201 - AsyncIterator per Transport
        return self._read()

    async def _read(self):  # noqa: ANN202
        while (frame := await self._out.get()) is not None:
            yield frame
        if self.exit_code:
            raise ProcessError("CLI exited", exit_code=self.exit_code)

    async def end_input(self) -> None:
        await self._finish()

    async def close(self) -> None:
        await self._finish()

    async def _finish(self) -> None:
        if self._ready:
            self._ready = False
            for task in list(self._tasks):
                await task
            await self._out.put(None)
