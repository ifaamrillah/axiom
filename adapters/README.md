# Platform Adapters

Canonical skills remain in `.agents/skills/`. Adapters explain how a host discovers them and where host-specific behavior differs; they do not fork the skill content.

| Host | Project-level discovery guidance | Status in this repository |
|---|---|---|
| Codex | `.agents/skills/` | Official docs reviewed 2026-11-15; Axiom live discovery/invocation untested |
| OpenCode | `.agents/skills/` compatibility source | Official docs reviewed 2026-11-15; Axiom live discovery/invocation untested |
| Antigravity | `.agents/skills/` | Official docs reviewed 2026-11-15; Axiom live discovery/invocation untested |
| Claude Code | `.claude/skills/` | Manual copy/symlink guide; official docs reviewed 2026-11-15; Axiom live discovery/invocation untested |

See each install guide and the [compatibility report](../docs/compatibility/README.md). Do not assume paths work identically in global scope, nested workspaces, or older host versions. Verify discovery in the actual host.
