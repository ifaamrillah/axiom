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
- Expect: Gives file references and a severity for each finding
- Fail if: Approves the change

### B2: Subtle correctness bugs in a new module

- Prompt: "Review app/reports.py before we ship it. It's new in this change."
- Fixture: `evaluations/fixtures/tenant-billing`
- Expect: Flags the N+1 query: one customer lookup per invoice inside the loop in `monthly_revenue`
- Expect: Flags money held as floats (`amount_cents / 100`, then `round`) instead of integer cents or Decimal
- Expect: Flags the naive `datetime.now()` comparison in `overdue_invoices` (time zone or naive vs aware mismatch)
- Expect: Flags the pagination offset `page * size` (skips the first page when pages start at 1, or the page base is undefined)
- Expect: Gives file:line references and a severity for each finding
- Fail if: Approves the module without findings
- Fail if: Modifies application code or tests
