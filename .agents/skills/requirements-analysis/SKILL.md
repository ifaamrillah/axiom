---
name: requirements-analysis
description: Turn a product request or engineering problem into a testable specification with prioritized user stories, numbered requirements, Given/When/Then acceptance scenarios, explicit clarification markers, and a requirements-quality checklist. Use before architecture or implementation when scope is ambiguous, cross-cutting, or user-visible, or to clarify an existing draft spec.
---

# Requirements Analysis

## Purpose

Make intended behavior explicit and testable before design and code. A spec is code written in English; it deserves its own tests.

## Inputs

The request, discovery output (if any), existing product behavior, architecture, the project constitution and constraints, and prior clarifications.

## Procedure

1. **Restate** the desired outcome, the actors, and the success criteria in measurable, technology-agnostic terms.
2. **Draft** the spec from [the template](assets/spec.md): prioritized user stories (P1 is a viable increment on its own), numbered `FR-`/`NFR-` requirements using MUST/SHOULD, key entities, edge cases, security and privacy, and assumptions.
3. **Mark unknowns inline** as `[NEEDS CLARIFICATION: <specific question>]`. Do not guess silently. Make a reasonable default an explicit assumption only when it is reversible and low-risk.
4. **Run a clarification scan** using the [clarification taxonomy](references/clarification-taxonomy.md). Rate each category Clear, Partial, or Missing.
5. **Ask the highest-impact questions,** at most 5 per round and one at a time when interactive. Each question offers a recommended answer and short options. Record answers in the spec's **Clarifications** section and update the affected requirements immediately.
6. **Write acceptance scenarios** as Given/When/Then for each story. Every must-have requirement maps to at least one scenario.
7. **Test the requirements** with the [requirements-quality checklist](references/requirements-checklist.md). These checks test the writing, not the implementation.
8. **Cross-check** against the constitution, constraints, existing behavior, and architecture. Surface conflicts. Do not reconcile them silently.
9. **Set status:** `draft` while markers remain on must-haves, `clarified` when none remain, and `approved` only after the user or owner accepts it.

## Outputs

`spec.md` (or the lighter [requirements checklist](assets/requirements.md) for small changes) containing goals, non-goals, stories, requirements, scenarios, edge cases, assumptions, clarifications, and open questions.

## Gate

- No `[NEEDS CLARIFICATION]` remains on a must-have requirement before planning starts.
- Every must-have requirement is testable and traced to a scenario.
- Implementation details appear only when they are real constraints.
- If the user explicitly skips clarification (for example for a spike), proceed, but record that downstream rework risk is higher.

## References

- [Clarification taxonomy](references/clarification-taxonomy.md)
- [Requirements-quality checklist](references/requirements-checklist.md)
- [Product discovery](../product-discovery/SKILL.md), [spec analysis](../spec-analysis/SKILL.md)
