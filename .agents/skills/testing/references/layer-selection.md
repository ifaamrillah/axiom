# Test Layer Selection, Coverage, and Contracts

Open this when deciding which layer a test belongs in, what to test at each layer, how to read a coverage number, or how to test an API boundary between services.

## The pyramid as a budget

Most tests should be small and fast; few should be slow and broad. A common starting budget is about 70-80 percent unit, 15-25 percent integration, and under 5-10 percent end-to-end, by count. The exact ratio matters less than the direction: push each check to the lowest layer that can catch the bug.

| Layer | Scope | Typical speed | Real dependencies | Catches | Misses |
|---|---|---|---|---|---|
| Unit | One function, class, or module | < 10 ms | None (pure) or in-memory fakes | Logic, branches, boundaries, error mapping | Wiring, SQL, serialization, config |
| Component | One UI component or one service with in-process fakes | 10-200 ms | DOM emulation, in-memory stores | Rendering rules, event handling, state transitions | Real browser layout, network |
| Integration | Your code plus one real dependency (DB, cache, queue, filesystem) | 100 ms - 2 s | Disposable DB/container | Queries, transactions, migrations, ORM mapping, serialization | Cross-service agreement |
| API | HTTP or RPC surface of one service, in process or on localhost | 50-500 ms | Test DB, stubbed third parties | Status codes, auth, validation, response shape | UI behavior |
| Contract | Agreement between consumer and provider | Seconds | Neither side's full stack | Breaking schema or field changes between teams | Business logic |
| End-to-end | Full user journey through deployed stack | Seconds to minutes | Everything | Integration of all parts on critical paths | Fine-grained branches (too slow to enumerate) |

Resource model (useful when the CI time budget matters): small tests are single-process with no I/O; medium tests may use localhost services; large tests may cross machines. Keep small tests the majority.

## Choose the layer

```
Is the behavior pure computation (input -> output, no I/O)?          -> unit
Does it depend on a query, transaction, file, or message format?     -> integration with the real dependency
Is it the request/response contract of an endpoint (status, auth)?   -> API test
Do two separately deployed services depend on a shared shape?        -> contract test
Is it a critical user journey, or a UI fix needing rendered proof?   -> end-to-end (see e2e-testing)
Is it how a component renders and reacts to events?                  -> component test
```

Red flags:

| You see | Problem | Do instead |
|---|---|---|
| Ten E2E tests for each validation rule | Slow, flaky, redundant | One E2E happy path; unit-test the rules |
| Unit test with a mocked DB asserting SQL text | Tests the mock, misses real query bugs | Integration test against a real test DB |
| Integration test for a pure date formatter | Slow for no gain | Unit test |
| Only mocked HTTP in a client with no contract check | Provider can change shape silently | Add a contract or schema test |

## What to test per layer

**Unit**

- Each branch and each error path.
- Boundaries: 0, 1, many; min, max, max+1; empty string, whitespace, Unicode; null/None/nil; negative numbers; exact thresholds.
- Rounding, time zones, and date edges (month end, leap day, DST change) when the code touches them.
- Derived values and normalization (trim, case, defaults).

**Integration**

- Each new or changed query returns the right rows, including filters, sort, and pagination edges (first page, last page, empty page).
- Transactions roll back on failure (use the real DB; a mocked `rollback()` call proves nothing).
- Unique and foreign-key constraints fire as the code expects.
- Migrations apply to an empty DB and to a DB with representative data.
- Serialization round-trips (write then read gives the same object).

**API**

- Success status and response body shape.
- Validation failure: 400 or 422 with a machine-readable error code and the failing field.
- Authentication missing: 401. Authenticated but not allowed: 403. Another tenant's resource: 404 or 403, never the data.
- Not found: 404. Conflict or duplicate: 409. Idempotent retries of PUT/DELETE behave the same.
- Pagination limits and maximum page size are enforced.
- Headers that are part of the contract (`Content-Type`, `Location` on 201, cache headers).

**Contract**

- Consumer-driven: the consumer records the requests it sends and the fields it reads (Pact). The provider verifies those recordings in its own CI.
- Schema-driven: validate real responses against the OpenAPI or JSON Schema document (`schemathesis`, `openapi-response-validator`, `kin-openapi`). Fail CI on breaking changes (`oasdiff breaking old.yaml new.yaml`).
- Test additive changes as safe and removals or type changes as breaking.

**End-to-end**

- Login, the main money or data path, and anything a past incident broke.
- Not every form permutation; those belong in unit or component tests.

## Coverage: what the number means

| Metric | Measures | Limit |
|---|---|---|
| Line | Lines executed at least once | A line can run without any assertion checking its effect |
| Branch | Each side of each condition taken | Better signal; still says nothing about assertions |
| Function | Functions called | Weakest |
| Mutation score | Share of injected bugs that some test kills | Best signal of test strength; slow to run |

Rules of thumb:

- Coverage shows what is **not** tested. High coverage does not show what **is** well tested.
- Aim coverage effort at changed code (diff coverage) and at risky modules, not at a global percentage. A useful gate is "new or changed lines are covered at 80 percent or more, with branches," not "repo total above 90."
- Never write assertion-free tests to raise the number. Coverage gained by executing code without checking results is negative value; it hides gaps.
- Exclude generated code, vendored code, and trivial glue explicitly in the coverage config. Do not exclude hard-to-test code just because it is hard.
- Use mutation testing on critical logic: `mutmut` (Python), Stryker (JS/TS, C#), `go-mutesting` or `gremlins` (Go), PIT (JVM), Infection (PHP). Inspect survivors: each is a missing assertion or a redundant line.

Coverage commands:

```sh
pytest --cov=src --cov-branch --cov-report=term-missing
npx vitest run --coverage          # needs @vitest/coverage-v8
npx jest --coverage
go test ./... -coverprofile=cover.out && go tool cover -func=cover.out
./gradlew test jacocoTestReport    # JaCoCo
XDEBUG_MODE=coverage vendor/bin/phpunit --coverage-text
COVERAGE=true bundle exec rspec    # with simplecov configured in spec_helper
```

## Contract and API testing examples

```ts
// API test with Supertest (Express/Fastify/Nest in process)
it("returns 403 when a member edits another team's project", async () => {
  const project = await createProject({ teamId: teamB.id });
  await request(app)
    .patch(`/api/projects/${project.id}`)
    .set("Authorization", `Bearer ${tokenFor(memberOfTeamA)}`)
    .send({ name: "x" })
    .expect(403);
  expect((await getProject(project.id)).name).not.toBe("x");   // no side effect
});
```

```python
# FastAPI / Starlette TestClient
def test_create_task_rejects_empty_title(client, auth_headers):
    r = client.post("/tasks", json={"title": ""}, headers=auth_headers)
    assert r.status_code == 422
    assert r.json()["detail"][0]["loc"] == ["body", "title"]
```

```go
// net/http/httptest
func TestGetTask_NotFound(t *testing.T) {
	srv := httptest.NewServer(NewRouter(newFakeStore()))
	defer srv.Close()
	res, err := http.Get(srv.URL + "/tasks/missing")
	if err != nil { t.Fatal(err) }
	if res.StatusCode != http.StatusNotFound {
		t.Fatalf("status = %d, want 404", res.StatusCode)
	}
}
```

Always assert the absence of side effects on denied or failed requests. A 403 that still wrote the row is a security bug.

Sources: adapted from addyosmani/agent-skills (MIT) skills/test-driven-development/SKILL.md and references/testing-patterns.md, and general practice.
