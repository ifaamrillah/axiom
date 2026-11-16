# TDD in Hard Places

Open this when the code under change is legacy (untested, tangled), a user interface, asynchronous or time-based, or talks to an external service. Each section gives the seam to test through and the order of moves.

## Legacy code without tests

Goal: get a safety net around the area you will change, then change it test-first. Do not try to test the whole module.

1. **Find the change point.** Name the function or class that must change.
2. **Find a test point.** Pick the nearest place where you can observe the effect: a return value, a written file, a database row, an HTTP response.
3. **Break dependencies at a seam** so the code runs in a test:

| Obstacle | Seam | Example |
|---|---|---|
| Hard-coded `new Client()` inside a method | Parameter or constructor injection with the old default | `def sync(client=None): client = client or ApiClient()` |
| Calls `datetime.now()` / `Date.now()` / `time.Now()` | Inject a clock | `func NewBiller(now func() time.Time)` |
| Static or global singleton | Wrap in an interface; pass it in | `type Mailer interface { Send(Msg) error }` |
| Giant method | Extract the pure calculation, test it directly | Move the pricing math out of the controller |
| Reads env or files at import time | Move the read into a function called at startup | `load_settings()` instead of module-level `SETTINGS = ...` |

4. **Write characterization tests** that record what the code does today, even if it looks wrong. Use real recorded inputs. Name questionable behavior explicitly: `test_rounds_half_down_currently`.
5. **Prove each characterization test can fail.** Mutate the production line it covers, watch it fail, restore. Confirm with `git diff` that only test files changed.
6. **Now do normal TDD** for the new behavior: red, green, refactor.
7. **If you find a bug while characterizing**, do not fix it silently. Record it, and either fix it in its own red-green cycle or report it.

Approval (golden master) tests help for large outputs such as reports or rendered HTML. Store the approved output in a file, compare on each run, and review every diff by hand. Do not auto-approve a changed golden file to get green.

## UI components

Test behavior the user can observe: text, roles, enabled or disabled state, what happens after an event. Do not assert component state, hook calls, or CSS class names unless the class is the contract.

```tsx
// Red: React Testing Library + Vitest/Jest
it("disables Save until the title is non-empty", async () => {
  const user = userEvent.setup();
  render(<TaskForm onSave={vi.fn()} />);
  const save = screen.getByRole("button", { name: /save/i });
  expect(save).toBeDisabled();
  await user.type(screen.getByRole("textbox", { name: /title/i }), "Buy milk");
  expect(save).toBeEnabled();
});

it("calls onSave with the trimmed title", async () => {
  const user = userEvent.setup();
  const onSave = vi.fn();
  render(<TaskForm onSave={onSave} />);
  await user.type(screen.getByRole("textbox", { name: /title/i }), "  Buy milk  ");
  await user.click(screen.getByRole("button", { name: /save/i }));
  expect(onSave).toHaveBeenCalledWith({ title: "Buy milk" });
});
```

Notes:

- Query priority: role with name, then label, then placeholder or text, then test ID. Same order as the E2E locator table in [Playwright patterns](../../e2e-testing/references/playwright-patterns.md).
- `onSave` is a callback prop, which is the component's public output. Asserting it is a behavior check, not a mock-the-unit smell.
- Pure layout and visual polish are hard to TDD. Pull logic (formatting, validation, derived state) into plain functions and TDD those. Verify visuals with screenshots through the E2E or UI review path.
- Use `findBy*` or `waitFor` for async UI updates. Never add sleeps.

## Async code, timers, and concurrency

1. **Await everything.** A missing `await` or unreturned promise makes the test pass before the assertion runs.
2. **Control time.** Inject a clock or use the framework's fake timers instead of waiting for real time.

```ts
it("retries once after 1s on 503", async () => {
  vi.useFakeTimers();
  const fetcher = vi.fn()
    .mockResolvedValueOnce({ status: 503 })
    .mockResolvedValueOnce({ status: 200, body: "ok" });
  const p = getWithRetry(fetcher, "/x");
  await vi.advanceTimersByTimeAsync(1000);
  await expect(p).resolves.toEqual({ status: 200, body: "ok" });
  expect(fetcher).toHaveBeenCalledTimes(2);   // call count is the contract here
  vi.useRealTimers();
});
```

```python
# pytest-asyncio
@pytest.mark.asyncio
async def test_worker_marks_job_done(queue, worker):
    await queue.put(Job(id=1))
    await asyncio.wait_for(worker.drain(), timeout=2)
    assert (await queue.status(1)) == "done"
```

```go
// Go: wait on a channel with a deadline, never time.Sleep
select {
case got := <-results:
	if got != want { t.Fatalf("got %v want %v", got, want) }
case <-time.After(2 * time.Second):
	t.Fatal("timed out waiting for result")
}
```

3. **Wait on conditions** when real concurrency is involved. Poll for the observable state with a timeout; see [condition-based waiting](../../debugging/references/condition-based-waiting.md).
4. **Run race detectors** where they exist: `go test -race`, ThreadSanitizer builds. Run a suspected flaky async test 50-100 times (`go test -count=100`, `pytest --count=100` with pytest-repeat) before calling it fixed.

## External services (HTTP APIs, payment, email, queues)

Do not call real third-party services from unit tests. Pick the double by what the test needs:

| Need | Use | Tools |
|---|---|---|
| Your logic, given a response | Fake client behind your own interface | Hand-written fake class |
| Your HTTP request and parsing | HTTP-level stub | `responses` / `respx` (Python), `msw` / `nock` (JS), `httptest.Server` (Go), WireMock (JVM) |
| Real response shapes | Recorded fixtures | `vcrpy`, Polly.js, go-vcr; scrub secrets from recordings |
| Agreement with the provider | Contract test | Pact, or schema validation against the provider's OpenAPI |
| Real database or broker | Disposable container | Testcontainers, `docker compose` service in CI |

Order of moves:

1. Define a narrow interface you own (`PaymentGateway.charge(amount, token) -> ChargeResult`).
2. TDD your logic against a fake that implements that interface, including failure modes: timeout, 4xx, 5xx, malformed body, duplicate delivery.
3. Write a small number of adapter tests that hit an HTTP stub to prove request shape and parsing.
4. Keep one opt-in integration test against the provider's sandbox, marked so it does not run by default (`@pytest.mark.external`, `test.skipIf(!process.env.STRIPE_TEST_KEY)`). Never run against production accounts.

```python
# Fake that records calls and can be told to fail
class FakeGateway:
    def __init__(self, fail_with=None):
        self.charges, self.fail_with = [], fail_with
    def charge(self, amount, token):
        if self.fail_with:
            raise self.fail_with
        self.charges.append((amount, token))
        return ChargeResult(id=f"ch_{len(self.charges)}", status="succeeded")

def test_order_is_marked_unpaid_when_gateway_times_out():
    orders = OrderService(gateway=FakeGateway(fail_with=GatewayTimeout()))
    order = orders.checkout(cart_with_total(5000))
    assert order.status == "payment_pending"
```

## When TDD truly does not fit

| Situation | Substitute evidence |
|---|---|
| Exploratory spike | Throw the spike away; restart with TDD on the chosen design |
| Generated code | Test the generator's input contract, or one smoke test of the output |
| Pure configuration change | Load the config in a test or run the app and check the effective value |
| No runnable harness | State the gap; propose the smallest harness; verify manually with recorded steps |

Sources: adapted from obra/superpowers (MIT) skills/test-driven-development/SKILL.md and skills/systematic-debugging/condition-based-waiting.md, addyosmani/agent-skills (MIT) skills/test-driven-development/SKILL.md and references/testing-patterns.md, and general practice.
