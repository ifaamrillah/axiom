# Plan Anti-Patterns

Failures that make a plan look done while leaving the executor to guess. Run this list during the self-check (procedure step 8). Each row gives the red flag, why it hurts, and what to write instead.

## Content anti-patterns

| Red flag | Why it hurts | Do instead |
|---|---|---|
| "Implement the refund feature" as one task | No test cycle, no review point, no stopping place | Vertical slices of S–M size, each with its own verification |
| "Handle edge cases", "add appropriate validation", "add error handling" | Decides nothing; each executor picks different cases | List the cases with exact inputs and expected results |
| "Write tests for the above" as a separate final task | Tests written after code confirm what was built, not what was specified | Put the failing test as step 1 of each task |
| "Similar to T003" | The executor of T007 may never see T003 | Repeat what matters, or reference T003's Interfaces block by name |
| TBD, TODO, "decide later" | A known gap disguised as a plan | Decide now, or mark the plan `blocked` with the question |
| A function or type used but never defined in any task | Executor invents a name; the next task uses another | Every consumed name appears in some task's "Produces" |
| Name drift (`clearLayers` in T3, `clearAllLayers` in T7) | Compile error or duplicate code | Type-consistency pass in the self-check |
| Full function bodies for straightforward code | Plan longer than the code; executor copies bugs | Signature + test + spec values; body only for a non-obvious algorithm |
| Verification "run the tests" | Which tests? What result means pass? | Exact command + expected output ("4 passed") |
| No failing-run step | Test may pass for the wrong reason | "Run; expect FAIL with <reason>" before implementing |
| Spec values paraphrased ("about a month") | Executor picks 30, 31, or 28 | Copy exact values into Global constraints |
| File paths missing or "somewhere in services/" | Executor creates parallel structures | Exact path; new vs modify |

## Structure anti-patterns

| Red flag | Why it hurts | Do instead |
|---|---|---|
| Horizontal layers by default (all DB, then all API, then all UI) | Nothing works until the last task; integration bugs found late | Vertical slices; horizontal only for real foundations |
| "Set up project" task with no test | Unreviewable; often half-done | Fold setup into the first task that needs it |
| Every task marked `[P]` | Merge conflicts; tasks built on missing code | Apply the four `[P]` conditions in [sizing and ordering](sizing-and-ordering.md) |
| Two migrations in parallel | Ordering conflicts, broken rollbacks | Migrations are always sequential |
| Risky unknown task scheduled last | Design must change after most work is done | Risk first within each priority level |
| No checkpoints | Broken build discovered after 10 tasks | Checkpoint every 2–4 tasks and per priority level |
| A task leaves the build red "until the next task" | Bisect and review impossible; a stop leaves broken code | Merge the two tasks or reorder |
| P2 work before P1 is shippable | No viable increment if time runs out | P1 slice first, then Checkpoint A |
| One plan for three unrelated goals | Too large to hold in context; mixed reviews | Split into one plan per independently shippable goal |
| Splitting one goal across plans by layer | Neither plan ships value | Keep one goal in one plan |

## Scope anti-patterns

| Red flag | Why it hurts | Do instead |
|---|---|---|
| Task with no requirement ID ("add CSV export while we are here") | Scope creep; unreviewed behavior | Drop it, or get a requirement added to the spec |
| Requirement with no task | Silent gap found in production | Coverage map; every MUST maps to a task or checkpoint |
| Refactor bundled into a feature task | Review mixes structure and behavior | Separate refactor task with "no behavior change" verification, or a separate plan |
| Gold-plated abstractions ("make it pluggable for future providers") | Cost now for a need nobody stated | YAGNI; build for the spec |
| Plan silently changes a spec decision | Spec and code drift | Raise the conflict; change the spec through requirements-analysis |
| No `Scope mode:` line, or work outside the stated mode | Reviewers cannot tell whether extra or missing work was intended | State hold, selective, expand, or reduce; list expanded or deferred items by name |

## Process anti-patterns

| Red flag | Why it hurts | Do instead |
|---|---|---|
| Overwriting an existing plan with unchecked tasks | Destroys another session's progress | Same work: update in place. Different work: stop and ask |
| Planning while `[NEEDS CLARIFICATION]` sits on a must-have | Plan built on a guess | Return to requirements-analysis |
| `status: ready` with failing self-check items | Executor trusts a broken plan | Set `ready` only when all six Ready-for-Development checks hold |
| Writing code during planning | Plan becomes a justification of code already written | Planning is read-only for application code |

## Quick self-check

```bash
# Placeholders and vague steps left in the plan
grep -nEi 'TBD|TODO|TKTK|similar to|as above|appropriate|handle (edge|error)|etc\.' PLAN.md
# Tasks without a verify line (count should match the task count)
grep -c '^### T[0-9]\{3\}' PLAN.md; grep -c '^- Verify:' PLAN.md
# Requirement IDs in spec not cited anywhere in the plan
comm -23 <(grep -oE '\b(FR|NFR)-[0-9]{3}\b' spec.md | sort -u) \
         <(grep -oE '\b(FR|NFR)-[0-9]{3}\b' PLAN.md | sort -u)
```

The last command prints requirement IDs that the plan never mentions. Each one is a coverage gap or a deliberate deferral that the plan must state.

Sources: adapted from obra/superpowers (MIT) `skills/writing-plans/SKILL.md`, addyosmani/agent-skills (MIT) `skills/planning-and-task-breakdown/SKILL.md`, and general practice.
