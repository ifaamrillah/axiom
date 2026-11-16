# Test-Pollution Bisection

Symptom: a test passes when run alone but fails when run with others. Another test leaks state (globals, environment variables, files, database rows, mocks, time, locale, or caches).

## Procedure

1. Confirm the target test passes alone and fails in the full ordered run. Record both commands.
2. List the tests that run before the target, in execution order.
3. Bisect: run the first half of that list followed by the target.
   - If the target fails, the polluter is in that half. Otherwise it is in the other half.
4. Repeat until one test remains. Confirm with `<polluter> + <target>` → fail and `<target>` alone → pass.
5. Inspect the polluter for state it sets without restoring. Fix the leak at the polluter. Use teardown, fixtures with scope, or isolation. Do not change the target test to tolerate the leaked state.

## Command shapes (adapt to the project)

```sh
# pytest: run a chosen subset in a fixed order, then the target
pytest -p no:randomly tests/a_test.py tests/b_test.py tests/target_test.py::test_x
# pytest-randomly: replay a failing order
pytest --randomly-seed=12345

# jest/vitest: run a subset serially
npx vitest run --sequence.concurrent=false a.test.ts b.test.ts target.test.ts
npx jest --runInBand a.test.ts b.test.ts target.test.ts

# go: package-level ordering; isolate with -run and -count=1; replay shuffles
go test ./pkg/... -run 'TestA|TestB|TestTarget' -count=1
go test ./pkg -shuffle=on        # prints the seed; replay with -shuffle=<seed>

# phpunit: replay a random order by its seed
vendor/bin/phpunit --order-by=random --random-order-seed=12345
```

Some runners randomize order. Record the seed and replay it, or disable randomization while bisecting.

## Finding a test that leaves an artifact behind

When the pollution is a visible artifact (a file, a directory, a database row), you do not need halving. Run each test file alone and check for the artifact after each:

```sh
#!/usr/bin/env bash
# usage: find-polluter.sh <path-that-should-not-exist> <test files...>
set -u
artifact=$1; shift
for f in "$@"; do
  [ -e "$artifact" ] && { echo "artifact already present before $f"; exit 2; }
  npx vitest run "$f" >/dev/null 2>&1    # substitute the project's single-file test command
  if [ -e "$artifact" ]; then echo "polluter: $f"; ls -la "$artifact"; exit 1; fi
done
echo "no polluter found"
```

Call it with a file list, for example `find-polluter.sh packages/core/.git $(git ls-files 'packages/core/*.test.ts')`. Remove the artifact before each run if a test is expected to create and clean it.

## Common leaks and fixes

| Leak | Typical source | Fix at the polluter |
|---|---|---|
| Environment variables | `os.environ[...] = ...`, `process.env.X = ...` | `monkeypatch.setenv`, `vi.stubEnv` + `vi.unstubAllEnvs`, `t.Setenv` |
| Global mocks or spies | `jest.spyOn` without restore | `afterEach(() => vi.restoreAllMocks())`; `restoreMocks: true` in config |
| Module singletons and caches | memoized config, DI containers | Reset hook in `afterEach`; avoid module-level state |
| Database rows | tests that commit | Transaction per test with rollback; truncate in teardown |
| Files | writes into the repository or a shared dir | Per-test temp dirs (`tmp_path`, `t.TempDir()`, `fs.mkdtemp`) |
| Time and timezone | fake timers not restored, `TZ` set | `vi.useRealTimers()` in `afterEach`; set `TZ` in config only |
| Locale and global config | `setlocale`, `Intl` polyfills, `ini_set` | Restore in teardown |

## Output

The polluting test, the leaked state, the fix, and evidence of `<polluter> + <target>` passing after the fix.

Sources: adapted from obra/superpowers (MIT) `skills/systematic-debugging/find-polluter.sh`, `root-cause-tracing.md`, and general practice.
