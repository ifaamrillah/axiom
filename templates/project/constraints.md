# Quality Constraints

Numeric quality bar for this project. Each row names the check that enforces it. Rows marked *default* were proposed by Axiom and not yet chosen by the team; revisit them.

Verified: <YYYY-MM-DD> at <commit>.

| Dimension | Constraint | Check (command / CI job) | Blocks merge | Source |
|---|---|---|---|---|
| Tests | All tests pass; no new skips | `<test command>` | Yes | default |
| Coverage | Changed lines ≥ 80% covered; total does not decrease | `<coverage command>` | Yes | default |
| Types | 0 type errors; no new suppressions without reason | `<typecheck command>` | Yes | default |
| Lint | 0 errors; warnings do not increase | `<lint command>` | Yes | default |
| Security | No new high or critical dependency advisories; no secrets in diff | `<audit / secret scan>` | Yes | default |
| Accessibility | WCAG 2.2 AA for changed UI; 0 critical axe violations | `<a11y check>` | Yes (UI changes) | default |
| Web performance | LCP ≤ 2.5 s, INP ≤ 200 ms, CLS ≤ 0.1 on key pages | `<lighthouse / RUM>` | No (report) | default |
| API latency | p95 ≤ <n> ms for <endpoint> | `<load test>` | No (report) | default |
| Bundle size | ≤ <n> KB gzip per entry | `<size check>` | Yes | default |
| Docs | Public API and config changes documented | review | Yes | default |

## Rules

- A constraint without a check is a wish. Mark it `unenforced` until a check exists.
- Lowering a number requires an owner-approved decision recorded in `DECISIONS.md` or an ADR, in a change separate from the one that would fail it.
- Waivers follow the quality gate contract: reason, scope, approver, expiry.
