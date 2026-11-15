# Security Coverage Ledger

Use this Markdown ledger to make audit scope and review coverage inspectable. It is a checklist, not proof that a system is secure. Keep it bounded to the authorized scope and link evidence to source paths, tests, or reproducible observations.

## Audit

- **Repository / system:**
- **Revision / environment:**
- **Authorized scope:**
- **Excluded areas:**
- **Reviewer(s):**
- **Date:**

## Review units

List concrete entry points, trust boundaries, sensitive data flows, privileged operations, and relevant security controls discovered during reconnaissance. Split broad areas into units small enough to disposition independently.

| ID | Surface / flow / control | Source or boundary | Risk question / check | Status | Evidence or rationale |
|---|---|---|---|---|---|
| COV-01 | Example: authenticated write endpoint | `src/...` | Is authorization enforced on the server for each object? | Pending | |

Allowed statuses: **Pending**, **Checked**, **Not applicable**, **Blocked**. `Not applicable` needs a short reason; `Blocked` needs the missing input or safe next step. Do not mark a unit checked based only on a filename or an assumption.

## Coverage review

- **Reviewed for omitted entry points and trust boundaries by:**
- **Additional units found:**
- **Unresolved coverage gaps:**
- **Disposition:** Complete / Blocked (explain)

Completion requires every identified unit to have a final status and evidence or rationale. A complete ledger describes the inspected scope; it does not claim the absence of vulnerabilities.
