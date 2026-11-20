"""Record the CLI side of a live session so tests can replay it offline."""

from __future__ import annotations

import json
from collections.abc import AsyncIterator
from pathlib import Path
from typing import Any

from claude_agent_sdk import Transport


class RecordingTransport(Transport):
    """Wraps another transport and saves what the CLI sends, per turn."""

    def __init__(self, inner: Transport, path: Path) -> None:
        self.inner, self.path = inner, path
        self.turns: list[list[dict[str, Any]]] = []

    async def connect(self) -> None:
        await self.inner.connect()

    def is_ready(self) -> bool:
        return self.inner.is_ready()

    async def write(self, data: str) -> None:
        if json.loads(data).get("type") == "user":
            self.turns.append([])                  # a new turn starts
        await self.inner.write(data)

    def read_messages(self) -> AsyncIterator[dict[str, Any]]:
        return self._tee()

    async def _tee(self) -> AsyncIterator[dict[str, Any]]:
        async for frame in self.inner.read_messages():
            # Replies to the SDK's own requests (initialize, interrupt)
            # are regenerated on replay, so they are not recorded.
            if frame.get("type") != "control_response" and self.turns:
                self.turns[-1].append(frame)
            yield frame

    async def end_input(self) -> None:
        await self.inner.end_input()

    async def close(self) -> None:
        await self.inner.close()
        self.path.write_text(json.dumps(self.turns, indent=1), encoding="utf-8")


def load_turns(path: Path) -> list[list[dict[str, Any]]]:
    turns: list[list[dict[str, Any]]] = json.loads(path.read_text("utf-8"))
    return turns
