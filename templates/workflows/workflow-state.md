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
- Base commit:
- Customization layers: canonical only / list overrides, overlays, and hooks applied

## Stage status

| Stage | Status | Gate outcome | Evidence / notes |
|---|---|---|---|
| | Pending | Pending | |

Stage status values: Pending, Ready, In Progress, Completed, Blocked, Failed, Skipped, Cancelled.

Gate outcomes: Pending, Passed, Failed, Blocked, Waived. Skipped stages are not gate outcomes and must never be represented as Passed.

## Verification baseline

Recorded before the first edit. Gates compare against it: no new failures.

- Command(s):
- Commit:
- Date:
- Pre-existing failures: none recorded.

## Task ledger

| Task | Status | Brief / report | Commit/diff | Review (spec / quality) | Evidence |
|---|---|---|---|---|---|
| | | | | | |

## Checkpoints

Write state at each checkpoint; compaction or a new session is safe only here, never mid-edit.

| Checkpoint | Date | Commit | State written |
|---|---|---|---|
| After research | | | |
| After spec approval | | | |
| After plan approval | | | |
| After task <n> verified | | | |

On resume, trust in this order: this file, then the ledger, briefs, reports, and `DECISIONS.md`, then Git since the base commit, then the transcript. Report any conflict before acting.

## Blockers

- None.

## Decisions and assumptions

See `DECISIONS.md` or linked ADRs. Record assumptions that affect scope or downstream work. Append each decision when it is made; never rewrite an earlier entry.

## Latest evidence

- Not yet recorded.

## Next action

- Define the next concrete action.

## Known risks

- Not yet assessed.
