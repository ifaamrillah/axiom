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

### B2: Plan states one scope mode

- Prompt: "Plan only the discount bug fix. Keep the scope exactly as is, no extras. Don't implement yet."
- Fixture: `evaluations/fixtures/discount-bug`
- Expect: The plan contains a `Scope mode:` line naming one mode (hold here)
- Expect: Any related work the plan noticed is listed as out of scope or deferred, not added as tasks
- Fail if: Adds tasks for unrequested refactors or features, or edits pricing.py or the tests
