# Hunting and Validation

Use this file in both modes. Guidance mode uses the hunting method and the validation techniques directly; a full audit also uses the briefs, critic, and consolidation rules.

## Hunting method

Work from a concrete invariant, not from a checklist:

1. Name the lower-trust principal and what it can do by design.
2. Name the value, action, state transition, or resource selector it controls.
3. Find the control that should reject, bind, isolate, limit, or revoke it (file:line).
4. Trace the path **after** that control to the sink. Read the whole handler, the data layer, and framework defaults.
5. Stop at the smallest effect on a dummy record, wrong return value, or local marker.
6. State the source change and regression test that would enforce the invariant.

Stop a line of investigation as soon as the invariant is settled either way, and record the outcome.

### Read sideways, not only forward

The effective control is the weakest of all parallel paths to the same effect. For each sensitive operation, list:

- sibling routes (v1 and v2, web and mobile API, GraphQL and REST, admin and user);
- batch, bulk, export, import, and sync variants;
- background jobs, retries, webhooks, and queue consumers that perform the same write;
- legacy, compatibility, migration, and feature-flagged paths;
- error, timeout, and fallback branches (`catch` blocks that allow).

Compare the controls for **equivalence**, not just presence. A role check on one path and an owner check on another are different controls.

### Sad paths to try at each handoff

Absent, empty, `null`, zero, negative, maximum, over-limit, duplicate keys, arrays where scalars are expected, objects where strings are expected, mixed or double encoding, Unicode normalization variants, case variants, trailing slashes or dots, stale or revoked tokens, reordered steps, concurrent requests, partially migrated records, and a failed dependency. Try only shapes the interface accepts.

### Variant search

When a candidate looks high or critical, search the assigned scope for the same root cause in other places: the same helper misused elsewhere, the same pattern copy-pasted, and the same missing check on sibling resources. Report one fingerprint per root cause and list every affected entry point.

### Source-to-sink or sink-to-source

- **Sink-first** (grep the class reference's sink list, then trace backward) is fastest for injection, deserialization, SSRF, and file handling.
- **Source-first** (start at each entry point and follow input forward) is better for authorization, business logic, and multi-step flows.
- For authorization, start from the **data layer**: list every query on a tenant-scoped table and check each for the tenant predicate.

## Validation techniques that cause no harm

Validation proves the minimum boundary violation with dummy data. Choose the narrowest check that settles the claim.

| Claim | Preferred evidence | Never |
|---|---|---|
| Injection | Unit test on the query builder showing generated SQL; local SQLite/test DB with dummy rows and a boolean-difference input | Destructive statements, time-based payloads on shared DBs, exfiltration |
| Command / template / deserialization RCE | Marker effect inside scratch (`touch $SCRATCH/marker`, `{{7*191}}` → `1337`) | Reverse shells, outbound callbacks, persistence |
| IDOR / tenant isolation | Two dummy users in two dummy tenants on a local instance; B reads or writes A's record | Real accounts, production IDs |
| Authentication bypass | Local request without credentials, or a forged token verified by the target's own function in a test | Brute force against deployments |
| SSRF | Validator unit test with bypass inputs; local loopback canary listener | Real metadata endpoints, internal hosts, third-party URLs |
| XSS | Rendered output in a component/view test; a flag set by the payload in a local headless browser | Payloads that send data anywhere |
| CSRF / CORS | Local second origin submitting to the local app; inspecting response headers locally | Testing against real user sessions |
| Race condition | Deterministic two-task harness or an injected pause between check and write, local DB | Flooding shared services |
| Secrets | File, line, type, redacted prefix, and who can read the file | Calling the provider to test the key |
| Dependency CVE | Local test driving the vulnerable API through the app's call path | Publishing packages, opening PRs on real repos |

If the sandbox controls in `SKILL.md` cannot be enforced, keep the candidate as `needs_validation` with "execution sandbox unavailable" as the blocker and a precise owner-run plan.

## Candidate gate (apply before reporting anything)

1. A complete source trace exists, and the strongest source-visible control on the path has been read.
2. For `confirmed`: a bounded local observation, a named boundary, and no visible preventing layer.
3. Do not upgrade the result: a crash is not code execution, slow is not denial of service for others, and a same-principal action is not privilege gain.
4. A decisive fact outside source (proxy, IdP, WAF, IAM, cache, deployed flag) makes it `needs_validation`, with that fact named.
5. A missing best practice with no affected principal is a hardening note.
6. A candidate refuted by source is `rejected`, not `needs_validation`.

## Common false-positive patterns (all classes)

| Pattern | Why it is often wrong |
|---|---|
| Scanner or grep hit reported as-is | No trace to a lower-trust source; the value is constant or already validated |
| "No auth decorator on this handler" | Global middleware, router groups, gateway policy, or default permission classes apply |
| Dangerous API in tests, scripts, or dev tooling | Not reachable by a lower-trust principal in production |
| Admin can do something dangerous | Admins may hold that power by design; check the product's trust model |
| Framework would block it | Modern frameworks reject CRLF in headers, escape templates, enforce CSRF by default, and reject `*` with credentials. Verify the version |
| Self-impact | The attacker only affects their own account or data |
| Theoretical chain | One link is assumed, not shown. Each prerequisite needs its own evidence |

## Hunter brief (one ledger unit or a small group of units)

```text
You are auditing <unit IDs> in <target> at <source ref>. Read-only source review.
Do not contact deployed or external services. Run target code only inside the approved
sandbox (no network, empty allowlisted environment, read-only target, scratch-only writes,
explicit limits). If the sandbox is unavailable, do not execute anything.
Context: <architecture summary>; checklist sections: <attack-surface sections>;
class references: <for example injection.md, authz-and-tenancy.md> (sinks, traps, validation).
Exclude these unchanged prior root causes: <fingerprints>.
For each candidate, return a structured record (no prose-only results):
- fingerprint: stable, source-derived, e.g. <file>:<function>:<sink>:<class>
- proposed verdict: confirmed | needs_validation
- the six elements: principal, input, intended control, boundary, affected resource, result
- trace: entrypoint → propagation → sink, each step with file:line
- evidence: commands and fixtures used, with their output, or "static only"
- proposed likelihood, impact, and smallest fix
For units with no candidate, return what you checked, so the unit can be marked covered.
```

## Wave assignments

Each hunting wave has three kinds of hunter. Reserve budget for all three before assigning unit hunters.

| Hunter | Assignment | Returns |
|---|---|---|
| **Unit hunters** | One ledger unit or a small group, with the brief above | Candidates per unit, or what was checked |
| **Obvious-things hunter** (one per wave) | Run the obvious-exposure sweep from the [attack-surface checklists](attack-surfaces.md) literally over the whole scope: committed secrets, debug modes, operational routes, seed accounts, dynamic execution, CORS and cookies, redirects, error leaks, agent configuration. In later waves, only on surfaces added since the last sweep | One line per sweep item with its result, and candidates for traced hits |
| **Wildcard hunter** (one per wave) | No assigned unit. Look for what the ledger shape misses: chains that span units, the oddest or newest code, sibling paths that no unit names, and assumptions shared by every unit. Exclude fingerprints already found | Candidates, plus proposed new ledger units for the critic |

The `quick` profile runs one obvious-things hunter and may skip the wildcard. The wildcard hunter's units still pass through the critic and the verifiers like any other.

## Coverage critic (after each wave)

A fresh agent reviews the ledger and hunter returns:

- surfaces from reconnaissance with no unit, and new surfaces discovered during hunting;
- units marked covered with shallow evidence (no trace, no controls checked);
- attack classes that never applied to an important surface.

The parent adds or reassigns units. A **clean pass** means the critic found nothing material. The `standard` and `deep` profiles continue waves until a clean pass or until the budget forces deferral.

## Candidate verifier brief

```text
You did not write this candidate. Try to refute it from repository source and bounded
local evidence. Same sandbox rules apply; if a control is unavailable, do not execute,
and record the missing capability as a needs_validation blocker.
1. Check every trace step: does each cited file:line exist and do what is claimed?
   Is the first step a real lower-trust entrypoint, and the last the claimed effect?
2. Reconstruct the strongest controls on the path: validation, identity, authorization,
   normalization, framework defaults, containment. Does any of them stop it?
3. For a proposed confirmed candidate, reproduce the minimum result independently with
   dummy principals. Do not infer a stronger result than you observe.
4. Check that likelihood, impact, and the fix match only what the evidence shows.
5. For needs_validation: is the blocker genuinely outside source? Name the exact
   missing fact and a safe owner-run check. If source settles it, decide it.
6. Check the precedents (references/precedents.md). If one applies, check its
   "becomes reportable when" condition in source before rejecting.
7. Score exploitability 0-10 (reachability 0-3, trace 0-4, impact 0-3; see SKILL.md).
   Below 8, the verdict cannot be confirmed: settle it from source, or return
   needs_validation with the exact unresolved fact.
Return: verdict (confirmed | needs_validation | rejected), the score with one line per
part, corrected record fields, and the refuting control or precedent (file:line) for
a rejection.
```

The verifier receives only the candidate, its unit, the architecture facts it needs, the relevant checklist sections, and prior records with the same fingerprint. It never receives another verifier's conclusion.

## Final-record verifier brief

Candidate verification checks hunter output. This pass checks what will be published: the records as written in `findings.md`, after consolidation and editing. Use a fresh agent (or, without subagents, a fresh pass started from the record file alone) that did not hunt or verify the record.

```text
You are checking final written records, not candidates. For each record:
1. Open every cited file:line at <source ref>. Does it exist and say what the record claims?
2. Do the title, severity, and result claim only what the evidence shows?
3. Are the verdict's required fields present (see the required fields by verdict in
   references/reporting.md)? No severity on needs_validation or rejected.
4. Does the fix enforce the stated invariant at the cited decision point?
Return per record: ok, or the field to correct and the evidence for the correction.
```

The coordinator reconciles corrections before the report is written.

## Consolidation

Merge candidates that share a root cause (the same missing control at the same decision point) under one fingerprint. List all affected entry points in that record.

Sources: adapted from cloudflare/security-audit-skill (MIT) and general practice.
