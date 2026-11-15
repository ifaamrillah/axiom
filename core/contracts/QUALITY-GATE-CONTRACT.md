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
