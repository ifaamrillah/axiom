# Workflow Contract

## Purpose

Define how Axiom Markdown workflows describe repeatable engineering processes.

## Required sections

- Metadata: ID, version, status, purpose, scope.
- Triggers and non-triggers.
- Inputs and preconditions.
- Adaptive execution strategy.
- Stages in an understandable order.
- For each stage: purpose, skill/procedure, required or conditional status, condition where conditional, dependencies, outputs, and exit criteria.
- Parallelization constraints.
- Quality gates.
- Recovery and resumption behavior.
- Completion criteria and final report expectations.

## Rules

- Workflow definitions are Markdown, not YAML or executable code.
- Every referenced skill must exist or be explicitly external/optional.
- Conditions must be stated in plain, testable language.
- Define what happens when a dependency is skipped; a dependent stage may proceed only when its required inputs are otherwise satisfied.
- Release/deployment is conditional on scope and authorization.
- Skipped stages are recorded as Skipped and are never represented as Passed.
- Blocking quality-gate failures prevent workflow completion.
- Preserve valid completed work during recovery.

## Status

Workflow lifecycle status: Experimental, Stable, Deprecated. Runtime stage status is defined by the workflow state contract.
