# Bisection

Bisection turns "something somewhere is wrong" into one commit, one input element, or one dependency in `log2(n)` steps. Use it whenever a known-good and a known-bad state exist and you cannot see the difference by reading.

Requirements for any bisection:

- A **deterministic check** that says good or bad. If the bug is intermittent, make the check run the test enough times to be reliable (see below).
- A **known-good** and a **known-bad** point, both confirmed by running the check, not remembered.

## Git bisect

### Manual

```sh
git bisect start
git bisect bad                    # current HEAD is broken (confirm first)
git bisect good v2.3.0            # confirmed working tag or SHA
# git checks out a midpoint; run the check, then mark it:
git bisect good    # or: git bisect bad, or: git bisect skip (cannot build/test)
# repeat until git prints "<sha> is the first bad commit"
git bisect log > bisect.log       # keep the record
git bisect reset                  # return to the original branch
```

### Scripted with `git bisect run`

`git bisect run <cmd>` runs the command at each step and reads its exit code:

| Exit code | Meaning |
|---|---|
| 0 | good |
| 1–124, 126, 127 | bad |
| 125 | skip this commit (cannot be tested) |
| 128 or higher | abort the bisection |

Write the check as a script **outside the work tree** (or untracked), so checkouts do not change it:

```sh
#!/usr/bin/env bash
# /tmp/bisect-check.sh
set -u
npm ci --silent >/dev/null 2>&1 || exit 125      # cannot install: skip
npm run build --silent >/dev/null 2>&1 || exit 125  # unrelated build break: skip
npx vitest run src/orders/total.test.ts >/dev/null 2>&1
```

```sh
chmod +x /tmp/bisect-check.sh
git bisect start HEAD v2.3.0
git bisect run /tmp/bisect-check.sh
```

Language variants for the final line:

```sh
python -m pytest -x -q tests/test_total.py::test_discount     # Python
go test ./internal/orders -run TestTotal -count=1             # Go
./mvnw -q -Dtest=TotalTest test                               # Java (Maven)
vendor/bin/phpunit --filter testDiscount tests/TotalTest.php  # PHP
```

When the regression test does not exist in old commits, keep the test file outside the tree and copy it in from the script, or write the check against the observable behavior (a CLI call, an HTTP request to a locally started server).

### Bisecting an intermittent failure

Make the check fail if any of N runs fails. Pick N so a bad commit fails with high probability (if the failure rate is 20%, 20 runs miss it about 1% of the time).

```sh
for i in $(seq 20); do go test ./pkg -run TestRace -count=1 || exit 1; done; exit 0
```

### Bisecting on a threshold

For performance regressions, turn timing into good/bad:

```sh
#!/usr/bin/env bash
ms=$(node bench/orders.js --json | jq '.medianMs')
[ "$(echo "$ms < 120" | bc)" = 1 ]   # good if median under 120 ms
```

Set the threshold between the good and bad medians, with margin for noise.

### Tips

- `git bisect skip` costs precision. If many commits are untestable, the result is a range.
- Use `git bisect start --first-parent` on merge-heavy histories to find the merge first, then bisect inside it.
- Restrict to paths with `git bisect start HEAD v2.3.0 -- src/orders` when the cause is surely in one area.
- The first bad commit is where the bug became visible. Read it, then confirm it is the cause by reverting it on HEAD and re-running the check.

## Input bisection

Use when one input fails and you need the minimal failing input (delta debugging).

1. Confirm the full input fails and an empty or trivial input passes.
2. Split the input in halves (lines, records, JSON keys, list items, files, CSS rules).
3. Test each half alone. Keep a failing half. If neither half fails alone, the failure needs elements from both: try removing one quarter at a time instead.
4. Repeat until removing any remaining element makes it pass. That is a 1-minimal input.
5. Save the minimal input as a test fixture.

```python
def minimize(items, fails):
    """Return a smaller list for which fails(list) is still True."""
    n = 2
    while len(items) >= 2:
        chunk = len(items) // n
        for i in range(n):
            rest = items[:i * chunk] + items[(i + 1) * chunk:]
            if fails(rest):
                items, n = rest, max(n - 1, 2)
                break
        else:
            if n >= len(items):
                break
            n = min(n * 2, len(items))
    return items
```

Ready-made tools: `creduce`/`cvise` for C-like sources, `hypothesis` shrinking in Python, `fast-check` shrinking in JS/TS.

## Dependency bisection

Use when the code did not change but a lockfile, base image, or toolchain did.

1. Diff the lockfiles: `git diff <good>..<bad> -- package-lock.json poetry.lock go.sum composer.lock`.
2. List changed packages with old and new versions. Direct dependencies first, then transitive ones.
3. Restore the good lockfile, then apply half of the version changes. Install and run the check. Keep halving.
   - npm: `npm install pkg@1.4.2 --no-save` per package, or edit `package.json` overrides.
   - Python: `pip install 'pkg==1.4.2'` in a fresh virtualenv.
   - Go: `go get pkg@v1.4.2 && go mod tidy`.
   - PHP: `composer require vendor/pkg:1.4.2 --no-update && composer update vendor/pkg`.
4. Once one package is found, bisect its versions. Read its changelog and the diff between the two versions.
5. Fix forward when the new behavior is correct and your code relied on a bug. Pin back only with a recorded reason and an issue to remove the pin.

The same procedure works for config flags, feature toggles, base images, and compiler versions: list the differences, then halve.

## Test-order bisection

A test that passes alone but fails in the suite is a bisection over the tests that run before it. See [test-pollution bisection](test-pollution-bisection.md).

Sources: adapted from obra/superpowers (MIT) `skills/systematic-debugging/root-cause-tracing.md`, `find-polluter.sh`, addyosmani/agent-skills (MIT) `skills/debugging-and-error-recovery/SKILL.md`, and general practice.
