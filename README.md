# Claude Code for Python Developers — Companion Code

```bash
git clone https://github.com/claude-code-python-book/claude-code-python.git
```

Code listings, prompts, commands and sample projects from the book *Claude Code for Python Developers* by R.S. Nag, organised chapter by chapter.

- `chNN-.../snippets/` holds every code block from the chapter, exactly as printed and in reading order. Files named `listing-…` are the numbered listings; `output` files are captured command output; `prompt` files are prompts you type into Claude Code.
- `chNN-.../sample/` holds the chapter's tested sample project. Each has its own README with setup and test commands.
- `appendices/` holds the code blocks from Appendices A to C: the slash command library, the `CLAUDE.md` templates and the tooling cheat sheet.

## Important notice: reference material, not production-ready code

Everything in this repository comes from the book *Claude Code for Python Developers* and is meant for learning and reference. The snippets, commands, configuration files, prompts and sample projects illustrate ideas. They are **not production-ready**, and they have not been reviewed for your systems, data, security requirements or regulations.

Before you use any of it in your own codebase:

1. Verify it against trusted, authoritative sources: the official Claude Code documentation (code.claude.com/docs), the Claude Platform documentation (platform.claude.com/docs), the Python documentation (docs.python.org), and the official documentation of each library and tool involved.
2. Check your tool versions against the versions the book names. Claude Code, Python packages, command flags, plans and prices change often; this code reflects November 2026.
3. Read and understand every line, and try it first on a branch, in a fresh virtual environment or container, with test data and no real credentials.
4. Run your own tests, linters, type checker, security scanners and a human code review before anything ships.

The code is provided "as is", without warranty of any kind. The author is not responsible for any loss, damage, security incident, cost or other consequence arising from its use, in particular if snippets are used directly without being verified first. You use it at your own risk.

## Chapters

| Chapter | Title | Snippets | Sample project |
| --- | --- | --- | --- |
| 1 | [What Is Agentic AI? A Python Developer's Mental Model](ch01-what-is-agentic-ai/) | 19 | yes |
| 2 | [Sub-Agents and Multi-Agent Systems: How Orchestration Works](ch02-sub-agents-and-multi-agent-systems/) | 13 | yes |
| 3 | [Skills: What They Are and How SKILL.md Works](ch03-skills/) | 18 | yes |
| 4 | [Model Context Protocol (MCP) with Python](ch04-model-context-protocol/) | 12 | yes |
| 5 | [What Is Claude Code? Installing and Configuring It for Python](ch05-what-is-claude-code/) | 18 | yes |
| 6 | [CLAUDE.md Mastery: Teaching Claude Your Python Project](ch06-claude-md-mastery/) | 22 | yes |
| 7 | [Slash Commands, Subagents, and Hooks for Python Workflows](ch07-slash-commands-subagents-hooks/) | 35 | yes |
| 8 | [Writing Python Code with Claude Code: A Refactoring Tutorial](ch08-writing-python-code-refactoring/) | 37 | yes |
| 9 | [pytest and Test Coverage: Generate Tests and Fill the Gaps](ch09-pytest-and-test-coverage/) | 56 | yes |
| 10 | [Code Review, Linting, and Type Checking: Catch Bugs Before the PR](ch10-code-review-linting-type-checking/) | 42 | yes |
| 11 | [Docstrings, README, and API Docs](ch11-docstrings-readme-api-docs/) | 38 | yes |
| 12 | [FastAPI Scaffolding: Generate a Production-Ready API Fast](ch12-fastapi-scaffolding/) | 39 | yes |
| 13 | [Django and Django REST Framework](ch13-django-and-drf/) | 34 | yes |
| 14 | [SQLAlchemy 2.0, Database Queries, and Alembic Migrations](ch14-sqlalchemy-and-alembic/) | 38 | yes |
| 15 | [Async Python and Background Jobs: asyncio and Celery](ch15-async-and-celery/) | 22 | yes |
| 16 | [Data Work: pandas, Polars, and Jupyter Notebooks](ch16-data-work/) | 36 | yes |
| 17 | [Security Scanning and Dependency Auditing for Python](ch17-security-scanning/) | 26 | yes |
| 18 | [Writing and Debugging GitHub Actions for Python](ch18-github-actions/) | 14 | yes |
| 19 | [Docker, Compose, and Kubernetes for Python Apps](ch19-docker-compose-kubernetes/) | 25 | yes |
| 20 | [Building Your Own Agents with the Claude Agent SDK for Python](ch20-claude-agent-sdk/) | 21 | yes |
| 21 | [End-to-End Agentic Feature Development: Code → Test → Review → Deploy](ch21-end-to-end-feature-development/) | 23 | yes |
| 22 | [Building a Team Agentic Toolchain](ch22-team-agentic-toolchain/) | 19 | yes |

## Notes

- Each sample's `pyproject.toml` states its minimum Python (3.11, 3.12 or 3.13); the book's examples were tested with Python 3.13. Several samples also need PostgreSQL, Redis or Docker, as their READMEs say.
- Names such as Acme, `acme.example` and the tokens in tests are made-up examples. `.env.example` files hold placeholders only; never commit a real `.env`.
- The samples were separate Git repositories while the book was written; their commit history isn't included here.
- Chapters 1 to 4 call the Claude API. Their `tests/` and `checks/` folders replace the API with a small fake so the code can be checked offline; run the scripts themselves with an `ANTHROPIC_API_KEY` set.

## License

The code in this repository is released under the [MIT License](LICENSE), which also states that it comes without warranty. The book's text is not part of this repository and remains under the book's copyright.
