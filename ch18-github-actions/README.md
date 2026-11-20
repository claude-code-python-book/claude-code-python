# Chapter 18 — Writing and Debugging GitHub Actions for Python

Code and snippets exactly as they appear in the chapter, in reading order.

> **Reference material, not production-ready code.** Verify every snippet against the official documentation for the tools involved, and test it in your own environment, before you use it in your codebase. See the notice in the [repository README](../README.md).

## Sample project

`sample/` is the tested sample project for this chapter (`ch18-github-actions-sample`). See the README inside it for how to run it.

## Snippets

| File | What it is | Type | Section |
| --- | --- | --- | --- |
| [`01-output.txt`](snippets/01-output.txt) | Output | text | 2. Anatomy of a Workflow File |
| [`02-listing-18-1-a-test-job-with-setup-python-and-pip.yml`](snippets/02-listing-18-1-a-test-job-with-setup-python-and-pip.yml) | Listing 18-1: A test job with setup-python and pip | yaml | 3. Your First Workflow: setup-python or setup-uv, Lint, Type-Check, Test |
| [`03-listing-18-2-github-workflows-ci-yml.yml`](snippets/03-listing-18-2-github-workflows-ci-yml.yml) | Listing 18-2: .github/workflows/ci.yml | yaml | 3. Your First Workflow: setup-python or setup-uv, Lint, Type-Check, Test |
| [`04-output.txt`](snippets/04-output.txt) | Output | text | 3. Your First Workflow: setup-python or setup-uv, Lint, Type-Check, Test |
| [`05-prompt.txt`](snippets/05-prompt.txt) | Prompt | prompt | 3. Your First Workflow: setup-python or setup-uv, Lint, Type-Check, Test |
| [`06-listing-18-3-claude-s-first-version-of-batch-rows.py`](snippets/06-listing-18-3-claude-s-first-version-of-batch-rows.py) | Listing 18-3: Claude's first version of batch_rows() | python | 5. Testing Across Python Versions with a Matrix (and tox or nox) |
| [`07-listing-18-4-noxfile-py-not-run.py`](snippets/07-listing-18-4-noxfile-py-not-run.py) | Listing 18-4: noxfile.py (not run) | python | 5. Testing Across Python Versions with a Matrix (and tox or nox) |
| [`08-listing-18-5-github-workflows-release-yml.yml`](snippets/08-listing-18-5-github-workflows-release-yml.yml) | Listing 18-5: .github/workflows/release.yml | yaml | 6. Publishing a Package to PyPI with Trusted Publishing |
| [`09-output.txt`](snippets/09-output.txt) | Output | text | 6. Publishing a Package to PyPI with Trusted Publishing |
| [`10-output.txt`](snippets/10-output.txt) | Output | text | 7. Reading a Failed Run: Where to Look First |
| [`11-listing-18-6-claude-skills-fix-ci-skill-md.md`](snippets/11-listing-18-6-claude-skills-fix-ci-skill-md.md) | Listing 18-6: .claude/skills/fix-ci/SKILL.md | markdown | 8. Debugging Failed Workflows with Claude Code |
| [`12-listing-18-7-the-fixed-generator-in-src-rowbatch-batching.py`](snippets/12-listing-18-7-the-fixed-generator-in-src-rowbatch-batching.py) | Listing 18-7: The fixed generator in src/rowbatch/batching.py | python | 8. Debugging Failed Workflows with Claude Code |
| [`13-output.txt`](snippets/13-output.txt) | Output | text | 8. Debugging Failed Workflows with Claude Code |
| [`14-listing-18-8-github-workflows-claude-review-yml-not-run.yml`](snippets/14-listing-18-8-github-workflows-claude-review-yml-not-run.yml) | Listing 18-8: .github/workflows/claude-review.yml (not run) | yaml | 9. Running Claude Code Inside GitHub Actions for PR Reviews |
