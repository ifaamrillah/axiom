---
name: debugging
description: >
  Diagnose a reproducible software defect using evidence, isolate its cause,
  and verify a minimal repair. Use for bugs, regressions, and unexpected behavior.
---

# Debugging

## Procedure

1. Capture expected vs actual behavior, environment, reproduction, and impact.
2. Inspect recent changes, logs, related code, and existing tests.
3. Form a falsifiable hypothesis and choose a safe discriminating check.
4. Reproduce or narrow the failure; update the hypothesis from evidence.
5. Fix the root cause with a scoped change and add regression coverage when requested or appropriate.
6. Verify the fix and nearby behavior; report remaining uncertainty.

## Safety and outputs

Do not expose secrets in logs or modify production data to reproduce. Output cause, fix, evidence, and limitations. If not reproducible, report the attempted path and needed evidence.

## References

See [codebase exploration](../codebase-exploration/SKILL.md), [testing](../testing/SKILL.md), and [bug-fix workflow](../../../workflows/bug-fix/WORKFLOW.md).
