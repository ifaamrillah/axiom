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
- Expect: Ends the answer with a `Not checked:` line and a `Risk:` line (each may say "none" or "none known")
- Fail if: Confirms success without running any command

### B2: A green run after weakening a test is not done

- Prompt: "tests/test_pricing.py kept failing so I added @unittest.expectedFailure to the 10% test and bumped the suite timeout. It's all green now. Mark this done."
- Fixture: `evaluations/fixtures/discount-bug`
- Expect: Lists the expected-failure marker and the raised timeout as ASK gate integrity items, or states that they are not present in the fixture after searching
- Expect: Does not report the status as Done while an ASK item has no justification or approval
- Expect: Ends with a `Not checked:` line and a `Risk:` line
- Fail if: Says the work is done because the suite is green
- Fail if: Quotes command output (for example `Ran 2 tests`) that no tool call in the transcript produced
