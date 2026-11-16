---
skill: tdd
fixture: evaluations/fixtures/discount-bug
---

# Eval cases: tdd

## Should trigger

- "Use TDD to add a percent cap to apply_discount"
- "apply_discount(1000, 10) returns 0. Write a failing test for this bug first, then fix it"
- "Make apply_discount reject negative totals, test-first please"

## Should not trigger

- "Why is the build slow?" → `none`
- "Review this diff for security issues" → `code-review`

## Behavior

### B1: Red before green

- Prompt: "Using TDD, make apply_discount(1000, 10) return 900."
- Fixture: `evaluations/fixtures/discount-bug`
- Expect: Writes a new test before changing `pricing.py`
- Expect: Runs the new test and reports that it fails, with the assertion output
- Expect: Changes the production code minimally, then reruns and reports the test passing
- Fail if: Modifies `pricing.py` before the failing test was run
- Fail if: Deletes or weakens an existing test
