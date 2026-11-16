# Refactoring Workflow

## Metadata
- **ID:** refactoring
- **Version:** 1.0.0
- **Status:** Experimental
- **Purpose:** Improve internal structure while preserving externally observable behavior.

## Triggers and non-triggers
Use when structural improvement is the goal and behavior should remain stable. If behavior or requirements change, use Feature Development. Use Bug Fix when correction is primary.

## Inputs and preconditions
Identify structural goal, affected boundaries, behavior to preserve, repository instructions, current work, and available verification. Establish a baseline where feasible.

## Adaptive stages
1. **Scope and inspect (Required; no dependencies):** inspect call sites, boundaries, tests, current work, and patterns. Map dependents with [blast radius](../../.agents/skills/code-review/references/blast-radius.md) and record the verification baseline. Output scope, invariants, and the classified dependent list.
2. **Design (Conditional; depends on inspection):** required for cross-module or API changes; otherwise choose a small sequence. Output target structure and compatibility constraints.
3. **Plan and refactor (Required; depends on scope, and design when required):** make small behavior-preserving steps and exclude feature work. **Output:** incremental structural changes; exit when the intended structure is reached without scope expansion.
4. **Verify (Required; depends on refactor):** run relevant checks and compare behavior/final diff. **Output:** verification evidence and gaps; exit when behavior-preservation claims are supported or qualified.
5. **Document and deliver (Conditional; depends on verification):** update architecture/conventions when rationale or boundaries materially change; otherwise record why not. **Output:** current docs or a no-change rationale; exit when the handoff reflects repository state.

## Dependencies and state
A stage exits only when its stated output exists and its stage-specific gate is met. Otherwise record Blocked or Failed with evidence and the next action. A dependent stage may proceed after a skipped stage only when its required inputs are independently satisfied.

Do not begin dependent edits when preservation constraints are unclear. Stage statuses: Pending, Ready, In Progress, Completed, Blocked, Failed, Skipped, Cancelled. Gate outcomes: Pending, Passed, Failed, Blocked, Waived. Use the [workflow state template](../../templates/workflows/workflow-state.md) for multi-step work.

## Parallelization

Use one editor for overlapping modules. Independent inventory/read-only review may be delegated by path.

## Quality gates

- The structural goal and preserved behavior are explicit.
- Edits are incremental; behavior-preservation claims have evidence.
- Architecture docs are updated for material changes.

## Recovery and completion
If verification reveals changed behavior, revert or switch to Feature Development and update scope. Preserve completed safe steps. Complete when required checks and limitations are reported.
