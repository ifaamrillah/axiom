---
name: security-audit
description: Assess application and infrastructure changes for security risks, validate suspected vulnerabilities, and produce evidence-based findings with severity and remediation guidance. Use for security-sensitive changes, threat reviews, and risk-based verification.
---

# Security Audit

## Procedure

1. Confirm authorized scope, assets, data sensitivity, and excluded systems.
2. Understand architecture, trust boundaries, entry points, identities, and data flows. Start a [security coverage ledger](../../../templates/security/coverage-ledger.md) with concrete review units and source/boundary references.
3. Identify threats and abuse cases relevant to the change; record checks and evidence against ledger units.
4. Review authentication, authorization, input handling, output encoding, secrets, dependencies, storage, logging, and infrastructure as applicable.
5. Use available static analysis, dependency, secret, and configuration scanners when appropriate.
6. Perform a separate coverage pass for omitted entry points, trust boundaries, sensitive data flows, and controls. Give each identified unit a Checked, Not applicable with rationale, or Blocked status.
7. Validate each suspected finding with safe evidence; distinguish exploitable issues from theoretical concerns.
8. Rate severity using impact and exploitability, explain assumptions, and give actionable remediation.
9. Re-test fixes and report the ledger, residual risk, and coverage limitations.

## Safety

Do not test systems outside authorization. Do not expose secrets in reports. Never perform destructive validation without explicit approval. A scanner's output is not automatically a confirmed vulnerability.

## Gate

Every identified review unit has evidence or a reasoned disposition. A completed ledger describes reviewed scope; it does not prove that no vulnerabilities exist.
