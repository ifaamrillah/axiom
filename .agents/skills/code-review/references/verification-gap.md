# Verification Gap

A focused review prompt that compares what was claimed with what was actually proven.

## Brief

```text
You are auditing verification for <task>. Do not edit files.
Inputs: the acceptance criteria, the diff, and the author's report of checks run.
1. For each acceptance criterion, find the test or observation that proves it.
   Classify each one as proven, partially proven, asserted only, or not addressed.
2. For each new or changed test, decide whether it would fail if the change were
   reverted. Flag tests that assert mocks, snapshot whatever the code outputs,
   or check only that no exception was thrown.
3. Compare the claimed commands with the evidence. Was each claimed check
   actually run after the final edit? Is the output shown?
4. List failure paths and boundary behaviors with no test.
5. List quality-bar changes: skipped tests, loosened assertions, suppressions,
   lowered thresholds.
Report each gap with the criterion or file:line, what is missing, and the
smallest check that would close it.
```

## Output expectation

A table of acceptance criteria and their proof status, followed by verification gaps. "Asserted only" for a must-have criterion is a blocking finding.
