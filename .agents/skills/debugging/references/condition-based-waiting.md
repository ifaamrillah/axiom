# Condition-Based Waiting

Fixed sleeps make tests slow and flaky: too short on a busy CI machine, wasted time on a fast one. Wait for the condition instead.

## Pattern

```text
wait_until(condition, timeout, interval):
    deadline = now + timeout
    loop:
        if condition(): return
        if now > deadline: fail with a message naming the condition and the last observed state
        sleep(interval)        # short, e.g. 10–50 ms
```

Rules:

- Wait for the **observable effect** you need (row exists, element visible, event received, port open), not for a duration.
- Always set a **timeout** and fail with a message that names the condition and the last observed value.
- **Read fresh state inside the loop.** Capturing the value before the loop makes the wait useless.
- Poll at 10–50 ms. Polling every 1 ms burns CPU and can starve the work you are waiting for.
- Prefer the framework's built-in waits: Playwright auto-waiting and `expect(...).toBeVisible()`, Testing Library `findBy*`/`waitFor`, `pytest` helpers, Awaitility for the JVM.
- For background work under your control, expose a completion signal (a future, promise, callback, or event) and await it instead of polling.

## Implementations

TypeScript:

```ts
export async function waitFor<T>(
  check: () => T | undefined | null | false,
  what: string,
  timeoutMs = 5000,
): Promise<T> {
  const start = Date.now();
  for (;;) {
    const v = check();
    if (v) return v;
    if (Date.now() - start > timeoutMs) throw new Error(`timed out after ${timeoutMs}ms waiting for ${what}`);
    await new Promise((r) => setTimeout(r, 10));
  }
}
// await waitFor(() => events.find((e) => e.type === "DONE"), "DONE event");
```

Python:

```python
def wait_for(check, what, timeout=5.0, interval=0.02):
    deadline = time.monotonic() + timeout
    last = None
    while time.monotonic() < deadline:
        last = check()
        if last:
            return last
        time.sleep(interval)
    raise AssertionError(f"timed out after {timeout}s waiting for {what}; last={last!r}")
```

Go (testify has `require.Eventually`; plain version):

```go
func waitFor(t *testing.T, what string, timeout time.Duration, check func() bool) {
    t.Helper()
    deadline := time.Now().Add(timeout)
    for !check() {
        if time.Now().After(deadline) { t.Fatalf("timed out after %s waiting for %s", timeout, what) }
        time.Sleep(20 * time.Millisecond)
    }
}
```

Java: `await().atMost(5, SECONDS).until(() -> repo.count() == 1);` (Awaitility).

PHP: loop with `usleep(20_000)` and a `microtime(true)` deadline; Laravel Dusk has `waitFor`, `waitForText`.

## Quick patterns

| Waiting for | Condition |
|---|---|
| An event | `events.find(e => e.type === "DONE")` |
| A state | `machine.state === "ready"` |
| A count | `items.length >= 5` |
| A file | `fs.existsSync(path)` |
| A port | a TCP connect to `host:port` succeeds |
| A DB row | `SELECT 1 FROM jobs WHERE id = ? AND status = 'done'` returns a row |
| UI text (Playwright) | `await expect(page.getByText("Saved")).toBeVisible()` |

## When a fixed delay is legitimate

Only when the behavior under test is itself time-based (debounce, rate limit, TTL, a ticker). Even then, prefer a fake or controllable clock (`vi.useFakeTimers()`, `freezegun`, `clock.Advance` with an injected clock). If a real delay remains:

1. First wait for the triggering condition.
2. Base the delay on known timing (for example, two ticks of a 100 ms ticker = 200 ms), not a guess.
3. Comment why.

## Diagnosing flakiness

1. Run the test in a loop (for example 50 times) to measure the failure rate before and after the change.
2. Look for shared state, ordering assumptions, real clocks, network calls, and unawaited asynchronous work.
3. A flaky test fixed by increasing a sleep is not fixed.
4. Proof of a fix: the same loop count, before N failures, after 0.

Sources: adapted from obra/superpowers (MIT) `skills/systematic-debugging/condition-based-waiting.md`, `condition-based-waiting-example.ts`, and general practice.
