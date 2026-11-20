"""Test the server in memory: no subprocess, no port."""
import pytest
from mcp import Client
from mcp.types import TextContent, TextResourceContents

from hello_server import mcp

@pytest.fixture
def anyio_backend() -> str:
    return "asyncio"

@pytest.mark.anyio
async def test_tool_converts_names() -> None:
    async with Client(mcp) as client:
        result = await client.call_tool("to_snake_case", {"name": "OrderTotal"})
        assert result.content == [TextContent(type="text", text="order_total")]

@pytest.mark.anyio
async def test_resource_and_prompt() -> None:
    async with Client(mcp) as client:
        result = await client.read_resource("team://conventions")
        resource = result.contents[0]
        assert isinstance(resource, TextResourceContents)
        assert "pytest" in resource.text
        prompt = await client.get_prompt("review_module", {"path": "app.py"})
        message = prompt.messages[0].content
        assert isinstance(message, TextContent)
        assert "app.py" in message.text
