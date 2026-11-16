# Platform Adapters

Canonical skills remain in `.agents/skills/`. Adapters explain how a host discovers them and where host-specific behavior differs. They never fork skill content.

| Host | Project-level discovery | Packaging / bootstrap | Status |
|---|---|---|---|
| Claude Code | `.claude/skills/`, or the plugin manifest | `.claude-plugin/` plugin and marketplace; optional SessionStart kernel hook | Manifest validated with `claude plugin validate` (2026-11-16); see [compatibility](../docs/compatibility/README.md) for live runs |
| Codex | `.agents/skills/` | Axiom block in `AGENTS.md` | Docs reviewed 2026-11-15; live invocation untested |
| OpenCode | `.agents/skills/` (compatibility source) | Axiom block in `AGENTS.md` | Docs reviewed 2026-11-15; live invocation untested |
| Antigravity | `.agents/skills/` | Axiom block in `AGENTS.md` | Docs reviewed 2026-11-15; live invocation untested |

## Installing into another project without a custom CLI

**Git:** clone or vendor this repository and copy or link `.agents/skills/` into the target project. Keep the references next to each skill.

**`skills` installer (third-party, optional):** the open [`skills`](https://github.com/vercel-labs/skills) installer discovers skills in a repository's `.agents/skills/` and installs them for many agents:

```sh
npx skills add ifaamrillah/axiom                                  # choose agents interactively
npx skills add ifaamrillah/axiom --skill debugging -a claude-code # one skill, one agent
```

Its documented targets (checked 2026-11-16) are Claude Code `.claude/skills/`; Codex, OpenCode, and Antigravity `.agents/skills/` (project scope). Review what it installs. Per-skill installs copy only that skill's directory, so links from a skill to `templates/`, `core/`, or `workflows/` in this repository will not resolve. Install the whole set, or vendor the repository, when you need workflows and templates.

**Bootstrap:** paste the [Axiom block](../templates/project/agents-md-block.md) into the project's `AGENTS.md` (or `CLAUDE.md`), or use the Claude Code plugin hook.

See each install guide. Do not assume paths work identically in global scope, nested workspaces, or older host versions. Verify discovery in the actual host.
