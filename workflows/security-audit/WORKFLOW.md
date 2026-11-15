# Security Audit Workflow

## Metadata
- **ID:** security-audit
- **Version:** 1.0.0
- **Status:** Experimental
- **Purpose:** Assess a defined system boundary for security risks and produce verified, actionable findings.

## Triggers and non-triggers
Use when requested, when changes affect authentication, authorization, sensitive data, payments, external input, dependencies, infrastructure, secrets, or when onboarding reveals material risk. Secure coding checks remain part of implementation. This is not authorization to test outside the stated scope.

## Inputs and preconditions
Confirm authorized repository/system, environment, review depth, test permissions, sensitive-data rules, and exclusions. Inspect relevant architecture. Never include credentials in notes or reports.

## Adaptive stages
1. **Scope and assets (Required; no dependencies):** map authorized boundaries, assets, identities, trust boundaries, and data flows. Output scope and asset map.
2. **Threat/control review (Required; depends on scope):** inspect relevant source, configuration, dependencies, and controls; use tools only when authorized. Output candidate risks tied to evidence.
3. **Verify and rank (Required; depends on review):** validate issues safely and rank by impact/likelihood. **Output:** confirmed findings and labeled hypotheses; exit when each finding has evidence and severity rationale.
4. **Remediate or accept (Conditional; depends on verified findings):** implement approved in-scope fixes and re-check, or report owner decisions needed. Material risk acceptance requires an authorized approver. **Output:** fix evidence or an explicit decision request; exit when disposition is recorded.
5. **Report and handoff (Required; depends on prior stages):** record reviewed areas, exclusions, findings, severity, evidence, mitigations, residual risk, and next steps with the [security review template](../../templates/security/review.md). **Output:** security report; exit when its scope and residual risk are clear.

## Dependencies and state
A stage exits only when its stated output exists and its stage-specific gate is met. Otherwise record Blocked or Failed with evidence and the next action. A dependent stage may proceed after a skipped stage only when its required inputs are independently satisfied.

Do not test beyond the authorization boundary. Tool/environment gaps are Blocked, not Passed. A skipped test must be inapplicable with rationale. Use the [workflow state template](../../templates/workflows/workflow-state.md).

## Parallelization

Independent read-only review may be delegated with non-overlapping paths and clear authorization. One audit owner validates findings.

## Quality gates

- Scope and authorization are explicit; confirmed findings have reproducible evidence and remediation guidance.
- Hypotheses and untested areas are labeled; no secrets or unauthorized exploit actions are included.
- Blocking findings are fixed or explicitly dispositioned.

## Recovery and completion
Preserve evidence and scope decisions. If authorization or environment changes, re-evaluate affected stages. Complete with residual risk documented, or mark Blocked and identify required authorization/input.
