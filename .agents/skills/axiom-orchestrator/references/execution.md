# Execution and Completion

## Before edits

Inspect instructions, Git status, and affected paths. Read references on demand. Use the project's established commands. For multi-stage work, keep state in `.axiom/workflows/active/<ID>/` using [workflow state](../../../../templates/workflows/workflow-state.md). For brief work, state tracking is optional.

## Record a verification baseline

Before the first edit in a repository whose checks may already fail:

1. Run the agreed checks (focused tests, lint, type check, build) once.
2. Record the failing test IDs and error counts in the workflow state as the **baseline**, with command, date, and commit.
3. From then on, a gate means **no new failures compared with the baseline**. A baseline-only failure is reported as pre-existing, never hidden and never fixed silently out of scope.
4. Never re-record the baseline to make a gate pass. If the baseline must legitimately change (for example, a flaky test is quarantined by the owner), record it as a decision.

## Plan execution loop

For an approved plan (see [task-planning](../../task-planning/SKILL.md)):

1. Check that the plan meets the Ready for Development standard. If it does not, return to planning.
2. For each task in dependency order:
   - **Inline mode:** implement the task yourself with the [implementation](../../implementation/SKILL.md) skill.
   - **Delegated mode:** when the host supports subagents and tasks are independent, dispatch a fresh implementer with a constructed brief ([implementer prompt](../../../../agents/prompts/implementer.md)). Subagents receive only what the task needs, not the session history.
   - Review the task in two stages: **spec compliance**, then **code quality** ([task reviewer prompt](../../../../agents/prompts/task-reviewer.md)).
   - If the review fails, run the [fix loop](../../../../agents/prompts/fix-loop.md). If it passes, verify the evidence yourself, then update the task status and the ledger in the workflow state.
3. After the last task, run a whole-change review and the full gate checks against the baseline.

Continue between tasks without asking "should I continue?" unless a stop condition applies.

## Rulings instead of stalls

When a running plan meets a minor conflict, ambiguity, or plan defect, decide it, record a ruling in `DECISIONS.md`, and continue:

```
Ruling: <what was decided> — <why> — <cost if wrong>
```

The specification is binding. The plan is its argument. Judgment settles what neither answers.

## Stop conditions

Stop and ask the user only for:

1. An irreversible or destructive operation (data, Git history, infrastructure).
2. A security-sensitive action or a change to a security control.
3. A side effect outside the working tree that normally needs approval: merge, push to a shared branch, publish, deploy, external message.
4. A plan so broken that every path forward is a guess, or a scope change the user has not approved.

When blocked on one item, continue independent safe work and isolate the blocker.

## Completion

Completion requires the workflow's required outputs and gates, verified through [verification-before-completion](../../verification-before-completion/SKILL.md), and a report that distinguishes:

- what changed (paths),
- checks run, with results compared against the baseline,
- checks skipped or blocked, with reasons,
- rulings made, remaining risks, and the next action.
