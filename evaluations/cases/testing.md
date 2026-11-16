---
skill: testing
fixture: evaluations/fixtures/discount-bug
---

# Eval cases: testing

## Should trigger

- "Add tests for apply_discount edge cases"
- "What test coverage do we need for the pricing module?"

## Should not trigger

- "Write an end-to-end browser test for checkout" → `e2e-testing`
- "Use TDD to add a coupon" → `tdd`

## Behavior

### B1: Tests encode intent, not the bug

- Prompt: "Add tests for apply_discount edge cases."
- Fixture: `evaluations/fixtures/discount-bug`
- Expect: Covers at least a typical non-zero discount, 0%, 100%, and above 100%
- Expect: Runs the tests and reports that the typical-discount test fails against the current code
- Fail if: Asserts that a 10% discount on 1000 returns 0 (encoding the bug as expected behavior)
