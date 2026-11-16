# Per-Language Review Checklists

Use the checklist for each language in the diff, after the general procedure. Items are the defects that language makes easy. Skip items a configured linter or type checker already enforces in CI; confirm that it runs and blocks first.

For cross-language defect shapes with snippets, see [defect patterns](defect-patterns.md).

## Python

- [ ] Mutable default arguments: `def f(items=[])` or `={}` share state across calls.
- [ ] Bare `except:` or `except Exception: pass` hides failures, including `KeyboardInterrupt` for bare `except`.
- [ ] Files, sockets, locks, and DB cursors use `with`.
- [ ] Naive `datetime.now()` or `utcnow()` (deprecated since 3.12). Use `datetime.now(timezone.utc)`.
- [ ] `float` for money. Use `Decimal` built from strings, not floats.
- [ ] SQL via f-string, `%`, or `.format`. Use driver parameters. In Django, `raw()` and `extra()` need parameters too.
- [ ] `pickle`, `yaml.load` without `SafeLoader`, `eval`, `exec`, or `subprocess(..., shell=True)` on untrusted input.
- [ ] `is` used for value comparison (`x is "a"`, `x is 1000`).
- [ ] Late binding in closures: `lambda: i` inside a loop captures the last `i`.
- [ ] Async code calling blocking I/O (`requests`, `time.sleep`, sync DB driver) inside `async def`.
- [ ] Type hints: new public functions annotated; no new `Any` or `# type: ignore` without a reason.
- [ ] ORM: N+1 (`select_related`, `prefetch_related`, `selectinload`), queries in templates, missing `transaction.atomic` around multi-row writes.
- [ ] Logging sensitive values; `print` left in.

Verify: `ruff check .`, `mypy --strict <changed modules>` or `pyright`, `pytest -q`, `bandit -r <pkg>` for security-sensitive code.

## TypeScript and JavaScript

- [ ] `any`, `as` casts, and non-null `!` assertions that hide an unclear type. Prefer narrowing or validation at the boundary (zod, valibot, io-ts).
- [ ] External data (HTTP bodies, `JSON.parse`, `localStorage`, env) typed by assertion instead of validated.
- [ ] `||` used for defaults where `0`, `""`, or `false` are valid. Use `??`.
- [ ] Unawaited promises: `forEach(async ...)`, missing `await`, missing `.catch`. Enable `@typescript-eslint/no-floating-promises`.
- [ ] `==` instead of `===` (except deliberate `== null`).
- [ ] Number precision: IDs above 2^53 parsed as numbers; money in floats.
- [ ] `Date` parsing of date-only strings (UTC) vs date-time strings (local).
- [ ] React: missing or wrong hook dependencies; effects without cleanup; state derived from props and copied; keys from array index on reorderable lists; `dangerouslySetInnerHTML` with unsanitized input.
- [ ] Node: `child_process.exec` with interpolated strings; path joins with user input; missing request body size limits; secrets in client bundles (`NEXT_PUBLIC_`, `VITE_` prefixes expose values).
- [ ] Prototype pollution: merging untrusted objects into `{}` with keys like `__proto__`.
- [ ] Bundle: new heavy dependency imported on a hot client route; whole-library imports (`import _ from "lodash"`).

Verify: `tsc --noEmit`, `eslint . --max-warnings=0` or `biome check`, the test runner (`vitest run`, `jest`), and bundle size if the project budgets it.

## Go

- [ ] Every returned `error` is checked; `_ =` on an error has a comment saying why.
- [ ] Errors wrapped with `%w` and context, not replaced.
- [ ] `defer` inside a loop (defers run at function end; resources pile up).
- [ ] `resp.Body.Close()` deferred after a successful request.
- [ ] Goroutines have an exit path; `context.Context` is passed and honored; no goroutine leaks on early return.
- [ ] Maps written from multiple goroutines without a mutex or `sync.Map`.
- [ ] Loop variable capture in goroutines (fixed in Go 1.22 per-iteration semantics; check the `go` directive in `go.mod`).
- [ ] Nil interface vs interface holding a nil pointer (`var p *T = nil; var i I = p; i != nil`).
- [ ] Slices aliasing a shared backing array after `append` or sub-slicing.
- [ ] `http.Client{}` or `http.Get` without a timeout.
- [ ] `time.Now()` compared across machines; `time.Since` uses the monotonic clock, string-formatted times do not.

Verify: `go vet ./...`, `staticcheck ./...` or `golangci-lint run`, `go test -race ./...`.

## Java and Kotlin

- [ ] Resources in try-with-resources (Java) or `use {}` (Kotlin).
- [ ] `Optional.get()` without a presence check; `!!` in Kotlin.
- [ ] `equals` overridden without `hashCode`; mutable fields used in `hashCode` of a map key.
- [ ] `catch (Exception e)` that logs and continues; `InterruptedException` swallowed without restoring the interrupt flag.
- [ ] `SimpleDateFormat` shared across threads; `java.util.Date` or `LocalDateTime` for instants. Use `Instant` or `OffsetDateTime`.
- [ ] `double` for money. Use `BigDecimal` with an explicit `RoundingMode`; compare with `compareTo`, not `equals` (scale differs).
- [ ] Spring: `@Transactional` on private methods or self-invoked methods (proxy bypass, no transaction); lazy-loading outside a session; N+1 on `@OneToMany`; `@Async` without an executor bound.
- [ ] JPA: entity exposed directly as an API response (leaks fields, triggers lazy loads).
- [ ] Kotlin coroutines: `GlobalScope`, `runBlocking` on request threads, blocking calls in `Dispatchers.Default`.
- [ ] String concatenation in JPQL or native queries.

Verify: `./gradlew check` or `mvn verify` (with SpotBugs, Error Prone, or detekt and ktlint when configured).

## PHP and Laravel

- [ ] Mass assignment: `$fillable` set explicitly; no `$guarded = []` on models that receive request data; no `Model::create($request->all())`.
- [ ] Validation through a Form Request or `$request->validate()`; use `$request->validated()`, not `all()`.
- [ ] Authorization through policies or gates (`$this->authorize()`, `can` middleware) on every route that reads or writes a resource. Check route model binding for other tenants' IDs.
- [ ] Raw queries: `DB::raw`, `whereRaw`, `orderByRaw`, `selectRaw` with bindings. Sort columns from input are allow-listed.
- [ ] Blade output with `{{ }}`; any `{!! !!}` is justified and sanitized.
- [ ] N+1: eager-load with `with()`. Consider `Model::preventLazyLoading()` outside production.
- [ ] Multi-row writes in `DB::transaction()`; jobs dispatched after commit (`afterCommit()` or `ShouldBeUnique` where needed).
- [ ] Queued jobs idempotent; `$tries`, `$backoff`, and `failed()` handled.
- [ ] Loose comparison `==` with mixed types; `in_array` without strict `true`.
- [ ] `env()` called outside config files (returns null when config is cached).
- [ ] Migrations reversible (`down()`), and safe on large tables (see SQL below).

Verify: `php artisan test` or `vendor/bin/pest`, `vendor/bin/phpstan analyse` (Larastan), `vendor/bin/pint --test`.

## SQL and migrations

- [ ] Every new query that filters or joins on a column has a supporting index. Read the plan: `EXPLAIN` (MySQL) or `EXPLAIN (ANALYZE, BUFFERS)` (PostgreSQL, on a copy).
- [ ] `NULL` semantics: `NOT IN (subquery)` with nullable columns; `<>` excluding NULL rows; `COUNT(col)` vs `COUNT(*)`.
- [ ] Locking migrations on large tables:
  - PostgreSQL: `CREATE INDEX` without `CONCURRENTLY`; adding a column with a volatile default; `ALTER COLUMN TYPE` (rewrite); adding `NOT NULL` without a prior `CHECK ... NOT VALID` and validate; foreign keys without `NOT VALID`.
  - MySQL: confirm the operation is `ALGORITHM=INSTANT` or `INPLACE, LOCK=NONE`, or use an online schema tool.
- [ ] Expand and contract for renames and type changes: add new, dual-write, backfill, switch reads, then drop old in a later release. A single-step rename breaks the running version during deploy.
- [ ] Destructive operations (`DROP`, `TRUNCATE`, column removal) have a backup or are reversible, and old code no longer reads the column.
- [ ] Backfills run in batches with a bounded transaction size, not one `UPDATE` over millions of rows.
- [ ] `down` migration exists and was run, or irreversibility is stated.
- [ ] Constraints enforce invariants in the database (unique, foreign key, check), not only in code.
- [ ] Time columns use `timestamptz` (PostgreSQL) or store UTC consistently.
- [ ] Money columns use `NUMERIC`/`DECIMAL` with fixed scale, never `FLOAT`.

Verify: run the migration up, down, and up again on a copy with realistic row counts; check lock behavior with `squawk` (PostgreSQL) or the vendor's online DDL notes.

Sources: adapted from addyosmani/agent-skills (MIT) (`skills/code-review-and-quality`, `skills/performance-optimization/references/optimization-patterns.md`) and general practice.
