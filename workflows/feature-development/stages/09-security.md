# Stage 9: Security review

**Skill:** `security-audit` (guidance mode unless a full audit is requested) · **Required:** conditional, risk-based · **Depends on:** stages 4–8 as applicable

## Entry

Run this stage when authentication, authorization, sensitive data, payments, external input, dependencies, infrastructure, secrets, or material attack surface changes, or when the user or a policy requires it. Basic secure-engineering checks always apply.

## Do

1. Identify trust boundaries crossed by the change.
2. Validate each candidate with a concrete boundary and result. Give severity only to confirmed findings.
3. Recommend the smallest effective fix and re-test it.

## Exit

No unresolved blocking finding remains, or an authorized, documented waiver exists.
