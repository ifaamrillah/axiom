# Testing Anti-Patterns Catalog

Open this when you write a mock, a test helper, or a cleanup method, when a test passed on its first run, or when reviewing tests someone else wrote. Each entry names the failure, shows a bad and a good version, and gives the check that catches it.

## The two questions

Ask both before writing any test body:

1. **Which realistic production bug makes this test fail?** If you cannot name one, the test protects nothing.
2. **Does the test run the real code path?** If a double replaces the thing you claim to test, the test checks the double.

## 1. Mocking the unit under test

The test replaces part of the code it claims to verify, so it passes regardless of that code.

```ts
// Bad: spies on and stubs the method being tested
const svc = new InvoiceService(repo);
vi.spyOn(svc, "computeTotal").mockReturnValue(100);
expect(svc.computeTotal(items)).toBe(100);

// Good: run the real method with real inputs
const svc = new InvoiceService(repo);
expect(svc.computeTotal([{ qty: 2, unit: 50 }])).toBe(100);
```

Check: delete the production method body. Does the test still pass? Then it tests the mock.

## 2. Asserting on the mock instead of the behavior

```tsx
// Bad: proves the mock rendered, not the component
vi.mock("./Sidebar", () => ({ Sidebar: () => <div data-testid="sidebar-mock" /> }));
render(<Layout />);
expect(screen.getByTestId("sidebar-mock")).toBeInTheDocument();

// Good: assert what the user sees from the real component
render(<Layout />);
expect(screen.getByRole("navigation", { name: /main/i })).toBeVisible();
```

Check: any assertion that targets a `*-mock` ID, or that fails only when the mock is removed.

## 3. Testing implementation details

The test locks in how the code works, so it breaks on safe refactors and misses real bugs.

```python
# Bad: asserts the SQL text and call order
repo.list_tasks(sort="created_at")
db.execute.assert_called_once_with("SELECT * FROM tasks ORDER BY created_at DESC")

# Good: asserts the observable result against a real test database
make_task(title="old", created_at=datetime(2024, 1, 1))
make_task(title="new", created_at=datetime(2024, 6, 1))
assert [t.title for t in repo.list_tasks(sort="created_at")] == ["new", "old"]
```

Other forms: reading private fields (`obj._cache`), asserting the number of internal helper calls, snapshotting a whole component tree.

## 4. Test-only methods in production code

```python
# Bad: production class grows a method only tests call
class ConnectionPool:
    def reset_for_tests(self):
        self._conns.clear()

# Good: the test owns the lifecycle through a fixture
@pytest.fixture
def pool():
    p = ConnectionPool(size=2)
    yield p
    p.close()          # real production method
```

Check: `grep -rn "reset_for_tests\|_for_testing" src/`. A method called only from test files belongs in test utilities.

## 5. Incomplete mocks

A partial fake returns only the fields the current test reads. Downstream code reads another field, and the test still passes while production breaks.

```ts
// Bad: real API also returns `currency` and `status`
fetchMock.mockResolvedValue({ amount: 1200 });

// Good: mirror the documented shape; build it from one factory
const payment = buildPayment({ amount: 1200 });   // fills currency, status, id, createdAt
fetchMock.mockResolvedValue(payment);
```

Check: compare the fake against the real schema, a recorded response, or the provider contract.

## 6. Mocking at the wrong level

The mock swallows a side effect the test depends on.

```ts
// Bad: mocking the whole catalog also drops the config write that dedup reads
vi.mock("./toolCatalog", () => ({ discoverAndCache: vi.fn() }));

// Good: mock only the slow, external piece below it
vi.mock("./serverLauncher");   // process spawn is slow; the config write stays real
```

Rule: list the real method's side effects before you replace it. Mock the slowest or most external layer that does not carry the behavior under test.

## 7. Mirror assertions (expected value computed by the code under test)

```go
// Bad: both sides use the same function, so the test is always true
want := BuildQuery(Filter{Tag: "urgent"})
if got := BuildQuery(Filter{Tag: "urgent"}); got != want { t.Fatal() }

// Good: a literal derived by hand
if got := BuildQuery(Filter{Tag: "urgent"}); got != `tag:"urgent"` {
	t.Fatalf("got %q", got)
}
```

## 8. Change detectors

The test fails only when someone makes a deliberate decision, never when a bug appears.

| Bad | Good |
|---|---|
| `expect(MAX_RETRIES).toBe(5)` | A failing call is retried 5 times, and no sixth attempt happens |
| Exact full error message string | Error type or code, plus the key field (`field == "email"`) |
| Snapshot of a 400-line component | Assertions on the 2-3 values the behavior depends on |
| Grep that a config file contains a line | Load the config and assert the effective setting |

## 9. Tests that cannot fail

```python
# Bad: no assertion; exceptions are swallowed
def test_import_runs():
    try:
        import_csv("fixtures/orders.csv")
    except Exception:
        pass

# Bad: async assertion never awaited (Jest/Vitest)
it("rejects bad input", () => {
  expect(save({})).rejects.toThrow();   // missing await -> always passes
});

# Good
def test_import_creates_one_order_per_row():
    import_csv("fixtures/orders.csv")
    assert Order.objects.count() == 3
```

Also: `assert result` when `result` is always truthy, `toBeDefined()` on a value that is never undefined, loops over an empty list.

## 10. Testing the framework or library

Asserting that the router calls a registered handler, or that the ORM saves a field, tests someone else's code. Test your boundary instead: the route you registered returns the right status, or the query you build returns the right rows.

## 11. Shared mutable state and order dependence

```python
# Bad: module-level list survives between tests
USERS = []
def test_add(): USERS.append("a"); assert len(USERS) == 1
def test_add_again(): USERS.append("b"); assert len(USERS) == 1   # fails when run after test_add

# Good: fresh state per test via fixture
@pytest.fixture
def users(): return []
```

Check: run the suite in random order (`pytest -p randomly` with pytest-randomly installed, `vitest --sequence.shuffle`, `go test -shuffle=on`). For an existing order-dependent failure, bisect the polluter with [test-pollution bisection](../../debugging/references/test-pollution-bisection.md).

## 12. Sleeping instead of waiting

`time.sleep(2)` or `setTimeout(r, 500)` is both slow and flaky. Wait on the condition the test needs (see [condition-based waiting](../../debugging/references/condition-based-waiting.md)). Use fake clocks for timers.

## 13. Weakening the test to get green

Red flags in a diff: an assertion changed from `toBe(3)` to `toBeGreaterThan(0)`, `skip`, `xfail`, `.only` left behind, a deleted test, a raised timeout with no root cause, or `expect.anything()` replacing a specific value. Each needs a stated reason; most need reverting.

## Mutation check before you finish

Mentally (or actually) apply each mutation. At least one test should fail for each:

- Change a constant or comparison (`>=` to `>`, `5` to `4`).
- Return the empty or default value (`[]`, `0`, `nil`, `None`).
- Remove a side effect (the save, the event, the log line the contract promises).
- Swap two branches (success handler on the error path).
- Skip validation for empty, zero, null, unauthorized, or malformed input.

A mutation that nothing catches marks unprotected behavior.

## Red flag to action table

| You notice | Do instead |
|---|---|
| Mock setup is longer than the test | Use a fake or a real integration test |
| You cannot explain why a mock is needed | Remove it and run against the real collaborator |
| Expected value comes from a helper or loop | Replace it with a literal |
| Test fails on every intentional change | Assert the behavior that depends on the decision |
| A method is only called from tests | Move it to test utilities |
| Test needs `sleep` | Wait on a condition or inject a clock |
| Test passed on its first run | Mutate production code and watch it fail |

Sources: adapted from obra/superpowers (MIT) skills/test-driven-development/writing-good-tests.md and skills/test-driven-development/SKILL.md, addyosmani/agent-skills (MIT) references/testing-patterns.md and skills/test-driven-development/SKILL.md, and general practice.
