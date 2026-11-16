---
status: draft          # draft | ready | in-progress | in-review | done | blocked | dropped
spec: <path to spec.md or "inline">
updated: <YYYY-MM-DD>
blocked_reason: ""
---

# Plan: <feature>

> Execute task by task with the Axiom execution loop (inline, or one fresh implementer per task with a two-stage review). Steps use checkboxes for tracking.

## Outcome

One user-facing goal, stated as an observable result.

## Scope

- In scope:
- Out of scope:

## Constitution check

| Principle | Result | Note |
|---|---|---|
| I. <name> | pass / fail / n.a. | |

### Complexity tracking (only for justified violations)

| Violation | Why needed | Simpler alternative rejected because |
|---|---|---|

## File map

| Path | New/Modify | Responsibility |
|---|---|---|

## Tasks

`[P]` = parallel-safe (different files, no unmet dependency).

### T001 <title> — covers FR-001, US1

- Files: `src/...` (modify), `tests/...` (new)
- Interface: `<signature decided here>`
- Depends on: none
- Steps:
  - [ ] Write the failing test `<test name>` in `<path>`
  - [ ] Run `<command>`; expect failure `<reason>`
  - [ ] Implement `<smallest change>`
  - [ ] Run `<command>`; expect pass
  - [ ] Commit `<message>`
- Verify: `<command>` → `<expected result>`

### T002 [P] <title> — covers …

…

## Coverage map

| Requirement | Tasks |
|---|---|
| FR-001 | T001 |

## Risks and mitigations

| Risk | Impact | Mitigation | Owner |
|---|---|---|---|

## Integration order and shared files

Shared-file owner: <role>. Integration order: <T001 → T003 → …>.
