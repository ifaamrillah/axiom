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
Add an entry only after a mistake actually happened; remove it when the cause is gone.

- <YYYY-MM-DD> <what went wrong> → <rule to follow instead>
<!-- axiom:end -->
```

## Maintenance

- The marker records which Axiom release the pasted kernel came from. When a release note says the kernel changed, re-paste the Behavior, Routing, and Proportionality sections and update the marker. Keep your Project facts and Pitfalls.

- Re-verify project facts when build tooling changes; update the date and commit.
- Pitfalls are a learning loop: record the concrete mistake and the preventive rule, not a narrative.
- Keep the whole block under roughly 80 lines. Move durable detail to `.axiom/` documents and link to it.
