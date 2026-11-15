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

- `.agents/skills/` — canonical, portable Agent Skills
- `core/` — architecture, principles, contracts, policies, and standards
- `workflows/` — Markdown workflow definitions
- `agents/` — role guidance and delegation patterns
- `integrations/` — optional tool integration guidance
- `adapters/` — host-specific installation and compatibility instructions
- `templates/` — reusable project and execution documents
- `evaluations/` — behavioral and efficiency evaluation scenarios
- `scripts/` — repository validation utilities
- `docs/` — user and contributor documentation

## Initial platforms

Axiom's initial compatibility targets are Claude Code, Codex, OpenCode, and Antigravity. Compatibility is documented per adapter and must be tested; shared skill format does not imply identical host capabilities.

## Getting started

1. Read [the architecture](core/ARCHITECTURE.md) and [principles](core/PRINCIPLES.md).
2. Choose the adapter for your coding agent under `adapters/`.
3. Install or expose the skills using that platform's documented discovery mechanism.
4. Start with [Codebase Onboarding](workflows/codebase-onboarding/WORKFLOW.md) for an unfamiliar repository.
5. Use [Feature Development](workflows/feature-development/WORKFLOW.md) for a feature request.

Axiom is currently distributed as repository content and Markdown instructions. It has no custom runtime and no CLI.

## Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md). Contributions should preserve portability, evidence-based execution, and minimal context overhead.

## Security

Do not commit credentials, tokens, private keys, or production secrets. Report security vulnerabilities privately using the process in [SECURITY.md](SECURITY.md).

## License

This project is licensed under the MIT License. See [LICENSE](LICENSE).
