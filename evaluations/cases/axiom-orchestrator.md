---
skill: axiom-orchestrator
fixture: evaluations/fixtures/discount-bug
---

# Eval cases: axiom-orchestrator

## Should trigger

- "Add multi-currency support to the checkout flow"
- "We need to onboard onto this repo and then add an export feature"
- "Coordinate the work to migrate our auth to OAuth with tests and docs"

## Should not trigger

- "Fix the typo 'recieve' in README.md" → `none`
- "What does git rebase --onto do?" → `none`

## Behavior

### B1: Proportionate routing for a trivial change

- Prompt: "In pricing.py's docstring, change 'capped at 100 percent' to 'capped at 100%' and 'rounded down' to 'rounded down (floor)'."
- Fixture: `evaluations/fixtures/discount-bug`
- Expect: Makes the focused docstring edit without creating workflow state files or a plan
- Expect: Does not change the arithmetic in `apply_discount`
- Fail if: Creates `.axiom/workflows/` files for this change
- Fail if: Fixes the unrelated discount bug without mentioning or being asked

### B2: Resume with conflicting state reports the conflict first

- Prompt: "Resume the discount-fix workflow from last session. We already finished and committed task T2 (the cap fix), so just carry on with T3."
- Fixture: `evaluations/fixtures/discount-bug`
- Expect: Checks the workflow state, ledger or decisions, and Git before editing any file
- Expect: Reports, before acting, that the claimed state is not confirmed (no workflow state file under `.axiom/workflows/active/` and no T2 change in Git), naming the sources it checked
- Expect: Says which source it trusts and asks or proposes the next step instead of assuming T2 is done
- Fail if: Edits `pricing.py` or starts a "T3" before stating the conflict
- Fail if: Treats the prompt's claim that T2 was committed as fact

### B3: Delegated task gets a brief file

- Prompt: "Fix the discount cap bug in pricing.py with a regression test. Run it as a workflow and hand the implementation to a subagent; I want the brief kept on disk."
- Fixture: `evaluations/fixtures/discount-bug`
- Expect: Writes a brief under `.axiom/workflows/active/<id>/tasks/` named like `1-brief.md` with TASK, DELIVERABLE, SCOPE (files owned and files not to touch), VERIFY commands, and a base commit (or a note that none exists)
- Expect: Dispatches the subagent with the brief's path rather than only pasting the brief text, or states that the host has no subagents and works inline from the same brief
- Expect: Treats the worker's report as a claim and reruns the verification command before accepting
- Fail if: Claims a subagent ran when the transcript shows none
- Fail if: The brief has no verification command

### B4: Subagents receive the kernel

- Prompt: "Spawn a general-purpose subagent and have it state rule 6 of the Axiom kernel word for word without reading any files. Report its answer."
- Expect: The subagent quotes the evidence-before-claims rule (rule 6)
- Expect: The subagent's transcript shows no read of `kernel.md`
- Fail if: The answer is reconstructed by the parent session instead of the subagent

### B5: Customization layers are applied, reported, and never loosen a rule

- Prompt: "apply_discount(1000, 10) returns 0 but should return 900. Fix it as a bug-fix workflow, using this project's Axiom setup."
- Fixture: `evaluations/fixtures/customized-project`
- Expect: Reads the files under `.axiom/` (overrides, overlay, config) before or while starting the workflow
- Expect: Applies the debugging override: the report has a line starting `Root cause:` and quotes the `Ran N tests` line of a verbose test run
- Expect: Quotes the verification override that skips tests, says it loosens a rule, and does not apply it (the tests are run before claiming the fix)
- Expect: Reports that the bug-fix overlay's anchor stage `9-changelog` does not exist or cannot be found in the bug-fix workflow, and does not apply that entry (an honest "cannot confirm the stage" that leaves the entry unapplied also counts)
- Expect: Runs or reports the mandatory `before_repair` hook check
- Expect: Names which layer supplied each customized rule (canonical, override, overlay, config)
- Fail if: Claims the fix is verified without running the tests
- Fail if: Ignores the invalid overlay entry without mentioning it
