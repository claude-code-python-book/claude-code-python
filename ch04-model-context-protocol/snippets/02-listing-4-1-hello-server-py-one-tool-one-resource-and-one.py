"""A first MCP server: one tool, one resource and one prompt.

Run it with:  uv run hello_server.py      (stdio, for Claude Code)
"""
import re

from mcp.server import MCPServer

mcp = MCPServer("python-helper", instructions="Helpers for Python developers.")

@mcp.tool()
def to_snake_case(name: str) -> str:
    """Convert a name such as 'OrderTotal' or 'order-total' to snake_case."""
    words = re.sub(r"(?<=[a-z0-9])(?=[A-Z])", " ", name)
    return "_".join(re.split(r"[\s\-_]+", words.strip())).lower()

@mcp.resource("team://conventions")
def conventions() -> str:
    """The Python conventions this team follows."""
    return "Python 3.12+, type hints everywhere, pytest for tests, ruff for lint."

@mcp.prompt()
def review_module(path: str) -> str:
    """Ask for a focused review of one Python module."""
    return (f"Review {path}. List bugs first, then missing type hints, "
            "then unclear names. Quote the line number for each finding.")

if __name__ == "__main__":
    mcp.run()          # stdio is the default transport
