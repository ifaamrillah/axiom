# Architecture Decision Records

An ADR records one decision: the context, the choice, the options rejected, and the consequences. Code shows what was built. The ADR shows why, so a later reader does not undo it by accident or keep it after its reason is gone.

## When to write one

Write an ADR when a decision is expensive to reverse or will surprise a future reader:

- choosing a framework, database, queue, or major library,
- data model or schema shape, multi-tenancy model,
- authentication or authorization strategy,
- API style and versioning (REST vs GraphQL vs RPC, URL vs header versioning),
- build, hosting, or deployment platform,
- a deliberate deviation from a project convention,
- rejecting an obvious approach for a non-obvious reason.

Do not write one for reversible, local choices (a helper's name, a library for one script).

## Match the existing convention first

Before writing, look for existing ADRs (`docs/adr/`, `docs/decisions/`, `doc/architecture/decisions/`, `.adr-dir`, `adr-tools` setup). Match their directory, numbering (`0007-title.md` vs `ADR-007-Title.md`), markup, and headings. Do not restart numbering or add a second scheme. If conventions conflict, report the conflict. Use the default below only when nothing exists.

## Default template

```markdown
# ADR-0007: Store money as integer cents

Status: Accepted          <!-- Proposed | Accepted | Superseded by ADR-0012 | Deprecated -->
Date: 2026-11-16
Deciders: billing team

## Context
Invoice totals drifted by 1 cent in 0.3% of invoices (issue #482) because
amounts were stored as float. We bill in USD and EUR; tax rounds per line item.

## Decision
Store all amounts as integer minor units (`amount_cents BIGINT`) plus an ISO
currency code. Round half to even, per line item, in `Money.round()`.

## Alternatives considered
- DECIMAL(12,2): exact, but our ORM maps it to float in JS; every read would
  need conversion. Rejected: same bug class returns at the edges.
- Keep float, round on display: hides drift; totals still disagree with the
  payment provider. Rejected.

## Consequences
- Migration 0084 converts existing columns; needs a maintenance window (~4 min).
- All arithmetic goes through `Money`; raw number math on amounts is a review finding.
- Currencies with 3 decimal places (KWD) need a per-currency exponent later.
```

## Lifecycle

```
Proposed → Accepted → Superseded (by a newer ADR) or Deprecated
```

- Never delete or rewrite an accepted ADR's decision. Write a new ADR that supersedes it, and update the old one's status line to point forward.
- Link the ADR from the code it governs when the reason is not obvious (`// See ADR-0007`).
- A Proposed ADR that the team rejected stays, with status Rejected, if the reasoning is useful.

## Quality checks

| Check | Fails when |
|---|---|
| Context has facts | Only opinions; no constraint, number, incident, or requirement |
| Decision is one sentence you can act on | "We will consider…", or several decisions in one record |
| Alternatives are real | Straw men; no reason for rejection |
| Consequences include costs | Only benefits listed |
| Date and status present | Missing, so freshness cannot be judged |

## Lightweight variant

For smaller decisions, a five-line record in the same folder is fine:

```markdown
# ADR-0015: Use pino for logging
Status: Accepted · Date: 2026-11-16
Context: Need structured JSON logs for Loki; winston config drifted across services.
Decision: pino with the shared config in packages/logger.
Consequences: Replace winston in 3 services; log level via LOG_LEVEL.
```

Sources: adapted from addyosmani/agent-skills (MIT) documentation-and-adrs, and general practice.
