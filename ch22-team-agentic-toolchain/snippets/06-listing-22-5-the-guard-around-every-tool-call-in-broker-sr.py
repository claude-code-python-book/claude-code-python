    @asynccontextmanager
    async def guard(tool: str, scope: str, target: str) -> AsyncIterator[str]:
        """Check scope, fetch this user's tracker token, audit the outcome."""
        token = get_access_token()
        user = token.subject if token and token.subject else "anonymous"
        started, outcome = perf_counter(), "error"
        try:
            if token is None or scope not in token.scopes:
                outcome = "denied"
                raise ToolError(f"{tool} needs the {scope} scope")
            secret = cfg.vault.get(user, "tracker")
            if secret is None:
                outcome = "no_credential"
                raise ToolError("No tracker token registered for you; "
                                "run python -m acme_broker.register once")
            yield secret
            outcome = "ok"
        except ToolError:
            if outcome == "error":
                outcome = "upstream_refused"
            raise
        finally:
            cfg.audit.record(user, tool, target, outcome, started)
