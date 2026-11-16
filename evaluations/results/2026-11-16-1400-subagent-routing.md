# Description routing check via subagents (2026-11-16)

- Harness: **subagent**, not native skill discovery. Two independent `general-purpose` subagents read a file listing all 24 skill names and descriptions plus all 113 trigger prompts from `evaluations/cases/` (shuffled, unlabeled), and named the one skill each prompt should load first, or `none`.
- Scoring: a positive passes when the router picks the case's skill (or an `accept:` alias); a negative passes when it does not pick that skill.
- Limits: every description is laid out side by side and the router is asked to choose, which is easier than native discovery, where the host decides on its own whether to load any skill. The latest valid native results remain the Claude Code CLI runs for 6 skills; the native 18-skill run was invalidated by a usage limit.

| Skill | Prompts | Router A | Router B |
|---|---|---|---|
| architecture-design | 5 | 5/5 | 5/5 |
| axiom-orchestrator | 5 | 5/5 | 5/5 |
| code-review | 5 | 5/5 | 5/5 |
| codebase-exploration | 5 | 5/5 | 5/5 |
| codebase-onboarding | 4 | 4/4 | 4/4 |
| debugging | 7 | 7/7 | 7/7 |
| e2e-testing | 5 | 5/5 | 5/5 |
| implementation | 4 | 4/4 | 4/4 |
| product-discovery | 5 | 5/5 | 5/5 |
| project-documentation | 4 | 4/4 | 4/4 |
| project-onboarding | 4 | 4/4 | 4/4 |
| quality-constraints | 5 | 5/5 | 5/5 |
| release-management | 5 | 5/5 | 5/5 |
| requirements-analysis | 5 | 5/5 | 5/5 |
| security-audit | 5 | 5/5 | 5/5 |
| skill-evaluator | 4 | 4/4 | 4/4 |
| skill-factory | 4 | 4/4 | 4/4 |
| spec-analysis | 5 | 5/5 | 5/5 |
| task-planning | 4 | 4/4 | 4/4 |
| tdd | 5 | 5/5 | 5/5 |
| technical-research | 4 | 4/4 | 4/4 |
| testing | 4 | 4/4 | 4/4 |
| ui-ux-design | 5 | 5/5 | 5/5 |
| verification-before-completion | 5 | 5/5 | 5/5 |

Total: A 113/113, B 113/113. The two routers disagreed on one prompt, and both answers were acceptable for it.
