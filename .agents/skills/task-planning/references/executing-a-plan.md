# How an Executor Consumes a Plan

Write plans for this reader. This page describes what an executing agent (you later, or a fresh implementer) does with a `status: ready` plan, so the plan gives it what it needs. The orchestration loop itself (inline vs delegated, two-stage review, baseline, rulings) is in axiom-orchestrator's [execution reference](../../axiom-orchestrator/references/execution.md). This page covers the plan-facing side.

## Before task 1

1. **Check status.** Execute only a plan with `status: ready`. If it says `draft` or `blocked`, return to planning.
2. **Read the spec too.** The spec is binding. The plan argues from it. When they conflict, the spec wins and the conflict is recorded as a ruling.
3. **Read Global constraints once.** They apply to every task even when a task does not repeat them.
4. **Resume, do not restart.** Look for a progress ledger and `git log`. Tasks with a completion record and a commit are done. Do not redo them after a context reset.
5. **Pre-flight interface scan.** For each task that consumes something an earlier task produces, compare names and types. Record mismatches and rule on them before starting.
6. **Record the baseline.** Run the full gate once and note pre-existing failures.

## Per task

```text
read task → mark in-progress → for each step:
    do the step
    run the step's check
    compare the output with the plan's expected result
        match     → next step
        mismatch  → is the plan wrong or the code wrong?
                    plan wrong → ruling, then continue
                    code wrong → debug, then continue
→ run the task's Verify command → commit → record done in the ledger
```

- **Expected FAIL must actually fail, for the stated reason.** A test that passes before the code exists is testing nothing. Fix the test.
- **Read every output.** Do not assume a command passed because it exited.
- **Stay in the file list.** Touching a file outside the task's files is a scope change. If it is needed, record a ruling with the reason.
- **Do not improve neighbors.** Refactors and fixes outside the task go in the ledger as follow-ups.
- **Mark done only with evidence:** the verify command's output, not the feeling of being finished.

## At a checkpoint

Run everything the checkpoint lists: full test suite, lint, build, the end-to-end check, and any load or accessibility check. Then:

| Result | Action |
|---|---|
| All pass | Record evidence; continue to the next task |
| New failure vs baseline | Fix before continuing; the last task is the first suspect |
| Only baseline failures | Report them as pre-existing; continue |
| Checkpoint asks for human review | Stop and present evidence; wait |

A checkpoint is also the safest place to stop if time runs out: the system works and the delivered slices have value.

## When to keep going and when to stop

Keep going without asking for:
- a small plan defect with an obvious fix (a typo in a path, a missing import step),
- an ambiguity that the spec answers,
- a choice the plan left open that the tests constrain.

Record each as `Ruling: <decision> — <why> — <cost if wrong>`.

Stop and ask for:
1. an irreversible or destructive action (data deletion, history rewrite, production change),
2. a security-sensitive change,
3. a side effect outside the working tree (push to a shared branch, merge, publish, deploy, external message),
4. a plan so broken that every path is a guess, or a change that alters spec scope.

When blocked on one task, continue with independent tasks whose dependencies are met, and report the blocker.

## Signs the plan itself is wrong

| Symptom | Likely plan defect | Response |
|---|---|---|
| Two tasks need the same function with different signatures | Interface drift | Rule in favor of the producer's signature; update consumer |
| A test from the plan cannot fail | Test checks setup, not behavior | Rewrite the assertion against the spec value |
| A task needs a file no task creates | Missing task | Add the minimal step to the current task; record the ruling |
| The spec value in a step differs from the spec | Copy error | Follow the spec; record it |
| Three or more rulings in one task | Task under-specified | Finish, then flag the plan for review before the next task |
| A step would change spec scope | Plan overreach | Stop; ask |

## What the executor reports at the end

- Tasks completed, with commit IDs.
- Verify and checkpoint commands with results, compared with the baseline.
- Rulings made.
- Skipped or blocked tasks with reasons.
- Follow-ups noticed but not done.

Then run spec-analysis in converge mode if the workflow asks for it.

## What this means for the plan writer

| The executor needs | So the plan must have |
|---|---|
| To know the task is done | An exact verify command and expected output |
| To check a test fails correctly | "Expect FAIL with <reason>" |
| To avoid name drift | Produces and Consumes lines with signatures |
| A safe place to stop | Checkpoints after each priority level |
| To stay in scope | A file list per task and a shared-file owner |
| To resolve conflicts | A link to the spec and a Global constraints section |

Sources: adapted from obra/superpowers (MIT) `skills/executing-plans/SKILL.md`, github/spec-kit (MIT) `templates/commands/implement.md`, addyosmani/agent-skills (MIT) `skills/planning-and-task-breakdown/SKILL.md`, and general practice.
