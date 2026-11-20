# 2. Store sent-reminder state as JSON, not pickle

Date: 2026-11-15

## Status

Accepted

## Context

The reminders job must remember which invoices it has already reminded, so
it doesn't remind a customer twice. The first version stored that list with
`pickle`. Unpickling data can run arbitrary code, and the file lives on a
shared volume that other jobs can write to.

## Decision

Store the ids as a JSON list of strings, read with
`invoicer.reminders.load_sent`, which validates the content with Pydantic.

## Consequences

The file is safe to read, readable by people, and easy to diff. It can only
hold a list of strings; richer state needs a new decision. A file with the
wrong shape fails loudly with `ValidationError` instead of loading.
