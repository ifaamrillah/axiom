---
name: debugging
description: >
  Find the root cause of a defect with evidence before changing code, then verify a
  minimal fix with a regression check. Use when something returns or does X but
  should do Y, when asked to "fix" a bug or error, and for failing or flaky tests,
  build failures, regressions, performance anomalies, and any unexpected
  behavior, before editing code.
---

# Debugging

## Purpose

Fix causes, not symptoms. A fix without a confirmed root cause is a guess, and guesses compound.

## The rule

```
NO FIX WITHOUT A ROOT-CAUSE HYPOTHESIS CONFIRMED BY EVIDENCE
```

## Pick the technique from the symptom

Classify the symptom first: crash, wrong value, regression, intermittent, performance, memory, hang, environment-only, or production-only. Open [symptom techniques](references/symptom-techniques.md) for the first technique and the trap to avoid for each.

## Phase 1: Investigate (no edits to production code)

1. **Read the failure completely.** Read the full error, stack trace, and log lines. Note the exact message, file, and line. For how to read traces per language and find the first repository frame, see [reading stack traces](references/reading-stack-traces.md).
2. **Reproduce reliably.** Find the smallest command or steps that show the failure. Record the frequency if it is intermittent.
3. **Check what changed.** Look at recent commits, dependency or lockfile updates, config, environment, and data. Use `git log`, `git diff`, and `git bisect` when a known-good revision exists. For scripted `git bisect run`, input minimization, and lockfile bisection, see [bisection](references/bisection.md).
4. **Trace backward from the symptom.** Follow the bad value to where it first went wrong, and fix it there. See [root-cause tracing](references/root-cause-tracing.md).
5. **Instrument boundaries** in multi-component systems. Log inputs and outputs at each layer once, then find the first layer that is wrong. Per-language recipes (Python, JS/TS, Go, Java, PHP): [instrumentation](references/instrumentation.md).

## Phase 2: Compare with a working pattern

Find similar code that works: the same API used elsewhere, an earlier revision, or the reference documentation. List every difference, however small. Do not assume a difference is irrelevant.

## Phase 3: Hypothesize and test

1. Write one falsifiable hypothesis: "X happens because Y; if true, check Z shows W."
2. Run the smallest discriminating check. Change one variable at a time.
3. If the hypothesis is refuted, record it and form a new one. Do not stack fixes on top of each other.

## Phase 4: Fix and verify

1. Write a failing regression test or reproduction script that captures the symptom (see [tdd](../tdd/SKILL.md)).
2. Fix the root cause at the layer where the bad state originates. Add validation at other layers only when it is justified. See [defense in depth](references/defense-in-depth.md) for when and how.
3. Run the regression check, then nearby and broader checks proportionate to risk.
4. Report the cause, the fix, the evidence, and remaining uncertainty. Evidence means the exact command you ran and its decisive output line, before and after the fix, for example: `python3 -m unittest` → `FAILED (failures=1)` before, `OK` after. "All tests pass" without the command is not evidence.

## Stop rule: three failed fixes

If three attempted fixes have failed, stop fixing. Repeated failure usually means the model of the system is wrong: wrong layer, wrong component, or an architectural problem. Return to Phase 1 with what was learned, and escalate to the user if the next step would change architecture or scope.

Count a fix as failed when its check still fails or the failure moves somewhere else. Before escalating, write down:

- the reproduction command and its decisive output line;
- each attempt: the change, the hypothesis behind it, and the observed result;
- the facts now established, and the assumption most likely to be wrong;
- two options (a narrow next experiment and a structural change) with cost and risk;
- the decision you need from the user.

Revert the failed attempts so only the reproduction and evidence remain. A fill-in template and two end-to-end examples are in [worked examples](references/worked-examples.md).

## Special cases

- **Flaky or timing-dependent failures:** replace sleeps with condition-based waits. See [condition-based waiting](references/condition-based-waiting.md).
- **A test passes alone but fails in the suite:** find the polluting test by bisection. See [test-pollution bisection](references/test-pollution-bisection.md).
- **Not reproducible:** report the attempted path, the evidence collected, and the specific data needed (logs, versions, inputs). Do not ship a speculative fix as a confirmed one.

## Red flags

| Thought | Answer |
|---|---|
| "Quick fix now, investigate later" | Later rarely happens, and a masked symptom is harder to find. |
| "Let me try changing this and see" | That is guessing. State a hypothesis first. |
| "It's probably X" | Then design the check that would prove X. |
| "One more attempt" after three failures | Stop. Question the architecture and the assumptions. |
| "Add a retry or try/except so it stops failing" | This hides the defect. Find why it fails. |

## Safety

Do not expose secrets in logs or reports. Do not modify production data or systems to reproduce a failure. Remove temporary instrumentation before completion.

## Outputs

Root cause (with evidence), fix, regression check, verification results, and limitations. For multi-stage work, record failed hypotheses in the workflow state so they are not retried.

## References

Open a reference when its trigger applies; do not preload all of them.

- [Symptom techniques](references/symptom-techniques.md): at the start, to choose a technique for the symptom.
- [Reading stack traces](references/reading-stack-traces.md): when there is an exception or panic.
- [Root-cause tracing](references/root-cause-tracing.md): when the bad value surfaces far from its origin.
- [Instrumentation](references/instrumentation.md): when reading the code does not localize the fault.
- [Bisection](references/bisection.md): when a known-good commit, input, or dependency set exists.
- [Condition-based waiting](references/condition-based-waiting.md): for flaky or timing-dependent tests.
- [Test-pollution bisection](references/test-pollution-bisection.md): when a test passes alone but fails in the suite.
- [Defense in depth](references/defense-in-depth.md): after the root-cause fix, when other paths can reach the bad state.
- [Worked examples](references/worked-examples.md): for end-to-end examples and the escalation template.
- [Codebase exploration](../codebase-exploration/SKILL.md), [testing](../testing/SKILL.md), bug-fix workflow (`workflows/bug-fix/WORKFLOW.md` in the Axiom repository)
