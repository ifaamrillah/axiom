# Axiom

**A universal, skills-first software engineering harness for AI agents.**

Axiom gives coding agents a consistent way to understand a codebase, plan changes, design experiences, implement software, verify results, assess risk, and deliver work. It is designed to work with the native capabilities of the host agent rather than introducing a separate agent runtime.

> **Project status:** Early development. Interfaces and workflows may evolve before the first stable release.

## Why Axiom?

AI coding agents are capable, but software engineering work benefits from durable context, explicit workflows, clear task boundaries, evidence-based quality gates, and reliable handoffs. Axiom provides those engineering practices in a portable, inspectable repository.

## Design principles

- **Skills-first:** reusable procedures use the Agent Skills `SKILL.md` format.
- **Native-first:** use the host platform's native agent, tool, and delegation capabilities.
- **Context before action:** inspect project instructions and existing knowledge before changing code.
- **Adaptive workflow:** choose the smallest workflow that safely satisfies the task.
- **Evidence over claims:** completion and quality gates require observable verification.
- **Living documentation:** update relevant project knowledge when changes invalidate it.
- **Parallel when safe:** delegate independent work with explicit file ownership and integration.
- **Human control:** require approval at consequential boundaries such as production deployment and destructive operations.
- **Portable by design:** keep canonical skills platform-neutral and isolate host-specific setup in adapters.
- **Progressive complexity:** do not impose heavyweight planning on trivial changes.

## Lifecycle

Axiom covers the full software lifecycle:

1. Discovery and codebase understanding
2. Product and visual design
3. Requirements and specification
4. Architecture and planning
5. Implementation
6. Verification and QA
7. Security and reliability
8. Release and delivery

Not every task needs every stage. The orchestrator selects and adapts the workflow based on scope, risk, uncertainty, and user intent.

## Repository map

- `.agents/skills/` — canonical, portable Agent Skills (including the always-on [kernel](.agents/skills/axiom-orchestrator/references/kernel.md))
- `.claude-plugin/` — Claude Code plugin and marketplace manifests that point at the canonical skills and the adapter hook
- `core/` — architecture, principles, contracts, policies, standards, and the definition of done
- `workflows/` — Markdown workflow definitions (feature development loads stage files on demand)
- `agents/` — role cards with capability/write metadata, subagent prompt templates, and delegation patterns
- `integrations/` — optional tool integration guidance
- `adapters/` — host-specific installation and compatibility instructions
- `templates/` — reusable project and execution documents
- `evaluations/` — behavioral and efficiency evaluation scenarios
- `scripts/` — repository validation utilities
- `docs/` — user and contributor documentation

## Initial platforms

Axiom's initial compatibility targets are Claude Code, Codex, OpenCode, and Antigravity. Compatibility is documented per adapter and must be tested; shared skill format does not imply identical host capabilities.

## Getting started

Claude Code (plugin, includes the optional kernel hook), one command at a time:

```text
/plugin marketplace add ifaamrillah/axiom
/plugin install axiom@axiom
```

Other hosts: copy or link `.agents/skills/` into the project (Codex, OpenCode, and Antigravity read `.agents/skills/`), or use the third-party installer `npx skills add ifaamrillah/axiom`. Then paste the [Axiom block](templates/project/agents-md-block.md) into the project's `AGENTS.md`.

1. Read [the architecture](core/ARCHITECTURE.md) and [principles](core/PRINCIPLES.md).
2. Choose the adapter for your coding agent under `adapters/`.
3. Install or expose the skills using that platform's documented discovery mechanism.
4. Start with [Codebase Onboarding](workflows/codebase-onboarding/WORKFLOW.md) for an unfamiliar repository.
5. Use [Feature Development](workflows/feature-development/WORKFLOW.md) for a feature request.

The [workflow catalog](workflows/README.md) includes focused procedures for bug fixes, refactoring, security and performance audits, and release readiness. See the [skill catalog](docs/skills/README.md) for discovery, design, specification, architecture, implementation, debugging, review, testing, security, release, documentation, and skill-quality guidance.

Axiom is distributed as repository content and Markdown instructions. It has no custom runtime and no user-facing CLI. Host packaging (the Claude Code plugin) and the optional read-only session-start hook only point at canonical Markdown ([ADR-0004](docs/decisions/0004-maintainer-tooling-and-adapter-hooks.md)).

The M0–M12 implementation scope and evidence limits are summarized in the [roadmap](docs/IMPLEMENTATION-ROADMAP.md). Maintainers run `python3 scripts/validate_repository.py` (structure) and `python3 scripts/run_evals.py` (eval case checks, plus optional headless runs against an installed host; results go to `evaluations/results/`). Ideas adapted from other open-source projects are credited in [acknowledgements](docs/acknowledgements.md).

## Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md). Contributions should preserve portability, evidence-based execution, and minimal context overhead.

## Security

Do not commit credentials, tokens, private keys, or production secrets. Report security vulnerabilities privately using the process in [SECURITY.md](SECURITY.md).

## License

This project is licensed under the MIT License. See [LICENSE](LICENSE).
