# M0–M12 Implementation Map

This map records the delivered baseline against the requested milestone sequence. “Implemented” means repository assets are present and validated structurally; it does not imply live platform testing, broad model evaluation, or a public release.

| Milestone | Focus | Delivered areas | Status / remaining evidence |
|---|---|---|---|
| M0 | Foundation | `README.md`, principles, architecture, six contracts, policies, standards, ADRs, contribution/security/release docs | Implemented. Existing MIT license retained; ADR-0002 records earlier design drift. |
| M1 | Orchestration | `axiom-orchestrator`, routing/execution/delegation references, task/handoff/quality contracts | Implemented; no custom runtime or CLI. |
| M2 | Codebase onboarding | Onboarding/exploration/documentation skills, Codebase Onboarding workflow, project/architecture templates | Implemented; project-specific usage has not been evaluated against external repos. |
| M3 | Feature development | Discovery, requirements, UI/UX, architecture, implementation, TDD, debugging, testing, review skills; Feature Development workflow | Implemented; model behavior evaluation remains unrun. |
| M4 | Delegation, QA, security | Optional role cards, parallel/sequential/review guidance, testing and E2E skills, security skill/workflow/templates | Implemented as portable guidance; host delegation and security tools are optional and untested here. |
| M5 | Full lifecycle coverage | Bug fix, refactoring, security audit, performance audit, release workflows; release management skill | Implemented as focused Markdown procedures; no release/publish action performed. |
| M6 | Platform and integration adapters | Claude Code, Codex, OpenCode, Antigravity, generic setup guides; optional integration fallbacks | Documentation checked against official docs. Live host discovery/invocation remains untested. |
| M7 | Evaluation and release readiness | Python validator, GitHub Actions, evaluation fixtures, templates, compatibility report, changelog, contributor/security/release docs | Implemented and structurally validated. Fixtures are not model test results; runtime compatibility and model behavior remain unverified. |
| M8 | Behavioral foundation | Kernel + project instructions block (pitfalls), `verification-before-completion`, rewritten `tdd`/`debugging`/`code-review` with references, optional Claude Code kernel hook | Implemented. Kernel injection via the plugin hook observed live on Claude Code 2.1.325 (2026-11-16). |
| M9 | Runnable evaluation | `evaluations/cases/` (10 skills), seeded fixture, `scripts/run_evals.py`, unit tests, CI case check, recorded results, test-first skill-factory/evaluator, stricter validator, ADR-0004 | Implemented. Trigger runs on Claude Code: 32/32 across 6 skills (latest runs). All 24 skills have cases. Behavior runs with an independent grader: 22 of 24 cases at 5/5 (or 4/4 graded) on the CLI or subagent harness; code-review 4/5; skill-factory 5/5 after a fix. Native trigger accuracy: Claude Code 110/113, Codex 107/113 (all 24 skills). Behavior rerun after the kernel change: all 24 cases covered, with Claude and Codex graders. OpenCode discovery 24/24. See [compatibility](compatibility/README.md). The runner supports Claude Code only. |
| M10 | Specification and execution discipline | `spec-analysis`, `quality-constraints`, clarification taxonomy and checklist, constitution/constraints/DoD, Ready-for-Development plans, prompt templates, rulings and stop conditions, baseline gates, step-file Feature Development | Implemented as Markdown guidance; `spec-analysis` triggers 5/5 on Claude Code. |
| M11 | Domain depth | `security-audit` modes/ledger/verifiers, elicitation in `product-discovery`, UI rule table + design master, browser and docs-search protocols, doc freshness metadata, role metadata, `.axiom/config.md` | Implemented; `security-audit` triggers 5/5 on Claude Code; other domain behavior untested. |
| M12 | Distribution | `.claude-plugin/` plugin + marketplace (skills, hook, read-only subagents), `npx skills` and AGENTS.md bootstrap guidance | Plugin validated with `claude plugin validate` and loaded live with `--plugin-dir` (24 skills, 4 subagents). Marketplace install from GitHub verified (local scope). `npx skills` install verified; skills are self-contained (bundled assets, no links outside `.agents/skills/`). |

## Shared completion gates

- Canonical skill frontmatter has portable `name` and `description` and matches its directory.
- Workflows and task state are Markdown; no custom runtime or user-facing CLI is introduced.
- Local Markdown links resolve.
- Optional tools include graceful fallbacks.
- Compatibility and evaluation status distinguish documentation inspection from live evidence.
- The owner explicitly authorized commits to `main` and pushing this implementation. This does not authorize tagging, package publication, deployment, destructive Git actions, or future pushes outside this task.
