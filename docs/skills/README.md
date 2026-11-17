# Skill Guide

Canonical skills live under `.agents/skills/`. Each directory has one `SKILL.md` entry point and optional `references/` that are read on demand. `project-onboarding` is canonical; `codebase-onboarding` remains only as a compatibility alias.

Every project using Axiom should also load the [Axiom kernel](../../.agents/skills/axiom-orchestrator/references/kernel.md), a short always-on behavioral baseline, through the project's instructions file or the Claude Code plugin hook.

## Lifecycle catalog

| Area | Skill | Use it for |
|---|---|---|
| Orchestration | [axiom-orchestrator](../../.agents/skills/axiom-orchestrator/SKILL.md) | Route a meaningful request through the smallest sufficient workflow; execution loop, rulings, baseline gates |
| Discovery | [product-discovery](../../.agents/skills/product-discovery/SKILL.md) | One-question-at-a-time elicitation, approaches with trade-offs, approved design summary |
| Codebase understanding | [project-onboarding](../../.agents/skills/project-onboarding/SKILL.md), [codebase-exploration](../../.agents/skills/codebase-exploration/SKILL.md) | Build project context or trace relevant code and dependencies |
| Requirements | [requirements-analysis](../../.agents/skills/requirements-analysis/SKILL.md), [spec-analysis](../../.agents/skills/spec-analysis/SKILL.md) | Testable specs with clarification markers; cross-artifact consistency and convergence |
| Design | [ui-ux-design](../../.agents/skills/ui-ux-design/SKILL.md), [architecture-design](../../.agents/skills/architecture-design/SKILL.md) | Priority-ordered UI rules, design-system master, critique and polish modes; system boundaries, trade-offs, deprecation, prototypes |
| Performance and operations | [performance-optimization](../../.agents/skills/performance-optimization/SKILL.md), [ci-and-observability](../../.agents/skills/ci-and-observability/SKILL.md) | Measured optimization; CI pipelines, logs, metrics, traces, and alerts |
| Planning and implementation | [task-planning](../../.agents/skills/task-planning/SKILL.md), [implementation](../../.agents/skills/implementation/SKILL.md), [tdd](../../.agents/skills/tdd/SKILL.md) | Ready-for-Development plans; scoped changes; red-green-refactor with observed failures |
| Debugging and verification | [debugging](../../.agents/skills/debugging/SKILL.md), [testing](../../.agents/skills/testing/SKILL.md), [e2e-testing](../../.agents/skills/e2e-testing/SKILL.md), [verification-before-completion](../../.agents/skills/verification-before-completion/SKILL.md) | Root cause before fix; proportionate verification; evidence before any completion claim |
| Quality bar | [quality-constraints](../../.agents/skills/quality-constraints/SKILL.md) | Constitution, numeric constraints, definition of done; detecting a lowered bar |
| Risk and review | [security-audit](../../.agents/skills/security-audit/SKILL.md), [code-review](../../.agents/skills/code-review/SKILL.md) | Trust-boundary findings with calibrated severity; spec-first review with gap analysis and blast radius |
| Delivery and knowledge | [release-management](../../.agents/skills/release-management/SKILL.md), [project-documentation](../../.agents/skills/project-documentation/SKILL.md), [technical-research](../../.agents/skills/technical-research/SKILL.md) | Release readiness; living docs with freshness metadata and pitfalls; version-pinned, cited research |
| Writing | [writing-quality](../../.agents/skills/writing-quality/SKILL.md) | Prose without AI writing tells, facts preserved |
| Skill quality | [skill-factory](../../.agents/skills/skill-factory/SKILL.md), [skill-evaluator](../../.agents/skills/skill-evaluator/SKILL.md) | Test-first skill authoring; trigger and behavior evaluation with recorded runs |

## Authoring

Follow the [skill contract](../../core/contracts/SKILL-CONTRACT.md) and the [skill template](../../templates/skills/SKILL.template.md). Write [eval cases](../../evaluations/cases/README.md) first. The structural validator enforces a "Use when …" trigger clause, a 250-line and 20,000-byte budget for `SKILL.md`, and that every reference is linked. `python3 scripts/run_evals.py --routing` reports how distinct the descriptions are, offline. Platform-specific discovery and invocation belong in [adapters](../../adapters/README.md).
