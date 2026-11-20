# 3. Late fee periods at exactly 60 days

Date: 2026-11-15

## Status

Proposed. Waiting for the finance team.

## Context

The original specification said the fee is 1.5% "per started 30 days past
the first 30". Read literally, an invoice 60 days old has started one period.
The code, unchanged since the legacy billing run, counts two periods at day
60, day 90 is three, and so on. The test
`test_late_fee_on_a_100_invoice[day-60]` is a strict expected failure until
this is decided.

## Options

- **A. Keep the code.** A new period starts on day 60, 90, 120 and so on.
  No change to invoices already sent.
- **B. Follow the specification.** Periods start on day 31, 61, 91 and so on.
  Invoices exactly 60, 90, ... days old get a smaller fee than today.

## Decision

Not yet made.

## Consequences

With A, the specification and the `late_fee` docstring are updated and the
test changes its expected value. With B, the code changes in its own pull
request, and the expected-failure test starts to pass.
