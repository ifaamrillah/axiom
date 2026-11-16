# Rollout, Rollback, and Hotfix

Use this to plan migrations and rollback, use feature flags, run a staged rollout with monitoring, and handle a hotfix. Back to [SKILL.md](../SKILL.md).

## Migration plan

Rule: every release must run safely beside the previous version. During a rolling deploy both versions serve traffic, and a rollback puts the old code on the new schema.

| Migration type | Safe in one release? | Approach |
|---|---|---|
| Add table, add nullable column, add index (concurrently) | Yes | Ship with or before the code |
| Add `NOT NULL` column | Only with a default that does not rewrite the table | Add nullable, backfill, then constrain |
| Rename column or table | No | Expand (add new), dual write, backfill, switch reads, contract later |
| Drop column or table | No | Stop all reads and writes in release N; drop in release N+1 or later |
| Change column type | No | New column plus expand and contract |
| Large backfill | Separate from deploy | Batched, idempotent, resumable job with progress logging |

Migration plan template:

```markdown
### Migration 0042_add_discount_codes
- Type: expand (additive)
- Compatible with previous app version: yes (old code ignores the table)
- Rehearsal: staging copy of prod (41 M orders) - 0.4 s, no locks > 50 ms
- Backup: automated snapshot 02:00 UTC; manual snapshot before deploy
- Run by: CI deploy job, before app rollout
- Down step: `DROP TABLE discount_codes;` (tested locally)
- Abort if: migration exceeds 60 s or lock wait > 5 s (lock_timeout set)
```

## Rollback plan

Write it before the release. Name the trigger, the method, the time, and the data consequences.

```markdown
## Rollback plan - v2.4.0

Triggers (any one):
- 5xx rate > 2x baseline for 5 min
- p95 latency > 1.5x baseline for 10 min
- Any data-integrity alert
- Payment success rate drops > 2 points

Methods, fastest first:
1. Feature flag `new-invoices` off - < 1 min, no deploy.
2. Redeploy previous image `billing:v2.3.2` - < 5 min.
   Safe because migration 0042 is additive.
3. Database restore - last resort, data loss since snapshot; needs approver.

Data created by the new version: discount_codes rows remain; harmless to
old code.
Who decides: on-call engineer can do 1 and 2; 3 needs the release approver.
Verify after rollback: health 200, error rate back to baseline, smoke test.
```

Rules:

- Prefer roll-forward-safe designs so rollback is a redeploy or a flag flip.
- If a step is irreversible (data deletion, external notifications sent, third-party state changed), say so in the plan and get explicit approval.
- Test the rollback path in staging when the release includes a migration.

## Feature flags

Use flags to separate deploy (code in production) from release (users see it).

| Flag type | Lifetime | Example |
|---|---|---|
| Release toggle | Days to weeks | New checkout flow during rollout |
| Kill switch | Long-lived | Turn off recommendations when the service degrades |
| Experiment | Length of the experiment | A/B test of pricing page |
| Permission / entitlement | Long-lived | Feature for enterprise plan only |

Rules:

- Default off for new behavior. The off path is the old, proven path.
- Every flag has an owner and a removal date. Remove release toggles within about two weeks of 100%.
- Test both states in CI.
- Do not nest flags; combinations grow fast and untested.
- Evaluate a flag once per request and pass the result down, so one request does not see both behaviors.
- Use sticky bucketing (hash of user or account ID) for percentage rollouts so users do not flip between variants.
- Flag changes are production changes: log who changed what and when.

## Staged rollout

Typical sequence (adapt to the platform and risk):

1. Deploy to staging; run smoke and E2E tests.
2. Deploy to production with the flag off; check health and error rates.
3. Enable for internal users; observe for a set window (for example 1-24 h).
4. Canary: 1-5% of traffic or users; observe 30 min to 24 h depending on traffic volume.
5. Increase: 25% -> 50% -> 100%, with the same checks at each step.
6. Full rollout; keep watching for at least one business cycle; schedule flag removal.

Go / hold / roll back thresholds (compare canary against baseline over the same window):

| Signal | Go | Hold and investigate | Roll back |
|---|---|---|---|
| Error rate (5xx, exceptions) | Within 10% of baseline | 10% to 2x baseline | Over 2x baseline |
| p95 latency | Within 20% | 20-50% higher | Over 50% higher |
| New error types | None | Rare (< 0.1% of requests) | Frequent or data-related |
| Saturation (CPU, memory, DB connections, queue age) | Normal headroom | Rising steadily | Near limits |
| Key business metric (sign-ups, payments) | Neutral or better | Down < 5% (may be noise) | Down > 5% |
| Error budget burn rate | Normal | Faster than baseline | Budget exhausted |

Make sure the canary has enough traffic for the numbers to mean something; a 1% canary on low traffic may need hours.

## What to monitor

- **Golden signals** for each changed service: latency (p50, p95, p99), traffic, errors, saturation.
- **Business signals** for the changed flow: conversion, payments succeeded, jobs processed.
- **Dependencies**: DB query latency and locks, queue depth and oldest-message age, third-party error rates.
- **Client side** (web, mobile): JS errors, crash-free sessions, Core Web Vitals.
- **Logs**: new error messages since the deploy (group by message, filter by version label).

Tag metrics and logs with the version or deploy ID so you can split canary from baseline.

First-hour check after each stage:

1. Health endpoint returns 200 on all instances.
2. Error and latency dashboards: no regression vs baseline.
3. No new error groups in the error tracker.
4. Run the key user journey once by hand or with the smoke test.
5. Logs flowing and readable for the new code paths.

## Hotfix procedure

For an urgent production defect that cannot wait for the normal release.

1. **Mitigate first.** Can a flag flip, config change, or rollback stop the harm now? Do that, with approval per the rollback plan. A hotfix is for when mitigation is not enough.
2. **Branch from the released tag**, not from main: `git switch -c hotfix/2.4.1 v2.4.0`. Main may hold unreleased work.
3. **Write a failing test** that reproduces the defect (see [debugging](../../debugging/SKILL.md)).
4. **Make the smallest fix.** No refactors, no unrelated changes, no dependency upgrades unless the fix needs one.
5. **Run the full required checks.** Urgency does not waive tests; it shrinks scope.
6. **Bump PATCH**, add a changelog entry under `Fixed` or `Security`.
7. **Review**: at least one reviewer, even if fast. Note the incident ID.
8. **Get release approval**, then release through the normal pipeline with a shortened, not skipped, staged rollout.
9. **Port the fix to main** (cherry-pick or merge the hotfix branch) so the next release does not regress.
10. **Follow up**: incident notes, root cause, and a regression test in main.

Red flags: editing code directly on a production server; hotfix branch from main with unreleased features; "skip tests, it's a one-liner"; forgetting to port the fix back.

Sources: adapted from addyosmani/agent-skills (MIT) `skills/shipping-and-launch/SKILL.md`, and general practice.
