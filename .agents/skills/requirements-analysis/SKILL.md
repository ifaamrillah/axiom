---
name: requirements-analysis
description: Turn a product request or engineering problem into clear, testable functional and non-functional requirements, user stories, constraints, edge cases, and acceptance criteria. Use before architecture or implementation when scope is ambiguous, cross-cutting, or user-visible.
---

# Requirements Analysis

## Procedure

1. Restate the desired outcome and target users or system actors.
2. Separate explicit requirements, inferred assumptions, constraints, and open questions.
3. Define functional behavior, inputs, outputs, permissions, errors, and state transitions.
4. Identify non-functional needs: security, privacy, reliability, performance, accessibility, compatibility, operability, and maintainability as relevant.
5. Enumerate boundaries, failure paths, edge cases, abuse cases, and backward-compatibility expectations.
6. Prioritize requirements and distinguish must-have from optional.
7. Write testable acceptance criteria using observable outcomes.
8. Resolve only blocking ambiguities with the user; record non-blocking assumptions.
9. Cross-check requirements against existing product behavior and architecture.

## Outputs

A concise specification containing context, goals, non-goals, requirements, constraints, assumptions, edge cases, acceptance criteria, and unresolved decisions.

## Verification

Each must-have requirement is testable and traceable to an acceptance criterion. Avoid implementation prescriptions unless they are constraints.
