# Task

## Identity

- ID:
- Title:
- Status: Pending
- Priority:
- Owner:

## Scope

### Allowed files

-

### Restricted files

-

### Shared files

-

## Inputs

-

## Dependencies

-

## Deliverables

-

## Acceptance criteria

-

## Verification

- Method:
- Evidence:

## Blockers and next action

- Blockers:
- Next action:

## Delegation brief

When this task is delegated, the coordinator writes the brief to `.axiom/workflows/active/<ID>/tasks/<n>-brief.md` and dispatches with that path. The worker writes `tasks/<n>-report.md`. A dispatched brief is never edited; a fix round gets `<n>-brief-r<round>.md`.

```markdown
# Brief <n>: <one-line goal>

## TASK
<context and the spec lines that matter>

## DELIVERABLE
- <observable result>

## SCOPE
- Owned (write): <paths>, plus tasks/<n>-report.md
- Do not touch: <paths>
- Shared (read only): <paths>

## VERIFY
- Commands: <exact commands>
- Base commit: <SHA>
- Baseline: <pre-existing failures, or "clean">

## REPORT
Status: WORKING (optional heartbeat) | DONE | DONE_WITH_CONCERNS | NEEDS_CONTEXT | BLOCKED
Then: changed files, commands run with results, concerns. Under 40 lines.
```
