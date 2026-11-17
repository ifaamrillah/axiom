# Implementer Prompt

Template for dispatching one task to a fresh implementer subagent. The coordinator fills in every `<...>` slot. The subagent receives only this brief, not the session history, so include everything it needs and nothing it does not.

In a workflow instance, save the filled brief as `.axiom/workflows/active/<ID>/tasks/<n>-brief.md` and dispatch with one line: "Read and follow `<brief path>`; write your report to `<report path>`." Do not paste the brief as well.

```text
You are implementing one task in an existing codebase. Work only on this task.

## Task
<task ID and title>
<task text from the plan, including steps>

## Acceptance
<Given/When/Then scenarios or checks this task must satisfy>

## Context you need
- Repository instructions: <path to AGENTS.md/CLAUDE.md>; follow them.
- Relevant interfaces and conventions: <quoted signatures, patterns, file excerpts or paths>
- Constraints: <constitution principles, quality constraints that apply>
- Verification baseline: <pre-existing failures to ignore, or "none">
- Base commit: <SHA recorded before dispatch>

## Files
- Allowed to modify: <paths>
- Allowed to create: <paths>, and your report file <report path or "none">
- Read-only: <paths>, and this brief
- Do not touch: everything else. If you need a change outside these files, stop and report it.

## Method
1. Before writing code, ask any question that blocks you, and wait for the answer.
2. Use test-first: write the failing test, run it, see it fail for the right reason, implement the minimum, run it again.
3. Keep the change surgical. Match the existing style. Make no unrelated edits.
4. Run: <focused verification command(s)>.
5. Self-review your diff: scope, edge cases, leftover debug code, weakened tests.
6. Commit with message: <convention or "do not commit">.

## Report (exact format)
While working on a long task, you may keep "Status: WORKING — <current step>" as the
first line of the report file. Replace it with the final status when you stop.
Status: DONE | DONE_WITH_CONCERNS | BLOCKED | NEEDS_CONTEXT
Files changed: <paths>
Tests added/changed: <names>
Commands run and results: <command → result, after the final edit>
Concerns or deviations: <list, or "none">
```

## Coordinator notes

- Answer questions before letting the implementer proceed. Do not let it guess.
- Treat `DONE` as a claim. Inspect the diff and rerun the verification before dispatching review.
- `BLOCKED` or `NEEDS_CONTEXT`: supply the missing context or re-plan. Do not push the subagent to finish anyway.
- `WORKING` is a heartbeat, not a result. Never review a task whose report still says `WORKING`.
- For a new round, write a new brief file (`<n>-brief-r<round>.md`) that states what changed. Do not edit a dispatched brief.
