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
- Prefer the framework's built-in waits: Playwright auto-waiting and `expect(...).toBeVisible()`, Testing Library `findBy*`/`waitFor`, `pytest` helpers, Awaitility for the JVM.
- For background work under your control, expose a completion signal (a future, promise, callback, or event) and await it instead of polling.

## When a fixed delay is legitimate

Only when the behavior under test is itself time-based (debounce, rate limit, TTL). Even then, prefer a fake or controllable clock. If a real delay remains, comment why.

## Diagnosing flakiness

1. Run the test in a loop (for example 50 times) to measure the failure rate before and after the change.
2. Look for shared state, ordering assumptions, real clocks, network calls, and unawaited asynchronous work.
3. A flaky test fixed by increasing a sleep is not fixed.
