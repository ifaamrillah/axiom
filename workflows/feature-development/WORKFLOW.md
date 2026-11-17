# Feature Development Workflow

## Metadata

- ID: feature-development
- Version: 1.1.0
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
- Accessible repository and project instructions (including the Axiom kernel).
- Existing project knowledge, or a scoped onboarding pass.
- Constitution and constraints when present; known approvals and target environments.

## Execution strategy

**Step-file loading:** this file is the index. Read only the current stage's file in `stages/` when you enter that stage; do not preload the others. Record a workflow instance under `.axiom/workflows/active/<ID>/` with the [workflow state](../../templates/workflows/workflow-state.md). Apply a project overlay (`.axiom/workflows/overlays/feature-development.md`) and stage hooks from `.axiom/config.md` when present. To resume, read the state and the plan's `status:` frontmatter, check them against the ledger, decisions, and Git, report any conflict, then open the stage file for the current stage. Do not force irrelevant stages. Clarify blocking ambiguity; record reversible assumptions.

## Stages

### 1. Discovery

Skill `product-discovery` · Required · Dependencies: none · Outputs: problem, goals, non-goals, actors, assumptions, success signal · Detail: [stages/01-discovery.md](stages/01-discovery.md)

### 2. Technical research

Skill `technical-research` · Conditional (version-specific or external facts) · Dependencies: stage 1 · Outputs: research brief with sources and versions · Detail: [stages/02-technical-research.md](stages/02-technical-research.md)

### 3. Visual and interaction design

Skill `ui-ux-design` · Conditional (user-facing change) · Dependencies: stage 1, and stage 2 when relevant · Outputs: flows, state inventory, accessibility notes, mockups · Detail: [stages/03-design.md](stages/03-design.md)

### 4. Requirements and acceptance

Skill `requirements-analysis` · Required · Dependencies: stages 1–3 when applicable · Outputs: approved spec with Given/When/Then scenarios; **hard gate: owner approval before any build** · Detail: [stages/04-requirements.md](stages/04-requirements.md)

### 5. Architecture and risk

Skill `architecture-design` · Required for non-trivial work · Dependencies: stage 4 · Outputs: boundaries, contracts, migration strategy, ADRs, risk mitigations · Detail: [stages/05-architecture.md](stages/05-architecture.md)

### 6. Planning and ownership

Skills `task-planning`, `spec-analysis` · Required for multi-step work · Dependencies: stages 4 and 5 · Outputs: Ready-for-Development `PLAN.md`, coverage map, analysis report · Detail: [stages/06-planning.md](stages/06-planning.md)

### 7. Implementation

Skills `implementation`, `tdd` · Required · Dependencies: stage 6 (or 5 for a small sequential change) · Outputs: source changes, tests, task ledger, rulings · Detail: [stages/07-implementation.md](stages/07-implementation.md)

### 8. Verification and QA

Skills `testing`, `e2e-testing`, `verification-before-completion`, `spec-analysis` (converge) · Required · Dependencies: stage 7 · Outputs: baseline-relative test report, visual evidence, convergence result · Detail: [stages/08-verification.md](stages/08-verification.md)

### 9. Security review

Skill `security-audit` · Conditional, risk-based · Dependencies: stages 4–8 as applicable · Outputs: validated findings, remediation, residual risks · Detail: [stages/09-security.md](stages/09-security.md)

### 10. Independent code review

Skill `code-review` · Required for substantial changes · Dependencies: stages 7 and 8 · Outputs: findings-first review, resolved findings · Detail: [stages/10-review.md](stages/10-review.md)

### 11. Documentation and knowledge update

Skill `project-documentation` · Required when behavior, config, API, or architecture changes · Dependencies: stages 7 and 10 · Outputs: updated docs, decisions, pitfalls, workflow state · Detail: [stages/11-documentation.md](stages/11-documentation.md)

### 12. Delivery and release readiness

Skill `release-management` · Conditional (release requested) · Dependencies: required verification, review, security, and documentation · Outputs: release notes, readiness report, rollback plan · Detail: [stages/12-delivery.md](stages/12-delivery.md)

## Parallelization

After planning, independent tasks marked `[P]` may run in parallel only with disjoint write scopes and satisfied dependencies. A single integrator owns shared files, conflict resolution, integration, and final verification.

## Quality gates

- Spec approved; must-have requirements testable with no clarification markers.
- Plan meets the Ready for Development standard; spec analysis shows no critical findings.
- Relevant tests and build checks have fresh evidence with no new failures compared with the baseline.
- No unapproved lowering of the quality bar.
- Review findings are resolved or disclosed; risk-based security checks are complete.
- Documentation and workflow state are accurate; required approvals exist for consequential actions.

## Recovery

Preserve completed valid work. If tests, review, or security checks invalidate an earlier decision, return to the relevant stage and update downstream tasks. Record failed attempts and do not erase evidence.

## State semantics

Record each stage as Pending, Ready, In Progress, Completed, Blocked, Failed, Skipped, or Cancelled. Record quality gates separately as Pending, Passed, Failed, Blocked, or Waived. A skipped stage is not a passed gate. A dependent stage may proceed after a skip only when its required inputs are independently satisfied.

## Completion criteria

All mandatory stages are complete; applicable quality gates are passed or explicitly waived by an authorized approver; deliverables and changed files are reported; residual risks and skipped stages are disclosed. A feature workflow can finish at release-ready status without production deployment.
