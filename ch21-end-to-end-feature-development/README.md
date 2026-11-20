# Chapter 21 — End-to-End Agentic Feature Development: Code → Test → Review → Deploy

Code and snippets exactly as they appear in the chapter, in reading order.

> **Reference material, not production-ready code.** Verify every snippet against the official documentation for the tools involved, and test it in your own environment, before you use it in your codebase. See the notice in the [repository README](../README.md).

## Sample project

`sample/` is the tested sample project for this chapter (`bookshop`). See the README inside it for how to run it.

## Snippets

| File | What it is | Type | Section |
| --- | --- | --- | --- |
| [`01-listing-21-1-docs-features-ratings-md.md`](snippets/01-listing-21-1-docs-features-ratings-md.md) | Listing 21-1: docs/features/ratings.md | markdown | 4. Our Sample Project: FastAPI + SQLAlchemy + Celery |
| [`02-listing-21-2-the-architecture-and-rules-in-claude-md.md`](snippets/02-listing-21-2-the-architecture-and-rules-in-claude-md.md) | Listing 21-2: The architecture and rules in CLAUDE.md | markdown | 4. Our Sample Project: FastAPI + SQLAlchemy + Celery |
| [`03-listing-21-3-claude-skills-ship-feature-skill-md.md`](snippets/03-listing-21-3-claude-skills-ship-feature-skill-md.md) | Listing 21-3: .claude/skills/ship-feature/SKILL.md | markdown | 5. Stage One: Writing the Feature Code |
| [`04-prompt.txt`](snippets/04-prompt.txt) | Prompt | prompt | 5. Stage One: Writing the Feature Code |
| [`05-listing-21-4-a-first-draft-of-the-rules.py`](snippets/05-listing-21-4-a-first-draft-of-the-rules.py) | Listing 21-4: A first draft of the rules | python | 5. Stage One: Writing the Feature Code |
| [`06-listing-21-5-src-bookshop-ratings-py.py`](snippets/06-listing-21-5-src-bookshop-ratings-py.py) | Listing 21-5: src/bookshop/ratings.py | python | 5. Stage One: Writing the Feature Code |
| [`07-listing-21-6-reviewservice-add-review-in-src-bookshop-serv.py`](snippets/07-listing-21-6-reviewservice-add-review-in-src-bookshop-serv.py) | Listing 21-6: ReviewService.add_review in src/bookshop/service.py | python | 5. Stage One: Writing the Feature Code |
| [`08-listing-21-7-the-post-route-in-src-bookshop-api-py.py`](snippets/08-listing-21-7-the-post-route-in-src-bookshop-api-py.py) | Listing 21-7: The POST route in src/bookshop/api.py | python | 5. Stage One: Writing the Feature Code |
| [`09-output.txt`](snippets/09-output.txt) | Output | text | 6. Stage Two: Building the Test Safety Net |
| [`10-listing-21-8-claude-agents-test-writer-md.md`](snippets/10-listing-21-8-claude-agents-test-writer-md.md) | Listing 21-8: .claude/agents/test-writer.md | markdown | 6. Stage Two: Building the Test Safety Net |
| [`11-listing-21-9-tests-that-pin-the-brief.py`](snippets/11-listing-21-9-tests-that-pin-the-brief.py) | Listing 21-9: Tests that pin the brief | python | 6. Stage Two: Building the Test Safety Net |
| [`12-output.txt`](snippets/12-output.txt) | Output | text | 6. Stage Two: Building the Test Safety Net |
| [`13-output.txt`](snippets/13-output.txt) | Output | text | 6. Stage Two: Building the Test Safety Net |
| [`14-output.txt`](snippets/14-output.txt) | Output | text | 6. Stage Two: Building the Test Safety Net |
| [`15-output.txt`](snippets/15-output.txt) | Output | text | 7. Stage Three: Reviewing from Every Angle (Ruff, mypy, Bandit, Coverage) |
| [`16-output.txt`](snippets/16-output.txt) | Output | text | 7. Stage Three: Reviewing from Every Angle (Ruff, mypy, Bandit, Coverage) |
| [`17-listing-21-10-the-draft-repository-s-aggregate-update.py`](snippets/17-listing-21-10-the-draft-repository-s-aggregate-update.py) | Listing 21-10: The draft repository's aggregate update | python | 7. Stage Three: Reviewing from Every Angle (Ruff, mypy, Bandit, Coverage) |
| [`18-output.txt`](snippets/18-output.txt) | Output | text | 7. Stage Three: Reviewing from Every Angle (Ruff, mypy, Bandit, Coverage) |
| [`19-listing-21-11-the-fixed-aggregate-update-in-src-bookshop-re.py`](snippets/19-listing-21-11-the-fixed-aggregate-update-in-src-bookshop-re.py) | Listing 21-11: The fixed aggregate update in src/bookshop/repository.py | python | 7. Stage Three: Reviewing from Every Angle (Ruff, mypy, Bandit, Coverage) |
| [`20-output.txt`](snippets/20-output.txt) | Output | text | 7. Stage Three: Reviewing from Every Angle (Ruff, mypy, Bandit, Coverage) |
| [`21-output.txt`](snippets/21-output.txt) | Output | text | 7. Stage Three: Reviewing from Every Angle (Ruff, mypy, Bandit, Coverage) |
| [`22-listing-21-12-the-image-and-deploy-jobs-in-github-workflows.yml`](snippets/22-listing-21-12-the-image-and-deploy-jobs-in-github-workflows.yml) | Listing 21-12: The image and deploy jobs in .github/workflows/ci.yml | yaml | 8. Stage Four: Shipping Through CI and Docker |
| [`23-output.txt`](snippets/23-output.txt) | Output | text | 8. Stage Four: Shipping Through CI and Docker |
