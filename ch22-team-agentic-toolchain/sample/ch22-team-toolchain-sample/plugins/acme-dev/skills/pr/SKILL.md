---
name: pr
description: Turn the reviewed changes on the current branch into a draft pull request and link it on the tracker ticket.
argument-hint: "<ticket key>"
disable-model-invocation: true
---

Prepare a pull request for ticket $ARGUMENTS from the current branch.

Changes against main:
!`git diff --stat main...HEAD`

1. Write a commit message and PR description: what changed, why, how it
   was tested, and `Closes $ARGUMENTS`. Show both and wait for approval.
2. Commit, then run `gh pr create --draft` with that description. The
   project's permission rules ask before each of these.
3. Post the PR link on $ARGUMENTS with the acme-tracker `comment_on_issue`
   tool, so the ticket shows who is working on it.
