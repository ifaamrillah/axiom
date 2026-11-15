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

- Every confirmed record has a severity, a trace, evidence, and a fix. No `needs_validation` or `rejected` record has a severity.
- Every fingerprint in the report exists in `findings.md`, and the reverse.
- Every final record links to at least one ledger unit, and every unit is in a terminal state (or the run is marked incomplete).
- The report contains no secrets and no live-probe instructions.
