# Platform Compatibility

**Documentation reviewed: 2026-11-15.** This report separates documentation inspection from live runtime testing. Axiom was not installed or invoked in any of these hosts during this review.

| Host | Officially documented discovery | Axiom-specific status |
|---|---|---|
| Codex | Project `.agents/skills/`; user `~/.agents/skills/` | Official docs inspected; Axiom live discovery and invocation not tested |
| OpenCode | `.agents/skills/` is a project compatibility source; permissions and precedence can affect loading | Official docs inspected; Axiom live discovery and invocation not tested |
| Antigravity | Workspace `.agents/skills/`; global `~/.gemini/config/skills/` | Official docs inspected; Axiom live discovery and invocation not tested |
| Claude Code | Project `.claude/skills/` | Official docs inspected; Axiom needs a copy/link adapter; live discovery and invocation not tested |

## What has been checked

Official documentation was inspected on 2026-11-15 for skill format and discovery path. Codex and Antigravity document `.agents/skills/`; OpenCode documents it as a compatibility source; Claude Code documents `.claude/skills/`. Canonical Axiom skills use `SKILL.md`, portable `name` and `description` fields, and relative references. Documentation-level compatibility does not guarantee runtime behavior.

## What has not been checked

No live host sessions were available for this repository validation. Discovery, invocation, frontmatter edge cases, reference loading, global installation, nested workspaces, and permission/precedence interactions remain untested. No platform is labeled runtime-verified.

## Graceful fallbacks

- If a skill is not discovered, open its `SKILL.md` directly and follow it manually.
- If host-specific metadata is rejected, keep canonical frontmatter at `name` and `description`; do not add a required Axiom extension.
- If Claude Code symlinks are unavailable, copy the skill directory and treat `.agents/skills/` as the source of truth.
- If workflow state is unsupported, maintain a Markdown checklist or use the host conversation.

## Primary documentation

- [Codex skills](https://developers.openai.com/codex/skills/)
- [OpenCode skills](https://opencode.ai/docs/skills/)
- [Antigravity skills](https://antigravity.google/docs/skills)
- [Claude Code skills](https://code.claude.com/docs/en/skills)
