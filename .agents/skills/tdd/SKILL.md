---
name: tdd
description: >
  Drive a behavior change with a red-green-refactor loop where every new test is
  seen failing for the intended reason before production code is written. Use when
  the user asks for TDD, test-first work, or to write a failing test before fixing
  a bug ("write a failing test for this bug first, then fix it"), and for new logic
  or bug fixes that need a regression test when the project has a runnable test
  harness. When the bug's cause is still unknown, pair with debugging.
---

# Test-Driven Development

## Purpose

Prove each behavior with a test that failed without the change and passes with it. A test that was never seen failing proves nothing.

## The rule

```
NO PRODUCTION CODE FOR NEW BEHAVIOR WITHOUT A TEST SEEN FAILING FIRST
```

If production code for the behavior was written before its test, set that code aside (stash or revert it), write the test, watch it fail, then reintroduce the smallest code that passes. Do not keep the earlier code "as a reference" and adapt the test to it.

## When to use / avoid

Use for new functions, branches, bug fixes, and contract changes where a focused test can run in seconds.

Avoid or adapt for exploratory spikes (throw the spike away afterward), pure configuration or copy changes, generated code, and projects with no runnable harness. In those cases, state the alternative verification path. Do not add a new test framework without justification and approval.

## Procedure

1. **Confirm the behavior and conventions.** Read the acceptance criterion, the nearest existing tests, and the project's test command.
2. **Red: write one small test** for one behavior. Name it after the behavior, not the implementation.
3. **Run it and watch it fail.** It must fail for the intended reason, such as an assertion on the missing behavior. A compile error, import error, or typo is not a valid red. Fix the test until it fails correctly.
4. **Green: write the minimum code** that makes this test pass. Hard-coding is acceptable if the next test forces generalization.
5. **Run the focused test and its neighbors.** Everything relevant must pass.
6. **Refactor** names, duplication, and structure while the tests stay green. Run the tests after each refactor step.
7. **Repeat** for the next behavior, edge case, or failure path.
8. **Close** with the broader suite proportionate to risk, then inspect the diff.

## Bug fixes

Reproduce the bug as a failing test first. The red run must show the reported symptom. After the fix, the same test passes. Keep it as the regression test.

## Test quality rules

- Test observable behavior through public interfaces; avoid asserting private implementation details.
- One reason to fail per test. Arrange, act, assert.
- Prefer real collaborators. Mock only slow, non-deterministic, or external boundaries.
- Never weaken an assertion, mark a test skipped, or delete a test to reach green.
- Avoid sleeps; wait on conditions (see [condition-based waiting](../debugging/references/condition-based-waiting.md)).

## Red flags

| Thought | Answer |
|---|---|
| "I'll write the tests after, it's faster" | Tests written after pass by construction and miss what they should catch. |
| "This is too simple to test" | Simple code with a test costs seconds. Simple code that breaks costs hours. |
| "I already wrote the code, I'll just add a test" | Set the code aside and do red first. |
| "The test passed on the first run" | Then it never proved anything. Make it fail, or check that it tests the right thing. |
| "I'll mock this to make it pass" | Mocking the unit under test hides the defect. |
| "Just this once" | That is the rationalization this rule exists for. |

## Outputs and gate

Changed tests and code, plus a short log of the cycle: the test, the observed failure, and the observed pass. Gate: every new behavior has a test that was observed failing and then passing. If the loop was impossible, record why and the substitute evidence.

## References

- [Testing](../testing/SKILL.md) for choosing test layers.
- [Verification before completion](../verification-before-completion/SKILL.md).
- [Quality gate contract](../../../core/contracts/QUALITY-GATE-CONTRACT.md).
