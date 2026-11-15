---
name: implementation
description: Implement an approved software change in an existing codebase while following repository conventions, keeping diffs scoped, and verifying behavior with relevant tests and checks. Use after requirements and planning are sufficient for the change's complexity.
---

# Implementation

## Procedure

1. Read repository instructions and inspect relevant code, tests, and patterns.
2. Confirm task scope, acceptance criteria, and owned files.
3. Identify the smallest coherent implementation.
4. Write or update tests appropriate to the behavior; prefer test-first where useful.
5. Implement incrementally, preserving existing conventions and compatibility.
6. Run focused tests, lint, type checks, and build checks as appropriate.
7. Review the diff for unrelated changes, regressions, secrets, and missed edge cases.
8. Update relevant documentation and handoff/state.
9. Report exact checks run and any checks not run.

## Rules

Do not broaden scope without coordination. Do not claim tests passed without executing them. Avoid needless abstraction, dependency changes, and unrelated formatting.
