---
skill: technical-research
fixture: evaluations/fixtures/discount-bug
---

# Eval cases: technical-research

## Should trigger

- "What does Python's round() do with 2.5, and should apply_discount use it?"
- "Check the current docs: is datetime.utcnow deprecated, and what replaces it?"

## Should not trigger

- "Where is the discount cap applied?" → `codebase-exploration`
- "Fix the discount bug" → `debugging`

## Behavior

### B1: Version-pinned fact, verified

- Prompt: "What does Python's round() return for 2.5, and should apply_discount use it instead of floor division?"
- Fixture: `evaluations/fixtures/discount-bug`
- Expect: States that round() uses round-half-to-even, so round(2.5) is 2
- Expect: Verifies it with a local command or cites official Python documentation
- Fail if: Claims round(2.5) returns 3
