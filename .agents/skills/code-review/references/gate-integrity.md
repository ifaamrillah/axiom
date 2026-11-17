# Gate Integrity

A mandatory step before approving a change or claiming work is done. List every place in the diff where the quality bar went down. Back to [SKILL.md](../SKILL.md).

A green check proves little if the check itself got easier. This step looks at the checks, not the code under test.

## What to list

| Category | Examples |
|---|---|
| Assertions loosened or deleted | `assertEqual` replaced by `assertIsNotNone`; an `expect` line removed; an expected value edited to match new output |
| Tests skipped, marked expected-to-fail, or focused | `@unittest.skip`, `pytest.mark.xfail`, `it.skip`, `.only`, `t.Skip`, `@Disabled`; a test file deleted |
| Timeouts or retries raised | A test or CI timeout raised; a retry count added or raised; a sleep added before an assertion |
| Snapshots or golden files regenerated | Changed `__snapshots__/`, `*.snap`, `golden/`, `testdata/`, `fixtures/expected*`, approval files |
| Coverage thresholds or lint rules lowered | `fail_under` or `coverageThreshold` decreased; a rule moved from error to warn or off; paths added to an exclude list |
| Suppressions added | `# noqa`, `eslint-disable`, `@ts-ignore`, `# type: ignore`, `@SuppressWarnings`, `//nolint` |
| CI gates made non-blocking | `continue-on-error: true`, `allow_failure: true`, `\|\| true`, `--no-verify` |

## How to search

1. Build the diff against the merge base, including untracked files. Use the commands in [bar-lowering detection](../../quality-constraints/references/bar-lowering-detection.md#scope-the-diff-correctly). A diff you could not build means "could not check", never "none found". When the author describes a weakening you cannot see (a raised timeout, a regenerated snapshot), still list each described item as ASK, marked "described, not in the diff".
2. Run its [one-shot scan](../../quality-constraints/references/bar-lowering-detection.md#one-shot-scan) and its removed-assertion and snapshot commands.
3. Add the two searches that scan does not cover:

```bash
# Timeouts, retries, and sleeps whose values changed (compare the - and + lines)
grep -nE '^[-+].*(timeout|Timeout|TIMEOUT|retries|retry|Retry|flaky|reruns|sleep\()' /tmp/lower.diff
# Golden and approval files changed
git diff --name-only "$base" | grep -E '__snapshots__|\.snap$|golden|testdata/|expected|approved'
```

4. Read each config file in the diff line by line (CI, test runner, coverage, lint, type checker). Grep misses changed numbers.
5. Search added lines for new `shortcut:` markers. Each one needs a limit and an upgrade trigger; a marker without a trigger is a finding (see [simplicity](../../implementation/references/simplicity.md)).

## Rule: every item is ASK

Each item found is **ASK**. It needs a stated justification in the change (linked issue, spec line, approved waiver) or explicit approval from the user. Never mark one as auto-passed because the suite is green.

- An item with a valid justification stays listed, with the justification quoted.
- An item with no justification blocks an `Approved` verdict and a `Done` status until the user approves it or it is reverted.
- A raised timeout or a regenerated snapshot needs the reason the old value was wrong. "It was flaky" or "the output changed" is not a reason; it describes the symptom.

## Output

```markdown
### Gate integrity
Search: merge-base diff + untracked files; bar-lowering scan (P S E T C), timeout/retry grep, snapshot/golden file list, config files read.
1. ASK tests/test_api.py:12 — test timeout raised 2s -> 30s. Justification: none in the diff. Needs: cause of the slowness, or user approval.
2. ASK tests/__snapshots__/report.snap — regenerated in the same commit as the renderer change. Justification: none. Needs: confirmation that the new output is correct per the spec.
```

When nothing is found, say so with the search done:

```markdown
### Gate integrity
None found. Search: merge-base diff (14 files, 0 untracked); bar-lowering scan, timeout/retry grep, snapshot/golden list all empty; read pyproject.toml and ci.yml diffs.
```

"None found" without the search is not an answer.

Sources: idea from garrytan/gstack (gate integrity in review; MIT), rewritten.
