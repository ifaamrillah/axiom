# Definition of Done

A standing bar that every change clears. Acceptance criteria vary per task and answer "did we build this thing?" The Definition of Done is the same for every change and answers "is it finished to our standard?" A task is done only when both are satisfied.

Projects may extend this list in `.axiom/CONSTRAINTS.md`. They should not shorten it silently.

## Correctness

- [ ] Every acceptance criterion is met and verified with evidence.
- [ ] New behavior has tests that fail without the change and pass with it.
- [ ] Existing tests pass, or failures match the recorded baseline exactly.
- [ ] Error paths and boundaries are handled, not only the happy path.

## Quality

- [ ] The change is scoped to the task; no unrelated refactors.
- [ ] No debug output, commented-out code, or orphaned code from this change.
- [ ] No unapproved lowering of the quality bar (see [quality-constraints](../../.agents/skills/quality-constraints/SKILL.md)).
- [ ] Lint, format, and type checks pass at the project's thresholds.

## Integration

- [ ] Migrations, configuration, and feature flags are accounted for, with a rollback path.
- [ ] Backward compatibility is considered for public interfaces and persisted data.
- [ ] Security-relevant changes were reviewed proportionately to risk.

## Knowledge

- [ ] Documentation affected by the change is updated, or the report states why none is needed.
- [ ] Decisions and rulings are recorded; workflow state reflects reality.
- [ ] The report lists checks run, checks not run, and remaining risks.
