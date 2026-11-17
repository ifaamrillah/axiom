# Completion Reports: Good and Bad

A completion report lists each claim with its evidence, then the gate integrity list, then a fixed closing block. It never upgrades a skipped or blocked check to passed.

## Structure

```markdown
**Status:** <Done | Done with limits | Blocked | Not done>

Verified (after the last edit):
- <claim>: `<command>` -> <decisive output line>

Gate integrity:
- ASK <file:line> — <bar lowered>. Justification: <quoted, or none>.
- (or) None found. Search: <what was searched>

Not checked: <check>: <not run | blocked> because <reason>. To run: `<command>`. (or "none")
Risk: <the main residual risk, with evidence or a pointer>. (or "none known")
```

The report always ends with `Not checked:` and `Risk:`, in that order. Write "none" or "none known" rather than dropping a line; a missing line reads as "forgot to look".

"Done with limits" is honest when the core claims are proven and some checks could not run. "Done" requires every check the task needs to be verified.

## Example 1: bug fix

Bad:

> Fixed the date bug! The issue was timezone handling. All tests should pass now and it's ready to merge.

Why it is bad: "should pass" has no command; "fixed" has no reproduction; "ready to merge" is a claim about review and CI that nobody checked.

Good:

> **Status:** Done
>
> Verified (after the last edit):
> - Bug fixed: the reproduction `pytest tests/test_reports.py::test_dst_boundary` failed before (`assert '2026-03-29' == '2026-03-30'`) and passes now.
> - Regression test valid: reverted the fix and saw the same assertion fail, then restored it.
> - No regressions: `pytest -q` -> `588 passed, 3 skipped` (the 3 skips are the existing Postgres-only tests, same as the baseline).
> - Types: `mypy app` -> `Success: no issues found in 142 source files`.
>
> Gate integrity: none found. Search: bar-lowering scan on the merge-base diff, timeout and snapshot greps; all empty.
>
> Not checked: CI has not run on this branch yet.
> Risk: none known beyond CI.

## Example 2: feature with a UI

Bad:

> Implemented the export button. Everything works.

Good:

> **Status:** Done with limits
>
> Verified (after the last edit):
> - Unit tests: `npx vitest run src/export` -> `Tests 14 passed (14)`.
> - Full suite: `npx vitest run` -> `Tests 302 passed (302)`, exit 0.
> - Types: `npx tsc --noEmit` -> exit 0, no output.
> - Build: `npm run build` -> exit 0.
> - Acceptance criteria: AC1 (CSV download) and AC2 (disabled while loading) are covered by `export.test.tsx`; AC3 (filename includes date) by `filename.test.ts`.
>
> Gate integrity: none found. Search: bar-lowering scan on the merge-base diff; no snapshot files changed.
>
> Not checked: browser behavior; no browser available in this session. To check: `npm run dev`, open `/reports`, click Export, confirm the file `report-YYYY-MM-DD.csv` downloads.
> Risk: the download may fail in Safari, which handles blob URLs differently; untested.

## Example 3: a check is blocked

Bad:

> Integration tests are failing because of the environment, so I skipped them. Everything else passes. Done.

Good:

> **Status:** Blocked on integration tests
>
> Verified:
> - Unit tests: `go test ./internal/... -count=1` -> all 9 packages `ok`.
>
> Not checked: integration tests, blocked. `go test ./integration/...` fails at setup with `dial tcp 127.0.0.1:5432: connect: connection refused`; no database runs in this environment. To run: `docker compose up -d db && go test ./integration/... -count=1`.
> Risk: the change touches the repository layer, which only the integration tests cover, so the feature may not work end to end.

## Example 4: reporting a failure

Bad:

> Mostly done. A couple of tests fail but they look unrelated.

Good:

> **Status:** Not done
>
> - `npm test` -> `Tests: 2 failed, 286 passed, 288 total`.
> - Both failures are in `billing/invoice.test.ts` (`expected 104.97, received 104.96`). The baseline on `main` has 0 failures, so my change caused them. Investigating the rounding path next.
>
> Not checked: none.
> Risk: invoice totals are off by one cent; do not merge.

## Example 5: commit or pull request

Before "committed" or "opened a PR":

- The checks above ran after the final edit, not before a last "small cleanup".
- `git status` shows only intended files; no debug logs, `.only`, or temporary files.
- The PR description lists the same verified and not-verified items. It does not claim CI results that do not exist yet.

## Phrases to replace

| Instead of | Write |
|---|---|
| "Should work now" | The command and its result, or "not verified" |
| "All tests pass" | `<command>` -> `<count line>` |
| "Looks good" | What you checked and how |
| "Ready to merge" | What is verified; what review or CI still has to happen |
| "Fixed" | "The reproduction `<cmd>` now passes; it failed before with `<line>`" |
| "Green after bumping the timeout" | "ASK: timeout raised 2s -> 30s at `<file:line>`; cause unknown; needs approval" |
| "No risks" (or no closing block) | `Not checked: none` and `Risk: none known`, after actually looking |
| "Unrelated failures" | The failing test IDs and the baseline evidence that they failed before your change |

Sources: adapted from obra/superpowers (MIT) `skills/verification-before-completion/SKILL.md` and general practice.
