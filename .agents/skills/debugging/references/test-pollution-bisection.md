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

# jest/vitest: run a subset serially
npx vitest run --sequence.concurrent=false a.test.ts b.test.ts target.test.ts

# go: package-level ordering; isolate with -run and -count=1
go test ./pkg/... -run 'TestA|TestB|TestTarget' -count=1
```

Some runners randomize order. Record the seed and replay it, or disable randomization while bisecting.

## Output

The polluting test, the leaked state, the fix, and evidence of `<polluter> + <target>` passing after the fix.
