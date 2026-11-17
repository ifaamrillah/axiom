# Reading Output Honestly

A command can print green and still prove nothing. Before you quote output as evidence, check that it says what you think it says.

## Checklist

1. **Exit code.** Read it directly (`echo $?`, or `; echo "exit=$?"` after the command). Text such as "done" is not an exit code.
2. **Counts.** Find passed, failed, skipped, errored, and total. Compare the total with what you expected.
3. **Scope.** Confirm which files, packages, or tests ran. Look for filters you or the config applied.
4. **Freshness.** Confirm the run happened after the last edit and was not served from a cache.
5. **Warnings.** Read them. Deprecations and "no tests found" warnings often explain a silent pass.
6. **The whole output.** Do not stop at the first green line; failures often appear after a summary of passing modules.

## Partial runs

| Signal | Example | What it means |
|---|---|---|
| Focus filter | `-k`, `-run`, `--grep`, `-t`, `--filter`, `it.only`, `fdescribe` | Only some tests ran. The claim is limited to those tests. |
| Fail-fast | `-x`, `--bail`, `-failfast` | The run stopped at the first failure; later tests did not run. |
| Path argument | `pytest tests/unit` | Integration and end-to-end tests were not included. |
| Changed-only mode | `jest --onlyChanged`, `vitest related`, `nx affected` | Selection depends on a dependency graph that may miss your change. |
| Low test count | `Ran 12 tests` when the suite has 400 | Collection failed or a filter is active. |
| "No tests found" | pytest exit code 5; `testing: warning: no tests to run` in Go | Nothing ran. That is not a pass. |

Search the code for committed focus markers before claiming a full pass: `grep -rnE '\b(it|describe|test)\.only\(|\bfit\(|\bfdescribe\(' src tests`.

## Cached results

| Tool | Cache sign | Force a fresh run |
|---|---|---|
| Go | `ok pkg 0.01s (cached)` | `go test ./... -count=1` |
| Gradle | `UP-TO-DATE`, `FROM-CACHE` | `./gradlew test --rerun-tasks` |
| Nx / Turborepo | `[local cache hit]`, `cache hit, replaying logs` | `--skip-nx-cache`, `--force` |
| Bazel | `(cached) PASSED` | `--nocache_test_results` |
| Jest / Vitest | watch mode reusing results | run once without watch: `npx vitest run` |
| CI | a re-run that reused artifacts from an older commit | Check the commit SHA the job ran on |

A cached pass proves the result for the inputs the cache keyed on. If you are not sure your change is in that key, force a fresh run.

## Skipped and expected-to-fail tests

- `skipped`, `xfail`, `pending`, `todo`, `t.Skip`, `@Disabled`, `markTestSkipped` all mean "not verified".
- Report them by count: "401 passed, 11 skipped". If any skipped test covers the changed code, the claim is not proven.
- An `xpass` (expected failure that passed) is a signal to investigate, not a bonus.
- A test you skipped or disabled to get a green run is a failure you hid. Say so.

## Filtered and piped output

| Trap | Why it misleads | Do instead |
|---|---|---|
| `cmd \| tail -20` | Hides earlier failures and changes the exit code to `tail`'s | `set -o pipefail`, or save the full log and grep it |
| `cmd \| grep PASS` | Shows only what you looked for | Grep for `FAIL\|ERROR\|panic\|Traceback` too |
| `cmd 2>/dev/null` | Drops errors written to stderr | Keep stderr while verifying |
| `cmd \|\| true` | Forces success | Remove it for the verification run |
| Quiet flags (`-q`, `--silent`) | May hide warnings and skips | Read the summary line and the exit code |
| Truncated tool output | The failure may be in the hidden part | Rerun with the output saved to a file, then search the file |
| Compressed output (an output-compressing hook such as RTK) | The decisive line may be summarized away | Rerun the proving command uncondensed (`rtk bypass <cmd>`) or save the full output to a file; quote the real line |

## Retries and flaky tests

- A test that passed on retry (`--reruns`, `retries: 2`, `flaky` markers) failed at least once. Report it as flaky, with the count.
- "It passed the second time" is not evidence that the change is correct.
- If a test is known to be flaky on the baseline, record that before your change and compare rates, not single runs.

## Environment mismatches

- A pass on your machine does not prove CI or production behavior when versions, data, or configuration differ. Name the environment in the evidence.
- A check that could not start (missing service, no network, no credentials) is **blocked**, not passed and not failed. Record the error line.

## Reading CI

1. Confirm the job ran on the commit you are claiming (compare the SHA).
2. Open the job log, not only the status icon. Steps can be marked `continue-on-error` or `allow_failure`.
3. Check that the expected jobs ran. Path filters and conditions can skip whole jobs, which then show as green or neutral.
4. Required checks still pending are not passed.

## Quoting evidence

Quote the command, the decisive line, and when it ran relative to the last edit:

```text
`go test ./... -count=1` -> all 14 packages `ok`, exit 0 (run after the last edit to service.go)
```

Do not paraphrase a failure as a pass with caveats. "Mostly passing" is failing.

Sources: adapted from obra/superpowers (MIT) `skills/verification-before-completion/SKILL.md` and general practice.
