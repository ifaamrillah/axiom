# Axiom Principles

These principles are normative guidance for all Axiom skills, workflows, adapters, and contributions.

## 1. Workflow-driven, not prompt-driven

Use documented workflows to coordinate substantial engineering work. A workflow is a guide for the host agent, not an executable program or custom runtime.

## 2. Context before action

Inspect repository instructions, project state, relevant source files, tests, and existing documentation before acting. Reuse verified knowledge; do not assume it is current.

## 3. Specification proportional to complexity

Clarify outcomes and acceptance criteria before implementation when the change is ambiguous, cross-cutting, risky, or user-visible. Trivial changes may use a lightweight plan.

## 4. Visual before code when appropriate

For meaningful user-interface changes, understand the design system and user journeys, then establish flows or mockups before implementation. This stage is not required for non-visual work.

## 5. Evidence over assumptions

Claims of success require observable evidence: commands, test results, review findings, reproducible observations, or explicit user confirmation. Report unavailable checks honestly.

## 6. Living knowledge

Update project knowledge when a change materially affects architecture, behavior, dependencies, conventions, operations, or risk. Prefer targeted updates over rewriting all documentation.

## 7. Parallel when safe

Use native delegation when supported and useful. Parallelize only independent tasks with explicit ownership and compatible dependencies. Otherwise work sequentially.

## 8. Progressive complexity

Choose the smallest sufficient process. Do not apply the full lifecycle to a typo or isolated low-risk fix.

## 9. Portable by design

Canonical skills and workflows remain platform-neutral. Platform-specific discovery, configuration, and delegation behavior belongs in adapters.

## 10. Human control at critical boundaries

Require explicit authorization for production deployment, destructive migrations or data operations, credential rotation, and other irreversible or high-impact actions.

## 11. Security throughout the lifecycle

Consider security during discovery, design, implementation, verification, and delivery—not only in a final audit.

## 12. Honest state

A skipped stage is not passed. A failed check cannot be silently waived. A waiver requires a reason, scope, and authorized approver.
