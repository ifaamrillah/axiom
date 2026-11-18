---
skill: tdd
fixture: evaluations/fixtures/discount-bug
---

# Eval cases: tdd

## Should trigger

- "Use TDD to add a percent cap to apply_discount"
- "apply_discount(1000, 10) returns 0. Write a failing test for this bug first, then fix it"
- "Make apply_discount reject negative totals, test-first please"
- "Run this through the tdd skill: apply_discount should accept a maximum discount in cents"
- "Red, green, refactor: add rounding to the nearest cent in apply_discount"

## Should not trigger

- "Why is the build slow?" → `ci-and-observability`
- "Review this diff for security issues" → `code-review`
- "apply_discount returns 0 for a 10% discount, find out why" → `debugging`
- "Which apply_discount edge cases do our tests miss?" → `testing`

## Behavior

### B1: Red before green

- Prompt: "Using TDD, make apply_discount(1000, 10) return 900."
- Fixture: `evaluations/fixtures/discount-bug`
- Expect: Writes a new test before changing `pricing.py`
- Expect: Runs the new test and reports that it fails, with the assertion output
- Expect: Changes the production code minimally, then reruns and reports the test passing
- Fail if: Modifies `pricing.py` before the failing test was run
- Fail if: Deletes or weakens an existing test
