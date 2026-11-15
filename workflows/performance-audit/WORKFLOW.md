# Performance Audit Workflow

## Metadata
- **ID:** performance-audit
- **Version:** 1.0.0
- **Status:** Experimental
- **Purpose:** Measure a defined performance concern, identify evidence-backed bottlenecks, and assess safe improvements.

## Triggers and non-triggers
Use when requested or when a user reports performance impact or defines a performance target. Routine changes without performance concerns use normal verification. Use Security Audit for security posture.

## Inputs and preconditions
Define user-visible metric, workload, baseline, environment, acceptable variance, and constraints. Inspect project instructions and telemetry. Do not run production load, incur material cost, or collect sensitive data without explicit authorization.

## Adaptive stages
1. **Scope (Required; no dependencies):** agree target, workload, environment, and safety boundaries. Output an audit brief; exit when measurements can be interpreted.
2. **Baseline (Required when safe measurement exists; depends on scope):** inspect telemetry and run a representative repeatable baseline. **Output:** measurement method and baseline, or a blocked record; exit when the metric is reproducible or the limitation is explicit.
3. **Analyze (Required; depends on baseline or documented limitation):** trace bottlenecks and distinguish observation from hypothesis. Output ranked findings with evidence and confidence.
4. **Recommend or change (Conditional; depends on analysis):** implement only when optimization is in scope and acceptance is clear; otherwise provide recommendations. **Output:** scoped change or ranked recommendations with trade-offs; exit when each recommendation traces to evidence.
5. **Re-measure and report (Required; depends on analysis and on changes if made):** compare using the same workload where possible; explain variance and limitations; update relevant docs and state. **Output:** comparison and audit report; exit when claims match the evidence.

## Dependencies and state
A stage exits only when its stated output exists and its stage-specific gate is met. Otherwise record Blocked or Failed with evidence and the next action. A dependent stage may proceed after a skipped stage only when its required inputs are independently satisfied.

Do not claim measured improvement without comparable before/after evidence. A skipped measurement must be inapplicable; unsafe or unavailable measurement is Blocked. Use the [workflow state template](../../templates/workflows/workflow-state.md) for multi-stage work.

## Parallelization

Independent read-only subsystem analysis may be delegated with disjoint scopes. Baseline design, interpretation, and conclusions have one owner.

## Quality gates

- State the measurement scope and environment.
- Support bottleneck claims with measurements or label them hypotheses.
- Keep measurement safe and reproducible; state trade-offs.

## Recovery and completion
If a measurement is noisy or invalidated, preserve it and re-establish a baseline before comparison. Complete with evidence-backed findings and limitations, or mark Blocked with a safe next step.
