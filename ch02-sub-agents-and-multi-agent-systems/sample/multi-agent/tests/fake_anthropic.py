"""A tiny offline stand-in for the `anthropic` package, for these tests only.

It is installed as `anthropic` in sys.modules by conftest.py, so the book's
code runs unchanged without an API key or network. Each test sets `SCRIPT`,
a function that receives the request's keyword arguments and returns a
`Response`. Every request is also recorded in `CALLS`.
"""
from types import SimpleNamespace
from typing import Any, Callable

CALLS: list[dict[str, Any]] = []
SCRIPT: Callable[[dict[str, Any]], "Response"] | None = None


def text(t: str) -> SimpleNamespace:
    return SimpleNamespace(type="text", text=t)


def thinking(t: str) -> SimpleNamespace:
    return SimpleNamespace(type="thinking", thinking=t)


def tool_use(name: str, args: dict[str, Any], id: str) -> SimpleNamespace:
    return SimpleNamespace(type="tool_use", name=name, input=args, id=id)


def Response(content: list[SimpleNamespace], stop_reason: str = "end_turn",
             input_tokens: int = 100, output_tokens: int = 20) -> SimpleNamespace:
    return SimpleNamespace(content=content, stop_reason=stop_reason,
                           usage=SimpleNamespace(input_tokens=input_tokens,
                                                 output_tokens=output_tokens))


def _create(**kwargs: Any) -> SimpleNamespace:
    # copy the message list: the caller appends to it after the call returns
    CALLS.append({**kwargs, "messages": list(kwargs.get("messages", []))})
    assert SCRIPT is not None, "test did not set fake_anthropic.SCRIPT"
    return SCRIPT(kwargs)


class _Messages:
    def create(self, **kwargs: Any) -> SimpleNamespace:
        return _create(**kwargs)


class _AsyncMessages:
    async def create(self, **kwargs: Any) -> SimpleNamespace:
        return _create(**kwargs)


class Anthropic:
    def __init__(self, **_: Any) -> None:
        self.messages = _Messages()
        self.beta = SimpleNamespace(messages=_Messages())


class AsyncAnthropic:
    def __init__(self, **_: Any) -> None:
        self.messages = _AsyncMessages()
