# Context Budget

The coordinator's context is the scarcest resource in a long run. Spend it on decisions, integration, and evidence. Push bulk reading and mechanical edits to workers or to targeted reads.

## What the coordinator keeps vs pushes out

| Keep in the coordinator | Push to a worker or to a file |
|---|---|
| Spec excerpts that drive decisions | Full-file reads of large modules |
| The plan, task status, rulings | Broad codebase searches across many directories |
| Interfaces shared between tasks | Mechanical edits across many files |
| Diff stats and failing test names | Full test logs (keep the failing lines only) |
| Review verdicts and open findings | Narrative worker reports (keep the contract fields) |

## Loading order

Load context from most durable to most transient, and only the slice the current task needs:

1. Project instructions and the [kernel](kernel.md) (always).
2. `.axiom/project/` knowledge and the active workflow state (at session start or resume).
3. The spec or plan section for the current task, not the whole document.
4. The files the task will change, their tests, and one existing example of the pattern.
5. Error output for the current iteration: the failing assertion and stack frame, not 500 lines of log.

## Budget rules

- Check size before reading: `wc -l <file>`. Over ~300 lines, read the outline or search for the symbol, then read only the relevant range.
- Search before reading. A good `rg -n` with a narrow path beats opening five files.
- Ask workers for a bounded return (for example "under 40 lines: status, files, commands, concerns"). Long reports burn coordinator context.
- Quote, do not paste. A brief carries the three spec lines that matter, not the spec.
- One concern per worker. A worker given two domains returns twice the noise.
- Prefer file paths and line numbers over code blocks in reports. Fetch code only when a decision depends on it.

## Durable state beats memory

Conversation memory does not survive compaction or a new session. Coordinators that lose their place have redone completed tasks, which is the most expensive failure in long runs.

- Keep progress in the workflow state file (`.axiom/workflows/active/<ID>/`), not only in the conversation.
- After every accepted task, write: task ID, status, commit or diff reference, verification command and result, and rulings.
- On resume, trust the state file plus `git log` and `git status` over recollection. Rerun verification when the recorded result predates later commits.

## Safe session boundaries

Start a fresh session or compact only at a task boundary, after persisting:

1. accepted scope and rulings,
2. finished tasks and the next pending task,
3. changed files and whether they are committed,
4. exact verification commands and outcomes,
5. open questions, risks, and approvals still needed.

Do not infer an approval from a previous conversation unless the state file records it.

## Signs the budget is going wrong

| Symptom | Fix |
|---|---|
| You re-read a file you read earlier in the session | Record the needed facts in the state file once |
| Worker reports are longer than the diffs | Tighten the return format in the brief |
| You are about to read a 2,000-line file to find one function | Search for the symbol; read a range |
| You are pasting full logs into briefs | Paste the failing test name, assertion, and top frame |
| Output quality drops: wrong conventions, invented APIs | Reload the conventions and the pattern file; consider a fresh session at the next boundary |

Sources: adapted from addyosmani/agent-skills (MIT) context-engineering, yeachan-heo/oh-my-claudecode (MIT) explore agent context budget, obra/superpowers (MIT) subagent-driven-development, and general practice.
