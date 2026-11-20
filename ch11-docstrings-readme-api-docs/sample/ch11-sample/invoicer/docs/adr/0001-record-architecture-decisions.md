# 1. Record architecture decisions

Date: 2026-11-15

## Status

Accepted

## Context

Decisions about invoicer's design live in pull request threads and people's
memories. New team members, and Claude Code, see what the code does but not
why, and they undo choices that had good reasons.

## Decision

We record each significant decision as a short Markdown file in `docs/adr/`,
numbered in order, using Michael Nygard's format: Title, Status, Context,
Decision, Consequences. An accepted record is not edited; a later record
supersedes it.

## Consequences

The reasons behind the code are versioned with the code and reviewed in pull
requests. Writing a record takes a few minutes per decision.
