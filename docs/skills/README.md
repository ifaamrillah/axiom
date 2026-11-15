# Skill Guide

Canonical skills live under `.agents/skills/`. Each directory has one `SKILL.md` entry point and optional colocated references. `project-onboarding` is canonical; `codebase-onboarding` remains only as a compatibility alias. `task-planning` is a supporting lifecycle skill used for multi-step work.

## Lifecycle catalog

| Area | Skill | Use it for |
|---|---|---|
| Orchestration | [axiom-orchestrator](../../.agents/skills/axiom-orchestrator/SKILL.md) | Route a meaningful request through the smallest sufficient workflow and quality gates |
| Discovery | [product-discovery](../../.agents/skills/product-discovery/SKILL.md) | Clarify users, problems, outcomes, constraints, and success signals |
| Codebase understanding | [project-onboarding](../../.agents/skills/project-onboarding/SKILL.md), [codebase-exploration](../../.agents/skills/codebase-exploration/SKILL.md) | Build project context or trace relevant code and dependencies |
| Requirements and design | [requirements-analysis](../../.agents/skills/requirements-analysis/SKILL.md), [ui-ux-design](../../.agents/skills/ui-ux-design/SKILL.md), [architecture-design](../../.agents/skills/architecture-design/SKILL.md) | Define acceptance, user interaction, system boundaries, and technical trade-offs |
| Planning and implementation | [task-planning](../../.agents/skills/task-planning/SKILL.md), [implementation](../../.agents/skills/implementation/SKILL.md), [tdd](../../.agents/skills/tdd/SKILL.md) | Order work, implement scoped changes, and use a test-first loop where suitable |
| Debugging and verification | [debugging](../../.agents/skills/debugging/SKILL.md), [testing](../../.agents/skills/testing/SKILL.md), [e2e-testing](../../.agents/skills/e2e-testing/SKILL.md) | Isolate defects and select proportionate verification |
| Risk and review | [security-audit](../../.agents/skills/security-audit/SKILL.md), [code-review](../../.agents/skills/code-review/SKILL.md) | Assess security boundaries and inspect changes for defects and regressions |
| Delivery and knowledge | [release-management](../../.agents/skills/release-management/SKILL.md), [project-documentation](../../.agents/skills/project-documentation/SKILL.md), [technical-research](../../.agents/skills/technical-research/SKILL.md) | Prepare releases, maintain living docs, and verify version-sensitive external facts |
| Skill quality | [skill-factory](../../.agents/skills/skill-factory/SKILL.md), [skill-evaluator](../../.agents/skills/skill-evaluator/SKILL.md) | Create or improve portable skills and evaluate their structure and behavior |

Follow the [skill contract](../../core/contracts/SKILL-CONTRACT.md) and [skill template](../../templates/skills/SKILL.template.md). Platform-specific discovery and invocation belong in [adapters](../../adapters/README.md).
