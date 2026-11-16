# Runbooks

A runbook tells a tired on-call engineer how to recognize a problem, make it safe, and recover. Write for someone who did not build the system and has five minutes.

## When to write one

- A service has an alert that pages someone.
- Recovery needs a manual step (restart, failover, replay a queue, rotate a key).
- A scheduled job can fail in a way that needs human action.
- An incident review found that responders had to search for steps.

## Template

```markdown
---
status: active
sources: [deploy/k8s/orders.yaml, src/orders/worker.ts, alerts/orders.yml]
verified_at_commit: <sha>
verified_on: <YYYY-MM-DD>
owner: orders team (#orders-oncall)
---

# Runbook: Orders queue backlog

## Symptoms
- Alert `OrdersQueueLag` fires: lag > 5,000 messages for 10 min (alerts/orders.yml:14).
- Customers report orders stuck in "pending".

## Impact
Orders are accepted but not charged or confirmed. No data loss: messages persist 7 days.

## Check first (read-only)
1. Worker pods: `kubectl -n orders get pods -l app=orders-worker`
   Expected: 4/4 Running.
2. Lag: `kubectl -n orders exec deploy/orders-worker -- node scripts/lag.js`
   Expected: lag falling after a restart.
3. Errors: logs query `service=orders-worker level=error` (last 15 min).

## Mitigate
| Cause seen | Action | Risk |
|---|---|---|
| Pods CrashLoopBackOff after a deploy | Roll back: `kubectl -n orders rollout undo deploy/orders-worker` | Low; previous image |
| Payment provider 5xx | Wait; workers retry with backoff. Post status update | None |
| Poison message (same ID failing) | Move it to DLQ: `node scripts/dlq-move.js <id>` | Needs approval from orders lead |

## Verify recovery
Lag below 500 and falling for 10 min; "pending" orders older than 15 min count = 0
(query in dashboards/orders.json).

## Escalate
After 30 min without falling lag: page orders lead, then payments on-call.

## Do not
- Do not purge the queue. Purged orders are lost.
- Do not scale workers above 12: the payment provider rate-limits at 50 rps.

## History
- 2026-10-02: poison message from malformed coupon (INC-311).
```

## Rules

- Put read-only checks before any action. Mark each action with its risk and who may approve it.
- Every command is copy-pasteable, with namespace, context, and expected output.
- Give thresholds and numbers, not "if lag is high".
- Include the "do not" list. Most incident damage comes from a reasonable-looking wrong action.
- Link the alert definition and dashboard by path or name. Keep credentials out; name the secret store entry instead.
- Verify the runbook: run the read-only checks against a non-production environment, or mark which steps are unverified.
- Update after every incident that used it. Stale runbooks are marked `status: stale`, not left as current.

## Red flags

| Red flag | Do instead |
|---|---|
| "Restart the service" with no command | Exact command with namespace and expected output |
| Destructive step with no warning | Risk column and approval requirement |
| Steps that need knowledge of the code | Translate to symptoms and commands |
| No way to tell recovery happened | A measurable "verify recovery" check |

Sources: general practice.
