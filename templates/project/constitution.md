---
version: 1.0.0
ratified: <YYYY-MM-DD>
last_amended: <YYYY-MM-DD>
---

# <Project> Constitution

Non-negotiable principles that every plan is checked against. Keep it short; each principle should change decisions. Delete the examples that do not apply.

## Principles

### I. <Name> (MUST)

<Rule stated as a testable obligation.>
*Rationale:* <why>.
*Example:* "Every feature ships behind a feature flag until it has run in staging for one release."

### II. Test-first for behavior changes (MUST)

New behavior is driven by a test seen failing first. No test is skipped or weakened to reach green.

### III. Simplicity (SHOULD)

Prefer the standard library and existing dependencies. A new dependency or service needs a recorded justification.

### IV. <Security / data / accessibility principle> (MUST)

<Rule.>

## Plan gate

Every plan includes a **Constitution check** section. It lists each MUST principle as pass, fail, or not applicable. A failed MUST blocks implementation unless the plan's **Complexity tracking** table justifies it and the owner approves:

| Violation | Why needed | Simpler alternative rejected because |
|---|---|---|
| | | |

## Amendments

Changes require the owner's approval. Bump the version: MAJOR when a principle is removed or redefined, MINOR when one is added, PATCH for wording. Record the change below.

- <YYYY-MM-DD> v1.0.0: ratified.
