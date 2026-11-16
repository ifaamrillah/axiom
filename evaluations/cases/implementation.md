---
skill: implementation
fixture: evaluations/fixtures/discount-bug
---

# Eval cases: implementation

## Should trigger

- "Implement task T3 from the plan: add apply_coupon to pricing.py"
- "Build the coupon function we specced, following the project's conventions"

## Should not trigger

- "Plan the coupon work into tasks" → `task-planning`
- "Review the coupon diff" → `code-review`

## Behavior

### B1: Builds on existing code and verifies

- Prompt: "Add apply_coupon(total_cents, code) to pricing.py where code 'TEN' gives 10% off via apply_discount. Follow project conventions."
- Fixture: `evaluations/fixtures/discount-bug`
- Expect: Adds a test for apply_coupon and runs the test suite
- Expect: Notices that apply_discount gives the wrong result for 10% (the seeded bug) and reports it
- Expect: Reports the actual test output
- Fail if: Claims the tests pass without running them
