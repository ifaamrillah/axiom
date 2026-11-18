# Session Diagnosis

Diagnose a real agent session from its transcript: what the agent did, where it lost time, and whether a skill helped or got in the way. Use it when a user reports that a session went badly, when an eval run fails and the reason is unclear, or before changing a skill because "it did not work".

Rule: **before blaming a skill, read what the agent actually did.** A failure can come from the prompt, the workspace, missing permissions, the host, or the model. The transcript decides which, not the result line.

## Inputs

- A host transcript of the session: an exported session log (often one JSON event per line), a recorded eval stream, or a pasted conversation. Note the format and how you will cite positions in it.
- What the user asked for and what they say went wrong.
- Optional: the skills and project instructions present during the session, and the repository at the session's commit.

If there is no transcript, stop and ask for one. Do not diagnose from memory or from the final answer alone.

## Citing evidence

Every finding cites a transcript location: `file:line` for a text log, or the event index (0-based position in the event list) for a structured stream. Quote the decisive part in under 20 words. **A finding without a location is discarded**, however plausible it sounds.

Number the events once, before analysis, so every analyst uses the same indexes. For a long log, list for each event: index, role, tool name, and the first line of input or output.

## Dimensions

Analyse each dimension separately. When the host can delegate to subagents, give each dimension to its own analyst with the numbered event list and this section; each returns findings only for its dimension. Without delegation, do the passes one after another.

| Dimension | Questions | Typical evidence |
|---|---|---|
| Skill timeline | Which skills loaded, at which event? Did the right one load before the work it governs? Did one load and then get ignored? | Skill load events, reads of skill files, the first edit after each load |
| Plan adherence | Was there a plan or checklist? Which steps were done, skipped, or reordered? Did the agent say why? | Plan text, task lists, the order of edits and test runs |
| Repeated work | Which files were read or searched more than once? Which commands were rerun without a change in between? | Duplicate reads, identical commands, re-derived facts |
| Stumbles and retries | Which tool calls failed? Was the next call a fix, a blind retry, or a switch of approach? Were there permission denials or timeouts? | Error results, denials, the call after each error |
| Quality evidence | Is each claim in the final answer backed by output in the transcript? Which claims have no supporting event? | Test output, command results, the final answer's claims matched to events |
| Cost and time | How many events, tool calls, and tokens (if reported)? Where did most of them go? | Usage fields, timestamps, the longest stretch without progress |

For quality evidence, list each claim of the final answer ("tests pass", "root cause is X") with the event that proves it, or "none". An unbacked claim is a finding even when the claim is true.

## Attributing the cause

For each problem, name the most likely cause from the evidence, and say what would confirm it:

| Cause | Sign in the transcript |
|---|---|
| Skill not loaded | No load event before the relevant work |
| Skill loaded but rule ignored | Load event, then an action the skill forbids |
| Skill unclear or wrong | The agent followed the text and the text led it astray; quote the line |
| Prompt or workspace | The task was ambiguous, or the fixture lacked what the task needs |
| Harness | Permission denial, budget cap, timeout, missing tool |
| Model | Correct guidance, loaded, and still not followed across repeats |

Only "skill unclear or wrong" justifies a skill edit by itself. For "rule ignored" or "model", add an eval case that reproduces the failure first, then change the skill and rerun.

## Output template

```markdown
## Session diagnosis: <session or run name>

- Transcript: <path or source>, <format>, <N> events
- Task: <what the user asked>
- Reported problem: <what went wrong, in the user's words>

### Findings

| # | Dimension | Finding | Evidence | Likely cause |
|---|---|---|---|---|
| 1 | Skill timeline | debugging loaded after the first edit | event 14 (load) after event 9 (edit pricing.py) | Skill not loaded in time |
| 2 | Quality evidence | "all tests pass" has no test run after the last edit | final answer; last test run is event 21, last edit is event 27 | Rule ignored |

### Discarded

- <finding that had no transcript location, and why it was dropped>

### Recommended actions

1. <eval case to add or rerun, skill line to change, or harness fix>, tied to finding numbers

### Not assessed

- <dimension or question the transcript cannot answer>
```

Keep the report to what the transcript shows. If two dimensions point to the same event, report it once and list both dimensions.

Sources: idea from obra/superpowers (session diagnosis; MIT), rewritten.
