# Getting Started

1. Choose the relevant host and follow its guide in [adapters](../../adapters/README.md).
2. Use the canonical skills under .agents/skills/.
3. Ask the host agent to use axiom-orchestrator or invoke a specialist skill directly.
4. For an unfamiliar project, follow [Codebase Onboarding](../../workflows/codebase-onboarding/WORKFLOW.md). For a change, follow [Feature Development](../../workflows/feature-development/WORKFLOW.md).

## Install and update

Axiom ships no installer, custom runtime, or CLI of its own. Choose one path:

- **Claude Code:** install the repository as a plugin (`/plugin marketplace add ifaamrillah/axiom`, then `/plugin install axiom@axiom`). See the [Claude Code adapter](../../adapters/claude-code/INSTALL.md).
- **Any host:** clone or fork this repository and copy or link `.agents/skills/` (with each skill's `references/`) into a host-supported location.
- **Third-party installer:** `npx skills add ifaamrillah/axiom` discovers `.agents/skills/` and installs it for the agents you select. It installs skill directories only. Skills carry the templates and prompts they fill under `assets/`; workflows and contracts are not included. Review what it installs. See the [adapter overview](../../adapters/README.md) for its limits.

Then load the kernel: paste the [Axiom block](../../templates/project/agents-md-block.md) into the project's `AGENTS.md` or `CLAUDE.md`, unless the Claude Code plugin hook already injects it. Keep .agents/skills/ as the source copy.

To update a clone, review upstream changes and use your normal Git workflow (fetch/pull or merge/rebase) after protecting local edits. For copied skills, compare and copy the updated skill directory together with referenced files. Review the changelog and compatibility notes before adopting behavior changes. Do not overwrite project-specific instructions or state.

If automatic skill discovery is unavailable, read the relevant SKILL.md and workflow as ordinary Markdown.
