---
name: axiom-orchestrator
description: Coordinate software engineering work with Axiom by inspecting project context, choosing an adaptive workflow, routing to skills, managing task boundaries and native delegation, enforcing evidence-based quality gates, and updating living documentation. Use when starting or coordinating meaningful engineering work in a project using Axiom.
---

# Axiom Orchestrator

## Purpose

Coordinate the smallest safe and sufficient engineering process. The host agent remains the runtime; follow the workflow as Markdown guidance.

## When to use

Use for new features, bug fixes, refactors, onboarding, audits, complex investigations, and release preparation. For a trivial change, use the lightweight path.

## Operating procedure

1. Read repository instructions such as `AGENTS.md`, platform instructions, and relevant package/project guidance.
2. Inspect `.axiom/` if present. Identify the project overview, architecture, conventions, glossary, active workflow state, and relevant decisions. Check freshness before trusting prior analysis.
3. Understand the request. Identify expected outcome, constraints, affected areas, uncertainty, risk, and acceptance criteria. Ask only when a genuinely blocking ambiguity cannot be resolved safely.
4. Select the smallest sufficient workflow:
   - Unfamiliar repository: `workflows/codebase-onboarding/WORKFLOW.md`
   - New or substantial feature: `workflows/feature-development/WORKFLOW.md`
   - Smaller bug, refactor, audit, or release: select the matching workflow when present, otherwise use a proportionate plan.
5. Create or update a Markdown workflow instance under `.axiom/workflows/active/<ID>/` for multi-stage work. Include state, plan, tasks, decisions, and handoffs as needed.
6. Load only the skills and references needed for the current stage. Check that referenced skill names and files exist.
7. Define task scope, dependencies, deliverables, acceptance, verification, and allowed/restricted/shared file ownership before delegation.
8. Use native subagents only when supported and beneficial. Parallelize only independent tasks with non-overlapping write scopes. Otherwise work sequentially.
9. Integrate work. Review diffs, run relevant checks, and apply the quality-gate contract. Never equate a completion claim with verified success.
10. Update relevant project knowledge and workflow state. Preserve failures, skipped stages, waivers, and remaining risks accurately.
11. Report summary, changed files, checks and evidence, skipped/unavailable checks, known limitations, and next action.

## Adaptive routing

Consider:
- Scope: isolated, component-level, cross-cutting, system-level.
- Risk: low, medium, high, critical.
- Uncertainty: understood, partially understood, unknown.
- Impact: internal, user-facing, data/security-sensitive, production.
- Verification needs: unit, integration, API, E2E, visual, accessibility, performance, security, release.

Avoid full lifecycle ceremony for trivial low-risk changes. User-facing UI work should include design discovery. Security-sensitive changes require early threat/risk consideration and appropriate review.

## Quality and safety

- Follow `core/PRINCIPLES.md` and `core/policies/`.
- Never say tests passed unless they ran and produced passing evidence.
- A skipped stage is Skipped, never Passed.
- Do not waive a blocking gate without an explicit authorized approval and documented rationale.
- Require approval before production deployment and destructive or irreversible operations.

## References

Read only when needed:
- `core/ARCHITECTURE.md`
- `core/contracts/`
- `core/policies/`
- `workflows/README.md`
- Relevant workflow definition and skill.
- [Routing guidance](references/routing.md)
- [Execution and completion](references/execution.md)
- [Delegation](references/delegation.md)
