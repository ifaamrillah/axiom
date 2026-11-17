# Stage 7: Implementation

**Skill:** `implementation`, `tdd` · **Required:** yes · **Depends on:** stage 6 (or 5 for a small sequential change)

## Do

1. Record the verification baseline before the first edit.
2. Execute tasks in order using the execution loop: inline, or one fresh implementer per task with a two-stage review (spec compliance, then quality). A delegated task gets a brief file at `tasks/<n>-brief.md`, dispatched by path; a re-review after a fix uses a fresh reviewer scoped to the fix delta.
3. Record rulings for minor decisions when they are made, and continue. Stop only on the stop conditions.
4. Update the task ledger after each verified task, with evidence. Each one is a checkpoint.

## Exit

Every task meets its acceptance with fresh evidence, and no new failures appear compared with the baseline.
