    @mcp.tool()
    async def get_issue(key: str) -> dict[str, Any]:
        """Fetch one issue, such as PAY-142, with its description and status."""
        async with guard("get_issue", READ, key) as secret:
            return dict(await tracker("GET", f"/api/issues/{key}", secret))

    @mcp.tool()
    async def comment_on_issue(key: str, body: str) -> dict[str, Any]:
        """Add a comment to an issue, posted as you."""
        async with guard("comment_on_issue", WRITE, key) as secret:
            return dict(await tracker("POST", f"/api/issues/{key}/comments", secret,
                                      body={"body": body[:4000]}))
