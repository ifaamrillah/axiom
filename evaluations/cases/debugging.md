---
skill: debugging
fixture: evaluations/fixtures/discount-bug
---

# Eval cases: debugging

## Should trigger

- "The checkout tests started failing after yesterday's merge. Can you figure out why?"
- "apply_discount returns 0 for a 10% discount, it should be 900"
- "This test passes alone but fails when I run the whole suite"
- "CI is red on the pricing tests since the last merge, fix pls"
- "Use the debugging skill on apply_discount: a 10% discount wipes out the whole total"
- "Skip the formalities and just fix apply_discount, it returns 0 for 10%"

## Should not trigger

- "Add a dark mode toggle to the settings page" → `ui-ux-design`
- "Review my PR before I merge it" → `code-review`
- "Write release notes for 2.3.0" → `release-management`
- "Write a failing test first, then make apply_discount reject totals over a million" → `tdd`
- "Add more edge-case tests for apply_discount" → `testing`

## Behavior

### B1: Root cause before fix

- Prompt: "apply_discount(1000, 10) returns 0 but should return 900. Fix it."
- Fixture: `evaluations/fixtures/discount-bug`
- Expect: Reproduces the defect by running code or a test before editing `pricing.py`
- Expect: Names the root cause as the divisor `// 10` instead of `// 100`
- Expect: Adds a regression test for a non-zero discount
- Expect: Reports the test command and its passing output after the fix
- Fail if: Edits `pricing.py` before any reproduction or hypothesis
- Fail if: Claims the fix works without running the tests

### B2: Find the seeded defect without inventing others

- Prompt: "Customers say apply_discount gives wrong totals. Find every defect in pricing.py and report each with its line number. Do not change any files yet."
- Fixture: `evaluations/fixtures/discount-bug`
- Seeded: `apply_discount` divides by `10` instead of `100`, so a 10% discount removes the whole total
- Expect: Runs code or a test that shows a wrong total before reporting defects
- Expect: Reports each defect with a `pricing.py` line reference
- Fail if: Edits or creates any file
