# Acme Claude Code toolchain

Sample for Chapter 22 of *Claude Code for Python Developers*.

| Path | What it is |
| --- | --- |
| `.claude-plugin/marketplace.json` | The `acme-tools` plugin marketplace (this repository) |
| `plugins/acme-dev/` | The team plugin: skills, reviewer agent, guard hook, broker MCP server |
| `broker/` | The credential broker: a remote MCP server in front of the tracker |
| `managed/managed-settings.json` | Fleet policy for `/etc/claude-code/managed-settings.json` |
| `examples/repo-settings.json` | A product repository's `.claude/settings.json` |

Install for yourself:

```text
/plugin marketplace add acme/claude-toolchain
/plugin install acme-dev@acme-tools
```

Check before publishing:

```bash
claude plugin validate .                    # marketplace
claude plugin validate plugins/acme-dev     # plugin
cd broker && uv run pytest && uv run ruff check . && uv run mypy
```

Run the broker (configuration is read from the environment, see
`broker/src/acme_broker/__main__.py`):

```bash
cd broker && uv run python -m acme_broker
```

The tracker in `broker/tests/tracker_stub.py` and the identity provider in the
tests are stand-ins. Point `ACME_TRACKER_URL`, `ACME_IDP_ISSUER` and
`ACME_IDP_JWKS_URL` at your real systems.

## Try it locally (from the book)

`demo/demo_broker.py` starts a tracker stub (port 8771), the broker (8772) and
an identity-provider metadata stub (8773), registers tracker tokens for Alice
and Bob, and writes test ID tokens. `demo/scenario.py` then drives the broker as
three developers:

```bash
python demo/demo_broker.py /tmp/acme-demo &
python demo/scenario.py /tmp/acme-demo
PYTHONPATH=broker/src python -m acme_broker.report /tmp/acme-demo/audit.jsonl
```

The test keys and tokens in the demo are throwaway values for local use only.
