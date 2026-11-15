---
name: code-review
description: Independently review a proposed code change for correctness, regressions, security, maintainability, performance, compatibility, and missing tests. Use before integrating substantial changes or completing a workflow.
---

# Code Review

## Review procedure

1. Read the task, specification, and acceptance criteria.
2. Inspect the complete diff and relevant surrounding code.
3. Prioritize correctness and user impact; trace changed behavior through callers and data flows.
4. Examine security boundaries, authorization, validation, secrets, error handling, and sensitive data.
5. Check compatibility, migrations, concurrency, performance, observability, and maintainability where relevant.
6. Evaluate tests against acceptance criteria and failure cases.
7. Report actionable findings with severity, file/line, impact, and reproduction or rationale.
8. Separate confirmed findings from questions and suggestions.
9. Re-review fixes and verify that findings are resolved.

## Outputs

Findings-first review report, followed by residual risks and areas not covered. Do not invent findings or approve work that was not inspected.
