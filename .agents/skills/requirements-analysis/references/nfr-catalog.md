# Non-Functional Requirements Catalog

A non-functional requirement (NFR) is only useful when it names a metric, a target, and the conditions under which it is measured. Use this catalog to pick the categories that matter for the feature and to phrase them measurably. Skip categories that do not apply. Starter numbers below are common defaults, not standards; confirm them with the owner.

## Phrasing pattern

> **NFR-###**: <metric> MUST be <comparison> <target> <unit> under <load or condition>, measured by <method> in <environment>.

Example: "**NFR-001**: Request submission latency MUST be ≤ 500 ms at p95 under 20 requests/second sustained for 10 minutes, measured by the load test in staging."

## Catalog

| Category | Weak phrasing | Measurable phrasing | How to verify |
|---|---|---|---|
| Latency | "fast" | "≤ 300 ms p95, ≤ 1 s p99 server time for `GET /orders/:id` at 50 req/s" | Load test (k6, Locust, JMeter, wrk) |
| Page performance | "loads quickly" | "LCP ≤ 2.5 s, INP ≤ 200 ms, CLS ≤ 0.1 at p75 on mid-range mobile, 4G" | Lighthouse CI, field RUM data |
| Throughput | "scalable" | "Sustain 200 orders/minute with error rate < 0.1%" | Load test |
| Capacity | "handles large data" | "Search returns in ≤ 1 s p95 with 5 million products indexed" | Seeded load test |
| Availability | "highly available" | "99.9% monthly success rate for checkout requests (≤ 43 min downtime/month)" | SLO dashboard |
| Durability and recovery | "no data loss" | "RPO ≤ 5 min, RTO ≤ 1 h; restore drill passes quarterly" | Restore drill |
| Reliability of integrations | "robust" | "Provider calls time out at 5 s, retry 3 times with exponential backoff, idempotency key per request" | Fault-injection test |
| Idempotency | "no duplicates" | "Repeating the same request ID within 24 h returns the first result and causes no second side effect" | Integration test with replay |
| Consistency | "always correct" | "Balance shown to the user reflects completed refunds within 5 s" | Integration test with clock |
| Security: authentication | "secure login" | "Sessions expire after 30 min idle; MFA required for `support_agent` role" | Test plus config review |
| Security: authorization | "only authorized users" | "A customer can read only requests where `customer_id` = their id; other ids return 404" | Negative tests per role |
| Security: input | "sanitize input" | "Free-text fields ≤ 500 chars, stored as given, HTML-escaped on render" | Test with `<script>` payloads |
| Security: secrets | "keep keys safe" | "No secret in source or logs; secrets read from the secret store at start" | Secret scanner in CI |
| Privacy | "GDPR compliant" | "Personal data in refund reasons deleted 24 months after closure; export on request within 30 days" | Retention job test, runbook |
| Auditability | "track changes" | "Every status change writes actor, before, after, timestamp, reason; entries are append-only" | Test plus DB permission review |
| Accessibility | "accessible" | "WCAG 2.2 AA: keyboard-only completion, visible focus, contrast ≥ 4.5:1 text, labels on all inputs" | axe-core in CI plus manual keyboard pass |
| Localization | "international" | "All user text from message catalogs; amounts formatted by locale; supports `en`, `id`" | Pseudo-locale test |
| Observability | "monitor it" | "Emit `refund.requested`, `refund.refunded`, `refund.failed` counters; alert if failed > 5 in 15 min" | Check metrics in staging |
| Usability | "intuitive" | "8 of 10 test users complete a refund request unaided in ≤ 2 min" | Moderated usability test |
| Compatibility | "works everywhere" | "Last 2 versions of Chrome, Firefox, Safari, Edge; iOS 17+, Android 13+" | Browser matrix in CI |
| Maintainability | "clean code" | Usually belongs in the constitution, not the spec. If needed: "New module has ≥ 80% line coverage" | Coverage report |
| Cost | "cheap to run" | "Added infra cost ≤ $200/month at current traffic" | Cost estimate, billing alert |
| Rate limiting | "prevent abuse" | "≤ 5 refund requests per customer per 24 h; excess returns 429 with retry-after" | Integration test |

## Rules

- **Percentiles, not averages,** for latency. An average hides the slow tail.
- **Name the load.** A latency target without a request rate is untestable.
- **Name the environment.** Staging numbers and production numbers differ.
- **One metric per NFR.** Split "fast and reliable" into two requirements.
- **Say what happens on breach** when it matters: alert, degrade, or block release.
- **Do not invent targets.** If nobody knows the number, write `[NEEDS CLARIFICATION: target p95 latency?]` and propose a default with the reason.
- **Business outcomes are success criteria, not NFRs.** "Support emails drop by half" goes in Success criteria. It does not need a task unless it needs buildable measurement.

## Which categories to ask about

| Feature touches | Always cover |
|---|---|
| Money or payments | Idempotency, auditability, authorization, integration reliability |
| Personal data | Privacy, retention, authorization, secrets |
| Public UI | Accessibility, page performance, localization (if multi-locale) |
| External APIs | Integration reliability, rate limiting, observability |
| Background jobs | Durability, retries, observability |
| High traffic paths | Latency, throughput, capacity |

Sources: adapted from github/spec-kit (MIT) `templates/commands/clarify.md` (non-functional categories) and general practice (Core Web Vitals thresholds, WCAG 2.2, SLO practice).
