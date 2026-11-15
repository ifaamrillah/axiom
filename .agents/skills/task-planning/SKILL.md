---
name: task-planning
description: Convert an approved specification and architecture into a Ready-for-Development plan of small, dependency-ordered tasks with exact file paths, owners, acceptance, and verification steps. Use before multi-step or delegated implementation, or to check whether an existing plan is ready to execute.
---

# Task Planning

## Purpose

Write the plan for an engineer who has never seen this codebase or spec. They can write idiomatic code once they know the exact interface and the exact test. What they cannot know is what you decided: which files, which names and signatures, which values from the spec, and which tests prove each task. Write those down.

## Inputs

An approved or clarified spec, architecture notes or ADRs, the constitution and constraints, and the current code structure. If must-have requirements still carry `[NEEDS CLARIFICATION]`, return to [requirements-analysis](../requirements-analysis/SKILL.md).

## Scope standard

A plan targets **one user-facing goal**. Split into separate plans only when parts are independently shippable deliverables, meaning each could be reviewed, tested, and merged on its own. Do not split on the word "and", and do not split cross-layer work inside one goal.

- Split: "add a dark mode toggle AND migrate auth to JWT AND build an admin dashboard".
- Do not split: "add validation and show the errors".

Keep the plan concise enough to hold in context. If it grows past a few pages, the scope is probably too large.

## Procedure

1. **Constitution check.** List each MUST principle as pass, fail, or not applicable. Justify unavoidable violations in a complexity-tracking table (see the [constitution template](../../../templates/project/constitution.md)).
2. **File map first.** List the files to create or modify and each file's single responsibility. Follow existing patterns. Files that change together live together.
3. **Decompose into tasks.** A task is the smallest unit that carries its own test cycle and is worth a reviewer's gate. Fold setup, configuration, and documentation into the task whose deliverable needs them.
4. **Order by dependency.** Put setup first, then foundations, then stories in priority order (P1 first, as a viable increment), then polish. Mark tasks that can run in parallel with `[P]`: different files and no unmet dependency.
5. **Specify each task:**
   - ID, title, story or requirement IDs covered (`US1`, `FR-003`), and `[P]` if parallel-safe.
   - Exact file paths, and the allowed, restricted, and shared files when delegating.
   - Interfaces: names and signatures decided here.
   - Steps, one checkable action each: write the failing test → run it (expect failure) → implement → run it (expect pass) → commit.
   - Verification command and expected result.
6. **Map coverage.** Every must-have requirement maps to at least one task. Every task maps to a requirement or a recorded technical need.
7. **Record risks**, the integration order, and the shared-file owner.
8. **Self-check** against the Ready for Development standard below. For non-trivial plans, request a plan review ([code-review](../code-review/SKILL.md) plan mode) or run [spec-analysis](../spec-analysis/SKILL.md).

## Ready for Development standard

A plan is ready when it is:

- **Actionable:** every task has file paths and a specific action.
- **Logical:** tasks are ordered by dependency, and `[P]` marks are correct.
- **Testable:** acceptance uses Given/When/Then or an equivalent observable check, and each task names its verification command.
- **Complete:** no TBD, TODO, "similar to above", or placeholder remains.
- **Sufficient:** no known requirement, dependency, or implementation gap remains open.
- **Coherent:** no contradictions with the spec, the constitution, or itself.

Set the plan frontmatter `status: ready` only when all six hold.

## Outputs

`PLAN.md` from the [plan template](../../../templates/workflows/PLAN.md), with frontmatter `status`, a constitution check, a file map, a task table, a coverage map, risks, and the integration order.

## References

- [Plan template](../../../templates/workflows/PLAN.md), [task template](../../../templates/workflows/TASK.md)
- [Execution loop](../axiom-orchestrator/references/execution.md)
