# Workflow State

## Identity

- Workflow ID:
- Workflow:
- Title:
- Overall status: Pending
- Created:
- Updated:
- Owner:

## Current execution

- Current stage:
- Current task:
- Execution mode: Sequential / Native parallel / Mixed
- Target outcome:

## Stage status

| Stage | Status | Gate outcome | Evidence / notes |
|---|---|---|---|
| | Pending | Pending | |

Stage status values: Pending, Ready, In Progress, Completed, Blocked, Failed, Skipped, Cancelled.

Gate outcomes: Pending, Passed, Failed, Blocked, Waived. Skipped stages are not gate outcomes and must never be represented as Passed.

## Blockers

- None.

## Decisions and assumptions

See `DECISIONS.md` or linked ADRs. Record assumptions that affect scope or downstream work.

## Latest evidence

- Not yet recorded.

## Next action

- Define the next concrete action.

## Known risks

- Not yet assessed.
