# Project Knowledge Files: Structure and What to Capture

Write knowledge that saves the next agent a rediscovery. Skip anything the code or an existing doc already says clearly. Every file carries freshness metadata so a later session can tell whether to trust it.

## Common header

```yaml
---
status: active            # draft | active | stale | superseded
sources: [package.json, src/server.ts, .github/workflows/ci.yml]
verified_at_commit: <sha>
verified_on: <YYYY-MM-DD>
---
```

`sources` lists the files whose change would make this document wrong. Keep it short and specific.

## File by file

| File | Capture | Do not capture |
|---|---|---|
| `overview.md` | What the system does in 3-5 sentences, users, deployables (services, apps, CLIs), repository layout table, where to start reading | Marketing copy, feature lists copied from README |
| `tech-stack.md` | Languages, runtimes, frameworks, databases, queues, major libraries, with version and the file that declares it; declared vs observed runtime | Every dependency in the lockfile |
| `architecture.md` | Module map with responsibilities, dependency direction, entry points, one or two traced request/data flows with `path:line`, external integrations, persistence, auth boundary | Class-by-class descriptions |
| `conventions.md` | Patterns the code actually follows, each with one example path: naming, layering, error handling, logging, testing style, commit/PR norms; deviations noted | Generic best practice the repo does not follow |
| `development-guide.md` | Setup, run, test (unit/integration/E2E), lint, type check, build, migrate, seed; each command with its source and verification status | Commands you did not find evidence for |
| `glossary.md` | Domain terms, abbreviations, and code-name-to-concept mappings (for example `Ledger` = customer balance history) | Standard programming terms |

## Module cards (inside `architecture.md`)

Document modules, not files. A module is a directory or package with one responsibility. Write a card only for modules that a typical task touches or that carry risk. Use this structure:

```markdown
### billing (`src/billing/`)

Purpose: Invoices, payments, and refunds for subscriptions.
Entry points: `BillingController` (src/billing/controller.ts:12), job `chargeRenewals` (src/billing/jobs.ts:30)
Key files:
| File | Role |
|---|---|
| service.ts | Invoice lifecycle; only place that writes `invoices` |
| stripe-client.ts | Wraps Stripe SDK; retries 3x on 5xx |
| money.ts | Integer-cents Money type; never use float |
Depends on: `accounts` (read customer), `notifications` (emails)
Used by: `api/routes/billing.ts`, `admin/`
Data: tables `invoices`, `payments`; Stripe webhooks at POST /webhooks/stripe
Tests: tests/billing/ (unit, mocks Stripe); no integration tests against Stripe
Working here: run `pnpm test tests/billing`; webhook signature check must stay first in the handler
Risks: refund path has no idempotency key (service.ts:88)
```

### Per-file notes: when and how

Per-file narrative docs for a whole codebase go stale fast and cost context. Write a per-file entry only for:

- entry points and composition roots (`main.ts`, `app.py`, `Startup.java`),
- hub files with many dependents (`rg -l "from './db'" | wc -l` is high),
- files with traps: ordering requirements, global state, security checks, hand-tuned performance.

For those, capture: purpose (one line), public surface (exported functions or classes and what each is for), important constants and config it reads, side effects (I/O, global mutation), invariants or traps, and improvement notes (dead imports, unused functions, refactor candidates) labeled as observations, not tasks.

## Optional nested instruction files

Some repositories keep per-directory agent instructions (nested `AGENTS.md` or equivalent). If the project already uses them, update the nearest one instead of `.axiom/project/`. Each should hold: purpose of the directory, key files table, subdirectories table, how to test changes here, patterns to follow, internal and external dependencies, and a human-maintained section that regeneration must preserve. Do not introduce a nested hierarchy the project does not use, and remember that not every host loads nested files automatically.

## Quality bar

- Each claim traces to a file, command output, or observed behavior.
- Each convention cites an example path.
- Each command has a status: verified (ran, with date), CI-evidenced, or unverified.
- Unknowns are listed, not filled in.
- No secrets, tokens, or personal data copied from `.env` or config.

Sources: adapted from abryant710/auto-codebase-documenter (MIT) per-file report structure, yeachan-heo/oh-my-claudecode (MIT) deepinit directory template, ideas from bmad-code-org/BMAD-METHOD document-project, and general practice.
