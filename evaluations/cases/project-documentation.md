---
skill: project-documentation
fixture: evaluations/fixtures/discount-bug
---

# Eval cases: project-documentation

## Should trigger

- "Update the README to document apply_discount's behavior"
- "Our docs are stale; refresh the project documentation from the code"

## Should not trigger

- "Fix the discount bug" → `debugging`
- "Write a spec for loyalty discounts" → `requirements-analysis`

## Behavior

### B1: Documents the code, not the intent

- Prompt: "Update the README to document how apply_discount behaves."
- Fixture: `evaluations/fixtures/discount-bug`
- Expect: Reads pricing.py before writing
- Expect: Flags that the implementation (divides by 10) disagrees with the documented intent instead of documenting the intent as current behavior
- Fail if: States that a 10% discount on 1000 returns 900 as current behavior without noting the bug
