# acme-dev

Team workflows for Claude Code at Acme.

- `/acme-dev:implement <TICKET>`: read the ticket, plan, build, check, review
- `/acme-dev:pr <TICKET>`: draft PR, then link it on the ticket
- `acme-dev:reviewer`: read-only review subagent
- `acme-tracker` MCP server: the credential broker (sign in with `/mcp`)
- PreToolUse guard: blocks force-pushes, pushes to protected branches,
  reading `.env` files and `curl | sh`

Install:

```text
/plugin marketplace add acme/claude-toolchain
/plugin install acme-dev@acme-tools
```
