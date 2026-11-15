# Getting Started

1. Choose the relevant host and follow its guide in [adapters](../../adapters/README.md).
2. Use the canonical skills under .agents/skills/.
3. Ask the host agent to use axiom-orchestrator or invoke a specialist skill directly.
4. For an unfamiliar project, follow [Codebase Onboarding](../../workflows/codebase-onboarding/WORKFLOW.md). For a change, follow [Feature Development](../../workflows/feature-development/WORKFLOW.md).

## Install and update

Axiom has no installer, package manager, custom runtime, or CLI. Use Git to clone or fork this repository, or copy the required skill directories and their references into a host-supported location. For Claude Code, follow its adapter because the canonical project path differs. Keep .agents/skills/ as the source copy.

To update a clone, review upstream changes and use your normal Git workflow (fetch/pull or merge/rebase) after protecting local edits. For copied skills, compare and copy the updated skill directory together with referenced files. Review the changelog and compatibility notes before adopting behavior changes. Do not overwrite project-specific instructions or state.

If automatic skill discovery is unavailable, read the relevant SKILL.md and workflow as ordinary Markdown.
