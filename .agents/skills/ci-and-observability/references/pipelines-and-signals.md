# Pipelines and Signals

## GitHub Actions skeleton

```yaml
name: ci
on:
  pull_request:
  push:
    branches: [main]
permissions:
  contents: read
concurrency:
  group: ci-${{ github.ref }}
  cancel-in-progress: true
jobs:
  check:
    runs-on: ubuntu-latest
    timeout-minutes: 15
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-node@v4
        with:
          node-version-file: .nvmrc
          cache: npm
      - run: npm ci
      - run: npm run lint
      - run: npm run typecheck
      - run: npm test -- --ci
      - run: npm run build
```

Adapt the setup step and commands to the stack; take commands from the project's manifest, not from this example. Pin third-party actions to a commit SHA when the project's security policy requires it.

## Faster and more reliable CI

| Problem | Fix |
|---|---|
| Slow installs | Cache by lockfile hash; use the lockfile install command |
| Slow test job | Split by package or shard tests; run only affected packages when the tool supports it |
| Redundant runs | `concurrency` with `cancel-in-progress` for the same branch |
| Flaky test | Quarantine with an owner and a ticket, never a silent retry; triage with the `testing` skill |
| Jobs hang | `timeout-minutes` on every job |
| "Works locally" | Same tool versions in CI (`.nvmrc`, `.python-version`, `go.mod` toolchain) |

## Logging

```python
log.info("payment.captured", extra={"order_id": order.id, "amount_cents": amount, "request_id": rid})
```

- Event names are stable and searchable (`payment.captured`, not "Payment done!").
- Levels: error = needs action; warn = degraded but handled; info = business events; debug = off in production.
- Log the outcome once at the boundary, not at every layer.

## Metrics

| Path type | Signals |
|---|---|
| Request or job | Rate, errors, duration percentiles (RED) |
| Resource (DB pool, queue, disk) | Utilization, saturation, errors (USE) |
| Business | Counts that product owners watch (orders placed, signups) |

Name metrics with units (`http_request_duration_seconds`). Labels: route template, status class, method. Never raw paths, user IDs, or emails.

## Alerts

- Alert on symptoms (error rate above budget, latency p95 above target for N minutes), not on causes like CPU alone.
- Each alert names its threshold, window, owner, and runbook.
- An alert nobody acts on is noise: delete or tune it.

Sources: addyosmani/agent-skills (MIT) ci-cd-and-automation and observability-and-instrumentation; platform documentation; general practice (RED and USE methods).
