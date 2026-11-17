---
skill: performance-optimization
fixture: evaluations/fixtures/tenant-billing
---

# Eval cases: performance-optimization

## Should trigger

- "The monthly revenue report is slow for big tenants. Speed it up."
- "monthly_revenue takes forever once a tenant has thousands of invoices"
- "Should we add a cache in front of the reports module? It feels slow."

## Should not trigger

- "monthly_revenue returns the wrong total for March, fix it" → `debugging`
- "Add a GitHub Actions workflow that runs the tests" → `ci-and-observability`
- "Review this PR before I merge" → `code-review`

## Behavior

### B1: Measure before optimizing

- Prompt: "monthly_revenue in app/reports.py is slow for tenants with many customers. Make it faster."
- Fixture: `evaluations/fixtures/tenant-billing`
- Expect: Measures or counts something before changing code (timing, query count, or profile), or states that it could not and why
- Expect: Identifies the per-row `SELECT name FROM customers` query inside the loop as an N+1
- Expect: Keeps behavior identical and runs the existing tests after the change
- Expect: Reports before and after numbers from the same workload, or labels the gain as unmeasured
- Fail if: Adds a cache or new dependency without evidence
- Fail if: Claims a speedup with no measurement
