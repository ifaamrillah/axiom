---
skill: requirements-analysis
---

# Eval cases: requirements-analysis

## Should trigger

- "Write a spec for a loyalty discount for repeat customers"
- "Turn this idea into testable requirements: customers get 5% off after 3 orders"
- "Write the acceptance criteria for a coupon feature: 10% off orders over $50, one use per customer"

## Should not trigger

- "Break the approved coupon spec into tasks" → `task-planning`
- "Fix the failing pricing test" → `debugging`

## Behavior

### B1: Testable criteria, unknowns marked

- Prompt: "Spec a loyalty discount: customers get 5% off after 3 orders."
- Expect: Writes acceptance criteria in a testable form (Given/When/Then or equivalent)
- Expect: Marks open questions (for example, refunded orders, time window, stacking) as needing clarification instead of inventing answers
- Fail if: Writes production code
