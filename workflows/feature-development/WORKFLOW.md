# Feature Development Workflow

## Metadata

- ID: feature-development
- Version: 1.0.0
- Status: Experimental
- Scope: end-to-end implementation of a new or substantial product capability

## Purpose

Deliver a feature that satisfies user needs and project constraints, with appropriate design, architecture, testing, security, documentation, and release readiness.

## Triggers

- New product capability or substantial behavior.
- Cross-cutting change across modules or services.
- Significant UI flow or data-model change.

For a small isolated change, use a lighter bug-fix or implementation path instead.

## Inputs and preconditions

- User request and expected outcome.
- Accessible repository and project instructions.
- Existing project knowledge, or a scoped onboarding pass.
- Known constraints, approvals, and target environments.

## Execution strategy

Adapt stages to complexity and risk. Record a workflow instance under `.axiom/workflows/active/<ID>/`. Do not force irrelevant stages. Clarify blocking ambiguity; record reversible assumptions.

## Stages

### 1. Discovery

- **Skill:** `product-discovery` when present; otherwise orchestrator-led discovery.
- **Required:** Yes.
- **Dependencies:** none.
- **Outputs:** user problem, goals, non-goals, actors, assumptions, constraints.
- **Exit criteria:** intended outcome and success signal are understood.

### 2. Technical research

- **Skill:** `technical-research`.
- **Required:** Conditional.
- **Condition:** correctness depends on external, current, or version-specific knowledge not adequately represented in verified project context.
- **Dependencies:** stage 1.
- **Outputs:** concise research brief with authoritative sources and version scope.
- **Exit criteria:** material external assumptions are verified or recorded as unresolved.

### 3. Visual and interaction design

- **Skill:** `ui-ux-design` when present; otherwise use design guidance and existing system patterns.
- **Required:** Conditional.
- **Condition:** change affects user-facing layout, navigation, interaction, content presentation, or responsive behavior.
- **Dependencies:** stage 1; stage 2 when research is relevant.
- **Outputs:** user flows, states, responsive behavior, accessibility notes, mockups where useful.
- **Exit criteria:** interaction and visual expectations are clear enough to specify and implement.

### 4. Requirements and acceptance

- **Skill:** `requirements-analysis`.
- **Required:** Yes.
- **Dependencies:** stages 1–3 when applicable.
- **Outputs:** specification, functional/non-functional requirements, edge cases, acceptance criteria.
- **Exit criteria:** all must-have requirements are testable; assumptions and open questions are visible.

### 5. Architecture and risk

- **Skill:** `architecture-design`.
- **Required:** Yes for cross-cutting or non-trivial work; lightweight design note for simple features.
- **Dependencies:** stage 4.
- **Outputs:** component boundaries, API/data contracts, migration strategy, ADRs, security considerations.
- **Exit criteria:** implementation approach satisfies constraints and material risks have mitigation.

### 6. Planning and ownership

- **Skill:** `task-planning`.
- **Required:** Yes for multi-step work; lightweight checklist for a small change.
- **Dependencies:** stages 4 and 5.
- **Outputs:** tasks, dependencies, ownership, file scopes, integration and verification plan.
- **Exit criteria:** each task has scope, deliverable, acceptance, and verification.

### 7. Implementation

- **Skill:** `implementation`.
- **Required:** Yes.
- **Dependencies:** stage 6, or stage 5 for a small sequential change.
- **Outputs:** source changes and tests.
- **Exit criteria:** implementation meets task acceptance criteria and relevant focused checks run.

### 8. Verification and QA

- **Skill:** `testing`; use E2E, visual, accessibility, performance, or API procedures when relevant.
- **Required:** Yes.
- **Dependencies:** stage 7.
- **Outputs:** test report and evidence.
- **Exit criteria:** required checks pass or a blocker/waiver is explicitly recorded; regressions are addressed.

### 9. Security review

- **Skill:** `security-audit`.
- **Required:** Conditional risk-based review; basic secure engineering checks always apply.
- **Condition:** authentication, authorization, sensitive data, payments, external input, dependencies, infrastructure, secrets, or material attack surface changes; also execute when user/policy requires.
- **Dependencies:** stages 4–8 as applicable.
- **Outputs:** validated findings, severity, remediation, residual risks.
- **Exit criteria:** no unresolved blocking findings, or an authorized documented waiver exists.

### 10. Independent code review

- **Skill:** `code-review`.
- **Required:** Yes for substantial or security-sensitive changes; optional self-review for trivial changes.
- **Dependencies:** implementation and relevant verification.
- **Outputs:** findings-first review report and resolved findings.
- **Exit criteria:** blocking findings are fixed or explicitly escalated.

### 11. Documentation and knowledge update

- **Skill:** `project-documentation`.
- **Required:** Yes when behavior, configuration, operations, public API, or architecture changes; otherwise record why no update is needed.
- **Dependencies:** implementation and review.
- **Outputs:** updated docs, decisions, workflow state.
- **Exit criteria:** relevant living knowledge is current or marked needing review.

### 12. Delivery and release readiness

- **Skill:** `release-management`.
- **Required:** Conditional.
- **Condition:** user requests release/deployment, or delivery scope explicitly includes staging/production preparation.
- **Dependencies:** required verification, review, security, and documentation.
- **Outputs:** release notes, readiness report, staging evidence, rollback plan.
- **Exit criteria:** requested readiness evidence is complete. Production deployment or publishing still requires explicit authorization.

## Parallelization

After planning, independent tasks may run in parallel only with disjoint write scopes and satisfied dependencies. A single integrator owns shared files, conflict resolution, integration, and final verification.

## Quality gates

- Requirements and acceptance criteria are clear.
- Relevant tests and build checks have evidence.
- Review findings are resolved or disclosed.
- Risk-based security checks are complete.
- Documentation and workflow state are accurate.
- Required approvals exist for consequential actions.

## Recovery

Preserve completed valid work. If tests, review, or security checks invalidate an earlier decision, return to the relevant stage and update downstream tasks. Record failed attempts and do not erase evidence.

## State semantics

Record each stage as Pending, Ready, In Progress, Completed, Blocked, Failed, Skipped, or Cancelled. Record quality gates separately as Pending, Passed, Failed, Blocked, or Waived. A skipped stage is not a passed gate. A dependent stage may proceed after a skip only when its required inputs are independently satisfied. Use the shared [workflow state template](../../templates/workflows/workflow-state.md) for multi-stage work.

## Completion criteria

All mandatory stages are complete; applicable quality gates are passed or explicitly waived by an authorized approver; deliverables and changed files are reported; residual risks and skipped stages are disclosed. A feature workflow can finish at release-ready status without production deployment.
