# Edge-Case Hunter

A focused review prompt for finding inputs and states the change does not handle. Use it as a separate pass or as a delegated reviewer brief.

## Brief

```text
You are reviewing <diff or files> against <acceptance criteria>. Do not edit files.
Find concrete inputs or states for which the changed code behaves incorrectly.
For each changed function or endpoint, enumerate:
- Empty, null/None/undefined, zero, negative, maximum, and off-by-one values
- Unicode, whitespace, very long strings, and mixed case where text is parsed or compared
- Duplicate, reordered, concurrent, or retried requests (idempotency)
- Partial failure: the second of two writes fails; timeouts; cancellation
- Time: time zones, DST transitions, leap days, clock skew, expiry boundaries
- Permissions: anonymous user, other tenant, revoked access, admin-only path
- State transitions: invalid order, repeated transition, terminal state
- Resource limits: pagination end, large payloads, empty collections
For each real problem, report: file:line, the input or state, the observed or
derived wrong behavior, why the code produces it, and the smallest fix.
Do not report a case the code already handles; cite the handling line instead.
Mark anything you could not confirm as a question.
```

## Output expectation

A short list of confirmed edge-case defects, each with a reproducing input, plus questions. An empty list is acceptable when justified by the cases checked.
