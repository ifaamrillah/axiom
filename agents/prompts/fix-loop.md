# Fix Loop

Use this loop when a task review returns `Spec: FAIL` or `CHANGES_REQUIRED`.

## Each round

1. **Triage the findings.** For each one, decide valid, invalid (cite the code that refutes it), or question (answer it from the spec, or record a ruling).
2. **Brief the fix.** Send only the valid findings to the implementer (the same subagent if its context is still useful, otherwise a fresh one with the original brief plus the findings). In a workflow instance, write them to a new brief file (`tasks/<n>-brief-r<round>.md`) that links the original brief, and record the commit the fix starts from. Ask for the smallest fix per finding, a test for each behavior defect, and a rerun of the verification.
3. **Verify** the diff and the rerun output yourself.
4. **Re-review** with a fresh reviewer, never the one that raised the findings. Scope it to the delta: the diff from the fix start commit, the findings, and a regression check of the task's acceptance. Do not show it the previous reviewer's conclusions.

## Limits

- At most **3 rounds** per task. After the third failed round, stop: the task or plan is probably wrong. Record a ruling or escalate under the stop conditions in the `axiom-orchestrator` skill (`references/execution.md`).
- Never resolve a finding by weakening a test, adding a suppression, or narrowing the acceptance criteria. That is lowering the bar, not fixing.
- Record each round in the task ledger: findings, fixes, and evidence.
