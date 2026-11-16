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
4. **Drive the journey with stable locators:** roles, labels, and test IDs. Avoid CSS paths tied to layout. Wait on conditions, never fixed sleeps.
5. **Capture evidence:** a snapshot or assertion per checkpoint, screenshots of the final state (and the before state for UI fixes), a trace or video for failures and new flows.
6. **Turn exploratory runs into tests** when the journey must stay protected. Generate or write a spec in the project's suite, and run it to green.
7. **Clean up** only test-owned data. Report the journeys covered, the results, the evidence paths, and the limitations.

## Evidence for reviewers

For user-visible changes, attach before and after screenshots or a short video to the pull request when the host's Git tooling supports attachments. Skip it for backend-only changes and refactors.

## Fallback

If browser or device automation is unavailable, use lower-level integration checks or a manual checklist and label the reduced coverage explicitly. Never describe a UI as verified without rendered evidence.

## References

See [testing](../testing/SKILL.md), [UI rules](../ui-ux-design/references/ui-rules.md), and browser automation (`integrations/playwright/README.md` in the Axiom repository).
