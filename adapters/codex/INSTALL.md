# Codex Adapter

## Project-level use

Codex discovers repository skills from `.agents/skills/`. Keep the canonical directories in that location and open the project root in Codex. For portable reuse in another repository, copy or link the desired skill directories into that repository's `.agents/skills/`.

## Global use

Codex documentation lists `~/.agents/skills/` for user-wide skills. Copy selected skill directories there only if global availability is desired.

## Bootstrap and role mapping

Paste the [Axiom block](../../templates/project/agents-md-block.md) into the project's `AGENTS.md` so that the kernel and skill routing are always loaded. Map role metadata from `agents/roles/` to the host's agent or model settings where it supports them: `capability` (deep, standard, fast) selects the model tier, and `writes: false` means a read-only agent. Where the host has no such controls, follow the role cards as instructions.

Work categories in the orchestrator (`quick`, `deep`, `visual`, `writing`) suggest one of these capability tiers. Codex documents a `model` key and `model_reasoning_effort` in its config, profiles selected with `--profile`, and `agents.default_subagent_model` for spawned agents (config reference checked 2026-11-17). Whether a custom role under `agents.<name>` can set its own model is not documented there; test before relying on it.

Optional installer: `npx skills add ifaamrillah/axiom -a codex` (see the [adapter overview](../README.md)).

## Verify

Start or refresh the Codex session and ask it to list or use `axiom-orchestrator`. Confirm a known instruction is applied. If not discovered, inspect the working root, exact `SKILL.md` path, frontmatter, and host version. Verified 2026-11-16 with codex-cli 0.169.0: in a project with `.agents/skills/` and the Axiom block in `AGENTS.md`, `codex exec` read the matching `SKILL.md` for 107 of 113 trigger prompts. Records are in `evaluations/results/*-codex-trigger.md`. Codex sometimes reads more than one skill, and it loads user-level config.

Official reference: [Codex skills](https://developers.openai.com/codex/skills).
