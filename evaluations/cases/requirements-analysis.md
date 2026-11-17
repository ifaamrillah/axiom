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

### B2: Change proposal opts out of specs instead of inventing requirements

- Prompt: "Write a change proposal for renaming the internal module pricing_utils to pricing. Nothing changes for users."
- Expect: The proposal states `Specs: none — <reason>` (or equivalent wording with a reason) instead of a Deltas section with requirements
- Fail if: Invents an ADDED or MODIFIED requirement to fill the delta format

### B3: Decided term goes into the glossary

- Prompt: "Spec loyalty points for repeat customers. We've decided to call the points 'Stars' everywhere, not 'points' or 'credits'."
- Expect: Adds or proposes a glossary entry for "Stars" (in the project's glossary, or `.axiom/project/glossary.md` when none exists) with its meaning and source
- Expect: The spec uses "Stars" consistently
- Fail if: The spec mixes "points", "credits", and "Stars" for the same concept
