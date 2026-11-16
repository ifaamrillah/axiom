# Per-Ecosystem Test Commands

Open this when you need the exact command to run one test, one file, the full suite, a filtered tier, or coverage in a given stack. Always prefer the project's own script (`npm test`, `make test`, `composer test`, a `justfile` target, a CI job definition) when it exists; it carries flags and environment the raw command lacks. Check `package.json` scripts, `Makefile`, `pyproject.toml`, `tox.ini`, `noxfile.py`, `composer.json`, `.github/workflows/*`, and the README first.

## Detect the stack

| File present | Runner to expect |
|---|---|
| `pyproject.toml` / `pytest.ini` / `conftest.py` | pytest (check `[tool.pytest.ini_options]`) |
| `manage.py` without pytest config | Django test runner (`python manage.py test`) |
| `vitest.config.*` or `vitest` in devDependencies | Vitest |
| `jest.config.*` or `jest` in devDependencies | Jest |
| `playwright.config.*` | Playwright Test (E2E) |
| `go.mod` | `go test` |
| `pom.xml` | Maven Surefire (JUnit) |
| `build.gradle(.kts)` | Gradle `test` task (JUnit) |
| `phpunit.xml(.dist)` | PHPUnit; Pest if `pestphp/pest` in `composer.json` |
| `.rspec` / `spec/spec_helper.rb` | RSpec |
| `Cargo.toml` | `cargo test` |
| `*.csproj` with xunit/nunit | `dotnet test` |

## Python: pytest

```sh
pytest                                   # full suite
pytest tests/test_orders.py              # one file
pytest tests/test_orders.py::test_total  # one test
pytest -k "discount and not slow"        # by name expression
pytest -m "not integration"              # by marker
pytest -x --lf                           # stop at first failure; rerun last failures
pytest -q -rA                            # quiet, but print a summary of all outcomes
pytest -n auto                           # parallel (pytest-xdist)
pytest -p no:randomly                    # disable random order (pytest-randomly)
pytest --cov=src --cov-branch --cov-report=term-missing
python -m pytest                         # when the package is not installed; adds cwd to sys.path
```

Django: `python manage.py test app.tests.test_models.OrderTests.test_total --parallel`.

## JavaScript / TypeScript: Vitest

```sh
npx vitest run                           # single run (no watch)
npx vitest run src/slug.test.ts          # one file
npx vitest run -t "collapses repeated"   # by test name
npx vitest run --coverage                # needs @vitest/coverage-v8 or -istanbul
npx vitest run --sequence.shuffle        # random order
npx vitest run --reporter=verbose
```

`npx vitest` with no `run` starts watch mode; avoid it in agent sessions and CI.

## JavaScript / TypeScript: Jest

```sh
npx jest                                 # full suite
npx jest src/slug.test.ts                # one file (path regex)
npx jest -t "collapses repeated"         # by test name
npx jest --runInBand                     # serial; use for DB-backed or flaky diagnosis
npx jest --coverage
npx jest --ci                            # no snapshot writes; fails on missing snapshots
npx jest --detectOpenHandles             # find leaked timers or sockets after tests
```

Monorepos: run in the package directory, or use the workspace runner (`pnpm --filter @app/api test`, `npm test -w packages/api`, `turbo run test --filter=api`).

## Go

```sh
go test ./...                            # all packages
go test ./internal/billing               # one package
go test ./internal/billing -run 'TestParseDuration/empty' -v   # one subtest (regex, slash-separated)
go test ./... -race                      # race detector
go test ./... -count=1                   # bypass the test cache
go test ./... -shuffle=on                # random order
go test ./... -short                     # skip tests guarded by testing.Short()
go test -tags=integration ./...          # build-tagged integration tier
go test ./... -coverprofile=cover.out && go tool cover -func=cover.out
go vet ./...                             # run alongside tests
```

## Java / Kotlin: JUnit 5

```sh
mvn test                                         # Maven
mvn -Dtest=OrderServiceTest test                 # one class
mvn -Dtest='OrderServiceTest#totals*' test       # methods by pattern
mvn verify                                       # includes Failsafe integration tests (*IT)
./gradlew test                                   # Gradle
./gradlew test --tests 'com.acme.OrderServiceTest.appliesDiscount'
./gradlew test --rerun-tasks                     # ignore up-to-date cache
./gradlew test jacocoTestReport                  # coverage with JaCoCo plugin
```

Use Testcontainers for real databases in integration tests; it needs a running Docker daemon.

## PHP: PHPUnit and Pest

```sh
vendor/bin/phpunit                               # full suite
vendor/bin/phpunit tests/Unit/OrderTest.php
vendor/bin/phpunit --filter 'test_applies_discount'
vendor/bin/phpunit --testsuite Feature
vendor/bin/phpunit --order-by=random
XDEBUG_MODE=coverage vendor/bin/phpunit --coverage-text   # or use pcov
vendor/bin/pest                                  # Pest
vendor/bin/pest --filter 'applies discount'
vendor/bin/pest --parallel
php artisan test --filter=OrderTest              # Laravel wrapper
```

## Ruby: RSpec

```sh
bundle exec rspec                                # full suite
bundle exec rspec spec/models/order_spec.rb
bundle exec rspec spec/models/order_spec.rb:42   # example at a line
bundle exec rspec -e "applies the discount"      # by description
bundle exec rspec --tag ~slow                    # exclude a tag
bundle exec rspec --order random --seed 1234     # reproduce an order
bundle exec rspec --only-failures                # needs example_status_persistence_file_path
bin/rails test test/models/order_test.rb:42      # Minitest (Rails default)
```

## Others in brief

```sh
cargo test                                       # Rust; cargo test name_substring -- --nocapture
dotnet test --filter "FullyQualifiedName~OrderTests"
mix test test/order_test.exs:42                  # Elixir
swift test --filter OrderTests                   # Swift Package Manager
```

## Reporting a run

Record enough that someone else can rerun it:

```
Command: pytest tests/billing -q
Env: Python 3.12.4, Postgres 16 via docker compose, TZ=UTC
Result: 214 passed, 2 skipped (both marked external), 0 failed in 18.4s
Not run: integration tier (-m integration) - needs sandbox credentials
```

A skipped test is not a passed test. Name skipped tiers and why.

Sources: general practice.
