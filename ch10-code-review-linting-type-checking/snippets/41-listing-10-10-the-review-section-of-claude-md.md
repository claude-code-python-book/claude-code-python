## Review
- Before a PR: Ruff, mypy, pyright and pytest green, then `/code-review`.
  Run `/security-review` for changes that touch SQL, files, HTTP or secrets.
- SQL takes values only through `?` placeholders. Secrets come from the
  environment. Never `pickle` data from outside the process.
- A `# noqa` or `# type: ignore` names its code and says why on the line above.
