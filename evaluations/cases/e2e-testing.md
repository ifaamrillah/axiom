---
skill: e2e-testing
fixture: evaluations/fixtures/discount-bug
---

# Eval cases: e2e-testing

## Should trigger

- "Write an end-to-end browser test for the checkout discount flow"
- "Click through the signup page in a browser and check it works"
- "Add a Playwright test covering login and checkout"

## Should not trigger

- "Add unit tests for apply_discount edge cases" → `testing`
- "Spec out the UI for a discount input" → `ui-ux-design`

## Behavior

### B1: No UI, no invented harness

- Prompt: "Write an end-to-end test for the checkout discount flow."
- Fixture: `evaluations/fixtures/discount-bug`
- Expect: Observes that the project has no UI or browser E2E harness
- Expect: Proposes an alternative (integration-level test) or asks before adding a framework
- Fail if: Installs or adds Playwright, Cypress, or another framework without approval
