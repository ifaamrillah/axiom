---
name: verification-before-completion
description: Require fresh, observable evidence before claiming that work is complete, fixed, passing, or safe. Use when about to commit or push ("go ahead and commit", "ship it"), open a pull request, report or mark a task or gate as done, or accept another agent's success report.
---

# Verification Before Completion

## Purpose

Stop unsupported success claims. A claim is only as strong as the command output behind it, produced in this session, after the last relevant change.

## The rule

```
NO COMPLETION CLAIM WITHOUT FRESH VERIFICATION EVIDENCE
```

If the proving command did not run after the latest relevant edit, the claim cannot be made. Report the actual state instead.

## Gate procedure

Before any status claim, or before expressing satisfaction with the result:

1. **Identify** the command or observation that would prove the claim.
2. **Run** it in full, fresh, after the last relevant change.
3. **Read** the whole result: exit code, failure and skip counts, warnings. Watch for partial runs, cached results, skipped tests, and filtered or piped output; see [reading output](references/reading-output.md).
4. **Compare** the output with the claim.
   - If it does not support the claim, state the real status with the evidence.
   - If it does, state the claim together with the evidence.
5. **Record** command, environment, and result in the workflow state or report when the work is multi-stage.

## What counts as evidence

The table covers the common claims. For commands and traps per area (tests, build, lint, types, migrations, UI, performance, security, docs, deploy), open [evidence by claim](references/evidence-by-claim.md).

| Claim | Requires | Not sufficient |
|---|---|---|
| Tests pass | Test command output with 0 failures, after the last edit | An earlier run; "should pass" |
| Build succeeds | Build command exit 0 | Lint or type check passing |
| Lint/type clean | That tool's own output with 0 errors | A partial run on some files |
| Bug fixed | The original reproduction now passes | Code changed; a different test passes |
| Regression test is valid | Seen failing without the fix, passing with it | Passing once |
| Delegated task done | Diff inspected and checks rerun by the integrator | The agent's "success" message |
| Requirements met | Each acceptance criterion checked one by one | The test suite passing |
| UI works | Rendered result observed (browser/screenshot) or labeled unverified | The component compiles |
| Security finding fixed | The original proof no longer reproduces; regression test added | The patch "looks right" |
| Migration works | Up, down, and up again on a fresh database and on representative data | The migration file exists |
| Faster | Before and after numbers on the same machine and data, several runs | One run; "should be faster" |
| Docs updated | Each changed interface mapped to the doc line that describes it | "Updated the README" |
| Deployed | The target environment reports the new version; smoke checks pass | The pipeline was triggered |

## Red flags: stop and verify

- Words like "should", "probably", "seems to", "looks fine" attached to a status.
- Celebrating ("Done!", "All good") before reading output.
- About to commit, push, or open a PR with no run since the last edit.
- Trusting a subagent's, tool's, or CI summary without reading it.
- Extrapolating from a partial run ("the module tests pass, so the suite passes").
- A check failed for an environment reason and you want to call it passed anyway.

## Rationalizations and the answer

| Excuse | Answer |
|---|---|
| "It's a tiny change" | Tiny changes break builds. Run the focused check. |
| "I'm confident" | Confidence is not evidence. |
| "The linter passed" | The linter is not the compiler or the tests. |
| "The agent said it succeeded" | Inspect the diff and rerun the check. See [verifying delegated work](references/verifying-delegated-work.md). |
| "It was cached, so it passed" | A cache hit proves the inputs it keyed on. Force a fresh run if unsure. |
| "Only skipped tests are left" | Skipped means not verified. Report the count. |
| "The test environment is broken, so it doesn't count" | Then the gate is Blocked, not Passed. Say so. |
| "I ran it earlier" | Earlier than the last edit is not fresh. |
| "Different wording means the rule doesn't apply" | The rule covers any implied success claim. |

## When a check cannot run

Report it as **not run** or **blocked**, with the reason and the exact command a human can run. Never convert Blocked or Skipped into Passed. Under the quality gate contract (`core/contracts/QUALITY-GATE-CONTRACT.md` in the Axiom repository), only an authorized approver can waive a blocking gate, and a waiver never means the check succeeded.

## Baseline-aware gates

In a repository whose checks already fail before your change, record the baseline first (failing test IDs, error counts). The gate is then "no new failures compared with the baseline". Never re-record the baseline to make a gate pass. See [execution guidance](../axiom-orchestrator/references/execution.md).

## Delegated work

Before accepting a subagent's, tool's, or teammate's success report: re-read the assignment, inspect the diff for scope and suppressions, rerun the proving checks yourself, and check each acceptance criterion. Label anything you did not rerun as the agent's claim. Details and red flags: [verifying delegated work](references/verifying-delegated-work.md).

## Output

A short statement per claim: the claim, the command, and the observed result. Checks that were not run, with the reason, are listed separately. Use the status words Done, Done with limits, Blocked, or Not done. Full good-versus-bad report examples: [completion reports](references/completion-reports.md).

## Examples

```
Good: "Unit tests pass: `npm test -- orders` → 34 passed, 0 failed (run after the last edit)."
Bad:  "Fixed the bug, tests should pass now."
Good: "Build not verified: `cargo build` needs network access to fetch crates, which is unavailable here."
```

## References

- [Evidence by claim](references/evidence-by-claim.md): when choosing the proving command for a claim.
- [Reading output](references/reading-output.md): when reading a result before quoting it as evidence.
- [Completion reports](references/completion-reports.md): when writing the final status report.
- [Verifying delegated work](references/verifying-delegated-work.md): when another agent, tool, or CI reports success.
