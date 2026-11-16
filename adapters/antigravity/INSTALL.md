# Antigravity Adapter

## Project-level use

Antigravity documents workspace skills in `.agents/skills/<skill-folder>/SKILL.md`. Open the workspace root containing Axiom's canonical skills.

## Global use

Antigravity documents `~/.gemini/config/skills/<skill-folder>/SKILL.md` for global skills. Copy selected skill directories there when user-wide availability is wanted.

## Bootstrap and role mapping

Paste the [Axiom block](../../templates/project/agents-md-block.md) into the project's `AGENTS.md` so that the kernel and skill routing are always loaded. Map role metadata from `agents/roles/` to the host's agent or model settings where it supports them: `capability` (deep, standard, fast) selects the model tier, and `writes: false` means a read-only agent. Where the host has no such controls, follow the role cards as instructions.

Optional installer: `npx skills add ifaamrillah/axiom -a antigravity` (see the [adapter overview](../README.md)).

## Verify

Start or refresh the workspace and ask the agent to invoke `axiom-orchestrator`. Confirm references and expected output. The host has adopted Agent Skills, but this repository has not been exercised in a live Antigravity session.

Official references: [Agent Skills](https://antigravity.google/docs/skills) and [workflow migration](https://antigravity.google/docs/migration/workflows-to-skills/).
