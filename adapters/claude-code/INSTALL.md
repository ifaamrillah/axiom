# Claude Code Adapter

Axiom's canonical skills live in `.agents/skills/`. Claude Code discovers project skills in `.claude/skills/`, and plugin skills from the directories that a plugin manifest declares. Choose one installation path.

*Docs checked 2026-11-16 (plugin manifest and marketplace reference). The manifest was validated with `claude plugin validate .` on Claude Code 2.1.325. The only warning is the deliberately omitted `version`, so that installs track the repository until the first tagged release (ADR-0003).*

## Option A: plugin (recommended)

The repository root is a Claude Code plugin and a single-plugin marketplace:

- `.claude-plugin/plugin.json` declares `"skills": ["./.agents/skills/"]` (added to the default scan) and `"hooks": "./adapters/claude-code/hooks/hooks.json"`.
- `.claude-plugin/marketplace.json` lists the plugin with `"source": "./"`.

Install inside Claude Code (one command at a time):

```text
/plugin marketplace add ifaamrillah/axiom
/plugin install axiom@axiom
```

For a local checkout during development:

```sh
claude --plugin-dir /path/to/axiom
```

Plugin skills are namespaced, for example `axiom:debugging`. Versions: the manifest sets `version`, which each release bumps (see [Upgrading](../../docs/UPGRADING.md)). Update with `claude plugin marketplace update axiom`, then `claude plugin update axiom@axiom`, and restart. To stay on one release, add the marketplace at its tag, for example `claude plugin marketplace add "https://github.com/ifaamrillah/axiom.git#v0.1.0"`.

Verified 2026-11-16 on Claude Code 2.1.325: adding the marketplace from GitHub at a branch ref and running `claude plugin install axiom@axiom` (both at `--scope local` in a scratch project) loaded all 24 `axiom:` skills (the count at that date), the 4 `axiom:` subagents, and the kernel through the session-start hook.

## Option B: project skills without a plugin

Link or copy each skill directory into the project's `.claude/skills/`:

```sh
mkdir -p .claude/skills
for d in /path/to/axiom/.agents/skills/*/; do ln -s "$d" ".claude/skills/$(basename "$d")"; done
```

Use copies when symlinks are unsuitable (some Windows setups). Treat `.agents/skills/` as the source of truth and do not edit the copies. Alternatively, the `skills` installer (`npx skills add ifaamrillah/axiom -a claude-code`) discovers `.agents/skills/` in this repository and installs into `.claude/skills/`. See the [adapter overview](../README.md).

## Kernel bootstrap (optional)

The plugin's `SessionStart` hook ([hooks.json](hooks/hooks.json) → [session-start.sh](hooks/session-start.sh)) prints the [Axiom kernel](../../.agents/skills/axiom-orchestrator/references/kernel.md) at startup, clear, and compaction. Claude Code adds SessionStart stdout to the context. The hook is read-only (ADR-0004).

Without the plugin, either paste the kernel into `CLAUDE.md` using the [Axiom block](../../templates/project/agents-md-block.md), or add the hook to `.claude/settings.json` yourself:

```json
{
  "hooks": {
    "SessionStart": [
      {
        "matcher": "startup|clear|compact",
        "hooks": [{ "type": "command", "command": "sh /path/to/axiom/adapters/claude-code/hooks/session-start.sh", "timeout": 10 }]
      }
    ]
  }
}
```

The hook needs a POSIX `sh` (on Windows, Git Bash). If no shell is available, use the `CLAUDE.md` block.

### Kernel in subagents

SessionStart context stays in the main conversation; subagents do not get it. The plugin adds a second hook for this:

- A `SubagentStart` hook with no matcher, so it runs for every subagent, built-in or custom. [subagent-start.sh](hooks/subagent-start.sh) reads the same kernel file and prints it as JSON: `{"hookSpecificOutput": {"hookEventName": "SubagentStart", "additionalContext": "<kernel>"}}`. The [hooks reference](https://code.claude.com/docs/en/hooks) (checked 2026-11-17) documents `additionalContext` for SubagentStart and does not list it among the events whose plain stdout becomes context. The script is read-only and needs only `sh` and `awk`.
- Each of the four Axiom subagents also tells itself to read the kernel file if it is not in its context. This covers hosts or versions where the hook does not run.

Cost: about 5 KB of kernel text per subagent launch. To limit it to Axiom's own subagents, add `"matcher": "^axiom:"` to the SubagentStart entry. Plugin subagents report a plugin-scoped type such as `axiom:reviewer`.

**Live-verified once (Claude Code 2.1.326, 2026-11-17).** With the hook, a general-purpose subagent quoted kernel rule 6 without reading files; with the hook removed, it said it did not have the kernel ([record](../../evaluations/results/2026-11-17-2030-claude-code-subagent-kernel.md)). One run per arm. To add it without the plugin, put the same entry under `"SubagentStart"` in `.claude/settings.json`, with the path to `subagent-start.sh`.

## Slash commands

The manifest's `commands` key adds four user-invoked commands from [commands/](commands/): `/axiom:spec`, `/axiom:plan`, `/axiom:review`, and `/axiom:ship`. Each sets `disable-model-invocation: true`, so the model never loads them on its own. They only name canonical skills and subagents; all procedure lives in the skills. Not yet verified in a live session.

## Role mapping

Portable role metadata in `agents/roles/` maps to Claude Code subagents as follows:

| Axiom | Claude Code |
|---|---|
| `capability: deep` | a high-reasoning model (for example `model: opus`) |
| `capability: standard` | the default model (for example `model: sonnet`) |
| `capability: fast` | a fast model (for example `model: haiku`) |
| `writes: false` | `disallowedTools: Write, Edit` in the subagent definition |

Model aliases change over time. Check current names in the Claude Code docs before pinning them.

### Work categories

The orchestrator names four host-neutral work categories. On Claude Code they map to the shipped subagents and their `model:` fields:

| Category | Claude Code choice |
|---|---|
| `quick` | `axiom:researcher` (`model: haiku`) for read-only lookups; otherwise inherit the session model |
| `deep` | `axiom:reviewer` or `axiom:security-reviewer` (`model: opus`) for review and audit |
| `visual` | inherit the session model; no dedicated subagent |
| `writing` | inherit the session model (`axiom:implementer` uses `model: inherit`) |

This table is a recommendation, not a rule enforced by the plugin. For Codex and OpenCode, see the work-category note in their INSTALL files; Antigravity has no mapping documented.

The plugin ships four subagents built on this mapping, in [agents/](agents/): `axiom:reviewer` and `axiom:security-reviewer` (deep, read-only), `axiom:researcher` (fast, read-only), and `axiom:implementer` (inherits the session model, writes). The manifest's `agents` key lists only these files, so the role cards in the repository's top-level `agents/` folder are **not** loaded as subagents. A live session listed exactly these four agent types. `claude plugin validate` still prints "No frontmatter" warnings for the role cards. These warnings do not change the loaded agents.

## Verify

1. Start a session and ask "What skills are available?" `verification-before-completion` and `axiom-orchestrator` should be listed (namespaced as `axiom:` when installed as a plugin).
2. With the hook enabled, ask "What is rule 6 of the Axiom kernel?" The answer should quote the evidence-before-claims rule without reading files.
3. Subagent kernel (not yet run): ask the main session to spawn a general-purpose subagent that must answer "What is rule 6 of the Axiom kernel?" without reading files. The subagent should quote the evidence-before-claims rule. Check the subagent transcript for a file read; if it read `kernel.md`, the hook did not deliver it.
4. Run the trigger evals: `python3 scripts/run_evals.py --host claude-code --kind trigger --skill debugging`.

Recorded results live in `evaluations/results/`. See the [compatibility report](../../docs/compatibility/README.md) for what has actually been run.

Official references: [skills](https://code.claude.com/docs/en/skills), [plugin manifest](https://code.claude.com/docs/en/plugins-reference), [marketplaces](https://code.claude.com/docs/en/plugins/marketplace-reference).
