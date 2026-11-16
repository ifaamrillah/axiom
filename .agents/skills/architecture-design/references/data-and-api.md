# Data and API Design

Use this when designing a data model, a schema migration, or an API contract. Back to [SKILL.md](../SKILL.md).

## Data modeling rules

1. **Model the domain, not the screen.** Tables follow entities and their invariants. Read models for screens come later, if needed.
2. **One owner per table.** Only one module or service writes it.
3. **Put invariants in the database** when the database can enforce them: `NOT NULL`, `UNIQUE`, `CHECK`, foreign keys. Application checks race; constraints do not.
4. **Choose IDs on purpose.** Use UUIDv7 or ULID for distributed or public IDs (sortable, not guessable). Use bigint sequences for internal-only keys. Never expose sequential IDs where enumeration is a risk.
5. **Store money as integer minor units** (cents) or `DECIMAL(19,4)`, plus a currency code. Never as float.
6. **Store timestamps in UTC** with a time-zone-aware type (`timestamptz` in Postgres). Store the user's zone separately when it matters.
7. **Index for the actual queries.** Every foreign key used in joins and every `WHERE`/`ORDER BY` on a hot path gets an index. Check with `EXPLAIN ANALYZE`, not intuition.
8. **Plan deletion.** Soft delete (`deleted_at`) complicates every query and unique index; use it only when recovery or audit requires it. Know your data retention and erasure obligations (for example GDPR).
9. **Normalize first.** Denormalize only for a measured read problem, and name the process that keeps copies in sync.
10. **Multi-tenant data** carries `tenant_id` on every row, in every index prefix, and in every query. Consider row-level security as a second guard.

## Migration strategy: expand and contract

Never ship a breaking schema change in one deploy. Old and new code run at the same time during rollout.

| Phase | Schema | Code | Rollback |
|---|---|---|---|
| 1. Expand | Add new column/table, nullable or with default | Old code untouched | Drop new column |
| 2. Dual write | - | Write both old and new | Deploy previous code |
| 3. Backfill | - | Batch job copies old to new, idempotent, in small batches | Stop job; data in old field is intact |
| 4. Switch reads | - | Read new, keep writing both | Deploy previous code |
| 5. Stop old writes | - | Write new only | Re-enable dual write |
| 6. Contract | Drop old column after a full release cycle | - | Restore from backup only; this is the one-way door |

Example: rename `users.name` to `users.full_name`.

```sql
-- Phase 1 (expand)
ALTER TABLE users ADD COLUMN full_name text;
-- Phase 3 (backfill in batches; repeat until 0 rows)
UPDATE users SET full_name = name
WHERE id IN (SELECT id FROM users WHERE full_name IS NULL LIMIT 5000);
-- Phase 6 (contract, a later release)
ALTER TABLE users DROP COLUMN name;
```

Migration safety rules:

- Large-table locks: in Postgres, use `CREATE INDEX CONCURRENTLY`; add `NOT NULL` via a `CHECK (...) NOT VALID` constraint then `VALIDATE CONSTRAINT`. In MySQL, check whether the `ALTER` is `ALGORITHM=INSTANT` or `INPLACE`, or use `gh-ost` / `pt-online-schema-change`.
- Set a `lock_timeout` (for example `SET lock_timeout = '5s'`) so a blocked migration fails instead of stalling traffic.
- Backfills run in batches, are idempotent, and are resumable.
- Rehearse on a production-sized copy and record the duration.
- Every migration has a tested down step, or a written reason why it cannot (data-destroying steps).
- Schema migrations and data backfills ship separately.

## API style choice

| Style | Use when | Avoid when |
|---|---|---|
| REST + JSON | Public or partner APIs; resource-shaped data; HTTP caching matters | Clients need many differently shaped reads per screen |
| GraphQL | Many client types with varied read shapes; one team owns the schema | Simple CRUD; heavy write workflows; you cannot invest in query cost limits |
| gRPC | Internal service-to-service; strict schemas; streaming; low latency | Browser clients without a proxy; public APIs |
| Async events | Consumers react later; producer must not wait | Caller needs an answer now |

## API design rules (all styles)

- **Contract first.** Write the OpenAPI, GraphQL SDL, or `.proto` before the handler.
- **Validate at the boundary.** Parse and validate every input at the edge. Treat third-party responses as untrusted too.
- **Prefer addition.** New fields optional; never change a field's type or meaning; never reuse a removed field name (or protobuf field number - mark it `reserved`).
- **Hyrum's law.** Any observable behavior (ordering, error text, timing) becomes a dependency. Expose only what you intend to support.
- **Separate input and output types.** Server-generated fields (`id`, `createdAt`) never appear in create inputs.
- **Consistent naming.** Pick one case style per API (camelCase or snake_case) and keep it.

## REST specifics

- Plural nouns, no verbs: `GET /orders`, `POST /orders`, `GET /orders/{id}`, `PATCH /orders/{id}`.
- Actions that are not CRUD become sub-resources: `POST /orders/{id}/cancellation`.
- Status codes: `200` OK, `201` Created (with `Location`), `202` Accepted (async), `204` No Content, `400` malformed, `401` unauthenticated, `403` forbidden, `404` not found, `409` conflict, `412` precondition failed (stale `If-Match`), `422` validation, `429` rate limited (with `Retry-After`), `500` internal, `503` unavailable.
- Use `ETag` + `If-Match` for optimistic concurrency on updates.

### Errors

Use one error shape everywhere. RFC 9457 (Problem Details) is a good default:

```json
{
  "type": "https://api.example.com/errors/insufficient-stock",
  "title": "Insufficient stock",
  "status": 409,
  "detail": "Only 2 units of SKU 123 remain.",
  "code": "INSUFFICIENT_STOCK",
  "errors": [{ "field": "items[0].quantity", "code": "MAX_EXCEEDED" }]
}
```

Clients branch on `code`, never on `detail` text. Never return stack traces or SQL errors.

### Pagination

| Type | Request | Use when | Problem |
|---|---|---|---|
| Offset | `?limit=50&offset=100` | Small, stable sets; admin UIs needing page numbers | Slow at deep offsets; skips or repeats rows under writes |
| Cursor (keyset) | `?limit=50&cursor=eyJpZCI6...` | Feeds, large or changing sets, public APIs | No random page access |

Cursor response:

```json
{ "data": [...], "next_cursor": "eyJjcmVhdGVkX2F0IjoiMjAyNi0..." , "has_more": true }
```

Rules: cap `limit` (for example max 100); order by a unique key (`created_at, id`); make the cursor opaque (base64 of the last key); paginate every list endpoint from day one.

### Idempotency

- `GET`, `PUT`, `DELETE` are idempotent by HTTP semantics; make sure the implementation honors that.
- For `POST` that creates effects (payments, orders), accept an `Idempotency-Key` header.
- The client generates the key once per intent and reuses it on retry. A key generated per attempt is useless.
- Claim the key atomically with a unique constraint, not a check-then-insert.
- Store the request hash; the same key with a different body returns `422`.
- An in-flight duplicate gets `409` (or waits, bounded). Never run it twice.
- Keep keys longer than the longest retry path (including DLQ replays).

### Versioning

| Approach | Example | Notes |
|---|---|---|
| URL major version | `/v1/orders` | Most visible; easy routing; default for public REST |
| Header / media type | `Accept: application/vnd.example.v2+json` | Clean URLs; harder to test by hand |
| Date-based | `Api-Version: 2026-03-01` | Fine-grained evolution; needs version-transform layer |
| No versioning, additive only | - | Works for internal APIs with controlled clients |

Rules: bump the major version only for breaking changes; announce deprecation with a `Deprecation` and `Sunset` header and a date; run old and new side by side for the stated window; measure old-version traffic before removal.

## GraphQL specifics

- Nullable by default for fields that can fail independently; non-null only when guaranteed.
- Use Relay-style connections (`edges`, `pageInfo`, `first`/`after`) for lists.
- Mutations take one `input` object and return a payload with the changed object and `userErrors`.
- Prevent N+1 with DataLoader-style batching per request.
- Enforce depth and cost limits; disable introspection in production if the API is not public.
- Evolve with `@deprecated(reason: ...)`; do not version the endpoint.

## gRPC specifics

- Never renumber or reuse field numbers; mark removed ones `reserved`.
- Wrap request and response in dedicated messages (`GetOrderRequest`), even with one field, so you can add fields later.
- Use standard status codes: `INVALID_ARGUMENT`, `NOT_FOUND`, `ALREADY_EXISTS`, `FAILED_PRECONDITION`, `UNAVAILABLE` (retryable), `DEADLINE_EXCEEDED`.
- Always set deadlines on client calls; propagate them.
- Run `buf breaking` (or an equivalent) in CI against the main branch.

## API verification checklist

- [ ] Contract file exists and is linted (Spectral for OpenAPI, `graphql-schema-linter`, `buf lint`).
- [ ] Breaking-change check runs in CI (`oasdiff breaking`, GraphQL Inspector, `buf breaking`).
- [ ] Every list is paginated with a capped limit.
- [ ] One error format across all endpoints.
- [ ] Retried writes are idempotent.
- [ ] Auth requirement is stated per operation.
- [ ] Deprecation path is documented for anything being replaced.

Sources: adapted from addyosmani/agent-skills (MIT) `skills/api-and-interface-design/SKILL.md`, and general practice.
