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

## Scope mode

The plan states one scope mode in a `Scope mode:` line under Scope. The default is **hold**.

| Mode | Plan does | Use when |
|---|---|---|
| **hold** | Exactly the approved scope; nothing added, nothing cut | Default; the spec is approved and the request is clear |
| **selective** | Holds the scope, but expands only the parts the user named | The user asks to go further on one area ("also harden the parser") |
| **expand** | Adds closely related work the plan found (adjacent gaps, tests, cleanup) | The user asks for a fuller job, and each addition is listed for approval |
| **reduce** | Cuts to the smallest slice that still delivers value; the rest is listed as deferred | Time or risk is tight, or the user asks for an MVP or a first slice |

Expanded or deferred items are listed by name under Scope. An item outside the mode needs the user's approval or a spec change, not a silent addition.

## Procedure

1. **Constitution check.** List each MUST principle as pass, fail, or not applicable. Justify unavoidable violations in a complexity-tracking table (see the [constitution template](../quality-constraints/assets/constitution.md)).
2. **File map first.** List the files to create or modify and each file's single responsibility. Follow existing patterns. Files that change together live together. Copy exact spec values (limits, names, messages, units) into a short **Global constraints** section under Scope.
3. **Decompose into tasks.** A task is the smallest unit that carries its own test cycle and is worth a reviewer's gate. Fold setup, configuration, and documentation into the task whose deliverable needs them. Aim for S–M tasks (1–5 files plus tests); split anything larger. Prefer vertical slices (one behavior through every layer) over horizontal layers. See [sizing and ordering](references/sizing-and-ordering.md) for split and merge rules.
4. **Order by dependency.** Put setup first, then foundations, then stories in priority order (P1 first, as a viable increment), then polish. Put the riskiest task early within each level. Every task leaves the build green. Add a checkpoint (full gate plus one end-to-end check) after every 2–4 tasks and after each priority level. Mark tasks that can run in parallel with `[P]`: different files, no unmet dependency, and no shared contract change. Migrations are never `[P]`.
5. **Specify each task:**
   - ID, title, story or requirement IDs covered (`US1`, `FR-003`), and `[P]` if parallel-safe.
   - Exact file paths, and the allowed, restricted, and shared files when delegating.
   - Interfaces: names and signatures decided here, as **Produces** and **Consumes** lines so neighboring tasks use identical names.
   - Steps, one checkable action each: write the failing test → run it (expect failure) → implement → run it (expect pass) → commit.
   - Verification command and expected result.
6. **Map coverage.** Every must-have requirement maps to at least one task. Every task maps to a requirement or a recorded technical need.
7. **Record risks**, the integration order, and the shared-file owner.
8. **Self-check** against the Ready for Development standard below and the [plan anti-patterns](references/plan-anti-patterns.md) (including its grep checks for placeholders, missing verify lines, and uncited requirement IDs). For non-trivial plans, request a plan review ([code-review](../code-review/SKILL.md) plan mode) or run [spec-analysis](../spec-analysis/SKILL.md).

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

`PLAN.md` from the [plan template](assets/PLAN.md), with frontmatter `status`, a `Scope mode:` line, a constitution check, a file map, a task table, a coverage map, risks, and the integration order.

## References

- [Plan template](assets/PLAN.md), [task template](assets/TASK.md)
- [Sizing and ordering](references/sizing-and-ordering.md): open when drawing task boundaries, choosing slices, ordering, marking `[P]`, or picking verification commands per stack.
- [Worked plan](references/worked-plan.md): open before writing your first plan, or to calibrate detail; a full ready plan built from a real spec.
- [Plan anti-patterns](references/plan-anti-patterns.md): open during the self-check (step 8).
- [How an executor consumes a plan](references/executing-a-plan.md): open to check the plan gives an executor what it needs (checkpoints, stop conditions, evidence), or when executing a plan yourself.
- [Execution loop](../axiom-orchestrator/references/execution.md)
