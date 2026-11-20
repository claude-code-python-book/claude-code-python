# Chapter 18 sample: Writing and Debugging GitHub Actions for Python

- `rowbatch/` - the library from the chapter, with
  - `.github/workflows/ci.yml` - lint, type-check, test matrix (Listing 18-2)
  - `.github/workflows/release.yml` - build + trusted publishing to PyPI (Listing 18-5)
  - `.github/workflows/claude-review.yml` - Claude Code PR review (Listing 18-8)
  - `.github/dependabot.yml` - keeps action and uv versions current
  - `.claude/skills/fix-ci/SKILL.md` - `/fix-ci` debugging skill (Listing 18-6)
  - `noxfile.py` - local multi-version test runs (Listing 18-4)
- `demos/` - the setup-python variant (Listing 18-1), Claude's first draft of
  `batch_rows` (Listing 18-3), the lint demo, and the real outputs quoted in the chapter.

## Before you push

1. `cd rowbatch && uv lock` and commit `uv.lock` (CI uses `uv sync --locked`).
2. Action versions were checked in November 2026. For a real repository, pin
   each action to its full commit SHA with the version as a comment.
3. For releases: create a `pypi` environment in the repository settings and add
   a trusted publisher on PyPI (owner, repository, `release.yml`, `pypi`).
4. For the review workflow: run `/install-github-app` in Claude Code, or add an
   `ANTHROPIC_API_KEY` secret and install the Claude GitHub App.

## What was run

Ruff, mypy and pytest (Python 3.12 and 3.13), `uv build` and the smoke tests,
and the tag check. GitHub Actions itself, Python 3.14, Windows/macOS jobs, nox,
trusted publishing and the Claude Code action were not run.
