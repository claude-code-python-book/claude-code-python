SECRET_GLOBS = (".env", ".env.*", "*.pem", "*.key", "id_rsa*")


def looks_secret(value: str) -> bool:
    name = PurePosixPath(value).name
    return any(fnmatch(name, pattern) for pattern in SECRET_GLOBS)


async def block_secrets(
    input_data: HookInput, tool_use_id: str | None, context: HookContext
) -> HookJSONOutput:
    data = cast(dict[str, Any], input_data)
    values = [v for v in data["tool_input"].values() if isinstance(v, str)]
    if any(looks_secret(v) for v in values):
        return {
            "hookSpecificOutput": {
                "hookEventName": "PreToolUse",
                "permissionDecision": "deny",
                "permissionDecisionReason": "Secret files are off limits.",
            }
        }
    return {}


def review_hooks(audit: AuditLog) -> dict[HookEvent, list[HookMatcher]]:
    return {
        "PreToolUse": [HookMatcher(matcher="Read|Grep|Glob", hooks=[block_secrets])],
        "PostToolUse": [HookMatcher(hooks=[audit])],
    }
