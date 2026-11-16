# Conventions and Code Rules

Use this to discover how the repository works before writing code, and for the rules on errors, logging, and configuration. Back to [SKILL.md](../SKILL.md).

## Discover the commands

Find the commands the project actually uses. Prefer scripts the project defines over generic tool invocations.

| Ecosystem | Where to look | Typical commands |
|---|---|---|
| Node/TS | `package.json` `scripts`, lockfile type (`package-lock.json`, `pnpm-lock.yaml`, `yarn.lock`, `bun.lockb`) | `npm test`, `pnpm test -- <path>`, `npx tsc --noEmit`, `npm run lint` |
| Python | `pyproject.toml` (`[tool.pytest]`, `[tool.ruff]`, `[tool.mypy]`), `tox.ini`, `noxfile.py`, `Makefile` | `pytest <path> -q`, `ruff check .`, `mypy <pkg>`; `uv run`/`poetry run` prefix if used |
| Go | `go.mod`, `Makefile`, `.golangci.yml` | `go test ./pkg/...`, `go vet ./...`, `golangci-lint run` |
| Rust | `Cargo.toml`, workspace members | `cargo test -p <crate>`, `cargo clippy -- -D warnings`, `cargo fmt --check` |
| Java/Kotlin | `build.gradle(.kts)`, `pom.xml` | `./gradlew test --tests <Class>`, `./mvnw -pl <module> test` |
| PHP | `composer.json` `scripts`, `phpunit.xml`, `phpstan.neon` | `vendor/bin/phpunit --filter <name>`, `vendor/bin/phpstan analyse` |
| Ruby | `Gemfile`, `.rspec`, `Rakefile` | `bundle exec rspec <file>:<line>`, `bundle exec rubocop` |
| .NET | `*.sln`, `*.csproj` | `dotnet test --filter <name>`, `dotnet build -warnaserror` |

Also check CI config (`.github/workflows/*.yml`, `.gitlab-ci.yml`) — it shows the exact checks a PR must pass — and `Makefile`/`justfile`/`Taskfile.yml`.

## Discover the conventions

Read one or two existing features that resemble yours, end to end. Note:

- **Layout:** where handlers, services, models, and tests live; file naming (`order_service.py` vs `OrderService.ts`).
- **Naming:** casing, prefixes, test naming (`test_<behavior>`, `it("does X when Y")`).
- **Error style:** exceptions, result types, error codes, HTTP mapping.
- **Data access:** ORM, query builder, raw SQL, repository classes.
- **Dependency injection:** constructor injection, module-level singletons, framework container.
- **Test style:** fixtures vs factories, mocks vs fakes, in-memory DB vs test containers.
- **Formatting:** formatter config (`.prettierrc`, `ruff format`, `gofmt`, `.editorconfig`). Let the formatter decide; do not hand-format.
- **Commit style:** `git log --oneline -20` shows Conventional Commits, ticket prefixes, or free text.

Quick searches:

```bash
git ls-files | head -100                 # layout
rg -l "class .*Service" src | head        # service pattern
rg -n "raise |throw new " src | head -20  # error style
rg -n "logger\.|log\." src | head -20     # logging style
git log --oneline -20                     # commit style
```

When the docs and the code disagree on a convention, follow the code in the area you edit and report the drift. When two conventions coexist, follow the one used in the module you edit, or the newer one if a migration is visibly underway.

## Error handling rules

1. **Handle or propagate; never swallow.** An empty `catch` or `except: pass` is a bug unless a comment explains why the error is expected and safe.
2. **Catch the narrowest type** you can handle. Not `Exception`, `Throwable`, or bare `except:`.
3. **Add context when re-raising**, keep the cause.
4. **Validate at boundaries** (request parsing, config load, external responses). Trust already-validated internal data.
5. **Map errors at the edge.** Domain errors become HTTP status and error codes in one place. Never leak stack traces, SQL, or internal paths to clients.
6. **Distinguish expected from unexpected.** Expected (validation, not found) -> typed error, no alert. Unexpected -> log with stack, alert.
7. **Clean up** with `finally`, `with`, `using`, `defer`, or `try-with-resources`.
8. **Timeouts on every network call.** No default-infinite waits.

```python
# Bad
try:
    charge(card)
except Exception:
    pass

# Good
try:
    charge(card)
except PaymentDeclined as e:
    raise DomainError(code="PAYMENT_DECLINED") from e
```

```ts
// Good: keep the cause
try {
  await repo.save(order);
} catch (err) {
  throw new Error(`save order ${order.id} failed`, { cause: err });
}
```

```go
// Good: wrap with %w so callers can errors.Is / errors.As
if err := repo.Save(ctx, o); err != nil {
    return fmt.Errorf("save order %s: %w", o.ID, err)
}
```

## Logging rules

- Use the project's logger, never `print`/`console.log` in production code.
- Use structured fields, not string interpolation: `logger.info("order placed", extra={"order_id": id})`, `log.Info("order placed", "order_id", id)`.
- Levels: `debug` for developer detail, `info` for business events, `warn` for recoverable oddities, `error` for failures that need attention. Do not log at `error` and also re-raise the same error; one owner logs it.
- Include correlation: request ID or trace ID, and the entity ID.
- Never log secrets, tokens, passwords, full card numbers, or personal data beyond what policy allows. Redact at the logger if possible.
- Do not log inside hot loops; aggregate.
- Remove temporary debug logs before finishing.

## Configuration rules

- Read configuration once at startup into a typed, validated object (pydantic `BaseSettings`, `zod` schema on `process.env`, `envconfig`, Spring `@ConfigurationProperties`). Fail fast on missing required values.
- No secrets in code, tests, fixtures, or committed `.env` files. Add new keys to `.env.example` (or the project's equivalent) with a placeholder.
- Give non-secret settings safe defaults; give secrets no default.
- Do not read environment variables deep inside business logic; pass config in.
- Document every new setting where the project documents settings.

```ts
const Env = z.object({
  DATABASE_URL: z.string().url(),
  CHECKOUT_DISCOUNTS: z.enum(["on", "off"]).default("off"),
});
export const env = Env.parse(process.env);
```

## Dependencies

- Prefer the standard library and existing dependencies.
- A new dependency needs: a real need, an active maintainer, a compatible license, and acceptable size. Ask before adding one when the task did not call for it.
- Use the project's package manager and update the lockfile in the same change. Never hand-edit lockfiles.

## Comments and code shape

- Comment why, not what. Delete commented-out code.
- Keep functions short enough to read in one screen; extract when a block needs a comment to explain what it does.
- Match existing patterns even when you would choose differently; propose changes separately.
- No `TODO` without an owner or ticket reference, if the project tracks them.

Sources: adapted from addyosmani/agent-skills (MIT) `skills/incremental-implementation/SKILL.md` and `skills/api-and-interface-design/SKILL.md`, and general practice.
