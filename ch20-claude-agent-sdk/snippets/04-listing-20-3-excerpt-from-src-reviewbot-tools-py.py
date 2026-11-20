def review_tools(state: ReviewState) -> list[SdkMcpTool[Any]]:
    read_only = ToolAnnotations(readOnlyHint=True)

    # changed_files: same shape, runs `git diff --name-only base...HEAD`

    @tool("file_diff", "Show the diff of one changed file.",
          {"path": str}, annotations=read_only)
    async def file_diff(args: dict[str, Any]) -> dict[str, Any]:
        rel = safe_path(state.repo, args["path"])
        if rel is None:
            return text(f"Refusing path {args['path']!r}", error=True)
        code, out = await git(state.repo, "diff", f"{state.base}...HEAD",
                              "--", rel)
        if code != 0:
            return text(f"git diff failed: {out.strip()}", error=True)
        if len(out) > MAX_DIFF_CHARS:
            out = out[:MAX_DIFF_CHARS] + "\n[diff truncated]"
        return text(out or "(no diff for this path)")

    @tool("record_finding", "Record one review finding.", {
        "type": "object",
        "properties": {
            "path": {"type": "string"},
            "line": {"type": "integer", "minimum": 1},
            "severity": {"type": "string", "enum": list(SEVERITIES)},
            "message": {"type": "string", "minLength": 1},
        },
        "required": ["path", "line", "severity", "message"],
    })
    async def record_finding(args: dict[str, Any]) -> dict[str, Any]:
        if safe_path(state.repo, args["path"]) is None:
            return text(f"Unknown path {args['path']!r}", error=True)
        state.findings.append(Finding(args["path"], args["line"],
                                      args["severity"], args["message"]))
        return text(f"Recorded finding #{len(state.findings)}")

    return [changed_files, file_diff, record_finding]


def build_review_server(state: ReviewState) -> McpSdkServerConfig:
    return create_sdk_mcp_server(name="review", version="1.0.0",
                                 tools=review_tools(state))
