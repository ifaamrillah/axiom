---
name: e2e-testing
description: >
  Verify critical user journeys across application boundaries with browser or
  device automation, capturing reproducible evidence such as snapshots, screenshots,
  traces, and videos. Use when a change affects integrated user-visible behavior,
  a UI fix needs visual proof, or acceptance criteria describe an end-to-end flow.
---

# End-to-End Testing

## Procedure

1. **Select journeys** linked to acceptance criteria and risk. Prefer few, critical, deterministic journeys over broad brittle coverage.
2. **Check the environment:** a local or test environment only, test-owned accounts, seeded data, and cleanup behavior. Never use production data or real user accounts.
3. **Pick the tool** in this order: the project's own E2E suite (for example `@playwright/test`, Cypress), then a token-efficient browser CLI, then a browser MCP server or the host's built-in browser. See the browser automation integration (`integrations/playwright/README.md` in the Axiom repository).
4. **Drive the journey with stable locators:** roles, labels, and test IDs. Avoid CSS paths tied to layout. Wait on conditions with web-first assertions, never fixed sleeps. Create test data through the API or fixtures, not the UI, and reuse saved login state per role. See [Playwright patterns](references/playwright-patterns.md).
   For exploratory checks without a spec, use the snapshot, act, verify loop in [playwright-cli exploration](references/playwright-cli-exploration.md).
5. **Capture evidence:** a snapshot or assertion per checkpoint, screenshots of the final state (and the before state for UI fixes), a trace or video for failures and new flows.
6. **Turn exploratory runs into tests** when the journey must stay protected. Generate or write a spec in the project's suite, and run it to green.
7. **Clean up** only test-owned data. Report the journeys covered, the results, the evidence paths, and the limitations.

## Failures and flakes

Read the trace, screenshot, and console before rerunning. Measure the failure rate with `--repeat-each`, classify the cause, and fix it. Do not fix flakes with sleeps, `force: true`, longer timeouts, or more retries. A test that passed only on retry is flaky, not passing. See [flake triage and evidence](references/flake-triage-and-evidence.md).

## Red flags

| You notice | Do instead |
|---|---|
| `waitForTimeout`, `cy.wait(2000)`, `sleep` | Web-first assertion or wait on a specific response |
| CSS chains or `nth-child` locators | Role, label, or test ID locator |
| Every test logs in through the form | Saved storage state per role; one login spec |
| Test B depends on data test A created | Fixture creates and deletes its own data |
| Ten E2E specs for one form's validation | One journey; validation rules in unit or component tests |
| "Verified" with no screenshot, snapshot, or assertion output | Capture evidence or say it was not verified |

## Evidence for reviewers

For user-visible changes, attach before and after screenshots or a short video to the pull request when the host's Git tooling supports attachments. Skip it for backend-only changes and refactors.

## Fallback

If browser or device automation is unavailable, use lower-level integration checks or a manual checklist and label the reduced coverage explicitly. Never describe a UI as verified without rendered evidence.

## References

- [Playwright patterns](references/playwright-patterns.md): locator priority table (with Cypress equivalents), waiting strategy, auth and session reuse, test data isolation with fixtures, CI configuration, and commands. Open when writing or fixing specs.
- [Flake triage and evidence](references/flake-triage-and-evidence.md): reading traces, flake cause-to-fix table, evidence types and when to capture each, report template. Open when a test fails or flakes, or when you must prove a UI change.
- [playwright-cli exploration](references/playwright-cli-exploration.md): snapshot, act, verify loop, cheap verification commands, sessions and saved state, network stubs, debugging a paused spec, and promoting exploration to a spec. Open for interactive checks.
- [Testing](../testing/SKILL.md) for layer choice, [UI rules](../ui-ux-design/references/ui-rules.md), and browser automation (`integrations/playwright/README.md` in the Axiom repository).
