# Platform Adapters

Canonical skills remain in `.agents/skills/`. Adapters explain how a host discovers them and where host-specific behavior differs. They never fork skill content.

| Host | Project-level discovery | Packaging / bootstrap | Status |
|---|---|---|---|
| Claude Code | `.claude/skills/`, or the plugin manifest | `.claude-plugin/` plugin and marketplace; optional SessionStart kernel hook | Manifest validated with `claude plugin validate` (2026-11-16); see [compatibility](../docs/compatibility/README.md) for live runs |
| Codex | `.agents/skills/` | Axiom block in `AGENTS.md` | Live trigger evals 107/113 (codex-cli 0.169.0, 2026-11-16) |
| OpenCode | `.agents/skills/` (compatibility source) | Axiom block in `AGENTS.md` | Discovery verified (opencode 1.19.5, 24/24 skills); invocation untested |
| Antigravity | `.agents/skills/` | Axiom block in `AGENTS.md` | Docs reviewed 2026-11-15; not tested (desktop IDE, needs a Google sign-in) |

## Installing into another project without a custom CLI

**Git:** clone or vendor this repository and copy or link `.agents/skills/` into the target project. Keep the references next to each skill.

**`skills` installer (third-party, optional):** the open [`skills`](https://github.com/vercel-labs/skills) installer discovers skills in a repository's `.agents/skills/` and installs them for many agents:

```sh
npx skills add ifaamrillah/axiom                                  # choose agents interactively
npx skills add ifaamrillah/axiom --skill debugging -a claude-code # one skill, one agent
```

Its documented targets (checked 2026-11-16) are Claude Code `.claude/skills/`; Codex, OpenCode, and Antigravity `.agents/skills/` (project scope). Review what it installs.

Verified 2026-11-16 with `skills@1.8.1` and Claude Code 2.1.325, from a scratch project:

- `npx skills add "ifaamrillah/axiom#<branch>" --skill '*' -a claude-code -a codex -a opencode -a antigravity -y` installed all 24 skills into `.agents/skills/`, symlinked them into `.claude/skills/`, and wrote `skills-lock.json` with the source and ref. Claude Code then listed all 24 as project skills.
- Pin a branch or tag with `owner/repo#ref`. The `/tree/<ref>` URL form failed for a branch name containing `/`.
- **Only skill directories are installed, even with `--skill '*'`.** That first check found 39 links in 17 skills that pointed outside `.agents/skills/` and did not resolve. Skills are now self-contained: templates and prompts that a skill fills are bundled under its `assets/`, and other repository files are named as plain text. A simulated skills-only copy has 102 local links and none broken; the validator keeps it that way. Workflows, contracts, and integration guides are still not installed. Use the Claude Code plugin, or vendor the whole repository, when you want them.
- As project skills, names are not namespaced. Axiom's `code-review` shares its name with a Claude Code built-in skill; the project skill was the one listed. The plugin's `axiom:` namespace avoids the clash.
- The installer does not add the kernel. Paste the bootstrap block as below.
- The installer sends install telemetry unless `DO_NOT_TRACK=1` is set.

**Bootstrap:** paste the [Axiom block](../templates/project/agents-md-block.md) into the project's `AGENTS.md` (or `CLAUDE.md`), or use the Claude Code plugin hook.

See each install guide. Do not assume paths work identically in global scope, nested workspaces, or older host versions. Verify discovery in the actual host.
