# Verifying Development Commands

A documented command that does not work is worse than no command: the next agent trusts it. Record where each command came from and whether it ran.

## Evidence levels

| Level | Meaning | How to write it |
|---|---|---|
| Verified | You ran it here and saw the result | `pnpm test` — verified 2026-11-16 @ abc123: 412 passed, 0 failed (41s) |
| CI-evidenced | CI runs it; you did not | `pnpm test` — from .github/workflows/ci.yml:28; not run locally |
| Declared | A manifest or README names it; nothing shows it runs | `make e2e` — Makefile:40; unverified |
| Unknown | No evidence | "No lint command found" |

Never upgrade a level without new evidence. A README command that CI does not run stays Declared.

## Where to find commands, in trust order

1. CI configuration (`.github/workflows/*.yml`, `.gitlab-ci.yml`, `Jenkinsfile`, `.circleci/config.yml`, `azure-pipelines.yml`). CI is what the team actually relies on.
2. Task runners: `package.json` `scripts`, `Makefile`, `justfile`, `Taskfile.yml`, `composer.json` `scripts`, `pyproject.toml` (`[tool.poe.tasks]`, `[tool.hatch.envs]`), `noxfile.py`, `tox.ini`, `Rakefile`, Gradle tasks.
3. Container files: `docker-compose.yml`, `Dockerfile`, `devcontainer.json`.
4. Contributor docs: `CONTRIBUTING.md`, `README.md`, `docs/development*`.

When sources disagree (README says `npm test`, CI runs `pnpm vitest run --coverage`), record both and mark the drift.

## Safe to run vs ask first

| Usually safe | Ask first or skip |
|---|---|
| `--version`, `--help`, listing commands (`npm run`, `make -n`, `php artisan list`, `bin/rails -T`) | Anything that deploys, publishes, or pushes |
| Unit tests, lint, type check, format check (`--check`), build | Migrations or seeds against a database you did not create |
| Dependency install into the project directory | `docker compose down -v`, `db:reset`, `migrate:fresh`, `prune` |
| Starting a dev server briefly to confirm it boots | Commands that read production credentials or call paid APIs |
| Read-only DB introspection on a local throwaway DB | Anything that changes global machine state |

Before running tests against a running container or service, check it belongs to this checkout (mount source, working directory, compose project name). It may serve a different branch.

## Procedure

1. List candidate commands from the sources above with file and line.
2. Check prerequisites: runtime version (`node -v`, `python3 --version`, `go version`, `java -version`, `php -v`, `ruby -v`) against `.nvmrc`, `.python-version`, `.tool-versions`, `go.mod`, `engines`.
3. Run the safe ones, fastest first: lint and type check, then unit tests, then build. Use a timeout.
4. Record each result with command, date, commit, and a one-line outcome (counts, exit code, duration).
5. On failure, capture the first decisive error line. Decide: missing setup step (document it), environment difference (document it), or pre-existing failure (record as baseline). Do not fix code during onboarding unless asked.
6. Write the results into `development-guide.md` with their evidence level.

## Example entry

```markdown
## Commands

| Task | Command | Evidence |
|---|---|---|
| Install | `pnpm install --frozen-lockfile` | verified 2026-11-16 @ 3f9c2e1 (pnpm 9.12, Node 20.11) |
| Unit tests | `pnpm test` | verified: 412 passed, 3 skipped, 0 failed |
| Lint | `pnpm lint` | verified: 0 errors, 14 warnings (pre-existing) |
| Type check | `pnpm typecheck` | verified: 2 errors in src/legacy/report.ts (pre-existing baseline) |
| E2E | `pnpm e2e` | CI-evidenced (.github/workflows/e2e.yml:31); needs Postgres; not run |
| Migrate | `pnpm db:migrate` | declared (package.json:18); not run: touches database |

Setup gotchas:
- `pnpm install` fails on Node 22 (sharp prebuild); use Node 20 per .nvmrc.
- Tests need `TZ=UTC`; CI sets it in ci.yml:12. Without it, 3 date tests fail.
```

Sources: general practice.
