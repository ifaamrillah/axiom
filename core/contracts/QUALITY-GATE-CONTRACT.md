# Quality Gate Contract

## Outcomes

- **Passed:** required criteria were checked and supported by evidence.
- **Failed:** a required criterion was not met.
- **Blocked:** the check could not be performed or a dependency is unavailable.
- **Waived:** an authorized approver explicitly accepted the stated risk.

## Required record

- Gate ID and scope
- Criteria
- Outcome
- Evidence and commands/environment where applicable
- Findings and limitations
- Timestamp
- Waiver reason, approver, and scope when waived

## Rules

- Never silently convert Failed or Blocked to Passed.
- A skipped stage is not a passed gate.
- A waiver must be explicit and must not imply that the check succeeded.
- Blocking failures prevent workflow completion unless properly waived by an authorized human.
- Verification reports must distinguish tests that ran, tests that did not run, and tests that could not run.
- Evidence must be fresh: produced after the last relevant change. An earlier run does not satisfy a gate.
- A delegated agent's success report is a claim, not evidence. The integrator inspects the diff and reruns checks.

## Baseline-relative gates

When checks already fail before the work starts, record a baseline (failing IDs, error counts, command, commit) before the first edit. The gate then passes when there are **no new failures compared with the baseline**. Pre-existing failures are reported as such. Re-recording the baseline to pass a gate is prohibited. A legitimate baseline change is a recorded decision.

## Quality-bar integrity

A gate fails when the change lowers the project's bar without an approved waiver: skipped, deleted, or weakened tests; new lint or type suppressions; relaxed thresholds; CI steps made non-blocking; or stubs reported as complete. See [quality-constraints](../../.agents/skills/quality-constraints/SKILL.md) and the [definition of done](../standards/definition-of-done.md).
