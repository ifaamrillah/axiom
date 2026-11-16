# Patterns and Anti-Patterns

Use this when picking a structural pattern, a cache, a queue, or an event design, or when reviewing an architecture for known failure shapes. Back to [SKILL.md](../SKILL.md).

Default stance: the simplest structure that meets measured drivers. Each pattern below has a cost; pay it only when the "use when" column is true now, not someday.

## Structural patterns

| Pattern | Use when | Avoid when | Main cost |
|---|---|---|---|
| Layered (controller, service, repository) | CRUD-heavy apps; team knows the convention | Business rules leak into every layer; layers are pass-through only | Anemic layers that add files, not meaning |
| Hexagonal (ports and adapters) | Core logic must be tested without DB or network; you will swap an external provider | Small app with one adapter per port and no test pain | Indirection; more interfaces |
| Modular monolith | One team or a few teams; one deploy is acceptable; you want clear boundaries | Modules need independent scaling or release cadence that you can measure | Requires enforced boundaries (lint rules, package visibility) |
| Microservices | Independent teams own independent domains; measured need for separate scaling, deploy, or fault isolation | One team; shared database; unclear domain boundaries | Network failure, distributed tracing, data consistency, ops load |
| Event-driven (pub/sub) | Several consumers react to one fact; producers must not know consumers | You need an immediate answer; one consumer only | Eventual consistency; ordering; debugging across hops |
| CQRS (separate read and write models) | Read shapes differ greatly from write shapes; read load far exceeds writes | Simple CRUD; one screen per table | Two models to keep in sync; stale reads |
| Event sourcing | Audit history is a hard requirement; you need to rebuild state at a point in time | You only want an audit log (use an append-only audit table) | Schema evolution of events; replay tooling; steep learning curve |
| Serverless functions | Spiky, low, or event-triggered load; small stateless units | Long-running jobs; steady high load; low-latency cold-start-sensitive paths | Cold starts, vendor coupling, local testing friction |

### Enforcing module boundaries in a monolith

- TypeScript: `eslint-plugin-boundaries` or `dependency-cruiser` rules; one `index.ts` public surface per module.
- Java/Kotlin: ArchUnit tests; Gradle modules with `api` vs `implementation`.
- Python: `import-linter` contracts in `pyproject.toml` or `.importlinter`.
- Go: `internal/` packages; one package per module.
- PHP: Deptrac layers.
- .NET: separate projects with `InternalsVisibleTo` used sparingly; NetArchTest.

A boundary that is not checked in CI erodes within months.

## Monolith vs services: decision table

| Question | If yes | If no |
|---|---|---|
| Do separate teams need to deploy independently today? | Lean services | Stay monolith |
| Is there a measured component that needs 10x the resources of the rest? | Extract that component | Stay monolith |
| Do domains share most of their data in transactions? | Stay monolith | Services are possible |
| Can the team operate tracing, per-service CI/CD, and on-call per service? | Services are possible | Stay monolith |

Extract with the strangler pattern: route one capability at a time to the new component behind a stable interface; keep the old path until traffic proves the new one.

## Caching strategies

| Strategy | How it works | Use when | Watch for |
|---|---|---|---|
| Cache-aside (lazy) | App reads cache; on miss, reads DB and fills cache | General read-heavy data | Stampede on hot key expiry; stale after writes |
| Read-through | Cache library loads from DB on miss | Same as cache-aside, with library support | Hidden coupling to loader |
| Write-through | Write to cache and DB together | Read-after-write freshness matters | Write latency; caching data never read |
| Write-behind | Write to cache; flush to DB later | Very high write rate, loss tolerable | Data loss on cache crash |
| HTTP caching (`Cache-Control`, `ETag`) | Client or CDN caches responses | Public or per-user GET responses | Caching private data in shared caches (`private` vs `public`) |
| Memoization (in-process) | Function result cached in memory | Pure, expensive, small key space | Unbounded growth; per-instance inconsistency |

Rules:

- Every cache entry has a TTL, even with explicit invalidation.
- Name the staleness budget and get product sign-off on it.
- Prevent stampedes: request coalescing (single-flight), jittered TTLs, or early refresh.
- Key design includes tenant and version: `v2:tenant:42:product:9001`.
- Never cache authorization decisions longer than the session or permission change window.
- Measure hit rate. Below about 80% for a hot path, the cache may cost more than it saves.

## Queues and async work

| Need | Pick |
|---|---|
| Background job for one consumer, same app | Job queue on existing store (Sidekiq, Celery, BullMQ, Oban, `SKIP LOCKED` table) |
| Event must commit atomically with a DB write | Transactional outbox, then publish |
| Many independent consumers, replay needed | Log-based broker (Kafka, Kinesis, Redpanda, NATS JetStream) |
| Simple fan-out, no replay | Pub/sub (SNS+SQS, Google Pub/Sub, RabbitMQ fanout) |
| Delayed or scheduled work | Delayed jobs or a scheduler with idempotent handlers |

Rules for every queue consumer:

- Assume at-least-once delivery. Make the handler idempotent (natural key, dedup table, or upsert).
- Set a max retry count with exponential backoff and jitter, then a dead-letter queue.
- Alert on DLQ depth and on age of oldest message, not only on queue length.
- Decide ordering needs explicitly. Per-key ordering (partition key) is cheap; global ordering is not.
- Put a schema version in every message. Consumers must ignore unknown fields.
- Never do "write DB, then publish" without an outbox; a crash between them loses the event.

## Event design

- Name events as past-tense facts: `OrderPlaced`, not `PlaceOrder`. A command is a request; an event is history.
- Choose payload style on purpose: thin events (ID only, consumer fetches) reduce coupling to schema but add load; fat events (full state) avoid callbacks but freeze the schema.
- Include `event_id`, `occurred_at`, `schema_version`, and the aggregate ID.
- Additive changes only within a version. Breaking changes get a new event name or version.

## Resilience patterns

| Pattern | Use for | Default starting values |
|---|---|---|
| Timeout | Every network call | Below the caller's own timeout; e.g. 2 s for an internal API |
| Retry with backoff + jitter | Transient errors on idempotent calls | 3 attempts, 100 ms base, x2, full jitter |
| Circuit breaker | A dependency that fails often or slowly | Open after ~50% failures over 20 calls; half-open after 30 s |
| Bulkhead | Isolating a slow dependency's thread or connection pool | Separate pool per dependency |
| Rate limit | Protecting your service and downstreams | Token bucket per client key |
| Graceful degradation | Non-critical features | Serve cached or default content; hide the widget |

Never retry non-idempotent writes without an idempotency key.

## Architecture anti-patterns

| Anti-pattern | Symptom | Do instead |
|---|---|---|
| Distributed monolith | Services must deploy together; shared DB; chatty sync calls | Merge back, or split along data ownership with async contracts |
| Shared database between services | Two services write the same tables | One owner per table; others use its API or events |
| Big ball of mud | No module boundaries; any file imports any file | Define modules, enforce with a boundary linter, move code gradually |
| Golden hammer | Same tool for every problem ("everything is a Kafka topic") | Choose per driver; a table often beats a broker |
| Premature abstraction | Interface with one implementation and no test seam need | Inline it; abstract at the third real use |
| Speculative generality | Plugin systems and config DSLs for one case | Build the one case |
| Anemic domain + god service | Entities are bags of fields; one `OrderService` has 3,000 lines | Move rules next to the data they guard; split by use case |
| Synchronous chain | Request goes A to B to C to D; availability multiplies (0.99^4 = 0.96) | Collapse, cache, or make the tail async |
| Leaky abstraction | ORM entities or DB errors returned from the API | Map to DTOs and stable error codes at the boundary |
| Dual writes | Write DB and publish event, or write two DBs, without a transaction | Outbox, CDC, or a single source of truth |
| Config as code smell | Behavior controlled by dozens of flags with no owners | Flag owner and expiry; remove dead flags |
| Resume-driven design | New tech with no driver the current stack fails | Show the measured gap or keep the current stack |

Sources: adapted from addyosmani/agent-skills (MIT) `skills/api-and-interface-design/SKILL.md` and general practice.
