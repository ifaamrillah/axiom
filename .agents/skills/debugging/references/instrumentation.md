# Instrumentation Recipes

Instrument to answer one question, run once, read, then remove. Each log line should carry a unique tag (for example `DBG-1234`) so you can grep for it and delete every line before completion.

## Rules

- **Log before the risky operation**, not only after it fails. A crash can swallow the "after" line.
- **Log inputs, outputs, and identity**: arguments, return value, object ID or request ID, thread/goroutine, and a timestamp with milliseconds.
- **Capture the call stack** where a bad value is first detected. That tells you who produced it.
- **Write to stderr in tests.** Test runners and logging configs often swallow stdout or debug-level logs.
- **Never log secrets or personal data.** Log presence and length (`token: set, len=40`), or a hash prefix.
- **One boundary per layer.** Log at handler, service, repository, and external-call boundaries first. Go deeper only in the layer that is wrong.
- **Remove it.** Grep for your tag before completion. Keep only logs that become intended observability.

## Python

```python
import sys, traceback, logging, pprint

# Quick probe with stack, to stderr
print(f"DBG-1234 total={total!r} items={len(items)}", file=sys.stderr)
traceback.print_stack(file=sys.stderr, limit=8)

# Structured, survives log config
log = logging.getLogger(__name__)
log.warning("DBG-1234 order=%s total=%r", order.id, total)

# Stop and inspect
breakpoint()                      # pdb; PYTHONBREAKPOINT=0 disables

# Assertion that fails loudly at the first bad state
assert total >= 0, f"DBG-1234 negative total {total!r} for {order.id}"
```

Useful flags: `pytest -s` (show prints), `pytest -x --pdb` (drop into pdb on first failure), `pytest --lf` (last failed), `python -X faulthandler` (dump stacks on segfault or hang), `PYTHONASYNCIODEBUG=1` (unawaited coroutines, slow callbacks).

## JavaScript and TypeScript

```ts
// Quick probe with stack
console.error("DBG-1234", { total, itemCount: items.length, stack: new Error().stack });

// Inspect deep objects without [Object] truncation (Node)
import { inspect } from "node:util";
console.error("DBG-1234", inspect(payload, { depth: 6, colors: false }));

// Stop and inspect
debugger;   // run with: node --inspect-brk, or vitest/jest with --inspect-brk

// Catch async failures that would otherwise vanish
process.on("unhandledRejection", (e) => { console.error("DBG-1234 unhandled", e); });
```

Useful flags: `node --trace-warnings`, `node --enable-source-maps` (TS line numbers in stacks), `NODE_DEBUG=http,net`, `DEBUG=*` for libraries using the `debug` package, `vitest run -t "name"` or `jest -t "name"` to focus one test, `jest --runInBand` to remove parallelism. In the browser: DevTools "Pause on exceptions", network tab "Preserve log", and conditional breakpoints.

## Go

```go
// Quick probe with stack
fmt.Fprintf(os.Stderr, "DBG-1234 total=%v items=%d\n", total, len(items))
debug.PrintStack() // import "runtime/debug"

// Structured
slog.Warn("DBG-1234", "order", order.ID, "total", total)

// Inside tests, attached to the test
t.Logf("DBG-1234 got=%+v", got)   // shown with -v or on failure
```

Useful flags: `go test -v -run TestName -count=1` (no cache), `go test -race`, `GOTRACEBACK=all` (all goroutine stacks on panic), `dlv test ./pkg -- -test.run TestName` (Delve debugger), `import _ "net/http/pprof"` for live goroutine and heap dumps.

## Java

```java
// Quick probe with stack
System.err.println("DBG-1234 total=" + total + " items=" + items.size());
new Throwable("DBG-1234 who called").printStackTrace();

// Structured (SLF4J)
log.warn("DBG-1234 order={} total={}", order.getId(), total);
```

Useful tools: IDE conditional breakpoints and "break on exception", `jstack <pid>` for thread dumps, `jcmd <pid> Thread.print`, JFR (`-XX:StartFlightRecording`) for timing, `-Dlogging.level.org.hibernate.SQL=DEBUG` (Spring/Hibernate SQL), Maven `-Dtest=Class#method -DtrimStackTrace=false` for full stacks in Surefire.

## PHP

```php
// Quick probe with stack
error_log('DBG-1234 total=' . var_export($total, true));
error_log('DBG-1234 ' . (new \Exception())->getTraceAsString());

// Structured (PSR-3, e.g. Monolog or Laravel's Log)
$logger->warning('DBG-1234', ['order' => $order->id, 'total' => $total]);
```

Useful tools: Xdebug step debugging (`XDEBUG_MODE=debug`), `XDEBUG_MODE=profile` for profiles, `vendor/bin/phpunit --filter testName --debug`, Laravel `DB::enableQueryLog()` / `DB::getQueryLog()`, Symfony profiler. Avoid `dd()`/`dump()` in code paths shared with other requests, and never commit them.

## Multi-component boundaries

When a value passes through several processes (CI job, build script, container, service), print the same facts at each hop, once:

```sh
echo "DBG hop=ci API_URL=${API_URL:-UNSET} TOKEN=$([ -n "${TOKEN:-}" ] && echo set || echo UNSET)"
# repeat at the build script, entrypoint, and application start
```

The first hop that prints `UNSET` or a different value is where propagation broke.

## Database and HTTP

- SQL: log the final statement and bound parameters, and run it with `EXPLAIN` (`EXPLAIN ANALYZE` in PostgreSQL, only on non-production data).
- HTTP: log method, URL without query secrets, status, latency, and a request ID. Use `curl -v` or a recording proxy to see the exact bytes.

Sources: adapted from obra/superpowers (MIT) `skills/systematic-debugging/SKILL.md`, `root-cause-tracing.md`, addyosmani/agent-skills (MIT) `skills/debugging-and-error-recovery/SKILL.md`, and general practice.
