---
name: product-discovery
description: >
  Turn a vague idea or underspecified request into a clear problem, outcome,
  and approach through one-question-at-a-time elicitation, alternative approaches
  with trade-offs, and an approved design summary before anything is built. Use
  when a request is vague, when the user asks to be interviewed or to brainstorm,
  or when product impact needs discovery before specification.
---

# Product Discovery

## Purpose

Understand what to build before building it. Ask "what are you assuming?" as well as "what do you want?"

## When to use / avoid

Use it for new capabilities, vague ideas ("some kind of loyalty feature"), and requests where the wrong interpretation would waste significant work.

Avoid it for explicit maintenance changes, or for requests that already state the outcome, the users, and the acceptance criteria. Execute those directly or go to requirements analysis. If the user says "skip the questions", stop the interview, write down the assumptions you are making, and continue.

## Inputs

The request, existing product docs and code, prior decisions, and constraints. Do not contact users or external parties unless explicitly authorized.

## Procedure

1. **Check context first.** Read the relevant code, docs, and decisions so you never ask what the repository already answers. Read the project glossary and out-of-scope records if they exist. If the concept was rejected before, show that record and ask what has changed.
2. **Separate request from problem.** Restate the request, then the underlying problem, who has it, and what success looks like.
3. **Challenge the premise** before elicitation goes deep. Answer from the repository first, then ask the user, one at a time: is this the right problem; what happens if we do nothing; what existing code or product already solves part of it; how will users get it or adopt it. For a clearly scoped small request, write one line saying why the premise holds and move on. Whenever you stop to wait for an answer, list the alternatives so far with S/M/L effort each, state the current verdict (usually `needs-clarification`), and say what answer would change it. Open [premise challenge and verdict](references/premise-and-verdict.md).
4. **Elicit one question at a time:**
   - Ask the question with the highest impact × uncertainty first.
   - Phrase it so that "yes" accepts your recommended answer ("I'd scope this to logged-in customers only. OK?").
   - Prefer multiple choice with a recommendation over open questions.
   - After each answer, update your understanding and choose the next question. Do not send a questionnaire.
   - Pick the technique that fits the gap (5 whys for solution-first requests, jobs to be done for unclear users, pre-mortem for untested ideas, constraint inversion for growing scope). Open [elicitation techniques](references/elicitation-techniques.md) when you are unsure which question to ask next.
   - When a domain term is decided, add or correct it in the project glossary in the same turn. Flag a word that conflicts with an existing entry. See [glossary and out-of-scope records](../requirements-analysis/references/glossary-and-out-of-scope.md).
5. **Track clarity** across the dimensions in the next section. Stop asking when the dimensions that matter are Clear, when the user wants to proceed, or after about 7 questions. Record the rest as assumptions.
6. **Propose 2–3 approaches** with trade-offs (value, cost, risk, reversibility) and rough effort (S/M/L). One of them is the smallest option that could still help (reuse, config, docs, or doing nothing). Recommend one and give the reason. Use the comparison table in the [worked example](references/discovery-example.md#step-3-approach-comparison). A strawman option does not count as an approach.
7. **Assess and give a verdict.** Rate each criterion (problem evidence, user value, feasibility, reuse, risk, adoption) strong, adequate, weak, or unknown, with one line of evidence. Verdict: `go`, `needs-clarification`, or `kill`. `go` is not allowed while a must-have criterion is weak or unknown. `kill` is a valid result: write an out-of-scope record (decision, reason, date, what would change it) and stop. Skip the scorecard only for a clearly scoped small request, and say you skipped it.
8. **Write a short design summary:** problem, users, outcome and success signal, the chosen approach and the rejected ones, scope and non-goals, assumptions, open decisions, and the verdict. Size it to the work: a paragraph for small features, a page for large ones. Write an out-of-scope record for each rejected concept that someone is likely to propose again.
9. **Get approval.** For feature work, nothing proceeds to specification or implementation until the user approves the summary. Approval covers only what was shown. Agreement with an idea is not approval of a summary you have not written.

## Clarity dimensions

| Dimension | Clear when |
|---|---|
| Problem | The pain and who has it are stated, with evidence or an explicit assumption |
| Outcome | A measurable or observable success signal exists |
| Users and context | Primary actors and their situation are named |
| Scope | In scope and out of scope are explicit |
| Constraints | Technical, legal, budget, and time limits are known or assumed |
| Risks | The riskiest assumption and a cheap way to test it are named |

Optional deep mode for high-stakes ideas: rate each dimension from 0 to 1 and continue until every rated dimension reaches the agreed threshold (default 0.8). Report the final scores in the summary.

## Outputs and gate

A design summary using the [discovery brief template](assets/brief.md), with a verdict. Gate: the work traces to a real need, success can be assessed, the verdict is `go`, and the user approved the summary. A `kill` verdict ends discovery with an out-of-scope record; it is a completed outcome, not a passed gate for building.

## References

- [Elicitation techniques](references/elicitation-techniques.md): open when choosing the next question, or when a session stalls.
- [Premise challenge and verdict](references/premise-and-verdict.md): open at step 3, and again for the scorecard and verdict at step 7.
- [Glossary and out-of-scope records](../requirements-analysis/references/glossary-and-out-of-scope.md): open when a term is decided or a concept is rejected.
- [Worked discovery example](references/discovery-example.md): open before your first discovery session, or to check pacing, approach comparison, and brief shape.
- [Requirements analysis](../requirements-analysis/SKILL.md), [clarification taxonomy](../requirements-analysis/references/clarification-taxonomy.md)
