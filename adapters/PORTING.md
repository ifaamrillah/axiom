# Porting Axiom to a New Host

This guide lists the steps to support a new agent host. Each step ends in evidence you can record. Canonical skills stay in `.agents/skills/` and are never forked. Everything host-specific goes in `adapters/<host>/`.

## Steps

1. **Find where the host discovers skills.** Read the host's own docs for its project and user skill directories and the `SKILL.md` format it accepts. Prefer a host that reads `.agents/skills/` directly. Otherwise, document a link, copy, or plugin manifest that points at it. Note the docs URL and the date you checked.
2. **Load the kernel always-on.** The [kernel](../.agents/skills/axiom-orchestrator/references/kernel.md) must be in context from the first prompt. Use, in order of preference:
   - the host's always-loaded instructions file, with the [Axiom block](../templates/project/agents-md-block.md) pasted in;
   - a documented session-start hook that prints the kernel, read-only and with no network access (see the [Claude Code hooks](claude-code/hooks/)).
   If the host loses context on compaction or clear, make sure the kernel comes back.
3. **Map delegation.** Check whether the host has subagents and whether they inherit the main session's instructions. If they do not, give each subagent the kernel: a subagent-start hook if the host documents one, and a line in each agent definition telling it to read the kernel file. Map role metadata from `agents/roles/`: `capability` (deep, standard, fast) to a model tier, and `writes: false` to a read-only tool set. If the host has no subagents, the roles become instructions the main session follows in turn.
4. **Write `adapters/<host>/INSTALL.md`.** Cover project use, global use, bootstrap, role mapping, and a Verify section. Mark every claim as documented, verified (with version and date), or untested.
5. **Verify discovery with evidence.** In a scratch project, list the skills through the host's own command or prompt. Record the host version and the count (all Axiom skills, none missing).
6. **Verify the kernel.** Ask "What is rule 6 of the Axiom kernel?" with no file reads allowed. The answer should quote the evidence-before-claims rule. Repeat inside a subagent if the host has them.
7. **Verify triggers.** Run the trigger cases in `evaluations/cases/`. If `scripts/run_evals.py` has no driver for the host, run the prompts by hand and record each result. Store records in `evaluations/results/`. Before calling a miss a skill defect, read what the agent actually did.
8. **Update the shared docs.** Add a row to the [adapter overview](README.md) and the [compatibility report](../docs/compatibility/README.md). State only what step 5 to step 7 showed.

A step you skipped is not a step that passed. Say which steps are still open.

## Tool names per host

These are the names used in the existing install guides. Anything not stated there is marked unknown. Check the host docs before relying on a name.

| Concept | Claude Code | Codex | OpenCode | Antigravity |
|---|---|---|---|---|
| Project skill directory | `.claude/skills/`, or plugin manifest `skills` paths | `.agents/skills/` | `.agents/skills/` (compatibility source); `.opencode/skills/` takes precedence | `.agents/skills/` |
| User skill directory | unknown (not documented in the adapter) | `~/.agents/skills/` | user-level directories and `skills` config (paths not listed in the adapter) | `~/.gemini/config/skills/` |
| Always-loaded instructions | `CLAUDE.md`, or the plugin's SessionStart hook | `AGENTS.md` | `AGENTS.md` | `AGENTS.md` |
| Kernel in subagents | SubagentStart hook plus a line in each agent file (not yet live-verified) | unknown | unknown | unknown |
| Subagent definitions | plugin `agents` (`adapters/claude-code/agents/`) | unknown | unknown | unknown |
| Model tier field | `model:` (`opus`, `sonnet`, `haiku`, `inherit`) | `model` in config; `agents.default_subagent_model` (docs, untested) | `model:` in `.opencode/agents/<name>.md` (docs, untested) | unknown |
| Read-only control | `disallowedTools: Write, Edit, NotebookEdit` | unknown | active agent's `skill` permission affects skill loading; read-only control unknown | unknown |
| Skill listing to verify | ask "What skills are available?" | ask it to list or use `axiom-orchestrator` | `opencode debug skill` | ask the agent to invoke `axiom-orchestrator` |
| Eval runner support | `scripts/run_evals.py --host claude-code` | `scripts/run_evals.py --host codex` | none | none |
