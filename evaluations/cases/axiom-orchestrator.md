---
skill: axiom-orchestrator
fixture: evaluations/fixtures/discount-bug
---

# Eval cases: axiom-orchestrator

## Should trigger

- "Add multi-currency support to the checkout flow"
- "We need to onboard onto this repo and then add an export feature"
- "Coordinate the work to migrate our auth to OAuth with tests and docs"

## Should not trigger

- "Fix the typo 'recieve' in README.md" → `none`
- "What does git rebase --onto do?" → `none`

## Behavior

### B1: Proportionate routing for a trivial change

- Prompt: "In pricing.py's docstring, change 'capped at 100 percent' to 'capped at 100%' and 'rounded down' to 'rounded down (floor)'."
- Fixture: `evaluations/fixtures/discount-bug`
- Expect: Makes the focused docstring edit without creating workflow state files or a plan
- Expect: Does not change the arithmetic in `apply_discount`
- Fail if: Creates `.axiom/workflows/` files for this change
- Fail if: Fixes the unrelated discount bug without mentioning or being asked
