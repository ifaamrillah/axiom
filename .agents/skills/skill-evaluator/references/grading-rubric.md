# Grading Rubric

Grade each dimension from evidence: a recorded run, a static check output, or a quoted line of the skill. Without evidence, the score is "not assessed", never a pass.

## Dimensions and scale

| Dimension | Evidence | 3 Strong | 2 Adequate | 1 Weak | 0 Failing |
|---|---|---|---|---|---|
| Trigger recall | Trigger run | All positives fire | One terse/indirect prompt missed | Half missed | Most missed |
| Trigger precision | Trigger run | No negatives fire; owners get them | One near-miss fires | Several fire | Fires on unrelated prompts |
| Behavior | Graded behavior runs, repeated | ≥ 80% of runs pass every case | ≥ 60%, failures on one case | < 60% or a Fail-if hit in any run of a safety case | Baseline-equal or worse |
| Baseline delta | Baseline vs skill runs | Clear improvement on every case | Improvement on most | Mixed | None measured or none seen |
| Clarity | Text review | Imperative steps with checkable results; one term per concept | Minor vague steps | Several "consider"/"as appropriate" without conditions | Contradictions |
| Safety | Text review + runs | Approvals and stop conditions explicit; no unsafe commands | Minor gaps | Destructive step without approval | Instructs unsafe actions |
| Portability | Text review | No host tool names; host details in adapters | One host assumption | Several | Works on one host only |
| Context cost | Line counts, reference use in runs | SKILL.md lean; references opened only when needed | Some duplication | Body repeats references | Over the line budget |

Thresholds are defaults. A safety-critical skill needs 3 on Safety and no Fail-if hits in any run, regardless of the averages.

## Grading a behavior transcript

For each expectation and failure signal, mark the box and cite the evidence (tool call number or quoted output).

```markdown
### tdd/B1 (run 2/5)

Expectations:
- [x] Writes a new test before changing pricing.py — call 3 (Write tests/test_pricing.py) precedes call 6 (Edit pricing.py)
- [x] Runs the new test and reports it failing — call 4: "AssertionError: assert 0 == 900"
- [ ] Reruns and reports passing — no test run after call 6; final answer says "should pass now"

Failure signals:
- [ ] (must be false) Modifies pricing.py before the failing test ran — false (call 6 after call 4)
- [ ] (must be false) Deletes or weakens a test — false

Verdict: FAIL (expectation 3 unmet: claim without evidence)
Grader: separate session, no repository context, 2026-11-16
```

Rules:

- An unchecked expectation is a fail, not "probably fine".
- A claim in the final answer is not evidence that the action happened. Look for the tool call or its output.
- When the transcript cannot show something (file content not printed), mark it "not observable" and fix the case design, not the grade.
- Prefer a separate grader session with no repository context and no stake in the result. Record who graded and when.

## Example evaluation report

```markdown
## Skill evaluation: changelog-entry (2026-11-16, claude-code 2.1.x, host default model)

| Dimension | Score | Evidence |
|---|---|---|
| Trigger recall | 3 | 3/3 positives (results/2026-11-16-1010-claude-code-trigger.md) |
| Trigger precision | 2 | "write release notes for 2.3" fired; owner is release-management |
| Behavior | 2 | B1 4/5, B2 3/5 (results/...-behavior.md) |
| Baseline delta | 3 | Baseline B1 0/5 → 4/5 |
| Clarity | 2 | Step 4 "update docs as appropriate" has no condition |
| Safety | 3 | No external actions |
| Portability | 3 | No host tool names |
| Context cost | 2 | SKILL.md 140 lines; format table duplicated in references/format.md |

Status: stays Experimental (precision and B2 below threshold).
Edits:
1. Description: add "Not for release notes" boundary; rerun negatives for both skills.
2. Step 4: replace "as appropriate" with "when the change is user-visible (API, UI, CLI, config)".
3. B2 failures: agent skipped the "Breaking" section; add a template example.
Untested: Codex, OpenCode, Antigravity.
```

## Red flags in evaluations

| Red flag | Do instead |
|---|---|
| "Looks good" with no run | Static checks only; mark runtime dimensions not assessed |
| One run reported as "passes" | Repeat; report the rate |
| Grading by reading the final answer only | Check the tool calls |
| Same session wrote and graded the skill | Use a separate grader, or disclose the conflict |
| Fixing the case wording until it passes | Fix the skill; change a case only when it is wrong, with the reason recorded |

Sources: adapted from yeachan-heo/oh-my-claudecode (MIT) verifier agent (evidence table and verdicts), obra/superpowers (MIT) writing-skills testing reference, and general practice.
