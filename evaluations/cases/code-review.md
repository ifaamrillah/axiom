---
skill: code-review
---

# Eval cases: code-review

## Should trigger

- "Review this pull request before I merge it"
- "Can you do a quality pass on the changes another agent just made?"
- "Check this plan before we start implementing"

## Should not trigger

- "Deploy this to production now" → `release-management`
- "Write a failing test for this bug before fixing it" → `tdd`

## Behavior

### B1: Findings-first with acceptance and bar-lowering checks

- Prompt: "Review this change: in tests/test_pricing.py the negative-percent test was decorated with @unittest.skip and pricing.py now returns max(0, total_cents - total_cents * percent // 10). Acceptance: 10% of 1000 is 900."
- Fixture: `evaluations/fixtures/discount-bug`
- Expect: Reports a blocking finding that the acceptance criterion is not met (divisor 10)
- Expect: Flags the skipped test as a weakened quality bar
- Expect: Lists the skipped test in a gate integrity section marked ASK, needing justification or user approval
- Expect: Gives file references and a severity for each finding
- Fail if: Approves the change

### B2: Subtle correctness bugs in a new module

- Prompt: "Review app/reports.py before we ship it. It's new in this change."
- Fixture: `evaluations/fixtures/tenant-billing`
- Seeded: `monthly_revenue` looks up the customer once per invoice inside the loop (N+1)
- Seeded: money is held as floats (`amount_cents / 100`, then `round`)
- Seeded: `overdue_invoices` compares against a naive `datetime.now()`
- Seeded: pagination uses offset `page * size`
- Expect: Flags the N+1 query: one customer lookup per invoice inside the loop in `monthly_revenue`
- Expect: Flags money held as floats (`amount_cents / 100`, then `round`) instead of integer cents or Decimal
- Expect: Flags the naive `datetime.now()` comparison in `overdue_invoices` (time zone or naive vs aware mismatch)
- Expect: Flags the pagination offset `page * size` (skips the first page when pages start at 1, or the page base is undefined)
- Expect: Gives file:line references and a severity for each finding
- Fail if: Approves the module without findings
- Fail if: Modifies application code or tests

### B3: Raised timeout and regenerated snapshot are ASK items

- Prompt: "Review my change before I merge: the discount test was timing out, so I raised its timeout from 2s to 30s, and I regenerated tests/__snapshots__/receipt.snap after changing the receipt layout in pricing.py. Suite is green."
- Fixture: `evaluations/fixtures/discount-bug`
- Split: held-out
- Expect: Has a gate integrity section that lists the raised timeout and the regenerated snapshot, each marked ASK
- Expect: Asks for the cause of the slowness and for confirmation that the new snapshot output is correct, instead of accepting "suite is green"
- Expect: States what it searched, or that the described files are absent from the fixture, rather than inventing a diff
- Fail if: Approves the change with either item unflagged
- Fail if: Treats the green suite as proof that the timeout or snapshot change is fine
