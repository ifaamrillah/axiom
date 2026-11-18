# Eval run: kernel in subagents (manual, claude-code)

- Date: 2026-11-17T20:30
- Host version: 2.1.326 (Claude Code)
- Model: host default
- Install: plugin loaded with `--plugin-dir` (this repository), `--setting-sources project,local`, empty git workspace
- Case: `evaluations/cases/axiom-orchestrator.md` B4, run by hand (the runner copies skills and does not load the plugin hooks)
- Prompt to the main session: spawn one general-purpose subagent with exactly "Without reading any files or using any tools, quote rule 6 of the Axiom kernel word for word, or say you do not have it." and include no kernel text.
- Grader: the coordinating session read the stream; no independent grader

| Arm | Agent tool input contained kernel text | Subagent tool calls | Subagent answer | Verdict |
|---|---|---|---|---|
| Plugin with `SubagentStart` hook | no (prompt sent exactly as given) | 0 | Quoted rule 6, "Evidence before claims", word for word | pass |
| Control: same plugin copy with the `SubagentStart` entry removed from `hooks.json` | no | 0 | "I don't have rule 6 of the Axiom kernel. Nothing in my current context contains the kernel's text." | expected miss |

Conclusion: on Claude Code 2.1.326 the SessionStart kernel does not reach a general-purpose subagent; the `SubagentStart` hook delivers it. One run per arm; the agent-file instruction to read the kernel was not exercised, because no file read was allowed.
