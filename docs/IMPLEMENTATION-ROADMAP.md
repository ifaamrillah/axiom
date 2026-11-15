# M0–M7 Implementation Map

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

## Shared completion gates

- Canonical skill frontmatter has portable `name` and `description` and matches its directory.
- Workflows and task state are Markdown; no custom runtime or user-facing CLI is introduced.
- Local Markdown links resolve.
- Optional tools include graceful fallbacks.
- Compatibility and evaluation status distinguish documentation inspection from live evidence.
- The owner explicitly authorized commits to `main` and pushing this implementation. This does not authorize tagging, package publication, deployment, destructive Git actions, or future pushes outside this task.
