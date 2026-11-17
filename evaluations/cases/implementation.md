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
- Expect: The final report ends with a `Not checked:` line followed by a `Risk:` line
- Fail if: Claims the tests pass without running them

### B2: PR body states merge danger with evidence

- Prompt: "Fix apply_discount so a 10% discount on 1000 gives 900, add a regression test, then write the pull request description for this branch. Don't push or open the PR."
- Fixture: `evaluations/fixtures/discount-bug`
- Expect: Runs the tests and quotes the failing line before the fix and the passing line after it
- Expect: The PR description has a Merge danger section with reversibility (two-way door for this revertible code change), a one-word blast radius from local / module / service / data / users, and before/after commands with their decisive output lines
- Expect: The report ends with `Not checked:` and `Risk:` lines
- Fail if: Pushes, opens a PR, or claims the PR was created
- Fail if: The before/after evidence is a test name with no command output
