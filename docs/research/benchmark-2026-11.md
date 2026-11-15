# Axiom Benchmark: 11 Agent Projects

**Reviewed:** 2026-11-16  
**Scope:** public repository documentation, current default-branch README/license material, and Axiom at `d7cfd87997176b9c308075a81926f810ccf0b306`. This is a capability comparison, not a code security audit of the benchmark projects.

## Feature comparison and adoption decisions

| Project | Capability observed upstream | Axiom coverage | Decision |
|---|---|---|---|
| [addyosmani/agent-skills](https://github.com/addyosmani/agent-skills) | Broad lifecycle skills, host adapters, focused skill anatomy, positive/negative trigger and behavioral evaluation cases. | Lifecycle skills and adapters exist; evaluation fixtures are illustrative Markdown and do not share a structured case schema. | Adopt the emphasis on trigger precision, behavioral evidence, and small skill scope when expanding Axiom's evaluation fixtures. Do not copy skills wholesale. |
| [multica-ai/andrej-karpathy-skills](https://github.com/multica-ai/andrej-karpathy-skills) | Compact behavioral rules: think first, prefer simplicity, make surgical changes, define goal-driven success criteria. | Present across Axiom's principles, repository instructions, orchestration, and implementation guidance. | No new skill needed. Keep these as shared principles rather than duplicating them in another always-loaded router. |
| [obra/superpowers](https://github.com/obra/superpowers) | Composable software-development methodology covering brainstorming, planning, TDD, debugging, review, and delivery, with skill-behavior evaluations. | Equivalent lifecycle coverage exists across skills and focused workflows; Axiom intentionally routes by task and risk. | Retain task-sized routing and evidence gates. Adopt explicit behavioral evaluation where it improves confidence; do not import plugin hooks or runtime assumptions. |
| [github/spec-kit](https://github.com/github/spec-kit) | Spec-driven flow from principles and specification through plan, tasks, implementation, and repeated convergence against the spec; supports presets and extensions. | Requirements, architecture, planning, implementation, and verification are separate stages, but the feature workflow did not explicitly require another implement/verify loop for unmet criteria. | Adopt an acceptance-driven convergence loop in feature development. Keep requirements and project state in Markdown; do not add a CLI or workflow engine. |
| [nextlevelbuilder/ui-ux-pro-max-skill](https://github.com/nextlevelbuilder/ui-ux-pro-max-skill) | Design-system generation and industry-specific UI heuristics, responsive and accessibility checklists, plus tooling/catalogs. | Axiom has a UI/UX skill and design workflow, but no bundled style catalogs or generators. | Reuse the general practice of checking context, accessibility, responsiveness, and anti-patterns. Avoid importing large evolving catalogs and generators into the platform-neutral core. |
| [bmad-code-org/BMAD-METHOD](https://github.com/bmad-code-org/BMAD-METHOD) | Scale-adaptive agile workflows, durable briefs/specs/architecture, specialized agent roles, facilitated collaboration, and domain modules. | Axiom has adaptive lifecycle workflows, role cards, project knowledge, and native-first delegation, but no large module ecosystem or guided agent runtime. | Keep the lightweight adaptive workflow and optional role guidance. Do not reproduce its installer, modules, agent orchestration, or trademarked branding. |
| [microsoft/playwright-cli](https://github.com/microsoft/playwright-cli) | Browser automation via concise CLI commands, persisted named sessions, screenshots, and optional agent skills; positions CLI as a token-efficient choice for coding agents. | Axiom documents optional browser automation and E2E testing but does not name a preferred command interface. | Recommend a host/project's available CLI for bounded browser tasks when it gives sufficient evidence; preserve native browser tools and test fallback. No Playwright dependency is added. |
| [upstash/context7](https://github.com/upstash/context7) | Version-aware retrieval of current library/framework documentation for coding agents via tools, rules, and plugins. | Axiom already treats Context7 as optional, asks agents to confirm package/version, prefer official docs, and record version scope. | Existing integration guidance covers the useful principle. Keep optional lookup and a manual official-doc fallback; no service dependency is added. |
| [abryant710/auto-codebase-documenter](https://github.com/abryant710/auto-codebase-documenter) | Generates per-file Markdown assessments by walking configured source file types and mirroring paths; the project describes an OpenAI API dependency. | Axiom's onboarding and project-documentation skills create concise, source-linked architecture and workflow knowledge; they avoid exhaustive generated file-by-file docs. | Do not adopt automatic per-file generation. Retain curated, incremental docs and update only knowledge that changed, with code as the implementation source of truth. |
| [yeachan-heo/oh-my-claudecode](https://github.com/yeachan-heo/oh-my-claudecode) | Claude Code-centered multi-agent orchestration, teams/modes, task management, hooks, and workflow automation. | Axiom provides portable role/delegation guidance and defers execution to host-native capabilities; cross-host behavior is documented as unverified where appropriate. | Preserve native-first portability and explicit fallbacks. Do not add Claude-specific runtime or hooks to canonical skills. |
| [cloudflare/security-audit-skill](https://github.com/cloudflare/security-audit-skill) | Structured security phases with architecture reconnaissance, coverage-led hunting, isolated review roles, candidate validation, and separate coverage critique. | Axiom already defines scope, threat/control review, verification, remediation, and reporting, but had no durable coverage ledger or distinct coverage-completeness gate. | Adopt a Markdown coverage ledger and a separate coverage review before ranking findings. Keep delegation optional and authorization-bounded. |

## License and attribution review

| Project | Repository license signal observed | Reuse constraint for this change |
|---|---|---|
| Addy Osmani agent-skills | MIT | Redistribution of substantial copied portions requires retaining copyright and license notices. |
| Andrej Karpathy skills (Multica) | README declares MIT; no separate LICENSE file was present on the reviewed default branch. | Treat the README declaration as the observed signal, not an independently supplied license grant. Use only high-level behavioral ideas here; no source text is copied. |
| Superpowers | MIT | Preserve copyright and license notice if substantial text/code is redistributed. |
| GitHub Spec Kit | MIT | Preserve license and modification notices if material is copied. |
| UI UX Pro Max | Root README and LICENSE state MIT. A current repository issue documents a conflicting Apache-2.0 license text for the `ui-styling` subskill; treat that subskill as Apache-2.0 until upstream resolves the inconsistency. | No assets, catalogs, code, or skill text copied. |
| BMAD METHOD | MIT; project documentation also identifies BMAD names as trademarks. | Do not use BMAD branding or imply affiliation. |
| Microsoft Playwright CLI | Apache-2.0 | If source material is redistributed, include the license and applicable NOTICE, retain attribution, and identify modified files. |
| Upstash Context7 | MIT | Preserve copyright and license notice if substantial text/code is redistributed. |
| Auto Codebase Documenter | MIT | Preserve copyright and license notice if substantial text/code is redistributed. |
| oh-my-claudecode | MIT | Preserve copyright and license notice if substantial text/code is redistributed. |
| Cloudflare security-audit-skill | MIT | Preserve copyright and license notice if substantial text/code is redistributed. |

This change adapts general workflow ideas and uses original wording. It does not copy upstream skill files, scripts, datasets, branding, or images, so no third-party source material or license files are added to Axiom.

## Evidence sources

- [Addy Osmani agent-skills README](https://github.com/addyosmani/agent-skills) and [LICENSE](https://github.com/addyosmani/agent-skills/blob/main/LICENSE)
- [Andrej Karpathy skills README](https://github.com/multica-ai/andrej-karpathy-skills)
- [Superpowers README](https://github.com/obra/superpowers) and [LICENSE](https://github.com/obra/superpowers/blob/main/LICENSE)
- [Spec Kit README](https://github.com/github/spec-kit) and [LICENSE](https://github.com/github/spec-kit/blob/main/LICENSE)
- [UI UX Pro Max README](https://github.com/nextlevelbuilder/ui-ux-pro-max-skill) and [LICENSE](https://github.com/nextlevelbuilder/ui-ux-pro-max-skill/blob/main/LICENSE); [upstream license inconsistency discussion](https://github.com/nextlevelbuilder/ui-ux-pro-max-skill/issues/544)
- [BMAD METHOD README](https://github.com/bmad-code-org/BMAD-METHOD) and [LICENSE](https://github.com/bmad-code-org/BMAD-METHOD/blob/main/LICENSE)
- [Playwright CLI README](https://github.com/microsoft/playwright-cli) and [LICENSE](https://github.com/microsoft/playwright-cli/blob/main/LICENSE)
- [Context7 README](https://github.com/upstash/context7) and [LICENSE](https://github.com/upstash/context7/blob/master/LICENSE)
- [Auto Codebase Documenter README](https://github.com/abryant710/auto-codebase-documenter) and [LICENSE](https://github.com/abryant710/auto-codebase-documenter/blob/main/LICENSE)
- [oh-my-claudecode README](https://github.com/yeachan-heo/oh-my-claudecode) and [LICENSE](https://github.com/yeachan-heo/oh-my-claudecode/blob/main/LICENSE)
- [Cloudflare security-audit-skill README](https://github.com/cloudflare/security-audit-skill) and [LICENSE](https://github.com/cloudflare/security-audit-skill/blob/main/LICENSE)

## Changes made from the audit

- Feature Development now loops implementation and focused verification against every acceptance criterion until evidenced, blocked, or explicitly waived.
- Security Audit now records review units in a Markdown ledger and requires a separate coverage-completeness pass before issue verification and ranking.

The benchmark is a dated snapshot: upstream default branches and license details can change. Re-check sources before future redistribution or when revising these adoption decisions.
