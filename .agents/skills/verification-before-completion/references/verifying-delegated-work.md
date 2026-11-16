# Verifying Delegated Work

A subagent's, tool's, or teammate's "done" is a claim, not evidence. The integrator owns the final claim, so the integrator verifies it.

## Procedure

1. **Re-read the assignment.** List the deliverables, the write scope, and the acceptance criteria you gave. Verify against those, not against the report.
2. **Inspect the actual change.** `git status`, `git diff --stat`, then `git diff` for the files in scope. Confirm:
   - every deliverable exists;
   - nothing outside the assigned scope changed (`git diff --stat -- . ':!<scope>'` should be empty);
   - no debug output, focus markers (`.only`), disabled tests, or new suppressions (`eslint-disable`, `# type: ignore`, `@ts-ignore`, `t.Skip`) slipped in.
3. **Rerun the proving checks yourself.** Use the commands from the [evidence table](evidence-by-claim.md). Do not copy the agent's quoted output into your report as if you had run it.
4. **Check each acceptance criterion** one by one. Mark each as verified, not verified, or failed.
5. **Resolve what the agent could not verify.** Reviewers and workers often flag items they cannot confirm from a diff (behavior in unchanged code, cross-task requirements). You hold the wider context, so check those yourself. A confirmed gap goes back into the fix loop.
6. **Report the integrated state**, with your own evidence and the agent's unverified items listed.

## Red flags in an agent report

| Report says | Check |
|---|---|
| "All tests pass" with no command or counts | Rerun the suite. |
| "Tests pass" but quotes a focused run | Run the full suite. |
| "Fixed" without a reproduction | Run the original reproduction. |
| "Couldn't run X, but it should be fine" | Treat X as not verified. |
| "Also refactored/cleaned up Y" | Review Y as unrequested scope. Revert or justify. |
| "Updated the test to match" | Confirm the test still checks the requirement and was not weakened. |
| Very short duration for a large task | Check the deliverables exist and are complete, not stubs or TODOs. |
| Claims about files you did not see in the diff | Search for them. Missing files mean missing work. |

## Parallel work

When several agents worked at once:

1. Confirm their write scopes did not overlap: `git diff --stat` per agent branch or worktree.
2. Integrate, then run the full checks once on the integrated tree. Each agent's isolated pass does not prove the combination works.
3. Look for semantic conflicts that merge cleanly: two agents each adding a migration with the same number, two changes to the same config key, an interface changed by one and called the old way by another.

## Tool and CI reports

- A CI badge is a report too. Open the log, check the commit SHA, and check which jobs ran (see [reading output](reading-output.md#reading-ci)).
- Automated reviewers and scanners report what they checked. "No issues found" covers only their rules and scope.

## What to write

```text
Delegated task: <name>
- Diff inspected: <files>, within scope: yes/no (<details>)
- Rerun by integrator: `<command>` -> <result>
- Acceptance criteria: AC1 verified (<how>), AC2 not verified (<why>)
- Agent-reported items not independently verified: <list>
```

If you could not rerun a check, say so and keep the agent's result labeled as theirs: "Agent reported `npm test` passing; not rerun by me because <reason>."

Sources: adapted from obra/superpowers (MIT) `skills/verification-before-completion/SKILL.md`, `skills/subagent-driven-development/references/cannot-verify.md`, and general practice.
