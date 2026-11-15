# Release Workflow

## Metadata
- **ID:** release
- **Version:** 1.0.0
- **Status:** Experimental
- **Purpose:** Prepare a reviewable release candidate and assess readiness without assuming permission to publish or deploy.

## Triggers and non-triggers
Use when release preparation or readiness is requested. Such a request does not itself authorize publishing, tagging, pushing, or deployment unless it explicitly says so. Use feature/bug-fix workflows for changes not yet integrated.

## Inputs and preconditions
Identify target version or policy, release scope, Git state, changelog, compatibility promises, artifacts, environments, and approvals. Inspect repository release instructions and branch state.

## Adaptive stages
1. **Scope and inventory (Required; no dependencies):** identify included changes, audience, and version constraints. Output release scope.
2. **Readiness review (Required; depends on inventory):** assess checks, security, migrations, compatibility, dependencies, license, and risks. Output evidence and blockers.
3. **Prepare (Required; depends on readiness):** draft version recommendation and release notes; prepare artifacts/rollback guidance only when relevant. No external action is implied. **Output:** candidate notes and delivery plan; exit when they match the reviewed scope.
4. **Candidate verification (Required when an artifact can be built; depends on preparation):** verify checks and artifact identity. **Output:** build/check evidence or blocked/skipped rationale; exit when artifact identity and required checks are established.
5. **Approval and delivery (Conditional; depends on readiness):** present a reviewable checklist. Perform tag, push, publication, or deployment only when the user explicitly authorized that action and safeguards are satisfied. **Output:** readiness handoff or authorized action evidence; exit when requested delivery is complete or blocked.

## Dependencies and state
A stage exits only when its stated output exists and its stage-specific gate is met. Otherwise record Blocked or Failed with evidence and the next action. A dependent stage may proceed after a skipped stage only when its required inputs are independently satisfied.

Failed/Blocked required gates prevent a Ready recommendation unless an authorized waiver is recorded. Keep stage state separate from gate outcomes. Use the [workflow state template](../../templates/workflows/workflow-state.md).

## Parallelization

Independent notes/checklist review may be delegated. Version, artifact, and readiness decisions have one integrator.

## Quality gates

- Confirm scope and version rationale.
- Review verification, security, migration, and compatibility evidence.
- Match the changelog to the candidate; require action-specific authorization.

## Recovery and completion
If changes or failed checks invalidate the candidate, return to inventory/readiness and preserve prior evidence. Completion means requested readiness deliverables are complete; it does not imply a release occurred.
