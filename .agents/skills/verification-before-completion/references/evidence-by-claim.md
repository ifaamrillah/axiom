# Evidence by Claim

For each claim, run the proving command after the last relevant change, then quote the decisive line. Commands below are common shapes; use the repository's own scripts first (`package.json` scripts, `Makefile`, `pyproject.toml`, CI config).

## Tests

| Claim | Proving evidence | Not sufficient |
|---|---|---|
| "Tests pass" | Full suite command, exit 0, line with counts: `412 passed`, `Tests: 88 passed, 88 total`, `ok` for every Go package | A focused run; an earlier run; "should pass" |
| "The new test covers the fix" | Test fails with the fix reverted, passes with it restored | The test passing once |
| "No regressions" | Same suite, same command, compared with the pre-change baseline | New tests passing |

Common commands: `pytest -q`, `npm test`, `npx vitest run`, `go test ./... -count=1`, `./mvnw test`, `./gradlew test`, `vendor/bin/phpunit`, `cargo test`.

Check: the reported count is close to the expected total. A run that collected 0 or far fewer tests than usual is not a pass.

## Build

| Claim | Proving evidence | Not sufficient |
|---|---|---|
| "It builds" | Build command exit 0 from a clean state when caching is involved | Lint or type check; the dev server starting; IDE showing no errors |
| "The release artifact is correct" | Artifact produced, version and size checked, smoke-run (`./dist/app --version`) | Build log saying "done" |

Commands: `npm run build`, `go build ./...`, `cargo build --release`, `./mvnw -q package -DskipTests` (then tests separately), `docker build .`, `composer install --no-dev && php -l`.

## Lint and format

| Claim | Proving evidence | Not sufficient |
|---|---|---|
| "Lint clean" | Linter over the whole configured scope, 0 errors, exit 0 | Running on only the changed file when the claim is about the project |
| "Formatted" | Formatter in check mode exits 0 (`prettier --check .`, `black --check .`, `gofmt -l .` prints nothing, `cargo fmt --check`) | Formatter ran in write mode with no check afterward |

Watch for: rules disabled inline to make lint pass (`eslint-disable`, `# noqa`, `//nolint`). Those need a stated reason.

## Types

| Claim | Proving evidence | Not sufficient |
|---|---|---|
| "Type-safe" / "no type errors" | `tsc --noEmit` exit 0; `mypy .` or `pyright` with `0 errors`; `go vet ./...` clean | The bundler building (many bundlers strip types without checking) |

Watch for: new `any`, `# type: ignore`, `@ts-expect-error`, or casts that only silence the checker.

## Database migrations

| Claim | Proving evidence | Not sufficient |
|---|---|---|
| "Migration works" | Applied to a fresh database and to a copy with representative data; schema inspected afterward | The migration file exists; the ORM model compiles |
| "Migration is reversible" | Up, down, up again succeeds, and data survives where promised | A `down` method exists |
| "Safe for production" | Lock and duration estimate on realistic row counts; backward-compatible with the running app version | It ran fast on an empty dev database |

Commands: `alembic upgrade head && alembic downgrade -1 && alembic upgrade head`, `npx prisma migrate deploy`, `rails db:migrate db:rollback db:migrate`, `php artisan migrate && php artisan migrate:rollback`, `flyway migrate`. Never run against production without explicit authorization.

## UI

| Claim | Proving evidence | Not sufficient |
|---|---|---|
| "The page works" | The flow driven in a real browser (Playwright, or manual with screenshots), including the changed states: loading, empty, error, success | The component compiles; a unit test with a mocked DOM |
| "Responsive" / "accessible" | Observed at named widths (for example 375 and 1280 px); axe or Lighthouse output; keyboard pass recorded | "Uses the design system" |

If no browser is available, say "UI not verified in a browser" and list what was checked instead.

## Performance

| Claim | Proving evidence | Not sufficient |
|---|---|---|
| "Faster" | Before and after numbers, same machine and data, several runs, median and spread | One run; a different dataset; "should be faster" |
| "No performance regression" | Benchmark or load test compared with baseline within a stated tolerance | Tests passing |

Examples: `hyperfine 'old' 'new'`, `go test -bench . -count=10` with `benchstat old.txt new.txt`, `pytest-benchmark`, k6 or `wrk` for HTTP, Lighthouse for page load.

## Security

| Claim | Proving evidence | Not sufficient |
|---|---|---|
| "Vulnerability fixed" | The original proof of concept no longer reproduces; regression test added; variants checked (other endpoints, encodings) | The patch "looks right" |
| "No known vulnerable dependencies" | `npm audit --omit=dev`, `pip-audit`, `govulncheck ./...`, `composer audit`, `osv-scanner` output, with any accepted findings listed | A clean lockfile diff |
| "No secrets committed" | Secret scanner over the diff (`gitleaks detect`, `trufflehog git file://.`) | Reading the diff by eye |

## Documentation

| Claim | Proving evidence | Not sufficient |
|---|---|---|
| "Docs updated" | Each changed interface (flag, endpoint, config key, behavior) mapped to the doc line that now describes it | "Updated the README" |
| "Examples work" | Example commands or snippets executed, output matches the doc | The snippet looks right |
| "Links valid" | Link checker or repository validator output | Spot-checking one link |

## Deployment

| Claim | Proving evidence | Not sufficient |
|---|---|---|
| "Deployed" | The target environment reports the new version (health or version endpoint, deployment status) | The pipeline was triggered; the merge happened |
| "Working in staging/production" | Smoke checks against that environment; error rate and latency watched for a stated period | The deploy job turned green |
| "Rolled back" | The environment reports the previous version and the symptom is gone | The rollback command was issued |

Deployment to production and other consequential external actions need explicit user authorization before they run.

## Requirements

| Claim | Proving evidence | Not sufficient |
|---|---|---|
| "Requirements met" / "spec complete" | Each acceptance criterion listed with the check that proves it, and its result | The suite passing |

Sources: adapted from obra/superpowers (MIT) `skills/verification-before-completion/SKILL.md`, addyosmani/agent-skills (MIT) `skills/debugging-and-error-recovery/SKILL.md`, and general practice.
