# Decisions and ADRs

Use this when you must choose between designs and record why. Back to [SKILL.md](../SKILL.md).

## Decision procedure

1. **State the decision as a question.** "How do order confirmations reach the email provider?" not "Should we use Kafka?"
2. **List drivers with weights.** Use must / should / nice. A must is pass-or-fail; it eliminates options outright.
3. **List options.** Include "extend what exists" and, where honest, "do nothing yet".
4. **Eliminate** options that fail a must. Write the reason in one line.
5. **Compare survivors** on should and nice drivers with the template below.
6. **Check reversibility.** A two-way door (easy to undo) deserves a fast choice. A one-way door (data format, public API, datastore, vendor lock) deserves a spike or prototype first.
7. **Decide, then write the ADR.** If the evidence is not enough, name the experiment that would settle it and its cost.

## Option-comparison template

```markdown
### Decision: <question>

Drivers (M = must, S = should, N = nice):
- M1 Confirmation email is sent at least once per order.
- S1 p95 checkout latency stays under 400 ms.
- S2 One on-call team can operate it.
- N1 Reusable for other notifications.

| Option | M1 | S1 | S2 | N1 | Reversal cost | Notes |
|---|---|---|---|---|---|---|
| A. Send email inline in checkout | pass | fail (provider p95 900 ms) | good | poor | low | Simplest; couples checkout to provider uptime |
| B. Outbox table + worker | pass | good | good | fair | low | Uses existing Postgres; no new infra |
| C. Kafka topic + consumer | pass | good | poor (new cluster) | good | high | Adds a platform the team does not run |

Eliminated: none failed M1.
Choice: B. It meets M1 and S1 with no new infrastructure. Revisit C if more than 3 consumers need the event stream.
Evidence: provider latency from last 30 days of logs; outbox pattern already used in `billing/`.
```

Rules for the table:

- Use pass / fail for musts, and good / fair / poor for the rest. Avoid fake-precise numeric scores.
- Every cell that drives the choice cites evidence: a measurement, a doc, a spike result, or existing code.
- Name the trigger that would reopen the decision.

## Quality-attribute trade-offs

Most choices buy one attribute with another. Name the trade explicitly.

| You gain | You usually pay | Typical lever |
|---|---|---|
| Latency (read) | Freshness, memory, invalidation complexity | Cache, denormalized read model, CDN |
| Latency (write path) | Consistency becomes eventual; more failure modes | Async queue, outbox, write-behind |
| Availability | Consistency during partitions (CAP); conflict resolution | Replicas, multi-region, AP datastores |
| Strong consistency | Latency and availability under failure | Single writer, transactions, consensus |
| Scalability (independent) | Operational cost, distributed debugging, network failure | Separate services, sharding |
| Simplicity | Peak scale or flexibility | Monolith, one datastore, sync calls |
| Security (isolation) | Latency and developer friction | Network segmentation, per-service credentials, extra auth hops |
| Evolvability | Upfront design time, indirection | Ports and adapters, versioned contracts |
| Throughput | Per-request latency | Batching, buffering |
| Cost | Headroom and resilience | Smaller instances, fewer replicas, spot capacity |

Quantify where you can. "Cache cuts p95 from 220 ms to 40 ms; data can be up to 60 s stale; product confirmed 60 s is acceptable."

## When to write an ADR

Write one when the decision:

- Picks or replaces a framework, datastore, queue, cloud service, or major library.
- Defines or breaks a contract other teams or clients consume.
- Sets a data model that will hold production data.
- Chooses sync vs async, or a consistency model.
- Rejects an obvious alternative a future reader will ask about.
- Is expensive to reverse (more than a few days of work, or data migration).

Do not write one for local choices that a code review covers.

## Match the existing convention first

Look for `docs/adr/`, `docs/decisions/`, `doc/architecture/decisions/`, an `.adr-dir` file, or `adr-tools` usage. Continue the existing numbering, filename pattern, file format, and section headings. If two conventions conflict, report the conflict instead of adding a third. Use the default template below only when no convention exists.

## Default ADR template

```markdown
# ADR-NNNN: <decision in a short active phrase>

- Status: Proposed | Accepted | Superseded by ADR-XXXX | Deprecated
- Date: YYYY-MM-DD
- Deciders: <names or roles>

## Context
The problem, the drivers (with numbers), and the constraints. Facts, not the answer.

## Options considered
1. <Option> - one-line summary, main pro, main con.
2. ...

## Decision
What we will do, stated plainly.

## Consequences
- Positive: ...
- Negative / accepted costs: ...
- Follow-up work: ...
- Revisit when: <measurable trigger>

## Evidence
Links to measurements, spikes, docs (with versions), related ADRs.
```

ADR rules:

- One decision per ADR. Keep it under about one page.
- ADRs are append-only. To change a decision, write a new ADR and mark the old one "Superseded by ADR-XXXX".
- Write in the present tense at decision time. A retroactive ADR says so in the Context section.
- Link the ADR from the code or module README it governs.

## Worked example

```markdown
# ADR-0007: Deliver order emails through a transactional outbox

- Status: Accepted
- Date: 2026-03-04
- Deciders: checkout team lead, platform on-call

## Context
Checkout sends the confirmation email inline. The email provider's p95 is
900 ms and it had 3 outages last quarter. During outages checkout returns
500 and orders are lost after the payment succeeded (14 support tickets in
February). Driver: checkout p95 < 400 ms; every paid order gets an email at
least once. Constraint: one team, Postgres 15 already in use, no message
broker in production.

## Options considered
1. Inline send with retry - simplest; still couples checkout latency and
   availability to the provider.
2. Outbox table written in the order transaction, drained by a worker -
   no new infrastructure; adds a worker and at-least-once delivery.
3. Kafka topic - good fan-out; requires running a cluster the team has
   never operated.

## Decision
Write an `outbox` row in the same transaction as the order. A worker polls
with `SELECT ... FOR UPDATE SKIP LOCKED`, sends the email with the order ID
as the provider idempotency key, and marks the row sent.

## Consequences
- Positive: checkout no longer waits on the provider; no lost emails on
  provider outage.
- Negative: emails can arrive up to ~30 s late; duplicates are possible if
  the provider ignores the idempotency key.
- Follow-up: alert when the oldest unsent row is older than 5 minutes.
- Revisit when: more than 3 consumers need order events, or outbox
  throughput exceeds 200 rows/s.

## Evidence
Provider latency: logs 2026-02-01..2026-02-28. Pattern already proven in
`billing/outbox.py`. Postgres docs on SKIP LOCKED (v15).
```

## Architecture readiness gate

Before implementation starts on a large change, check:

- [ ] Drivers are written with numbers, and the user confirmed assumptions that matter.
- [ ] At least two options were compared with evidence.
- [ ] Each component has one responsibility and each data set has one owner.
- [ ] Contracts are specified: inputs, outputs, errors, versioning.
- [ ] Failure behavior is defined for every external call and async path.
- [ ] Migration and rollback steps exist for every schema or contract change.
- [ ] ADRs are written for one-way-door decisions.
- [ ] Verification plan names concrete tests, load checks, and alerts.

Any unchecked item is a stated gap, not a pass.

Sources: adapted from addyosmani/agent-skills (MIT) `skills/documentation-and-adrs/SKILL.md`, ideas from bmad-code-org/BMAD-METHOD (architecture document structure and readiness checks, ideas only), and general practice.
