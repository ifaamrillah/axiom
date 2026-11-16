# Platform Compatibility

**Documentation reviewed: 2026-11-15/16. Live runs: Claude Code only, 2026-11-16.** This report separates documentation inspection from live runtime evidence.

| Host | Officially documented discovery | Axiom-specific status |
|---|---|---|
| Claude Code | Project `.claude/skills/`; plugin manifest `skills` paths | **Live-tested (2.1.325):** plugin validated and loaded with `--plugin-dir` (24 skills, 4 subagents, kernel hook observed in context); trigger evals recorded (see below) |
| Codex | Project `.agents/skills/`; user `~/.agents/skills/` | Official docs inspected; live discovery and invocation not tested |
| OpenCode | `.agents/skills/` is a project compatibility source; permissions and precedence can affect loading | Official docs inspected; live discovery and invocation not tested |
| Antigravity | Workspace `.agents/skills/`; global `~/.gemini/config/skills/` | Official docs inspected; live discovery and invocation not tested |

## Claude Code live evidence (2026-11-16, Claude Code 2.1.325, host default model)

All runs used `scripts/run_evals.py` with user-level settings excluded (`--setting-sources project,local`). Each run happened in a disposable workspace with the skills copied into `.claude/skills/`. Full records are in [`evaluations/results/`](../../evaluations/results/README.md).

**Plugin:** `claude plugin validate .` passed. Its only warnings were the intentionally omitted `version`, plus "no frontmatter" notices for role cards, which are not loaded as agents. A headless session with `--plugin-dir` listed all 24 `axiom:` skills and exactly 4 `axiom:` subagents, and quoted kernel rule 5 from context without reading files.

**Trigger accuracy** (latest run per skill; positives must invoke the skill, negatives must not):

| Skill | Result | Note |
|---|---|---|
| verification-before-completion | 5/5 | 4/5 before the description gained commit and ship phrasing |
| debugging | 7/7 | 6/7 before the description gained the "returns X but should be Y" phrasing |
| tdd | 4/5 | "Write a failing test for this bug first, then fix it" still not triggered |
| code-review | 5/5 | 3/5 before; one miss was routed to the host's built-in `simplify` skill |
| security-audit | 5/5 | |
| spec-analysis | 5/5 | 4/5 before the "what's left to implement" phrasing |

Total on the latest runs: 31/32. Not run: `axiom-orchestrator`, `quality-constraints`, `product-discovery`, `ui-ux-design`.

**Behavior:** `debugging/B1` (seeded divisor bug) **failed** twice. The agent named the root cause, added a regression test, and ran the tests after the fix. It did not invoke the skill, and it edited before reproducing. Grading was done by the authoring session, not an independent grader. Other behavior cases have not been run.

## What has not been checked

- Marketplace install from GitHub (`/plugin marketplace add`), the `npx skills` installer, and global installs.
- Any live run on Codex, OpenCode, or Antigravity. The eval runner supports only Claude Code.
- Behavior cases other than `debugging/B1`; independent grading.
- Results may differ with other models, versions, or user settings.

## Graceful fallbacks

- If a skill is not discovered, open its `SKILL.md` directly and follow it manually.
- If host-specific metadata is rejected, keep canonical frontmatter at `name` and `description`; do not add a required Axiom extension.
- If Claude Code symlinks are unavailable, copy the skill directory or use the plugin, and treat `.agents/skills/` as the source of truth.
- If hooks are unavailable, paste the kernel block into the project's instructions file.
- If workflow state is unsupported, maintain a Markdown checklist or use the host conversation.

## Primary documentation

- [Codex skills](https://developers.openai.com/codex/skills/)
- [OpenCode skills](https://opencode.ai/docs/skills/)
- [Antigravity skills](https://antigravity.google/docs/skills)
- [Claude Code skills](https://code.claude.com/docs/en/skills), [plugin manifest](https://code.claude.com/docs/en/plugins-reference)
