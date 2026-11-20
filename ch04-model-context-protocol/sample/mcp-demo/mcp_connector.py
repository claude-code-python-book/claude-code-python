"""Let the Claude API connect to a remote MCP server (the beta MCP connector)."""
import os

import anthropic

client = anthropic.Anthropic()

response = client.beta.messages.create(
    model="claude-sonnet-5-5",
    max_tokens=16000,
    messages=[{"role": "user", "content": "Who has spent the most?"}],
    mcp_servers=[{
        "type": "url",
        "url": "https://mcp.example.com/mcp",          # must be public HTTPS
        "name": "shop-db",
        "authorization_token": os.environ["SHOP_MCP_TOKEN"],
    }],
    tools=[{"type": "mcp_toolset", "mcp_server_name": "shop-db"}],
    betas=["mcp-client-2025-11-20"],
)
for block in response.content:
    if block.type == "mcp_tool_use":
        print(f"[{block.server_name}] {block.name}({block.input})")
    elif block.type == "text":
        print(block.text)
