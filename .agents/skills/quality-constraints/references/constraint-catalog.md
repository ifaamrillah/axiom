# Constraint Catalog

Measurable constraints, a suggested default for each, and the command that enforces it per ecosystem. Use it in setup steps 3 and 4: pick the dimensions the user chose, propose the default, and bind it to the command. Mark every proposed number `default` in `.axiom/CONSTRAINTS.md` until the team confirms it.

Before proposing anything, detect what already exists. Never ask what you can read:

| What | Where to look |
|---|---|
| Stack | `package.json`, `pyproject.toml`, `go.mod`, `pom.xml`, `build.gradle*`, `composer.json`, `Cargo.toml` |
| Linters and config | `eslint.config.*`, `biome.json`, `ruff.toml`, `pyproject.toml [tool.*]`, `.golangci.yml`, `phpstan.neon`, `detekt.yml` |
| Type strictness | `tsconfig.json` `strict`, `mypy.ini`/`[tool.mypy]`, PHPStan `level` |
| Coverage today | existing `coverage/`, `lcov.info`, `coverage.xml`; or run the suite once |
| CI and what blocks | `.github/workflows/*`, `.gitlab-ci.yml`, branch protection required checks |

## Choosing a default

- If the project already meets a number, hold it. If it does not, use a **ratchet** (today's value, must not get worse) rather than an aspirational number. See [ratchets and waivers](ratchets-and-waivers.md).
- Give each number with its reason. A number without a reason gets deleted by the next person it blocks.
- Put slow checks late. Edit loop under ~5 s, task end under ~90 s, CI unbounded.
- Include at least one **external** check the agent cannot satisfy by writing its own tests (dependency advisories, a real browser, WCAG rules, a type checker).

## Catalog

### Correctness and tests

| Constraint | Default | Why |
|---|---|---|
| Test suite | 0 failures, no new skips | The floor |
| Coverage of changed lines | ≥ 80% | Forces a test; leaves room for wiring lines |
| Project coverage | today's value, must not fall (0.5% tolerance) | Adoptable on day one |
| Mutation score on changed files (optional) | ≥ 60% to start | Typical for a suite never mutated; 80% is mature |

| Ecosystem | Coverage command | Mutation |
|---|---|---|
| JS/TS | `vitest run --coverage` or `jest --coverage` (lcov) | `npx stryker run --mutate "<changed files>"` |
| Python | `pytest --cov=<pkg> --cov-report=xml --cov-fail-under=<n>` | `mutmut run --paths-to-mutate <files>` |
| Go | `go test -coverprofile=cover.out ./... && go tool cover -func=cover.out` | `go-mutesting` (less mature) |
| JVM | JaCoCo `jacocoTestCoverageVerification` (Gradle) / `jacoco:check` (Maven) | PIT `pitest` |
| PHP | `vendor/bin/pest --coverage --min=<n>` or PHPUnit `--coverage-clover` | `vendor/bin/infection --min-msi=<n>` |

Changed-line coverage: intersect the coverage report with `git diff -U0 <base>`. Tools: `diff-cover coverage.xml --compare-branch=origin/main --fail-under=80` (Python, also reads lcov and Cobertura from any language), or the CI coverage service's patch check.

### Complexity and size

| Constraint | Default | Why |
|---|---|---|
| Cyclomatic complexity per function | ≤ 10 (warn), ≤ 15 (block) | Above 10, test cases needed grow fast |
| Cognitive complexity per function | ≤ 15 | Sonar's default |
| Function length | ≤ 50 lines (warn) | Fits on one screen |
| File length | ≤ 500 lines (warn); a change must not push a file over 1000 | Inspection signal, not a hard cap |
| Parameters per function | ≤ 5 | More suggests a missing object |
| Nesting depth | ≤ 4 | Deep nesting hides branches |
| Diff size per change | ~300 changed lines (warn) | Reviewable in one sitting |

| Ecosystem | Command or rule |
|---|---|
| JS/TS (ESLint) | `complexity: ["error", 15]`, `max-lines: ["warn", 500]`, `max-lines-per-function: ["warn", 50]`, `max-params: ["error", 5]`, `max-depth: ["error", 4]`; cognitive via `eslint-plugin-sonarjs` `sonarjs/cognitive-complexity` |
| JS/TS (Biome) | `lint.rules.complexity.noExcessiveCognitiveComplexity` with `maxAllowedComplexity: 15` |
| Python (Ruff) | `C901` with `[tool.ruff.lint.mccabe] max-complexity = 10`; `PLR0913` (`max-args = 5`), `PLR0912` (branches), `PLR0915` (statements); or `radon cc -n C <pkg>` / `xenon --max-absolute B` |
| Go | `gocyclo -over 15 .`, `gocognit -over 15 .`, or `golangci-lint` linters `gocyclo`, `gocognit`, `funlen`, `nestif` |
| Java | Checkstyle `CyclomaticComplexity`, `MethodLength`, `ParameterNumber`; PMD `CognitiveComplexity` |
| Kotlin | detekt `CyclomaticComplexMethod`, `LongMethod`, `LongParameterList`, `LargeClass` |
| PHP | PHPMD `CyclomaticComplexity`, `ExcessiveMethodLength`; PHPStan with `phpstan-cognitive-complexity` |

### Type strictness

| Ecosystem | Strict setting | Check |
|---|---|---|
| TypeScript | `"strict": true`, plus `noUncheckedIndexedAccess`, `noImplicitOverride`, `exactOptionalPropertyTypes` for new projects | `tsc --noEmit` = 0 errors; ESLint `@typescript-eslint/no-explicit-any: error`, `no-floating-promises: error` |
| Python | mypy `strict = true` on new modules (per-module overrides for legacy); or pyright `"typeCheckingMode": "strict"` | `mypy <pkg>` or `pyright` = 0 errors |
| PHP | PHPStan level ≥ 6 for existing code, 8 or `max` for new; use a baseline file for legacy errors | `vendor/bin/phpstan analyse --no-progress` |
| Kotlin | `allWarningsAsErrors = true` | `./gradlew build` |
| Java | `-Xlint:all -Werror`; NullAway or Error Prone where adopted | `./gradlew compileJava` |
| Go | compiler is strict; add `go vet` + `staticcheck` | `go vet ./... && staticcheck ./...` |

Baselines (`phpstan-baseline.neon`, mypy per-module `ignore_errors`, `detekt-baseline.xml`, `.eslint` bulk suppressions) freeze legacy errors. The baseline may only shrink.

### Lint rule sets

| Ecosystem | Default set | Gate |
|---|---|---|
| JS/TS | `@eslint/js` recommended + `typescript-eslint` `recommendedTypeChecked`; or Biome recommended | `eslint . --max-warnings=0` or `biome ci .` |
| Python | Ruff `select = ["E", "F", "W", "I", "B", "UP", "S", "C4", "SIM", "RUF"]` | `ruff check . && ruff format --check .` |
| Go | `golangci-lint` defaults + `errorlint`, `bodyclose`, `gosec`, `contextcheck` | `golangci-lint run` |
| Java/Kotlin | Checkstyle or Spotless; detekt + ktlint | `./gradlew check` |
| PHP | Laravel Pint (or PHP-CS-Fixer) + PHPStan/Larastan | `vendor/bin/pint --test && vendor/bin/phpstan analyse` |
| SQL migrations | `squawk` (PostgreSQL) | `squawk migrations/*.sql` |

Warnings policy: either warnings block (`--max-warnings=0`) or the warning count is ratcheted. A growing warning count nobody reads is not a constraint.

### Bundle size and web performance

| Constraint | Default | Command |
|---|---|---|
| JS per entry (gzip) | today's value, must not grow; new apps ≤ 170 KB initial JS | `size-limit` (`npx size-limit`), `bundlesize`, or Next.js build output |
| LCP | ≤ 2.5 s (p75) | `lighthouse $URL --output=json` or Lighthouse CI `assert` |
| INP | ≤ 200 ms (p75) | Field data (RUM, CrUX); lab proxy: Total Blocking Time ≤ 200 ms |
| CLS | ≤ 0.1 | Lighthouse / RUM |
| Image weight | no new image > 200 KB without reason | build step or review |

Lighthouse CI example (`lighthouserc.json`): `"assertions": {"largest-contentful-paint": ["error", {"maxNumericValue": 2500}], "cumulative-layout-shift": ["error", {"maxNumericValue": 0.1}]}`.

### Latency and resource budgets (services)

| Constraint | Default | Command |
|---|---|---|
| API p95 latency | measure today, hold it; typical target p95 ≤ 300 ms for reads | `k6 run` with `thresholds: { http_req_duration: ["p(95)<300"] }` |
| Error rate under load | < 1% | k6 `http_req_failed: ["rate<0.01"]` |
| Queries per request | no N+1; cap per endpoint (for example ≤ 10) | Django `assertNumQueries`, Laravel `DB::getQueryLog` in tests, Rails `bullet`, Hibernate statistics |
| Benchmark regression | ≤ 10% slower than base | `go test -bench . -count 10` + `benchstat`, `pytest-benchmark --benchmark-compare-fail=mean:10%`, JMH |
| Memory | no unbounded growth over a soak run | soak test with heap snapshots |

Latency budgets need a stable environment. On shared CI runners, report rather than block, or compare against a base run in the same job.

### Dependency policy

| Constraint | Default | Command |
|---|---|---|
| Known vulnerabilities | none at high or critical | `osv-scanner scan source -r .`, `npm audit --audit-level=high`, `pip-audit`, `govulncheck ./...`, `composer audit`, OWASP Dependency-Check |
| Secrets | none in source or history of the diff | `gitleaks dir . --redact` (or `gitleaks git --redact` for history) |
| Static security analysis | none at high | `semgrep scan --config p/default --error`, `bandit -r <pkg> -lll`, `gosec ./...` |
| Licenses | allow-list (for example MIT, Apache-2.0, BSD, ISC); deny GPL/AGPL in proprietary distribution | `license-checker --onlyAllow`, `pip-licenses --allow-only`, `go-licenses check`, `composer licenses` |
| Lockfile | committed; installs use it (`npm ci`, `pip install --require-hashes`, `composer install`) | CI install step fails on drift |
| New direct dependency | needs a reason in the PR (size, maintenance, license, alternatives) | review |
| Architecture boundaries | no forbidden imports between layers | `dependency-cruiser`, `eslint-plugin-boundaries`, `import-linter` (Python), ArchUnit (JVM), `deptrac` (PHP) |

Gate notes: some scanners exit 0 when they find issues (for example `semgrep` without `--error`, `axe` without `--exit`). Before calling a row enforced, run it once against a known violation and once against a clean control, and confirm the exit codes.

### Accessibility (UI)

| Constraint | Default | Command |
|---|---|---|
| Automated WCAG | 0 critical or serious axe violations on changed pages | `npx @axe-core/cli $URL --tags wcag2a,wcag2aa,wcag21aa --exit`, `@axe-core/playwright` in e2e tests, `pa11y` |
| Lint | `eslint-plugin-jsx-a11y` recommended | ESLint |

## Placement

| Stage | Runs | Budget |
|---|---|---|
| Edit loop | format, lint and types on changed files, floor guard | < 5 s |
| Task end | related tests, changed-line coverage, secrets | < 90 s |
| CI | full suite, security scans, mutation on changed files, bundle, Lighthouse, load tests | minutes |

## Template row

```markdown
| Coverage | Changed lines ≥ 80%; project ≥ 71.3% (ratchet, 0.5% tolerance) | `pytest --cov=app --cov-report=xml && diff-cover coverage.xml --compare-branch=origin/main --fail-under=80` | Yes (CI) | default |
```

Sources: adapted from addyosmani/agent-skills (MIT) (`skills/constraint-driven-development/SKILL.md`, `skills/performance-optimization`) and general practice.
