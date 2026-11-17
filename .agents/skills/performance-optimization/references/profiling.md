# Profiling and Measurement Recipes

Commands come from each tool's documented usage. Confirm the tool is installed and check its version before relying on flags.

## Measure a baseline

- Repeat each measurement at least 3 times; report the median and the range.
- Warm up first (JIT, caches, connection pools), then measure.
- Keep the machine, data size, and configuration fixed between before and after.
- Save the raw output to a file and quote only the summary lines in reports.

## By ecosystem

| Ecosystem | CPU profile | Memory | Micro-benchmark |
|---|---|---|---|
| Python | `python -m cProfile -o out.prof script.py`, then `python -m pstats out.prof`; `py-spy record -o flame.svg -- python script.py` | `tracemalloc` snapshots | `python -m timeit` |
| Node.js | `node --cpu-prof app.js` (open the `.cpuprofile` in DevTools) | `node --heap-prof`, heap snapshots | `benchmark` or `tinybench` package if installed |
| Go | `go test -cpuprofile cpu.out -bench .`, then `go tool pprof cpu.out` | `-memprofile mem.out` | `go test -bench . -benchmem -count 5` |
| Java/Kotlin | JDK Flight Recorder (`-XX:StartFlightRecording`) | heap dump with `jcmd <pid> GC.heap_dump` | JMH |
| PHP | Xdebug profiler or Blackfire if installed | `memory_get_peak_usage()` | PHPBench |
| Ruby | `stackprof`, `ruby-prof` | `memory_profiler` | `benchmark-ips` |

## Databases

- Run `EXPLAIN` (PostgreSQL: `EXPLAIN (ANALYZE, BUFFERS)`, MySQL: `EXPLAIN ANALYZE`) on the slow query. Look for sequential scans on large tables, row estimates far from actual, and sorts spilling to disk.
- Count queries per request in a test: Django `assertNumQueries`, Rails `ActiveSupport::Notifications`, Laravel `DB::listen`, SQLAlchemy event listeners. A count that grows with the number of items is an N+1.
- Adding an index is a schema change: follow the migration steps in `architecture-design`.

## HTTP and load

- Single endpoint latency: `curl -w "%{time_total}\n" -o /dev/null -s <url>` in a loop.
- Load: `hey`, `wrk`, `k6`, or `ab` if installed. State concurrency, duration, and payload.
- Only against local or staging environments unless the user approves otherwise.

## Frontend

- Lighthouse or the browser Performance panel for LCP, INP, CLS, and total blocking time.
- Bundle size: the build tool's analyzer (`vite build` with a visualizer plugin, `webpack-bundle-analyzer`, `next build` output).
- React re-renders: the React DevTools Profiler.

## Reading results

- Optimize the largest self-time item first; a function that is slow only because it calls something slow is not the target.
- Compare percentiles, not averages, for latency.
- If the profile is flat (no item above ~10%), the gain is in architecture (fewer calls, batching, caching with a reason), not in micro-tuning.

Sources: addyosmani/agent-skills (MIT) performance-optimization; tool documentation; general practice.
