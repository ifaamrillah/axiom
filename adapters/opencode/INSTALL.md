# OpenCode Adapter

## Project-level use

OpenCode documents `.agents/skills/` as a project compatibility source. Open the repository root containing the canonical skills. Its skill IDs are path-derived; this catalog uses lowercase kebab-case directory names aligned with frontmatter names.

OpenCode's own `.opencode/skills/` path has higher precedence. Avoid duplicate IDs there unless intentionally overriding Axiom. Skill permissions can prevent discovery or loading; check the active agent's `skill` permission if invocation fails.

## Global/configured use

OpenCode documents user-level directories and explicit `skills` configuration. Use those host mechanisms when desired; no Axiom-specific configuration is required for the project path.

## Bootstrap and role mapping

Paste the [Axiom block](../../templates/project/agents-md-block.md) into the project's `AGENTS.md` so that the kernel and skill routing are always loaded. Map role metadata from `agents/roles/` to the host's agent or model settings where it supports them: `capability` (deep, standard, fast) selects the model tier, and `writes: false` means a read-only agent. Where the host has no such controls, follow the role cards as instructions.

Work categories in the orchestrator (`quick`, `deep`, `visual`, `writing`) suggest one of these capability tiers. OpenCode agents in `.opencode/agents/<name>.md` take a `model` field (`provider/model`) and `mode: subagent`; a subagent without `model` inherits the session model, and a read-only agent denies `edit` and `shell` in `permissions` (agents docs checked 2026-11-17). Not tested with Axiom.

Optional installer: `npx skills add ifaamrillah/axiom -a opencode` (see the [adapter overview](../README.md)).

## Verify

Use the host's skill listing/invocation and confirm `axiom-orchestrator` loads. Then check relative references from the skill directory. Verified 2026-11-16 with opencode 1.19.5: `opencode debug skill`, run from a project root, listed all 24 Axiom skills from `.agents/skills/`. Model invocation was not tested.

Official reference: [OpenCode skills](https://opencode.ai/docs/skills/).
