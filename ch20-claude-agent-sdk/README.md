# Chapter 20 — Building Your Own Agents with the Claude Agent SDK for Python

Code and snippets exactly as they appear in the chapter, in reading order.

> **Reference material, not production-ready code.** Verify every snippet against the official documentation for the tools involved, and test it in your own environment, before you use it in your codebase. See the notice in the [repository README](../README.md).

## Sample project

`sample/` is the tested sample project for this chapter (`reviewbot`). See the README inside it for how to run it.

## Snippets

| File | What it is | Type | Section |
| --- | --- | --- | --- |
| [`01-output.txt`](snippets/01-output.txt) | Output | text | 2. Installing claude-agent-sdk and Authenticating |
| [`02-listing-20-1-src-reviewbot-oneshot-py-asking-questions-abo.py`](snippets/02-listing-20-1-src-reviewbot-oneshot-py-asking-questions-abo.py) | Listing 20-1: src/reviewbot/oneshot.py, asking questions about a repository | python | 3. One-Shot Agents with query() |
| [`03-listing-20-2-src-reviewbot-session-py-a-review-conversatio.py`](snippets/03-listing-20-2-src-reviewbot-session-py-a-review-conversatio.py) | Listing 20-2: src/reviewbot/session.py, a review conversation with a deadline per turn | python | 4. Interactive Sessions with ClaudeSDKClient |
| [`04-listing-20-3-excerpt-from-src-reviewbot-tools-py.py`](snippets/04-listing-20-3-excerpt-from-src-reviewbot-tools-py.py) | Listing 20-3: Excerpt from src/reviewbot/tools.py | python | 5. Custom Tools as Python Functions (In-Process MCP Servers) |
| [`05-output.txt`](snippets/05-output.txt) | Output | text | 5. Custom Tools as Python Functions (In-Process MCP Servers) |
| [`06-listing-20-4-src-reviewbot-policy-py.py`](snippets/06-listing-20-4-src-reviewbot-policy-py.py) | Listing 20-4: src/reviewbot/policy.py | python | 6. Permissions and Allowed Tools |
| [`07-output.txt`](snippets/07-output.txt) | Output | text | 6. Permissions and Allowed Tools |
| [`08-listing-20-5-excerpt-from-src-reviewbot-hooks-py.py`](snippets/08-listing-20-5-excerpt-from-src-reviewbot-hooks-py.py) | Listing 20-5: Excerpt from src/reviewbot/hooks.py | python | 7. Hooks as Python Callbacks |
| [`09-listing-20-6-excerpt-from-src-reviewbot-agent-py.py`](snippets/09-listing-20-6-excerpt-from-src-reviewbot-agent-py.py) | Listing 20-6: Excerpt from src/reviewbot/agent.py | python | 8. Worked Example: A Code-Review Bot for Your Repository |
| [`10-output.txt`](snippets/10-output.txt) | Output | text | 8. Worked Example: A Code-Review Bot for Your Repository |
| [`11-output.txt`](snippets/11-output.txt) | Output | text | 8. Worked Example: A Code-Review Bot for Your Repository |
| [`12-listing-20-7-the-guard-rails-in-src-reviewbot-service-py.py`](snippets/12-listing-20-7-the-guard-rails-in-src-reviewbot-service-py.py) | Listing 20-7: The guard rails in src/reviewbot/service.py | python | 9. Exposing an Agent Behind a FastAPI Endpoint |
| [`13-listing-20-8-src-reviewbot-api-py.py`](snippets/13-listing-20-8-src-reviewbot-api-py.py) | Listing 20-8: src/reviewbot/api.py | python | 9. Exposing an Agent Behind a FastAPI Endpoint |
| [`14-listing-20-9-src-reviewbot-cost-py-a-ledger-that-follows-t.py`](snippets/14-listing-20-9-src-reviewbot-cost-py-a-ledger-that-follows-t.py) | Listing 20-9: src/reviewbot/cost.py, a ledger that follows the guide's rules | python | 10. Cost, Limits, and Observability |
| [`15-listing-20-10-the-core-of-tests-fakecli-py.py`](snippets/15-listing-20-10-the-core-of-tests-fakecli-py.py) | Listing 20-10: The core of tests/fakecli.py | python | 11. Testing Agents: Fakes, Recorded Sessions, Evals |
| [`16-listing-20-11-two-tool-calls-from-tests-test-review-session.py`](snippets/16-listing-20-11-two-tool-calls-from-tests-test-review-session.py) | Listing 20-11: Two tool calls from tests/test_review_session.py | python | 11. Testing Agents: Fakes, Recorded Sessions, Evals |
| [`17-listing-20-12-the-assertions-in-tests-test-review-session-p.py`](snippets/17-listing-20-12-the-assertions-in-tests-test-review-session-p.py) | Listing 20-12: The assertions in tests/test_review_session.py | python | 11. Testing Agents: Fakes, Recorded Sessions, Evals |
| [`18-output.txt`](snippets/18-output.txt) | Output | text | 11. Testing Agents: Fakes, Recorded Sessions, Evals |
| [`19-listing-20-13-one-case-from-evals-cases-toml-and-how-a-find.toml`](snippets/19-listing-20-13-one-case-from-evals-cases-toml-and-how-a-find.toml) | Listing 20-13: One case from evals/cases.toml, and how a finding is matched | toml | 11. Testing Agents: Fakes, Recorded Sessions, Evals |
| [`20-code.py`](snippets/20-code.py) | Code | python | 11. Testing Agents: Fakes, Recorded Sessions, Evals |
| [`21-output.txt`](snippets/21-output.txt) | Output | text | 11. Testing Agents: Fakes, Recorded Sessions, Evals |
