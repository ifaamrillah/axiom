---
name: tdd
description: >
  Use a test-first red-green-refactor loop for behavior changes when the project
  supports it or the user requests it. Use for well-specified logic and regression fixes.
---

# Test-Driven Development

## Procedure

1. Confirm expected behavior and test conventions.
2. Add the smallest test that demonstrates the missing behavior.
3. Run it and confirm it fails for the intended reason.
4. Implement the smallest change to pass.
5. Run focused tests, then relevant broader checks if proportionate.
6. Refactor while keeping tests green and inspect the resulting diff.

## Gates and fallback

Do not claim a red/green step without running the test. If project setup prevents the loop, document the obstacle and use the project's accepted verification path. Do not introduce a test framework without justification.

## References

See [testing skill](../testing/SKILL.md) and [quality gate contract](../../../core/contracts/QUALITY-GATE-CONTRACT.md).
