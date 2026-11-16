# Reviewing AI-Generated Code

AI-written code is fluent and confident even when wrong. It rarely has typos; it has plausible mistakes. Review it with more scrutiny, not less. Use this checklist in addition to the main procedure when the diff came from an agent, including your own earlier turns.

## Why it fails differently

- **Plausible invention.** It calls functions, flags, config keys, and package versions that do not exist, or that exist with different semantics.
- **Shortest road to green.** When a check fails, an agent tends to silence the check rather than fix the cause.
- **Local reasoning.** It edits the file in front of it and misses callers, other implementations, and persisted formats.
- **Over-building.** It adds options, abstractions, and fallback paths nobody asked for.
- **Self-confirming tests.** It writes tests that restate the implementation, so the tests cannot fail.
- **Confident reports.** It reports "all tests pass" or "verified" without having run anything after the last edit.

## Checklist

### Existence and correctness of references

- [ ] Every imported module, called function, method, and CLI flag exists in the installed version. Check the lockfile version and the library source or docs, not memory.
- [ ] New dependencies are real, correctly spelled, and maintained. A misspelled or invented package name is a supply-chain risk (an attacker can register it).
- [ ] Config keys and environment variables are read somewhere and documented.
- [ ] API endpoints called by new client code exist on the server with the same shape.

### Scope

- [ ] Every changed file is needed for the task. Unrelated reformatting, renames, and "while I was here" edits are findings.
- [ ] No unrequested features, options, or abstractions. One implementation does not need an interface and a factory.
- [ ] No duplicate of an existing helper. Search for the function name and its purpose before accepting a new utility.
- [ ] No dead code: unused parameters, unreachable branches, commented-out blocks, `_unused` variables, compatibility shims for callers that do not exist.

### Bar-lowering (the most common agent failure)

- [ ] No new suppressions, skips, deleted assertions, broadened catches, or lowered thresholds. Run the grep patterns in [bar-lowering detection](../../quality-constraints/references/bar-lowering-detection.md).
- [ ] No test changed to match new behavior without a stated reason why the old expectation was wrong.
- [ ] No mocks added to avoid a failing integration rather than fix it.
- [ ] No placeholder returns (`return []`, `return true`, `pass`, `TODO`) reported as done.

### Tests that cannot fail

- [ ] Expected values are literals or come from the spec, not recomputed with the implementation's own formula.
- [ ] The test fails when the change is reverted (see the quick mutation check in [API and test review](api-and-test-review.md#quick-mutation-check)).
- [ ] The mock is not the thing being asserted.

### Claims vs evidence

- [ ] Each "ran X, passed" claim has output from after the final edit. If not, run it yourself or mark it unverified.
- [ ] Each "handles edge case Y" claim points to a line and a test.
- [ ] Summaries match the diff. Agents sometimes describe intended changes that were never made, or omit changes that were.

### Consistency with the codebase

- [ ] The change follows the existing patterns for errors, logging, naming, and layering. A new style for an old problem is a finding.
- [ ] Every implementation of an interface or every handler of an event type was updated, not just the first one found.
- [ ] Security-sensitive code (auth, crypto, input parsing, SQL) uses the project's existing vetted helpers, not a fresh implementation.

## Red flags

| Red flag | Likely cause | Do instead |
|---|---|---|
| Large diff for a small task | Over-building or unrelated edits | Ask for the minimal diff; split refactors out |
| New `utils` or `helpers` file | Duplicate of an existing helper | Search and reuse |
| `try/except` around the whole function | Silencing an error seen once | Catch the specific error at the specific call |
| Test expectations changed in the same diff as logic | Tests bent to fit the code | Ask which behavior the spec requires |
| `// @ts-ignore` or `# type: ignore` next to new code | Type error not understood | Fix the type or narrow at the boundary |
| "Should work" or "this ensures" in the summary | No evidence | Ask for the command and output |
| Version-specific API with no version check | Training-data drift | Confirm against the installed version |

## Verification commands

Run the project's own checks rather than trusting the report:

```bash
git diff --stat <base>...HEAD          # scope: which files changed and how much
git diff <base>...HEAD -- '*test*'     # read test changes on their own
<typecheck> && <lint> && <tests>       # the project's real commands, after the final edit
```

Sources: adapted from addyosmani/agent-skills (MIT) (`skills/code-review-and-quality`, `skills/doubt-driven-development`), obra/superpowers (MIT) (`skills/requesting-code-review/code-reviewer.md`) and general practice.
