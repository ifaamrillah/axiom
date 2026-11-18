---
name: performance-optimization
description: >
  Make code faster or lighter by measuring first, finding the real bottleneck,
  changing one thing, and proving the gain with the same workload. Use when
  something is slow, times out, uses too much memory or CPU, or when a page or
  endpoint misses a latency target. A design trade-off with no measured slowness
  ("cache or not, weigh the options") belongs to architecture-design.
---

# Performance Optimization

## Purpose

Spend effort where time actually goes. An optimization without a before-and-after measurement on the same workload is a guess, and guesses add complexity without proof.

## The rule

```
NO OPTIMIZATION WITHOUT A BASELINE AND A COMPARABLE AFTER MEASUREMENT
```

## Inputs

The symptom or target (for example "p95 under 300 ms at 50 rps"), the workload, the environment, and any telemetry. If no target exists, ask for one or propose one before changing code.

## Procedure

1. **Define the metric.** Name one user-visible number (latency percentile, throughput, memory peak, bundle size, page LCP) and the workload that produces it.
2. **Measure a baseline.** Run the workload at least 3 times on the same machine and state the spread. Use the recipes in [profiling](references/profiling.md). Never run load against production without explicit approval.
3. **Find the bottleneck.** Profile; do not guess from reading code. Rank where time or memory goes. Check the usual causes first: N+1 queries, missing indexes, work inside loops, synchronous I/O on hot paths, unbounded result sets, large payloads, re-renders.
4. **Change one thing.** The smallest change that targets the top item. Keep behavior identical; tests must pass before and after. Before keeping it, list every input whose result could differ (missing rows, ordering, rounding, time zones, errors); any difference means the change is not done, so fix it or report it as a behavior change.
5. **Re-measure** with the same workload and environment. Report the before, the after, and the spread. A gain inside the noise is no gain.
6. **Decide.** Keep the change only if the gain is real and worth its complexity. Revert otherwise and record what was tried.
7. **Guard it** when the path is critical: a benchmark, a query-count assertion, or a budget check in CI.

## Red flags

| Thought | Answer |
|---|---|
| "This loop is obviously the slow part" | Profile. The obvious part is wrong often enough to matter. |
| "Add a cache" | First find why the call is slow. A cache adds invalidation bugs; justify it with numbers. |
| "It felt faster" | Not evidence. Show the measured numbers. |
| "One run shows 20% better" | Run it again. Report the spread. |
| "Optimize everything while I'm here" | One change per measurement, or you cannot tell which one helped. |

## Outputs and gate

A report with the metric, workload, environment, baseline, bottleneck evidence, change, after measurement, and decision. Gate: improvement claims have comparable before-and-after numbers; without them, label the change as unmeasured.

## Fallback

When measurement is impossible (no environment, no data), deliver ranked hypotheses with the evidence for each and the measurement that would confirm it. Do not claim a speedup.

## References

- [Profiling and measurement recipes](references/profiling.md): per-ecosystem tools, query counting, frontend metrics.
- For a full audit across a system, the Performance Audit workflow (`workflows/performance-audit/WORKFLOW.md` in the Axiom repository).
- For N+1 and hot-path patterns in review, [code-review](../code-review/SKILL.md).
