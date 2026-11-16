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

1. **Check context first.** Read the relevant code, docs, and decisions so you never ask what the repository already answers.
2. **Separate request from problem.** Restate the request, then the underlying problem, who has it, and what success looks like.
3. **Elicit one question at a time:**
   - Ask the question with the highest impact × uncertainty first.
   - Phrase it so that "yes" accepts your recommended answer ("I'd scope this to logged-in customers only. OK?").
   - Prefer multiple choice with a recommendation over open questions.
   - After each answer, update your understanding and choose the next question. Do not send a questionnaire.
4. **Track clarity** across the dimensions in the next section. Stop asking when the dimensions that matter are Clear, when the user wants to proceed, or after about 7 questions. Record the rest as assumptions.
5. **Propose 2–3 approaches** with trade-offs (value, cost, risk, reversibility). Recommend one and give the reason.
6. **Write a short design summary:** problem, users, outcome and success signal, the chosen approach and the rejected ones, scope and non-goals, assumptions, and open decisions. Size it to the work: a paragraph for small features, a page for large ones.
7. **Get approval.** For feature work, nothing proceeds to specification or implementation until the user approves the summary. Approval covers only what was shown. Agreement with an idea is not approval of a summary you have not written.

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

A design summary using the [discovery brief template](assets/brief.md). Gate: the work traces to a real need, success can be assessed, and the user approved the summary.

## References

- [Requirements analysis](../requirements-analysis/SKILL.md), [clarification taxonomy](../requirements-analysis/references/clarification-taxonomy.md)
