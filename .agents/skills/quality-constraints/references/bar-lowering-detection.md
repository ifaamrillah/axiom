# Bar-Lowering Detection

Concrete patterns and commands for finding a lowered bar in a diff. Use it when reviewing any change, and before reporting your own work as done. The summary table in SKILL.md names the categories; this file gives the per-language patterns and a runnable scan.

Agents rarely craft clever loopholes. They hit a red check and take the cheapest road to green. The cheapest roads are predictable, so they can be grepped.

## Scope the diff correctly

`git diff` alone misses untracked files. Compare against the merge base and include new files:

```bash
base=$(git merge-base origin/main HEAD) || { echo "no merge base"; exit 2; }
git diff -U0 "$base" -- . > /tmp/lower.diff
git ls-files --others --exclude-standard | while read -r f; do
  git diff --no-index -U0 /dev/null "$f" >> /tmp/lower.diff
done
grep -E '^\+[^+]' /tmp/lower.diff > /tmp/added.txt     # added lines
grep -E '^-[^-]'  /tmp/lower.diff > /tmp/removed.txt   # removed lines
```

Treat a failure to compute the diff as "could not check", never as "clean".

## Patterns per language

Search **added** lines unless the row says removed.

### Suppressions

| Language | Pattern (ERE) |
|---|---|
| TS/JS | `@ts-ignore\|@ts-nocheck\|@ts-expect-error\|eslint-disable\|biome-ignore\|istanbul ignore\|c8 ignore\|v8 ignore` |
| Python | `#\s*type:\s*ignore\|#\s*noqa\|#\s*pyright:\s*ignore\|#\s*pragma:\s*no cover\|#\s*nosec\|#\s*pylint:\s*disable` |
| Go | `//\s*nolint\|//\s*#nosec\|//\s*lint:ignore` |
| Java | `@SuppressWarnings\|//\s*NOPMD\|CHECKSTYLE:OFF\|@SuppressFBWarnings` |
| Kotlin | `@Suppress\(\|//\s*ktlint-disable` |
| PHP | `@phpstan-ignore\|@psalm-suppress\|phpcs:ignore\|phpcs:disable\|@codeCoverageIgnore` |
| Rust | `#\[allow\(\|#!\[allow\(` |
| Any | `nosemgrep\|gitleaks:allow\|Stryker disable\|NOSONAR` |

Coverage and mutation suppressions (`istanbul ignore`, `pragma: no cover`, `@codeCoverageIgnore`, `Stryker disable`) deserve extra attention: they remove code from the measurement instead of testing it.

### Skipped, focused, or disabled tests

| Language | Pattern |
|---|---|
| TS/JS | `\b(it\|test\|describe)\.(skip\|todo)\(\|\bx(it\|describe\|test)\(\|\.only\(\|\bf(it\|describe)\(` |
| Python | `@pytest\.mark\.(skip\|skipif\|xfail)\|@unittest\.skip\|pytest\.skip\(\|raise\s+SkipTest` |
| Go | `t\.Skip\(\|t\.SkipNow\(\|testing\.Short\(\)` |
| Java/Kotlin | `@Disabled\|@Ignore\|assumeTrue\(\|Assumptions\.assume` |
| PHP | `markTestSkipped\|markTestIncomplete\|->skip\(\|->todo\(` |

### Weakened or removed assertions

Search **removed** lines for assertions and **added** lines for weak ones:

```bash
# Assertions removed from test files that still exist
grep -E '^-.*\b(assert|expect|assertEquals|assertThat|should|require\.)' /tmp/lower.diff
# Weak assertions added
grep -E '^\+.*(toBeTruthy|toBeDefined|not\.toThrow|toHaveBeenCalled\(\)|assertIsNotNone|assertTrue\(True\)|assertNotNull|assert\s+True\b|toMatchSnapshot)' /tmp/lower.diff
```

Also check: test files deleted (`git diff --diff-filter=D --name-only "$base" | grep -E 'test|spec'`), snapshot files changed (`git diff --name-only "$base" | grep -E '__snapshots__|\.snap$'`), expected values edited in the same commit as the logic they test.

### Swallowed errors

| Language | Pattern |
|---|---|
| TS/JS | `catch\s*(\(\w*\))?\s*\{\s*\}\|\.catch\(\s*\(\)\s*=>\s*(\{\s*\}\|null\|undefined)\s*\)` |
| Python | `except\s*:\|except\s+(Exception\|BaseException)(\s+as\s+\w+)?\s*:\s*(pass)?$` |
| Go | `_\s*(,\s*_)?\s*=\s*\w+.*\(` on a call returning error; `if err != nil \{\s*\}` |
| Java/Kotlin | `catch\s*\((Exception\|Throwable\|RuntimeException)\s+\w+\)\s*\{\s*\}` |
| PHP | `catch\s*\(\\?(Exception\|Throwable)\s+\$\w+\)\s*\{\s*\}\|@\$?\w+\(` (the `@` error-suppression operator) |

Multi-line empty catches will not match a single-line grep. Read every new `catch`/`except` in the diff.

### Stubs and placeholders reported as done

```text
TODO|FIXME|XXX|HACK|NotImplementedError|NotImplementedException|todo!\(|unimplemented!\(|
throw new Error\(.(TODO|Not implemented)|panic\("(TODO|not implemented)|
return (null|None|\[\]|\{\}|true|false|0);?\s*(//|#).*(TODO|stub|placeholder)
```

### Relaxed thresholds and gates

Inspect diffs of these files line by line: `.axiom/CONSTRAINTS.md`, `.github/workflows/*`, `.gitlab-ci.yml`, `package.json` scripts, `jest.config.*`, `vitest.config.*`, `pyproject.toml`, `setup.cfg`, `.coveragerc`, `tsconfig*.json`, `eslint.config.*`, `.eslintrc*`, `biome.json`, `ruff.toml`, `mypy.ini`, `.golangci.yml`, `phpstan.neon*`, `phpunit.xml*`, `detekt.yml`, `.size-limit*`, `lighthouserc*`, `codecov.yml`.

| Pattern | Meaning |
|---|---|
| `continue-on-error:\s*true`, `allow_failure:\s*true`, `\|\|\s*true`, `;\s*exit 0` | CI step made non-blocking |
| Numbers decreased near `threshold`, `fail_under`, `--cov-fail-under`, `coverageThreshold`, `min-msi`, `--min`, `maxNumericValue`, `limit` | Threshold lowered |
| `"strict":\s*false`, `noImplicitAny":\s*false`, `strict = false`, `level:` decreased | Type strictness lowered |
| `"error"` changed to `"warn"` or `"off"`; rule removed from `select` or added to `ignore`/`extend-ignore`/`per-file-ignores` | Lint rule loosened |
| `--max-warnings` raised or removed; `--no-verify`, `SKIP=`, `HUSKY=0` | Gate bypassed |
| Baseline file grew (`phpstan-baseline.neon`, `detekt-baseline.xml`, `.eslint-suppressions*`) | Legacy errors added to the ignore list |
| Paths added to `exclude`, `omit`, `testPathIgnorePatterns`, `coveragePathIgnorePatterns` | Code removed from measurement |
| New row in the Exceptions table | Waiver added; check approval and expiry |

## One-shot scan

```bash
# Run from repo root after building /tmp/added.txt as above. Prints candidates; review each.
P='@ts-ignore|@ts-nocheck|eslint-disable|biome-ignore|istanbul ignore|c8 ignore|#\s*type:\s*ignore|#\s*noqa|pragma:\s*no cover|#\s*nosec|//\s*nolint|@SuppressWarnings|@Suppress\(|@phpstan-ignore|@psalm-suppress|phpcs:(ignore|disable)|nosemgrep|NOSONAR|Stryker disable'
S='\.(skip|only|todo)\(|\bx(it|describe|test)\(|\bf(it|describe)\(|pytest\.mark\.(skip|xfail)|unittest\.skip|t\.Skip\(|@Disabled|@Ignore|markTestSkipped'
E='catch\s*(\([^)]*\))?\s*\{\s*\}|except\s*:|except\s+Exception.*:\s*pass'
T='TODO|FIXME|NotImplemented|todo!\(|unimplemented!\(|Not implemented'
C='continue-on-error:\s*true|allow_failure:\s*true|\|\|\s*true|--no-verify'
for name in P S E T C; do
  eval "pat=\$$name"
  grep -nE "$pat" /tmp/added.txt | sed "s/^/[$name] /"
done
```

`P` suppressions, `S` skipped tests, `E` swallowed errors, `T` stubs, `C` gate bypass. A hit is a candidate, not a verdict: a new `# noqa: E501` on a long URL with a reason is fine. Report each confirmed one with file:line, the pattern, and the requirement it undermines.

## Judging a hit

| Hit | Acceptable when | Finding when |
|---|---|---|
| Suppression | Specific rule id, inline reason, narrowest scope (next line), and a waiver if the rule is a constraint | Blanket (`eslint-disable` for a whole file, bare `# type: ignore`), no reason, or hides a real defect |
| Skipped test | Linked issue, conditional on a real platform limit (`skipif(sys.platform == "win32")`) | Skipped because it fails after this change |
| Changed expectation | The spec or ticket says the old expectation was wrong | Expectation changed to match new output with no reason |
| Broad catch | Top-level boundary that logs, reports, and returns an error response | Inside business logic, or discards the error |
| Threshold change | Raised, or lowered in a separate approved change | Lowered in the change that would otherwise fail it |

Sources: adapted from addyosmani/agent-skills (MIT) (`skills/constraint-driven-development/SKILL.md`, `skills/constraint-driven-development/references/floor-guard.md`) and general practice.
