# Document Types and README Structure

Write the smallest document that answers a real reader's question. Pick the type from the question, not from habit.

## Which document?

| Reader's question | Type | Where | Write when |
|---|---|---|---|
| "What is this and how do I start?" | README | repo root, package root | New repo or package; setup or commands changed |
| "Why is it built this way?" | ADR | `docs/adr/` or the existing ADR folder | A decision is expensive to reverse ([ADRs](adrs.md)) |
| "How do I call it?" | API reference | generated from code or OpenAPI; prose guide beside it | Public endpoint, library function, CLI flag, event added or changed ([API docs](api-docs.md)) |
| "It is broken at 3 a.m. What do I do?" | Runbook | `docs/runbooks/` or ops wiki | A service has an alert, a manual recovery step, or an on-call rotation ([runbooks](runbooks.md)) |
| "How do I do task X?" | How-to guide | `docs/guides/` | A multi-step task recurs and is not obvious from commands |
| "How does the system fit together?" | Architecture overview | `docs/architecture.md` or `.axiom/project/architecture.md` | Onboarding; a new service or boundary appears |
| "What changed in this release?" | Changelog / release notes | `CHANGELOG.md` | Every user-visible change (owned by release management) |
| "How do I contribute?" | CONTRIBUTING | repo root | Outside or new contributors; review or commit rules exist |
| "What must agents know here?" | Agent instructions | `AGENTS.md` or the host's instructions file | Agents repeat a mistake; a command or boundary is non-obvious |
| "What does this odd line do?" | Code comment | inline | The *why* is not visible from the code |

### Do not write

- Comments that restate code (`// increment i`).
- Per-file narrative docs for the whole codebase.
- A second document that repeats an accurate existing one. Link to it.
- TODO comments for work you can do now, or commented-out code. Git keeps history.
- Docs for throwaway prototypes.

## README structure

Keep it scannable. A reader should know what the project is and run it in under five minutes.

```markdown
# <Project name>

<One paragraph: what it does, for whom, and its status (alpha, production, deprecated).>

## Quick start
Prerequisites: Node 20 (see .nvmrc), Docker 24+, pnpm 9.

    git clone <url> && cd <dir>
    pnpm install
    cp .env.example .env        # fill DATABASE_URL
    docker compose up -d db
    pnpm db:migrate
    pnpm dev                    # http://localhost:3000

## Commands
| Command | Does |
|---|---|
| `pnpm dev` | Dev server with reload |
| `pnpm test` | Unit tests (vitest) |
| `pnpm lint` | ESLint + Prettier check |
| `pnpm build` | Production build to dist/ |

## Configuration
| Variable | Required | Default | Meaning |
|---|---|---|---|
| DATABASE_URL | yes | — | Postgres connection string |
| LOG_LEVEL | no | info | pino log level |

## Project layout
| Path | Holds |
|---|---|
| src/api | HTTP routes |
| src/domain | Business rules |

## Further reading
Architecture: docs/architecture.md · Decisions: docs/adr/ · Runbooks: docs/runbooks/
```

README checks:

- Every command was run or is marked with where it came from.
- Prerequisites name versions and the file that pins them.
- Configuration lists keys and meaning, never real values.
- No badge walls, no feature marketing above the quick start.

## How-to guide shape

```markdown
# How to <task>

Applies to: <version / service>. Last verified: <date> @ <commit>.

Prerequisites: <access, tools>

1. <step> — expected: <what you see>
2. <step> — expected: <what you see>

If <symptom>: <fix>.
Rollback: <how to undo>, if the task changes state.
```

## Code comments that earn their place

```python
# BAD: restates the code
retries += 1

# GOOD: explains a non-obvious reason
# Stripe returns 409 while a previous idempotent request is still running.
# Retrying after 1s is safe because the idempotency key is reused.
if resp.status == 409:
    time.sleep(1)
```

Sources: adapted from addyosmani/agent-skills (MIT) documentation-and-adrs, and general practice.
