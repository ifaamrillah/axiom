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
1. **Scope and assets (Required; no dependencies):** map authorized boundaries, assets, identities, trust boundaries, entry points, and sensitive data flows. Start the [coverage ledger](../../templates/security/coverage-ledger.md) with review units tied to source paths or interfaces. Output scope, asset map, and initial ledger.
2. **Threat/control review (Required; depends on scope):** inspect relevant source, configuration, dependencies, and controls; use tools only when authorized. Record the checks and evidence against ledger units. Output candidate risks tied to evidence and an updated ledger.
3. **Coverage review (Required; depends on threat/control review):** review the ledger for omitted entry points, trust boundaries, sensitive flows, and checks. A second reviewer may do this when native delegation is available and useful; otherwise perform a separate focused pass. Mark each unit Checked, Not applicable with rationale, or Blocked with evidence. Output a reviewed ledger; exit only when every identified unit has a disposition and high-risk gaps are resolved or clearly blocked.
4. **Verify and rank (Required; depends on coverage review):** validate candidate issues safely and rank by impact/likelihood. **Output:** confirmed findings and labeled hypotheses; exit when each finding has evidence and severity rationale.
5. **Remediate or accept (Conditional; depends on verified findings):** implement approved in-scope fixes and re-check, or report owner decisions needed. Material risk acceptance requires an authorized approver. **Output:** fix evidence or an explicit decision request; exit when disposition is recorded.
6. **Report and handoff (Required; depends on prior stages):** record reviewed areas and ledger, exclusions, findings, severity, evidence, mitigations, residual risk, and next steps with the [security review template](../../templates/security/review.md). **Output:** security report; exit when its scope and residual risk are clear.

## Dependencies and state
A stage exits only when its stated output exists and its stage-specific gate is met. Otherwise record Blocked or Failed with evidence and the next action. A dependent stage may proceed after a skipped stage only when its required inputs are independently satisfied.

Do not test beyond the authorization boundary. Tool/environment gaps are Blocked, not Passed. A skipped test must be inapplicable with rationale. Use the [workflow state template](../../templates/workflows/workflow-state.md).

## Parallelization

Independent read-only review may be delegated with non-overlapping paths and clear authorization. One audit owner validates findings.

## Quality gates

- Scope and authorization are explicit; every identified review unit is checked, justified as not applicable, or marked blocked; confirmed findings have reproducible evidence and remediation guidance.
- Hypotheses and untested areas are labeled; no secrets or unauthorized exploit actions are included.
- Blocking findings are fixed or explicitly dispositioned.

## Recovery and completion
Preserve evidence and scope decisions. If authorization or environment changes, re-evaluate affected stages. Complete with residual risk documented, or mark Blocked and identify required authorization/input.
