---
skill: ci-and-observability
fixture: evaluations/fixtures/discount-bug
---

# Eval cases: ci-and-observability

## Should trigger

- "Add a GitHub Actions workflow that runs the tests on every PR"
- "Our CI takes 20 minutes, can you make the pipeline faster?"
- "Add structured logging and a latency metric to the checkout endpoint"

## Should not trigger

- "CI is red on the pricing tests since the last merge, fix pls" → `debugging`
- "Cut release 1.2.0" → `release-management`
- "apply_discount is slow, speed it up" → `performance-optimization`

## Behavior

### B1: Pipeline from the project's real commands

- Prompt: "Add a GitHub Actions CI workflow for this project that runs the tests on pull requests."
- Fixture: `evaluations/fixtures/discount-bug`
- Expect: Takes the test command from the project (`python3 -m unittest discover -s tests -t .`) instead of inventing one
- Expect: Sets read-only `permissions` and a job timeout
- Expect: Does not use `continue-on-error`, `|| true`, or skipped tests
- Expect: States whether the workflow was validated (linter, local runner, or a real run) or reports it as unverified
- Fail if: Claims the pipeline works without any run or validation
