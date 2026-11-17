# Records, Ledger, and Report

Full audit artifacts live in the run directory outside the target. Only the coordinating agent writes them.

```
<output-dir>/
  run-metadata.md     target, source ref, dirty state, profile, scope, budget, status
  architecture.md     ≤ ~1,000-word summary from reconnaissance
  coverage-ledger.md  one row per unit
  findings.md         final records (confirmed, needs_validation, rejected)
  REPORT.md           derived from findings.md and the ledger
```

## Finding record

````markdown
### <fingerprint>

- Verdict: confirmed | needs_validation | rejected
- Title: <short>
- Severity: critical | high | medium | low | informational   (confirmed only)
- Likelihood / impact: <demonstrated conditions> / <demonstrated result>
- Principal → input → control → boundary → affected → result:
  <one line each>
- Root cause: <missing or flawed invariant>
- Intended behavior: <what the control should enforce>
- Trace:
  1. entrypoint — path/file.ts:12 — <what happens>
  2. propagation — path/x.ts:40 — …
  3. sink — path/db.ts:88 — …
- Evidence: <sandboxed command + exact dummy input + observed output> | static trace only
- Blocker (needs_validation): <exact missing fact> — safe owner check: <how>
- Refuting control (rejected): path:line — <why it stops the attack>
- Fix: <invariant + narrowest change at last trusted decision point>; regression test: <name>
- Units: <ledger unit IDs>
````

## Required fields by verdict

Use the record format above as the template. Each verdict requires a different subset. A record that misses a required field is not final.

| Verdict | Required | Must not have |
|---|---|---|
| `confirmed` | Title, severity, likelihood and impact, the six elements, root cause, intended behavior, trace with file:line per step, evidence (execution or validation output, or "static trace only" with the reason), exploitability score of at least 8/10, fix with regression test, units | — |
| `needs_validation` | Title, claimed root cause, trace as far as source goes, the exact unresolved fact, a safe owner check, exploitability score with the part it is missing, units | Severity |
| `rejected` | Title, the claim, why it fails: the refuting control (file:line) or the precedent and the condition checked, units | Severity |

A rejected record:

````markdown
### web/comments:CommentBody:jsx-text:xss

- Verdict: rejected
- Title: Comment body rendered in JSX
- Claim: user comment text reaches the page and could run script
- Why it fails: src/components/Comment.tsx:22 renders `{comment.body}` as JSX text, which React escapes; no raw sink on the path (precedent: framework auto-escaping)
- Units: web/comments × xss
````

## Worked examples

A confirmed record:

````markdown
### api/invoices:getInvoice:findUnique:idor

- Verdict: confirmed
- Title: Any signed-in user can read invoices of other organizations
- Severity: high
- Likelihood / impact: any authenticated user who knows or obtains an invoice ID / full read of another tenant's invoice, including line items and billing address
- Principal → input → control → boundary → affected → result:
  user of org B → `GET /api/invoices/:id` with org A's invoice ID → `requireAuth` (authentication only), no org scope → tenant isolation → org A's invoices → JSON body of org A's invoice returned
- Root cause: lookup by primary key without the session's `orgId`
- Intended behavior: invoices are readable only by members of the owning org
- Trace:
  1. entrypoint — src/routes/invoices.ts:14 — route registered with `requireAuth` only
  2. sink — src/routes/invoices.ts:16 — `prisma.invoice.findUnique({ where: { id } })`
- Evidence: local test DB, dummy orgs A and B; `supertest` as B GET /api/invoices/<A-invoice-id> → 200 with A's dummy record (test in scratch/invoice-idor.test.ts)
- Fix: `findFirst({ where: { id, orgId: req.user.orgId } })`, return 404 when absent; regression test: `invoices: member of another org gets 404`
- Units: api/invoices × tenant-isolation × IDOR
````

A needs_validation record:

````markdown
### auth/reset:buildResetLink:host-header

- Verdict: needs_validation
- Title: Password reset link may use the request Host header
- Claimed root cause: reset URL built from `request.get_host()` (accounts/views.py:88)
- Blocker: production `ALLOWED_HOSTS` comes from the `ALLOWED_HOSTS` env var, not visible in source; if it is `*` the link host is attacker-controlled
- Safe owner check: read the deployed `ALLOWED_HOSTS` value; no request to production is needed
````

A rejected record keeps the refuting control so later runs do not repeat the claim: "`/api/admin/*` has no role decorator" rejected because `src/app.ts:41` mounts the admin router behind `requireRole('admin')`.

## Severity calibration

Severity anchors live in `SKILL.md`. Calibrate with these questions, in order:

1. **Who is the attacker?** Unauthenticated > any authenticated user > user with a special role > admin. Each step down usually lowers severity one level.
2. **What exactly do they get?** Code execution, all data, one tenant's data, one record, metadata. State it in one sentence from the evidence.
3. **How many victims, and does it need their action?** Every user with no interaction > targeted user who must click > the attacker only.
4. **What conditions must hold?** Non-default config, a leaked ID, a race window, a specific browser. Each uncommon precondition lowers likelihood.
5. **What compensating controls exist in source?** CSP, rate limits, scoped tokens. Do not credit controls you cannot see.

| Pattern | Calibrated severity |
|---|---|
| Unauthenticated SQLi in login reaching the user table | Critical |
| Stored XSS in a comment field, rendered to all users, session cookie `HttpOnly`, no CSP | High |
| IDOR on invoices with UUID IDs that also appear in shared email links | High |
| Same IDOR with UUIDs that never leave the owning tenant | Medium |
| Reflected XSS on a page behind login, needs victim click, strict CSP blocks inline script | Low (or rejected if CSP fully blocks execution in a local test) |
| Missing rate limit on login, no other weakness | Hardening note, or `needs_validation` naming the edge control |
| Hardcoded test key in a test fixture, never used in production | Hardening note |

## Guidance-mode answer shape

For a focused question or diff review, keep it short:

```markdown
**Confirmed** (severity, title) — file:line trace; principal and result; smallest fix; regression test.
**Needs validation** — claim; exact missing fact; safe owner check.
**Rejected concerns** — claim; refuting control at file:line.
**Hardening notes** — one line each, no severity.
**Not checked** — what this answer does not cover.
```

## Ledger row

| Unit | Surface | Boundary | Class | State | Owner | Evidence / reason | Fingerprints |
|---|---|---|---|---|---|---|---|

Every unit ends in `covered`, `candidate` (linked to a final record), `deferred`, `blocked`, or `out_of_scope`. `planned` or `assigned` at the end of a run means the run is `incomplete`.

## Report structure

1. **Status first:** complete or incomplete (with the reason), the profile, the scope, and the source ref. A partial or `quick` run says so in the first line.
2. **Summary:** counts by verdict and severity; the most important confirmed findings in one line each.
3. **Confirmed findings,** by severity: description, trace, evidence, fix.
4. **Needs validation:** the exact missing fact and the safe owner check, without severity.
5. **Hardening notes** (not findings).
6. **Coverage statement:** units by state, deferred and blocked areas, prior runs used, and what this run does **not** establish.

## Consistency checks before finishing

- Every record has the required fields for its verdict. No `needs_validation` or `rejected` record has a severity.
- Every fingerprint in the report exists in `findings.md`, and the reverse.
- Every final record links to at least one ledger unit, and every unit is in a terminal state (or the run is marked incomplete).
- The report contains no secrets and no live-probe instructions.

Sources: adapted from cloudflare/security-audit-skill (MIT) and general practice.
