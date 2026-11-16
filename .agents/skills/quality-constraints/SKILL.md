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
| `.axiom/constitution.md` | Non-negotiable principles (MUST/SHOULD) that plans are checked against | [constitution](assets/constitution.md) |
| `.axiom/CONSTRAINTS.md` | Numeric thresholds and the check that enforces each | [constraints](assets/constraints.md) |
| Definition of Done | The standing checklist every change clears | [definition of done](assets/definition-of-done.md) |

If these files already exist and the user is not changing them, read and follow them. Do not re-interview.

## Setup procedure (interactive)

1. **Inspect** the existing CI, linters, type checker, test coverage, and performance or accessibility tooling. Record which checks exist and which ones block merges.
2. **Ask which dimensions matter** (correctness, coverage, types, security, accessibility, performance, bundle size, documentation). Ask one question at a time and recommend a default.
3. **Propose numbers** when the user has none. Use the defaults in the [constraints template](assets/constraints.md) as a starting point, and mark them as defaults. The [constraint catalog](references/constraint-catalog.md) gives a default, its reason, and the enforcing command per ecosystem for complexity, size, coverage, types, lint, bundle, latency, and dependency policy. If the project fails a proposed number today, use a ratchet instead (see [ratchets and waivers](references/ratchets-and-waivers.md)).
4. **Bind each constraint to a check:** the command, where it runs (local or CI), and whether it blocks. A constraint without a check is a wish. Record it as such. Before calling a row enforced, run its command once on a known violation and once on a clean control, and confirm the exit codes. Keep the edit loop under about 5 seconds; move slow checks to task end or CI.
5. **Write** the files and link them from the project's instructions file (see the [Axiom block](../project-documentation/assets/agents-md-block.md)).

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

Exact per-language grep patterns, a diff-scoping recipe that includes untracked files, a one-shot scan, and a table for judging each hit are in [bar-lowering detection](references/bar-lowering-detection.md). Open it whenever you review a diff for a lowered bar.

Report each one with file:line, the pattern, and the requirement it undermines. The remedy is to fix the underlying issue or obtain an explicit waiver (reason, scope, approver) under the quality gate contract (`core/contracts/QUALITY-GATE-CONTRACT.md` in the Axiom repository).

## Ratchets and waivers

- **Ratchet** when the codebase cannot meet a number today: record the current value, commit, and date; fail only when it gets worse; tighten when it improves. Never set a threshold the main branch fails.
- **Waiver** when one change needs an exception: one rule, one scope, a reason, an owner, an approver who is not the author, an expiry (90 days by default), and a tracking issue. Cite the waiver ID at each suppression site.
- Loosening a threshold, a rule, or a CI stage is a separate, approved change. Tightening needs no approval.

Templates, a worked waiver example, and check scripts are in [ratchets and waivers](references/ratchets-and-waivers.md).

## Outputs and gate

Written constitution and constraints, each constraint bound to a check, or a lowered-bar report for a diff. Gate: no unapproved lowering in the change.

## References

- [Constraint catalog](references/constraint-catalog.md): measurable constraints, defaults, and commands per ecosystem
- [Ratchets and waivers](references/ratchets-and-waivers.md)
- [Bar-lowering detection](references/bar-lowering-detection.md): grep patterns per language and a one-shot scan
- [Code review](../code-review/SKILL.md) step 6
- [Definition of done](assets/definition-of-done.md)
