---
name: quality-constraints
description: Establish a project's quality bar as a written, numeric contract (constitution, constraints, definition of done) and detect when a change quietly lowers it, such as skipped or deleted tests, removed assertions, new lint or type suppressions, or relaxed thresholds. Use when no quality bar is written down, when asked to set up standards or quality gates, before autonomous execution, or when an agent is silencing checks to get to green.
---

# Quality Constraints

## Purpose

Other skills describe what good looks like. This skill records what **this project** treats as good enough to ship, with numbers, in files that outlive the session and can be checked mechanically. An agent can write more code than anyone will read, so the bar must live in checks, not memory.

## Artifacts

| File | Holds | Template |
|---|---|---|
| `.axiom/constitution.md` | Non-negotiable principles (MUST/SHOULD) that plans are checked against | [constitution](../../../templates/project/constitution.md) |
| `.axiom/CONSTRAINTS.md` | Numeric thresholds and the check that enforces each | [constraints](../../../templates/project/constraints.md) |
| Definition of Done | The standing checklist every change clears | [definition of done](../../../core/standards/definition-of-done.md) |

If these files already exist and the user is not changing them, read and follow them. Do not re-interview.

## Setup procedure (interactive)

1. **Inspect** the existing CI, linters, type checker, test coverage, and performance or accessibility tooling. Record which checks exist and which ones block merges.
2. **Ask which dimensions matter** (correctness, coverage, types, security, accessibility, performance, bundle size, documentation). Ask one question at a time and recommend a default.
3. **Propose numbers** when the user has none. Use the defaults in the [constraints template](../../../templates/project/constraints.md) as a starting point, and mark them as defaults.
4. **Bind each constraint to a check:** the command, where it runs (local or CI), and whether it blocks. A constraint without a check is a wish. Record it as such.
5. **Write** the files and link them from the project's instructions file (see the [Axiom block](../../../templates/project/agents-md-block.md)).

In non-interactive contexts (CI or autonomous runs), do not interview. Apply the floor below, record that defaults were used, and flag the rest for a human.

## Floor (always applies)

- Existing tests are not skipped, deleted, or weakened to reach green.
- No new type or lint suppression without an inline reason and owner approval.
- Thresholds are never lowered in the same change that would otherwise fail them.
- Every new behavior has a test, or a recorded reason why it cannot have one.
- TODO stubs and placeholder returns are not reported as complete work.

## Detecting a lowered bar

Inspect the diff (and the CI configuration diff) for these patterns. Each one is a finding unless it is justified and approved.

| Pattern | Examples |
|---|---|
| Suppressions | `@ts-ignore`, `@ts-expect-error`, `eslint-disable`, `# type: ignore`, `# noqa`, `#[allow(...)]`, `//nolint`, `@SuppressWarnings` |
| Skipped or focused tests | `.skip`, `xit`, `@unittest.skip`, `pytest.mark.skip`, `t.Skip()`, `@Disabled`, `.only` left in |
| Deleted or emptied tests | removed test files or cases; assertions replaced by `pass`/`return` |
| Weakened assertions | exact → `toBeTruthy`, equality → `assertIsNotNone`, snapshot regenerated without review |
| Swallowed errors | new broad `catch {}`, `except Exception: pass`, ignored error returns |
| Relaxed thresholds | coverage, performance budget, lint level, or `--max-warnings` lowered; CI step made non-blocking (`continue-on-error`, `|| true`) |
| Stubs | `NotImplementedError`, `todo!()`, `throw new Error("TODO")` in code reported as done |

Report each one with file:line, the pattern, and the requirement it undermines. The remedy is to fix the underlying issue or obtain an explicit waiver (reason, scope, approver) under the [quality gate contract](../../../core/contracts/QUALITY-GATE-CONTRACT.md).

## Outputs and gate

Written constitution and constraints, each constraint bound to a check, or a lowered-bar report for a diff. Gate: no unapproved lowering in the change.

## References

- [Code review](../code-review/SKILL.md) step 6
- [Definition of done](../../../core/standards/definition-of-done.md)
