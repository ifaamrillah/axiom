# Symptom-to-Technique Guide

Pick the first technique from the symptom, not from a hunch. Each row names the evidence to collect first, the technique most likely to localize the cause, and the trap that wastes the most time.

## Decision table

| Symptom | Collect first | Best first technique | Common trap |
|---|---|---|---|
| Crash or uncaught exception | Full stack trace, input that triggered it, version | [Read the stack trace](reading-stack-traces.md), then [trace backward](root-cause-tracing.md) from the first frame in your code | Catching the exception at the crash site |
| Wrong value, no error | One concrete bad output and the expected one | Boundary logging; [trace backward](root-cause-tracing.md) to the first wrong value | Patching the formatter or renderer that shows it |
| Worked before, broken now | A known-good revision or version | [`git bisect run`](bisection.md#git-bisect) | Reading the whole diff by eye |
| Fails only with certain input | One failing input, one passing input | [Input bisection](bisection.md#input-bisection) to a minimal case | Special-casing that one input |
| Intermittent or flaky | Failure rate over N runs, seed, timing | Loop the test; [condition-based waiting](condition-based-waiting.md); look for shared state | Raising a timeout or adding a retry |
| Passes alone, fails in suite | Both commands and run order | [Test-pollution bisection](test-pollution-bisection.md) | Editing the victim test to tolerate the leak |
| Performance regression | Before/after timing on the same machine and data | Profile both versions; bisect on a timing threshold | Optimizing code that the profile does not show as hot |
| Memory leak or growth | Heap/RSS over time, workload that grows it | Two heap snapshots under steady load, diff the retained objects | Raising the memory limit |
| Deadlock or hang | Thread/goroutine dump while hung | Dump all stacks; find the lock or channel each one waits on | Adding timeouts around the hang |
| Only in one environment (CI, staging) | Versions, env vars, config, data, OS, locale, timezone | Diff the environments; make the local one match one variable at a time | "It's flaky in CI" |
| "Works on my machine" | Same as above, plus caches and untracked files | Clean checkout in a container or fresh clone; [dependency bisection](bisection.md#dependency-bisection) | Assuming the other machine is wrong |
| Only in production | Logs, traces, request IDs, error rate by version/host/region | Correlate by dimension; reproduce with captured input in a non-production copy | Debugging against production data or systems |
| Build or compile failure | First error in the output, not the last | Read the first error; check lockfile and toolchain versions | Fixing the 40th cascading error |
| Dependency upgrade broke it | Old and new lockfile | [Dependency bisection](bisection.md#dependency-bisection); read the changelog between versions | Pinning back without knowing why |

## Playbooks

### Crash

1. Copy the exception type, message, and the first frame that belongs to the repository.
2. Read that line and the values it uses. Ask which value could make it throw.
3. Reproduce with the same input in a test. Then trace the bad value backward.
4. A `NullPointerException`, `TypeError: Cannot read properties of undefined`, `AttributeError: 'NoneType'`, or `nil pointer dereference` is never the root cause. The cause is whoever produced the missing value.

### Wrong value

1. Write the bad value and the expected value side by side, with the exact input.
2. Log at each boundary the value crosses (handler, service, repository, serializer). Run once.
3. The first boundary whose output is wrong contains the defect. Narrow inside it with a debugger or assertions.
4. Check the usual suspects: integer vs float division, rounding, timezone and DST, locale-dependent parsing, off-by-one in ranges, string vs number comparison, mutated shared objects, stale caches.

### Intermittent

1. Measure the rate: run the test 50–200 times. Record failures, seeds, and durations.
   - `pytest -p no:randomly --count=100 tests/x.py::test_y` (needs `pytest-repeat`)
   - `go test -run TestY -count=200 -race ./pkg/...`
   - `for i in $(seq 100); do npx vitest run x.test.ts || echo FAIL $i; done`
2. Classify: timing (async not awaited, sleeps), order (shared state), environment (clock, network, filesystem), or true concurrency (data race).
3. Widen the window to make it reproducible: add load, a delay in the suspected critical section, or run with `-race`, ThreadSanitizer, or a stress tool.
4. The fix is proven when the rate goes from N% to 0 over the same number of runs.

### Performance regression

1. Fix the benchmark: same machine, same data, warm-up runs, at least 5 measured runs. Report median and spread.
2. Profile the slow version. Python `py-spy record -o out.svg -- python app.py` or `python -m cProfile -s cumtime`; Node `node --cpu-prof` or `0x`; Go `go test -bench . -cpuprofile cpu.out` then `go tool pprof`; Java async-profiler or JFR; PHP Xdebug profiler or Blackfire.
3. If a good revision exists, bisect with a threshold script (see [bisection](bisection.md#bisecting-on-a-threshold)).
4. Look for N+1 queries, missing indexes (`EXPLAIN ANALYZE`), quadratic loops, sync I/O on a hot path, cache misses, and serialization of large objects.

### Memory leak

1. Confirm growth under a steady, repeated workload. Restarts hide leaks.
2. Take a heap snapshot, run the workload N times, take another. Diff by retained size and count.
   - Node: `node --inspect`, Chrome DevTools heap snapshots, or `--heapsnapshot-signal=SIGUSR2`.
   - Python: `tracemalloc` snapshots and `compare_to`; `objgraph.show_growth()`.
   - Go: `go tool pprof http://localhost:6060/debug/pprof/heap` with `-base` for diffs.
   - Java: `jcmd <pid> GC.heap_dump`, Eclipse MAT dominator tree.
3. Typical causes: unbounded caches and maps, listeners never removed, closures holding large objects, goroutines blocked forever, static collections, connection pools not released.

### Deadlock or hang

1. Capture all stacks while it hangs. Go `kill -QUIT <pid>` or `/debug/pprof/goroutine?debug=2`; Java `jstack <pid>`; Python `py-spy dump --pid <pid>` or `faulthandler.dump_traceback_later`; Node `--inspect` then pause.
2. For each blocked thread, write what it holds and what it waits for. A cycle is a deadlock.
3. Fix lock order, shrink critical sections, or remove the blocking call inside the lock. A timeout only converts a hang into an error.
4. Database deadlocks: read the database's deadlock report (PostgreSQL log, MySQL `SHOW ENGINE INNODB STATUS`) and order row updates consistently.

### Environment-only and "works on my machine"

Diff these, one at a time, until the failure follows the change:

| Area | What to compare |
|---|---|
| Runtime | Language and toolchain versions (`node -v`, `python -V`, `go version`, `java -version`, `php -v`) |
| Dependencies | Lockfile committed and used (`npm ci`, `pip install -r` with hashes, `go mod verify`) |
| Configuration | Env vars, config files, feature flags, secrets present (names only, never values) |
| Data | Empty vs seeded database, migrations applied, fixture versions |
| OS | Case-sensitive filesystem, path separators, line endings, file permissions |
| Locale and time | `TZ`, `LANG`, `LC_ALL`, clock skew, DST dates |
| Resources | CPU count (affects concurrency), memory limits, open file limits |
| State | Caches, build artifacts, untracked files, `node_modules` from another branch |

A clean reproduction (fresh clone, container, or CI job) settles the dispute fast.

### Production-only

1. Do not attach debuggers to, or change data in, production without explicit authorization.
2. Slice the error rate by release version, host, region, tenant, client version, and time. The dimension that separates failing from healthy requests points at the cause.
3. Pull the request ID or trace for one failing request and read every log line and span for it.
4. Rebuild the input in a non-production environment (sanitized copy of the record, replayed request) and reproduce there.
5. If a release correlates, a rollback is mitigation, not a root cause. Keep investigating.

Sources: adapted from obra/superpowers (MIT) `skills/systematic-debugging/SKILL.md`, addyosmani/agent-skills (MIT) `skills/debugging-and-error-recovery/SKILL.md`, and general practice.
