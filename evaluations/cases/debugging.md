---
skill: debugging
---

# Eval cases: debugging

## Should trigger

- "The checkout tests started failing after yesterday's merge. Can you figure out why?"
- "apply_discount returns 0 for a 10% discount, it should be 900"
- "This test passes alone but fails when I run the whole suite"
- "build is broken on CI with 'undefined is not a function', fix pls"

## Should not trigger

- "Add a dark mode toggle to the settings page" → `ui-ux-design`
- "Review my PR before I merge it" → `code-review`
- "Write release notes for 2.3.0" → `release-management`

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
