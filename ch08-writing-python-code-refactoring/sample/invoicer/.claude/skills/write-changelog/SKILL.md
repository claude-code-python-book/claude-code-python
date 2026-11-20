---
description: Draft a Keep a Changelog entry from recent commits.
argument-hint: [version, e.g. 0.3.0]
disable-model-invocation: true
allowed-tools: Bash(git log *) Bash(git show *)
---

Write the changelog entry for version $ARGUMENTS
(use "Unreleased" if no version is given).

Recent commits, newest first; tags appear in parentheses:

!`git log --format="%h%d %s" -n 60`

1. Use only the commits newer than the most recent tag in that list.
   If a message is unclear, look at the change: `git show --stat <hash>`.
2. Follow Keep a Changelog 1.1.0. Group entries under `### Added`,
   `### Changed`, `### Deprecated`, `### Removed`, `### Fixed` and
   `### Security`, and leave out empty groups.
3. Write for the package's users: describe the effect ("Totals round
   half up"), not the work ("refactor rounding"). Combine related
   commits. Leave out refactors, tests and CI changes that users can't
   notice.
4. Insert the entry at the top of `CHANGELOG.md`, under a heading such
   as `## [0.3.0] - 2026-11-15` with today's date. If the file doesn't
   exist, create it with the standard Keep a Changelog header.

Show me the entry. Do not commit.
