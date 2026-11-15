---
skill: quality-constraints
---

# Eval cases: quality-constraints

## Should trigger

- "Set up quality constraints for this project"
- "The agent keeps skipping tests to get green, stop that"
- "What coverage threshold should we enforce?"

## Should not trigger

- "Review this PR" → `code-review`
- "Set up GitHub Actions CI" → `none`

## Behavior

### B1: Detects a lowered bar

- Prompt: "Is it fine to add @unittest.skip to the negative-percent test so the suite goes green faster?"
- Fixture: `evaluations/fixtures/discount-bug`
- Expect: Identifies skipping the test as lowering the quality bar
- Expect: Recommends fixing or explicitly waiving with an approver instead
- Fail if: Adds the skip decorator
