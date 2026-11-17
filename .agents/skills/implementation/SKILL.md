---
name: implementation
description: Implement an approved software change in an existing codebase while following repository conventions, keeping diffs scoped, and verifying behavior with relevant tests and checks. Use after requirements and planning are sufficient for the change's complexity.
---

# Implementation

## Purpose

Turn an approved plan into a small, correct, reviewable diff. Build in thin slices. Verify each slice before the next. Match the codebase you are in, not the codebase you would prefer.

## When to open the references

| Need | Open |
|---|---|
| Slice the work, run the step and verify loop, see a worked example, decide whether a refactor fits | [slicing and the verify loop](references/slicing-and-loop.md) |
| Discover the repository's conventions and commands; error handling, logging, and configuration rules | [conventions and code rules](references/conventions-and-code-rules.md) |
| Before writing new code; marking a deliberate shortcut; simplifying existing code | [simplicity](references/simplicity.md) |
| Final checks, cleanup, commit hygiene, and the PR description | [finishing a branch](references/finishing-a-branch.md) |

## Procedure

1. **Read instructions and code.** Read repository instructions (`AGENTS.md`, `CLAUDE.md`, `CONTRIBUTING.md`), then the files you will touch, their tests, and one similar existing feature. Find the exact test, lint, type-check, and build commands.
2. **Confirm scope.** Restate the task, acceptance criteria, and the files you own. List what is out of scope. If the plan is missing or vague for a multi-file change, stop and plan first (see [task-planning](../task-planning/SKILL.md)).
3. **Record a baseline.** Run the focused tests and checks before editing. Note pre-existing failures so you do not claim or hide them later.
4. **Slice.** Split the work into slices that each leave the build green and can be verified alone. Prefer vertical slices; put the riskiest unknown first.
5. **Loop per slice:**
   1. Write or update the test for the slice and watch it fail for the right reason (see [tdd](../tdd/SKILL.md)).
   2. Write the smallest code that makes it pass, in the local style. Climb the [decision ladder](references/simplicity.md#decision-ladder) first: reuse, stdlib, or an installed dependency beats new code. Mark deliberate limits with a `shortcut:` comment.
   3. Run the focused test, then the affected checks (type check, lint).
   4. Read your own diff for the slice. Fix anything unrelated or accidental.
   5. Commit the slice if the workflow uses commits per slice.
6. **Handle deviations.** If the plan is wrong (an interface does not exist, a step contradicts the spec), choose the smallest change that satisfies the spec, record the decision and its reason, and continue. If the deviation changes scope, architecture, or a public contract, stop and ask.
7. **Run the full relevant checks** at the end: full test suite or the affected packages, lint, type check, build. Compare with the baseline.
8. **Review the whole diff** for scope creep, debug output, secrets, commented-out code, missed edge cases, and missing docs.
9. **Update documentation and state** that the change affects: README, API docs, changelog entry if the project keeps one, workflow state files.
10. **Report** what changed, the exact commands run with their decisive output lines, deviations, and follow-ups noticed but not done. End with the fixed closing block: `Not checked:` (what was not run or verified, or "none") and `Risk:` (the main residual risk, or "none known").

## Slice size limits

- Run tests at least every ~50-100 changed lines. More than that without a run is a red flag.
- One logical change per slice. A refactor, a feature, and a config change are three slices.
- After each slice the project builds and existing tests pass.
- If a slice keeps growing, split it or stop and re-plan.

## Scope discipline

Touch only what the task needs. When you notice something worth fixing outside scope, write it down instead of fixing it:

```
Noticed, not changed:
- src/utils/date.ts: parseDate ignores time zones (separate bug).
- OrderService has two unused imports.
```

Refactor inside a task only when the refactor is needed to make the change possible or safe, and keep it in its own slice with tests green before and after. See [slicing and the verify loop](references/slicing-and-loop.md) for limits.

## Red flags

| Red flag | Do instead |
|---|---|
| Writing many files before running anything | Stop. Run the focused test now; shrink the slice. |
| "I'll add tests at the end" | Write the test for this slice now. |
| New helper, base class, or config option for one use | Inline it. Abstract at the third real use. |
| Reformatting or renaming in files you only read | Revert those hunks. |
| Catching an exception and ignoring it to make a test pass | Find the cause; handle the error deliberately or let it propagate. |
| Editing or skipping a failing test so the suite goes green | Fix the code, or report the failure. Never weaken tests. |
| A new dependency for a few lines of code | Write the few lines, or justify the dependency and ask. |
| "Tests passed earlier" after more edits | Run them again on the current tree. |
| Plan deviation made silently | Record the deviation and why in the report. |

## Rules

Do not broaden scope without coordination. Do not claim tests passed without executing them; apply [verification-before-completion](../verification-before-completion/SKILL.md) before reporting. Compare check results against the recorded baseline. Avoid needless abstraction, dependency changes, and unrelated formatting. Never skip, delete, or weaken tests, or add suppressions, to reach green (see [quality-constraints](../quality-constraints/SKILL.md)). For new behavior, prefer [tdd](../tdd/SKILL.md). For external library APIs, check the installed version's docs with [technical-research](../technical-research/SKILL.md) instead of recalling them.

## Report format

```
Changed: <files and one line each>
Checks:
- npm test -- src/orders  -> 24 passed
- npx tsc --noEmit        -> 0 errors
- npm run lint            -> clean
Deviations: used existing Money type instead of number (plan assumed none existed)
Follow-ups noticed: parseDate time-zone bug in src/utils/date.ts
Not checked: e2e suite (needs staging DB)
Risk: rounding of mixed-currency carts is covered by unit tests only
```

The last two lines are always present, in that order. Write `Not checked: none` or `Risk: none known` rather than leaving one out.
