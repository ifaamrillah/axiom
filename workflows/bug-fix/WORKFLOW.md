# Bug Fix Workflow

## Metadata
- **ID:** bug-fix
- **Version:** 1.0.0
- **Status:** Experimental
- **Purpose:** Diagnose and correct a specific defect while limiting unintended behavior changes.

## Triggers and non-triggers
Use for an observed failure, regression, or behavior that differs from an agreed expectation. Use Feature Development for new behavior or a fix that materially changes requirements. Use Security Audit when assessment of a security boundary is primary.

## Inputs and preconditions
Expected and observed behavior, impact, environment, reproduction if available, repository instructions and Git state, relevant code/configuration/tests, and authorization for any sensitive or production data.

## Adaptive stages
1. **Triage (Required; no dependencies):** establish impact, scope, reproducibility, and affected versions. Output a defect brief. Exit when expected and observed behavior are clear enough to investigate; otherwise record unknowns.
2. **Inspect (Required; depends on triage):** inspect relevant code, recent changes, configuration, and tests; use debugging and codebase exploration as needed. Output evidence and candidate causes. Exit when a cause is supported or the issue is explicitly unresolved.
3. **Repair (Required when a cause is supported; depends on inspection):** write a failing regression test that shows the symptom ([tdd](../../.agents/skills/tdd/SKILL.md)), then make the smallest root-cause change. No fix without a confirmed root-cause hypothesis ([debugging](../../.agents/skills/debugging/SKILL.md)); after three failed fixes, return to inspection. Output a focused change and regression check.
4. **Verify and review (Required; depends on repair):** run authorized focused checks, inspect neighboring behavior and final diff, and apply security review when the defect affects a security boundary. Output evidence and limitations.
5. **Document and deliver (Required; depends on verification):** update knowledge if behavior, operations, or risk changed. **Output:** a verdict, cause, fix, evidence, remaining uncertainty, and documentation links; exit when the handoff is accurate. Verdict is one of: **verified** (the regression check failed before and passes after, and neighboring checks pass), **partial** (the symptom is gone, but a check could not run or a related case is still open), or **failed** (the symptom remains).

## Dependencies and state
A stage exits only when its stated output exists and its stage-specific gate is met. Otherwise record Blocked or Failed with evidence and the next action. A dependent stage may proceed after a skipped stage only when its required inputs are independently satisfied.

If reproduction is unavailable, record that limitation and proceed only where static evidence supports a safe fix. A failed or blocked check is never Passed. Record statuses and gates in the shared [workflow state template](../../templates/workflows/workflow-state.md) for multi-step work; short fixes may use a concise checklist.

## Parallelization

Diagnosis and repair normally have one owner. Independent read-only investigation may be delegated after scope and evidence requirements are explicit. Do not have multiple workers edit the same repair area.

## Quality gates

- A cause is evidence-backed or unresolved status is disclosed.
- The repair addresses the cause and stays within scope.
- Checks and limitations are reported; production data is not used without authorization.

## Recovery and completion
Preserve investigation evidence. Resume from the earliest invalid stage if new evidence changes the cause. Complete when repair and required checks are reported, or return Blocked/Failed with the blocker and next action.
