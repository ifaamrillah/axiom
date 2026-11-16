# Fixtures, Test Data, Flaky Tests, and Suite Hygiene

Open this when building test data, when a test fails intermittently, or when cleaning up or reviewing the health of a regression suite.

## Test data: builders over shared fixtures

Each test should state only the fields that matter to it and get valid defaults for the rest.

| Approach | Use when | Risk |
|---|---|---|
| Inline literal | Small value objects | Repetition is fine if it keeps the test readable |
| Builder / factory function | Domain objects with many required fields | Defaults drift from reality; keep them valid |
| Factory library (`factory_boy`, `fishery`, FactoryBot, Laravel factories) | Persisted models with relations | Hidden cascades create many rows; keep associations explicit |
| Shared static fixture file | Large realistic payloads (recorded API responses) | Many tests depend on it; edits break unrelated tests |
| Seeded database dump | E2E or demo environments only | Slow, opaque; tests start depending on row IDs |

```python
# Python builder with explicit overrides
def make_user(**overrides):
    data = {"email": f"user{next(_seq)}@example.test", "role": "member", "active": True}
    data.update(overrides)
    return User.objects.create(**data)

def test_inactive_users_cannot_log_in():
    user = make_user(active=False)          # the one field that matters is visible
    assert login(user.email, "pw").error == "inactive"
```

```ts
// TypeScript builder
export const buildOrder = (o: Partial<Order> = {}): Order => ({
  id: crypto.randomUUID(),
  status: "pending",
  currency: "USD",
  lines: [{ sku: "SKU-1", qty: 1, unitCents: 1000 }],
  createdAt: new Date("2024-01-01T00:00:00Z"),
  ...o,
});
```

```go
// Go functional options
func newOrder(opts ...func(*Order)) Order {
	o := Order{ID: "o-1", Status: "pending", Currency: "USD"}
	for _, f := range opts { f(&o) }
	return o
}
```

Rules:

- Use unique values per test (sequence or UUID) for anything with a unique constraint. Never depend on a specific auto-increment ID.
- Use fixed dates in data (`2024-01-01T00:00:00Z`), not `now()`, unless the test is about the current time; then inject a clock.
- Prefer DAMP tests (each test readable alone) over deeply shared setup. Repetition in tests is acceptable when it makes intent visible.
- Use reserved domains for test emails and hosts (`example.test`, `example.com`) so nothing reaches a real inbox.

## Isolation strategies

| Resource | Isolation | Example |
|---|---|---|
| Relational DB | Transaction per test, rolled back | pytest-django `db` fixture, Rails transactional tests, Laravel `RefreshDatabase` |
| DB with code that commits | Truncate tables in teardown, or one schema per worker | `pytest-xdist` worker ID in DB name |
| Filesystem | Temp directory per test | `tmp_path` (pytest), `t.TempDir()` (Go), `fs.mkdtemp` (Node) |
| Environment variables | Set and restore per test | `monkeypatch.setenv`, `t.Setenv`, `vi.stubEnv` |
| Time | Fake clock | `freezegun`/`time-machine`, `vi.useFakeTimers`, injected `now func()` |
| Randomness | Seeded generator | `random.Random(42)`, `faker.seed(42)` |
| Network | Stub at HTTP layer; block real egress in unit runs | `respx`, `msw`, `pytest-socket` |
| Global singletons, module caches | Reset in teardown | `jest.resetModules()`, explicit reset function in test utils |

## Flaky test diagnosis

A flaky test passes and fails on the same code. Treat it as a real defect until proven otherwise: in a meaningful share of cases the flake is a real race in the product.

**Step 1: reproduce the rate.** Run the single test many times.

```sh
pytest tests/test_x.py::test_y --count=200 -x          # pytest-repeat
for i in $(seq 100); do npx vitest run src/x.test.ts -t "name" || break; done   # or test(..., { repeats: 100 })
for i in $(seq 100); do npx jest src/x.test.ts -t "name" --runInBand || break; done
go test ./pkg -run TestY -count=200 -race
bundle exec rspec spec/x_spec.rb:42 --seed 12345        # replay a failing seed
```

**Step 2: classify by when it fails.**

| Fails when | Likely cause | Fix |
|---|---|---|
| Run with others, passes alone | Shared state leak (order dependence) | Bisect the polluter; fix its teardown |
| Run in parallel only | Shared DB rows, ports, files, or global state | Per-worker resources; unique data |
| Under load or on slow CI | Timing assumption, fixed sleep, short timeout | Wait on a condition; inject the clock |
| Near midnight, month end, or in another time zone | Date math with real clock or local TZ | Fixed clock; set `TZ=UTC` in test runs |
| Randomly with no pattern | Unseeded randomness, unordered map or set iteration | Seed; sort before comparing |
| Only on first run after deploy or cache clear | Cold cache, lazy init, migrations | Explicit setup; warm in fixture |
| Only on one OS | Path separators, line endings, case-insensitive FS | Use path APIs; normalize |
| Network-related messages | Real external call | Stub at HTTP layer |

**Step 3: fix the cause, not the symptom.** Do not add retries, raise timeouts, or add sleeps as the fix. Retries in CI are acceptable only as a temporary, tracked mitigation with an owner and a linked issue.

**Step 4: prove the fix.** Rerun the same repeat count that reproduced it. Report the before and after failure rate (for example, "7/200 to 0/200").

For order-dependent failures, use [test-pollution bisection](../../debugging/references/test-pollution-bisection.md). For waits, use [condition-based waiting](../../debugging/references/condition-based-waiting.md).

## Quarantine policy

- Quarantine (skip with a tracked reason) only when the flake blocks unrelated work and the fix is not immediate.
- Each quarantined test has an issue link, an owner, and a date. Example: `@pytest.mark.skip(reason="flaky: #1234, owner @team-payments, 2026-11-16")`.
- Review the quarantine list on a schedule. A test quarantined for more than one or two release cycles is either fixed or deleted with a stated reason.
- Never quarantine a test that is failing consistently. That is a regression.

## Regression suite hygiene

- **Every fixed bug gets a regression test** named for the behavior, with the issue link in a comment if useful.
- **Keep the fast path fast.** Track suite time. Move slow tests into a separate tier (`-m "not slow"`, Jest projects, Go build tags `//go:build integration`) and run that tier in CI on every merge.
- **No permanent `skip`, `xit`, `.only`, `t.Skip` without a reason.** Search before merging: `grep -rnE "\.only\(|fit\(|fdescribe\(|xit\(|@skip|t\.Skip\(" tests src`.
- **Delete dead tests** that cover removed features. Do not keep them skipped.
- **Fail on warnings that hide bugs** (unhandled promise rejections, deprecation warnings in your own code): `pytest -W error::DeprecationWarning`, Node `--unhandled-rejections=strict`.
- **Run in random order** periodically to surface hidden coupling: pytest-randomly, `vitest --sequence.shuffle`, `go test -shuffle=on`, RSpec `--order random`, PHPUnit `--order-by=random`.
- **Review snapshot updates** line by line. A bulk `-u` that changes many snapshots is a review blocker.
- **Read failure output before rerunning.** A rerun that passes is not a diagnosis.

Sources: adapted from obra/superpowers (MIT) skills/systematic-debugging/condition-based-waiting.md, addyosmani/agent-skills (MIT) skills/test-driven-development/SKILL.md, and general practice.
