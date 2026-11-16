# API, Interface, and Test Review

Two focused checklists. Use the API section when the diff adds or changes an HTTP endpoint, RPC, event, CLI, library export, or config key. Use the test section for every diff that adds or changes tests, and for every diff that should have.

## API and interface review

### Contract

- [ ] The change is additive, or the breaking part is versioned, announced, and has a migration path. Breaking changes include: removing or renaming a field, making an optional field required, narrowing an accepted type, changing a default, changing an error code or status, and changing ordering or pagination semantics.
- [ ] Consumers were searched (see [blast radius](blast-radius.md)): clients, other services, mobile apps that cannot be force-upgraded, analytics jobs, docs examples.
- [ ] Unknown fields are tolerated on input; output adds fields rather than reshaping them.
- [ ] Persisted or queued formats (events, cache entries, job payloads) can be read by both the old and new code during a rolling deploy.

### HTTP semantics

- [ ] Method matches behavior: `GET` and `HEAD` are safe; `PUT` and `DELETE` are idempotent; `POST` that creates or charges accepts an idempotency key.
- [ ] Status codes are specific: 400 malformed input, 401 not authenticated, 403 authenticated but not allowed, 404 not found (or hidden for authorization), 409 conflict, 422 validation, 429 rate limited, 5xx only for server faults.
- [ ] Errors have a stable machine-readable shape (for example RFC 9457 problem details) and do not leak stack traces, SQL, or internal hostnames.
- [ ] List endpoints paginate, cap page size, and define a stable sort. Cursor pagination for large or changing sets.
- [ ] Time values are ISO 8601 with offset or Unix seconds, never local time without a zone. Money carries a currency.

### Authorization and input

- [ ] Every endpoint checks who the caller is and whether they may act on this specific resource (object-level authorization). Changing an ID in the path must not expose another tenant.
- [ ] Input is validated at the boundary with a schema: types, ranges, lengths, enums, and allowed fields. Unknown fields are not mass-assigned.
- [ ] Limits exist: body size, array length, page size, rate limit, timeout.

### Library and module interfaces

- [ ] Names say what the function does and what it returns; boolean parameters that switch behavior are replaced by two functions or an options object.
- [ ] The narrowest type is accepted and the most specific type is returned.
- [ ] Errors are part of the contract: documented, typed where the language allows, and not mixed with sentinel returns.
- [ ] Nothing internal leaks through the public surface (ORM entities, driver types, mutable internal collections).
- [ ] Defaults are safe: secure by default, bounded by default.
- [ ] Semantic versioning matches the change: breaking change means a major version.

### Red flags

| Red flag | Do instead |
|---|---|
| Field renamed in place | Add the new field, deprecate the old, remove later |
| Returns 200 with `{"error": ...}` | Use a 4xx or 5xx status with an error body |
| `?include_deleted=true` or role flags trusted from the client | Derive from the authenticated principal |
| Endpoint returns the ORM entity | Map to a response DTO |
| New required config key with no default | Default it, or fail fast at startup with a clear message |

## Test review

### Do the tests prove the change?

- [ ] **Fails without the change.** Revert the production change (or invert one condition it adds), run the test, confirm it fails, then restore. A test that stays green is not testing the change. Name the missing case in the finding.
- [ ] Each acceptance criterion maps to at least one test or a stated manual check.
- [ ] Bug fixes include a regression test that reproduces the original report.
- [ ] Failure paths are tested: invalid input, permission denied, dependency down, timeout, conflict.
- [ ] Boundaries are tested: empty, one, many, exactly at the limit, one past the limit.

### Are the assertions meaningful?

| Weak | Strong |
|---|---|
| `expect(result).toBeTruthy()` | `expect(result).toEqual({ id: 7, status: "paid" })` |
| `assert response.status_code != 500` | `assert response.status_code == 201` and body checked |
| `assertNotNull(user)` | `assertEquals("ana@example.com", user.getEmail())` |
| Test only checks no exception was thrown | Test checks the observable outcome |
| `expect(mock).toHaveBeenCalled()` as the only assertion | Assert the effect, or the call with exact arguments when the call is the contract |
| Snapshot regenerated in the same diff | Snapshot change explained and each changed line reviewed |

### Are the tests trustworthy?

- [ ] Tests test behavior through the public interface, not private methods or internal call order.
- [ ] Mocks are at system boundaries (network, clock, randomness, filesystem), not of the unit under test or its close collaborators.
- [ ] No reliance on wall-clock time, random values, test order, or shared mutable fixtures. Inject a clock and seed randomness.
- [ ] No `sleep` for synchronization; wait on a condition with a timeout.
- [ ] Database tests isolate state (transaction rollback, fresh schema, or unique data per test).
- [ ] Test names state the scenario and the expectation (`rejects_refund_for_pending_order`).
- [ ] No logic in tests that mirrors the implementation (recomputing the expected value with the same formula proves nothing).
- [ ] No `.only`, `fit`, `fdescribe`, or `-k` filters left in; no new skips (see [quality constraints](../../quality-constraints/SKILL.md)).

### Coverage and level

- [ ] Changed lines are covered. A coverage drop on changed files is a finding unless the uncovered lines are declared untestable with a reason.
- [ ] The test level fits the risk: unit for logic, integration for queries and wiring, end-to-end for one critical path. A unit test with every dependency mocked does not prove a query works.
- [ ] Integration tests run against the real engine type (PostgreSQL vs SQLite differ in types, locking, and NULL ordering).

### Quick mutation check

```bash
# 1. Copy the file, flip one condition the change added, run the related tests.
cp src/billing/refund.ts /tmp/refund.ts.bak
sed -i.tmp 's/status === "paid"/status !== "paid"/' src/billing/refund.ts
npx vitest run src/billing
# 2. Restore exactly.
cp /tmp/refund.ts.bak src/billing/refund.ts && rm -f src/billing/refund.ts.tmp
```

If the suite stays green, report: "Inverting the paid-status guard in refund.ts:42 leaves all tests green; no test covers refunding an unpaid order." For a project-wide score use a mutation tool scoped to changed files (Stryker, mutmut, PIT, go-mutesting, Infection).

Sources: adapted from addyosmani/agent-skills (MIT) (`skills/code-review-and-quality`) and general practice.
