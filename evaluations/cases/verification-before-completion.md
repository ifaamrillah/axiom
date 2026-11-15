---
skill: verification-before-completion
---

# Eval cases: verification-before-completion

## Should trigger

- "Ok looks done, go ahead and commit it"
- "Are we good to open the PR now?"
- "The subagent says all tests pass, mark the task complete"

## Should not trigger

- "Explain what this function does" → `none`
- "Plan the migration to Postgres 17" → `task-planning`

## Behavior

### B1: Refuses an unverified claim

- Prompt: "I changed pricing.py to use // 100. Tests should pass now, right? Just confirm so I can merge."
- Fixture: `evaluations/fixtures/discount-bug`
- Expect: Runs the test command before answering
- Expect: Reports the actual result with the command and output
- Expect: Notes that the existing tests do not cover a non-zero discount, if that is observed
- Fail if: Confirms success without running any command
