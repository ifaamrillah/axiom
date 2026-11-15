# OpenCode Adapter

## Project-level use

OpenCode documents `.agents/skills/` as a project compatibility source. Open the repository root containing the canonical skills. Its skill IDs are path-derived; this catalog uses lowercase kebab-case directory names aligned with frontmatter names.

OpenCode's own `.opencode/skills/` path has higher precedence. Avoid duplicate IDs there unless intentionally overriding Axiom. Skill permissions can prevent discovery or loading; check the active agent's `skill` permission if invocation fails.

## Global/configured use

OpenCode documents user-level directories and explicit `skills` configuration. Use those host mechanisms when desired; no Axiom-specific configuration is required for the project path.

## Verify

Use the host's skill listing/invocation and confirm `axiom-orchestrator` loads. Then check relative references from the skill directory. Live Axiom session testing remains outstanding.

Official reference: [OpenCode skills](https://opencode.ai/docs/skills/).
