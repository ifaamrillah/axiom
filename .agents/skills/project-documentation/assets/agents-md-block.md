# Axiom Block for Project Instructions

Paste the block below into the consuming project's instructions file (`AGENTS.md` for Codex, OpenCode, and Antigravity; `CLAUDE.md` for Claude Code unless the Claude Code plugin's session-start hook already injects the kernel). Keep it short: every line is loaded in every session.

Fill only verified facts. Remove placeholder lines you cannot verify.

```markdown
<!-- axiom:begin v0.1.0 -->
## Axiom

<copy the Behavior, Routing, and Proportionality sections of
.agents/skills/axiom-orchestrator/references/kernel.md here>

### Project facts (verified <YYYY-MM-DD> at <commit>)

- Install: `<command>`
- Focused test: `<command>`
- Full checks: `<command>`
- Conventions: `<link to .axiom/conventions.md or short rule>`
- Quality bar: `.axiom/CONSTRAINTS.md` (if present)
- Constitution: `.axiom/constitution.md` (if present)

### Pitfalls

Observed agent mistakes in this repository and the rule that prevents each.
Promote a learning from `.axiom/learnings/` here only when it was seen in 2 sessions
or the user confirmed it. Remove a line when its cause is gone or a check enforces it.

- <YYYY-MM-DD> <what went wrong> → <rule> (enforce: lint | type | check | test | doc)
<!-- axiom:end -->
```

## Maintenance

- The marker records which Axiom release the pasted kernel came from. When a release note says the kernel changed, re-paste the Behavior, Routing, and Proportionality sections and update the marker. Keep your Project facts and Pitfalls.

- Re-verify project facts when build tooling changes; update the date and commit.
- Pitfalls are the promoted end of a learning loop: retros write candidates to `.axiom/learnings/<yyyy-mm-dd>-<slug>.md`; only repeated or user-confirmed ones become a line here. Each line names the strongest enforcement that could replace it (lint, type, check, test) so the list stays short.
- Keep the whole block under roughly 80 lines. Move durable detail to `.axiom/` documents and link to it.
