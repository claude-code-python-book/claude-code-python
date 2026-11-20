@pytest.mark.anyio
async def test_review_session(repo: Path) -> None:
    cli = FakeCLI([review_turn()])
    report = await run_review(repo, "main", transport=cli)

    # The in-process tools ran for real against the git fixture.
    assert mcp_text(cli, "r-changed") == "stats.py"
    assert "-    if not xs:" in mcp_text(cli, "r-diff")
    assert [f.severity for f in report.findings] == ["major"]

    # The hook blocked the secret; the policy blocked the outside path.
    guard = cli.answers["r-guard"]["response"]["hookSpecificOutput"]
    assert guard["permissionDecision"] == "deny"
    assert cli.answers["r-perm"]["response"]["behavior"] == "deny"

    # Options reached the CLI: hooks registered, prompt sent.
    assert cli.init_request is not None
    assert cli.init_request["hooks"]["PreToolUse"] == [
        {"matcher": "Read|Grep|Glob", "hookCallbackIds": ["hook_0"]}]
    prompt = next(m for m in cli.sent if m["type"] == "user")
    assert "against main" in prompt["message"]["content"]

    assert report.subtype == "success"
    assert report.cost_usd == pytest.approx(0.0123)
    assert [r["tool"] for r in report.audit] == ["mcp__review__changed_files"]
