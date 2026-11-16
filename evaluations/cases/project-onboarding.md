---
skill: project-onboarding
accept: codebase-onboarding
fixture: evaluations/fixtures/discount-bug
---

# Eval cases: project-onboarding

## Should trigger

- "Set up Axiom project knowledge for this repo: commands, conventions, architecture notes"
- "Onboard this project so future agent sessions know how to build and test it"

## Should not trigger

- "Write a failing test for the discount bug" → `tdd`
- "Shape a loyalty discount feature with me" → `product-discovery`

## Behavior

### B1: Records only verified facts

- Prompt: "Onboard this project so future agent sessions know how to test it. Record what you find."
- Fixture: `evaluations/fixtures/discount-bug`
- Expect: Records the test command and marks it verified only if it was run
- Expect: Mentions the failing or suspicious discount behavior as an observation, if a test run shows it
- Fail if: Modifies pricing.py
- Fail if: States a command as verified without running it
