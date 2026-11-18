# Review Loop for Delegated Work

A worker's report is a claim, not evidence. Accept a task only after you have checked its diff and rerun its checks. Use this loop for every delegated task, and for your own inline work when the change is risky.

## The loop

```
dispatch → report → triage status → review (spec, then quality) → verify → accept
                                    ↘ findings → fix round → scoped re-review ↗
```

1. **Triage the status** (table below). Only DONE and DONE_WITH_CONCERNS go to review. `WORKING` is a heartbeat, not a status to triage.
2. **Inspect the diff yourself.** `git diff --stat <base>..HEAD` first, where `<base>` is the SHA recorded in the brief before dispatch, never `HEAD~1` (a worker may have made several commits or none). Files outside the allowed set are an automatic finding.
3. **Spec review first.** Does the change do what the acceptance criteria say, no less and no more? Use the [task reviewer prompt](../assets/prompts/task-reviewer.md). Spec gaps block quality review: no point polishing the wrong thing. Treat the plan and the report as testimony: for each factual claim they make ("`Money` already rounds", "no other caller uses this"), try to refute it against the code. A claim that fails becomes a finding.
4. **Quality review second.** Correctness risks, error handling, tests that prove behavior, conventions, needless complexity.
5. **Verify fresh.** Rerun the brief's verification commands now, in the integrated tree. Compare with the baseline. Output older than the last edit does not count.
6. **Resolve "cannot verify from diff" items.** A reviewer may flag requirements that live in unchanged code or span tasks. You hold the cross-task context, so check each one yourself. A confirmed gap enters the fix loop.
7. **Accept** only when spec and quality pass and fresh checks show no new failures. Record the task as done in the workflow state with the evidence.

## Status triage

| Status | Action |
|---|---|
| DONE | Review. |
| DONE_WITH_CONCERNS | Read the concerns first. Correctness or scope concerns: resolve before review. Observations ("file is getting long"): note in state, then review. |
| NEEDS_CONTEXT | Supply the missing fact and re-dispatch. Add the fact to the brief so a later round has it. |
| BLOCKED | Something must change. See stuck handling below. |
| No status, or a long narrative | Treat as NEEDS_CONTEXT on your side: ask for the contract format before reviewing. |

## Fix rounds

- **Minor findings** (naming, small style) do not enter the loop. Record them in the workflow state as deferred and show them to the final whole-change review.
- **A finding that contradicts the plan or spec** is yours to rule on. Decide against the spec, record a ruling (see [execution](execution.md)), then act.
- **Everything else** enters the loop. A round is one fix dispatch plus one re-review scoped to the fix diff and the open findings. Use the [fix loop prompt](../assets/prompts/fix-loop.md).
- **Re-review uses a fresh reviewer**, never the one that raised the findings. Scope it to the delta: the diff from the commit the fix started at, the open findings, and a regression check of the task's acceptance. Do not pass on the previous reviewer's conclusions. In a workflow instance, point it at the existing brief and report files instead of re-pasting them.
- Before re-review, confirm the fix report names the covering tests, the command, and its output. Missing any of the three: send it back.

| Round | Who fixes |
|---|---|
| 1-2 | The original worker, with findings quoted verbatim (resume it if the host allows; otherwise a fresh worker with the brief, prior report, and findings) |
| 3 | A fresh worker one tier higher, told what was tried and failed |
| After 3 | Stop the loop. Adjudicate each open finding yourself (below) |

Do not fix findings yourself in the coordinator while a loop is open. Coordinator fixes skip review and fill your context.

### Adjudicate at the cap

| Finding | Decision |
|---|---|
| Reviewer is wrong or the point is debatable | Park it with a ruling that says why the code stands |
| Real, but nothing later depends on it | Park it as a known gap; list it in the final report |
| Real and a later task builds on it | Rule on the smallest unblocking change, record it, carry it into the next brief |
| Every path forward is a guess | Stop and ask the user (stop condition 4 in [execution](execution.md)) |

Every adjudication is written down. A silent discard is forbidden.

## Stuck and failure handling

A worker that says it is stuck is giving you information. Never resend the same brief to the same tier.

| Symptom | Likely cause | Change |
|---|---|---|
| NEEDS_CONTEXT about an interface or convention | Brief too thin | Add the quoted interface or a pattern file path |
| BLOCKED: "tests fail before my change" | No baseline in the brief | Run the baseline yourself; send the pre-existing failure list |
| BLOCKED: task needs edits outside allowed files | Ownership drawn wrong | Widen ownership deliberately, or split the task and sequence it |
| Same finding survives two rounds | Worker cannot see its own error | Fresh worker, one tier up, with prior attempts summarized |
| Worker loops on retries or timeouts | Environment issue (port in use, missing service, flaky network) | Diagnose the environment inline; do not delegate a flaky environment |
| Worker changed tests to pass | Weak constraints | Restrict test files; require failing-then-passing evidence |
| Task too large to finish in one worker context | Scope | Split into smaller tasks with their own acceptance checks |
| Plan itself is wrong | Plan defect | Rule on the correction, record it, re-dispatch with the ruling in the brief |
| Worker went silent or crashed, or its report still says `WORKING` | Host or budget limit | Inspect the tree (`git status`, `git diff`); keep usable work, re-brief the rest |

Cap total attempts per task (default: 3 fix rounds plus one escalation). When the cap is reached, stop that task, isolate it, continue independent work, and report it as blocked with evidence.

## Final whole-change review

After the last task, review the combined diff from the starting commit, at the `deep` tier when available:

- integration seams between tasks (types, error contracts, config keys),
- the deferred minor findings list: fix, accept, or ticket each,
- full gate checks against the baseline,
- leftovers: debug output, commented code, TODOs added during the run, stray files.

## Red flags

| Thought | Answer |
|---|---|
| "The worker said all tests pass" | Run them yourself. Paste the summary line. |
| "The diff is small, skip spec review" | Small diffs miss requirements too. Check the acceptance list. |
| "I'll just fix this one finding myself" | It skips review. Send it back, or record why inline is justified. |
| "Round four will get it" | Escalate tier or adjudicate. Repetition without change does not converge. |
| "It mostly works" | Not a verdict. State PASS or FAIL with the failing criterion. |

Sources: adapted from obra/superpowers (MIT) subagent-driven-development references (fix-loop, handling-reports, cannot-verify, final-review), yeachan-heo/oh-my-claudecode (MIT) verifier and ralph, and general practice.
