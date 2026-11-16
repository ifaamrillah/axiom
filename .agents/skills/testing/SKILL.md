---
name: testing
description: Plan and execute appropriate unit, integration, API, and regression tests for software changes, analyze failures, and report verifiable evidence. Use during implementation and before completing engineering work.
---

# Testing

## Purpose

Give each changed behavior a test at the lowest layer that can catch its likely bugs, run the right tests at the right time, and report results someone else can reproduce.

## Procedure

1. **Inspect conventions.** Find the test framework, the project's test scripts, fixtures and factories, the CI job that runs tests, and the nearest existing tests for the code you change. Use the project's own commands. See [ecosystem commands](references/ecosystem-commands.md) to detect the runner and get exact commands.
2. **Map behavior to cases.** For each acceptance criterion and each changed behavior, list the cases: happy path, boundaries, invalid input, permission and tenant checks, failure of each dependency, and idempotency or retries where relevant.
3. **Choose layers.** Push each case to the lowest layer that can catch it: unit, component, integration, API, contract, or end-to-end. Use the decision rules in [layer selection](references/layer-selection.md). Use real dependencies (a test database, a temp directory) where the bug would live in the dependency interaction.
4. **Build data and isolation.** Use builders with valid defaults and explicit overrides. Give each test its own state: transaction rollback, temp dirs, fake clocks, seeded randomness, stubbed network. See [fixtures and flakiness](references/fixtures-and-flakiness.md).
5. **Write the tests.** Use test-first when practical (see the tdd skill). Assert observable outcomes with hand-derived literal expectations. On denied or failed requests, also assert that no side effect happened.
6. **Run focused, then broad.** Run the single test, then its file or package, then the suites the change can affect. Run the full suite, including slower tiers, at the quality gate.
7. **Diagnose failures.** Read the failure before rerunning. Classify each failure as a product defect, a test defect, or an environment problem, with evidence. For intermittent failures, measure the failure rate and follow the flaky-test procedure. Do not add retries, sleeps, or longer timeouts as a fix.
8. **Check strength.** Look at diff coverage with branches on, and ask whether a realistic mutation of each changed line would fail a test. Coverage shows gaps; it does not prove quality.
9. **Report.** Record commands, environment, counts, skipped tiers and why, and remaining risks.

## Rules

- Never weaken an assertion, skip, or delete a test only to get a pass. If a test is wrong, say why and fix it in the same change.
- A skipped stage is not a passed stage. Name every tier you did not run.
- Never call real third-party services or production data from automated tests. Use stubs, recorded fixtures, sandboxes, or test containers.
- Every bug fix ships with a regression test that failed before the fix.
- No `.only`, focused tests, or unexplained `skip` in a finished change.

## Layer quick guide

| Change | Primary layer | Add |
|---|---|---|
| Pure logic, parsing, calculation | Unit | Boundary table |
| New or changed query, migration, transaction | Integration with real DB | Rollback and constraint cases |
| New or changed endpoint | API test | 401, 403, 404, 422 cases and no-side-effect checks |
| Shape shared with another service | Contract or schema test | Breaking-change check in CI |
| UI component logic | Component test | Accessibility queries (role, label) |
| Critical user journey or UI fix | End-to-end (see the e2e-testing skill) | Screenshot or trace evidence |
| Bug fix | Lowest layer that reproduces it | Regression test named for the behavior |

## Red flags

| You notice | Do instead |
|---|---|
| Most new tests are E2E | Move rules down to unit or API tests; keep one journey |
| A mocked DB asserts SQL text | Use an integration test against a real test DB |
| "Coverage went up" is the only evidence | Show the assertions and the cases they cover |
| A failing test passed on rerun, so it is fine | Measure the flake rate and find the cause |
| Test data depends on IDs or today's date | Use builders, unique values, and a fixed clock |
| Snapshot files changed in bulk | Review each diff, or replace with targeted assertions |

## Outputs

- Test plan: behaviors, cases, and the chosen layer for each.
- Changed tests and fixtures.
- Execution report: exact commands, environment, pass/fail/skip counts, duration.
- Uncovered risks and skipped tiers, with reasons.

## References

- [Layer selection, coverage, and contracts](references/layer-selection.md): pyramid budget, layer decision table, what to test per layer, coverage metrics and their limits, mutation testing, API and contract test examples. Open when choosing layers or judging coverage.
- [Fixtures and flakiness](references/fixtures-and-flakiness.md): data builders in several languages, isolation strategies, flaky-test classification and repeat commands, quarantine policy, regression-suite hygiene. Open when building test data or when a test fails intermittently.
- [Ecosystem commands](references/ecosystem-commands.md): stack detection and exact commands for pytest, Vitest, Jest, Go, JUnit, PHPUnit and Pest, RSpec, and others, plus a run report template. Open when you need to run or filter tests.
- [TDD](../tdd/SKILL.md) for the test-first loop and the [testing anti-patterns catalog](../tdd/references/testing-anti-patterns.md).
- [End-to-end testing](../e2e-testing/SKILL.md) for browser journeys.
- [Test-pollution bisection](../debugging/references/test-pollution-bisection.md) and [condition-based waiting](../debugging/references/condition-based-waiting.md) for order-dependent and timing failures.
