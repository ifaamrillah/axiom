---
skill: task-planning
fixture: evaluations/fixtures/discount-bug
---

# Eval cases: task-planning

## Should trigger

- "Break the coupon spec into an implementation plan with tasks"
- "Plan the work to fix the discount bug and add edge-case tests"

## Should not trigger

- "Just fix the bug" → `debugging`
- "Is our spec consistent with the tasks?" → `spec-analysis`

## Behavior

### B1: Ordered tasks with paths and verification

- Prompt: "Plan the work to fix the discount bug and add edge-case tests. Don't implement yet."
- Fixture: `evaluations/fixtures/discount-bug`
- Expect: Each task names the file(s) it touches
- Expect: Each task has a verification step (a command or test)
- Expect: Orders a failing test before the fix
- Fail if: Edits pricing.py or the tests
