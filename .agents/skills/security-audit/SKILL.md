---
name: security-audit
description: Defensive, source-first security review that reports only vulnerabilities crossing a real trust boundary, with evidence, calibrated severity, and the smallest effective fix. Use for security questions, focused reviews of risky changes, and, only when explicitly requested, full codebase audits or pen-test style reviews with a coverage ledger and independent verification.
---

# Security Audit

## Purpose

Find vulnerabilities that violate a real trust boundary and give owners source evidence, a safe reproduction, a priority, and the smallest effective fix. A candidate without a concrete affected principal, resource, and security outcome is not a confirmed finding.

## Operating modes

Loading this skill does not authorize a full audit or the creation of files.

| Mode | When | Writes |
|---|---|---|
| **Guidance** (default) | Security questions, focused review of a diff or component, triage of a reported issue | Nothing beyond the answer, unless asked |
| **Full audit** | The user explicitly asks to audit or pen-test a codebase, asks for a comprehensive or end-to-end review, or requests report artifacts | Run directory with ledger, findings, and report |

If the request could mean either mode, ask one question before creating files.

## Authorization and execution safety (both modes)

- Confirm the authorized scope: repository paths, environments, and exclusions. Never probe deployed endpoints, shared services, production identities, or other users' data.
- Source inspection is read-only. Run target code (builds, tests, fixtures) only in a sandbox with **no external network**, an **empty allowlisted environment** (no inherited credentials), a **read-only target**, **scratch-only writes**, and **explicit CPU, memory, time, and disk limits**. If these cannot be enforced, do not execute. Record the missing capability as a validation blocker and give a safe validation plan.
- Do not install dependencies, fetch packages, spend paid API quota, or publish anything during an audit.
- Use dummy principals, fixtures, and secrets. Stop at the minimum effect that proves the boundary violation. Never build persistence, concealment, or post-exploitation material.
- Never put secrets in notes or reports.

## Finding requirements

For every candidate, name all six:

1. **Lower-trust principal** (anonymous user, other tenant, plugin, model output, local process, …).
2. **Input or action** that the principal controls.
3. **Intended control** that should stop it (with file:line).
4. **Boundary crossed** (authentication, authorization, tenant isolation, sandbox, …).
5. **Affected principal or resource.**
6. **Concrete result**, observed or owner-observable (unauthorized record read, script executed in another user's session, …).

Not findings: checklist deviations with no reachable violation, defense-in-depth advice, guesses about deployment behavior not visible in source, same-principal self-impact, and parser crashes with no security consequence. Report useful items of that kind as **hardening notes**, separately and without severity.

Before reporting, check the [precedents](references/precedents.md): claims that are normally noise (operator-set environment, unguessable IDs, auto-escaped output, test-only code, and others), each with the condition that makes it reportable again. Precedents reduce noise; they never override a concrete exploit with evidence. When in doubt, use `needs_validation`.

## Verdicts and severity

| Verdict | Meaning | Severity |
|---|---|---|
| `confirmed` | Source trace plus independent validation show the result | Required |
| `needs_validation` | Source-grounded hypothesis blocked on a specific missing fact (deployment config, proxy behavior, IdP policy), or below the reporting threshold | **None.** Name the exact missing fact and a safe owner-run check |
| `rejected` | Refuted by a control in source or by validation | None. Cite the refuting control |

Severity anchors (only for `confirmed`; severity cannot exceed the demonstrated impact):

- **Critical:** an unauthenticated actor gains code execution, full data-store access, or arbitrary account takeover.
- **High:** an explicit security control is fully defeated with real consequences: authentication bypass, cross-tenant read or write, stored XSS affecting other users, authenticated RCE, or an unauthenticated remote stop of a shared service.
- **Medium:** a real boundary violation with limited blast radius, uncommon preconditions, or a narrow resource set.
- **Low:** disclosure of non-secret internals, or an effect that needs sustained effort for minimal gain.
- **Informational:** confirmed but minimal impact, mainly useful as a building block.

The high/medium test: does the result **fully defeat** an explicit control for a consequential action, or only weaken it? If you cannot state the concrete damage, the severity is lower than it feels.

### Reporting threshold (both modes)

Report a candidate as a finding only when, **after a refuting check** (the verifier in a full audit, a deliberate attempt to disprove it in guidance mode), confidence that it is exploitable is at least **8/10**. Score three parts:

- **Reachability (0–3):** a lower-trust principal reaches the entry point with input it controls, shown in source.
- **Trace (0–4):** every step from entry to sink has file:line, and the strongest control on the path has been read and does not stop it.
- **Impact (0–3):** the concrete result follows from the trace or was observed, not assumed.

Below 8, settle the open part from source if you can (then report or reject). Otherwise record `needs_validation` with the exact unresolved fact. Never drop a candidate silently. The score gates reporting; it does not set severity, which follows the anchors above.

## Guidance mode procedure

1. Scope the question: the component, the diff, or the reported behavior.
2. Identify the trust boundaries the code touches ([reconnaissance](references/reconnaissance.md), questions only).
3. Load only the relevant [attack-surface checklist](references/attack-surfaces.md) sections, then the matching class reference from the table below for sinks, safe patterns, and traps.
4. Trace candidate paths from entry point to sink; check the strongest controls on each path ([hunting method](references/hunting-and-validation.md)). Validate with the harmless techniques listed there.
5. Try to refute each candidate: apply the precedents and score it against the reporting threshold.
6. Answer with confirmed findings, `needs_validation` items, rejected concerns, and hardening notes, each with file:line evidence and the smallest fix. Before sending, re-read each written item against its cited source once more.

## Full audit procedure

1. **Setup.** Record the target, source ref (commit, dirty state), profile, scope, budget, and an output directory **outside** the target (default `~/axiom-security-audit/<repo>/run-<N>/`). Use a directory inside the target only if the user chooses it and version control ignores it.
2. **Reconnaissance.** Map the product, principals, controls, entry surfaces, sinks, and local execution limits. Build the **coverage ledger** from stable units (surface × boundary × attack class). Read prior runs' ledgers and findings, and re-validate them against current source. See [reconnaissance](references/reconnaissance.md).
3. **Hunting waves.** Assign isolated hunters (subagents when available) to ledger units, with the relevant attack-surface sections, plus one obvious-things hunter and one wildcard hunter per wave. Each hunter returns structured candidates, never prose-only. After each wave, run a **coverage critic** that looks for unmapped surfaces and shallow units. See [hunting and validation](references/hunting-and-validation.md).
4. **Candidate validation.** Consolidate candidates by fingerprint. Give each one to a **fresh verifier** that did not hunt it and whose job is to refute it, including the precedents and the reporting threshold.
5. **Structured records.** Write the final `confirmed`, `needs_validation`, and `rejected` records in the [record format](references/reporting.md), and update every ledger unit's terminal state.
6. **Independent record verification.** Step 4 checks candidates; this step checks the final written records. Have fresh agents that did not hunt or verify a record re-check it against the cited source ([final-record verifier brief](references/hunting-and-validation.md)). Reconcile any corrections.
7. **Report.** Derive the report from the records only. Prose and records must agree. Include no live-probe instructions.

End in exactly one of two terminal states: all report artifacts written and every ledger unit in a terminal state, **or** the run marked `incomplete` with its exact reason, disclosed at the top of the report. Never claim complete coverage from one pass, a `quick` profile, or a scoped run.

## Profiles and budget (full audit)

| Profile | Use | Shape |
|---|---|---|
| `quick` | Small targets, re-runs, first look | Coarse units, one hunter wave, one final critic, one verifier per candidate. Report as partial coverage |
| `standard` (default) | Typical audit | Waves until a clean critic pass; separate candidate and record verification |
| `deep` | High-stakes or large targets | Finer units per subsystem and lifecycle; independent second pass on previously covered units |

Profiles change breadth, never the evidence bar. When the user sets a budget (maximum agent invocations), reserve the critic and verifier calls **before** assigning hunters. If the budget cannot fund validation, stop hunting, validate in fingerprint order, and mark the run incomplete. Never exceed a user-set budget silently.

## Fixes

For each confirmed finding, state the invariant the code must enforce and the narrowest source change that enforces it at the last trusted decision point, plus a regression test. The audit describes fixes. It does not modify target source unless the user separately asks for remediation, which is a normal implementation task.

## Anti-patterns

1. Presenting checklist deviations as vulnerabilities.
2. Assigning severity to `needs_validation`.
3. Probing live or shared environments when bounded local evidence would do.
4. Guessing provider, proxy, browser, or identity behavior that is not in source.
5. Prose-only hunter output that cannot be deduplicated or verified.
6. Writing the report before independent verification, or letting prose and records disagree.
7. Treating a scanner hit as a confirmed vulnerability.
8. Dropping a below-threshold or precedent-excluded candidate without a `needs_validation` or `rejected` record.

## References

Open a reference when its trigger applies. Do not load all of them.

| Reference | Open when |
|---|---|
| [Reconnaissance](references/reconnaissance.md) | Mapping a codebase: stack fingerprint, entry points, trust-boundary questions, ledger, prioritization |
| [Attack-surface checklists](references/attack-surfaces.md) | Choosing what to hunt; the obvious-exposure sweep; non-web surfaces (cloud, IPC, AI, memory safety) |
| [Precedents](references/precedents.md) | Before reporting any candidate: what is normally not reported, and when it becomes reportable |
| [Hunting and validation](references/hunting-and-validation.md) | Tracing a candidate, choosing a harmless validation, applying the candidate gate, wave assignments, briefing hunters and verifiers |
| [Records, ledger, and report](references/reporting.md) | Writing a finding, required fields by verdict, calibrating severity, shaping a guidance answer or full report |
| [Injection](references/injection.md) | Input reaches SQL, NoSQL, shell, templates, `eval`, LDAP, or headers |
| [Authentication and sessions](references/authn-and-session.md) | Login, sessions, JWT, OAuth/OIDC, SAML, MFA, password reset, API keys |
| [Authorization and tenancy](references/authz-and-tenancy.md) | Requests name resource IDs; roles differ; several tenants share storage; writes bind request bodies to models |
| [SSRF](references/ssrf.md) | The server fetches a URL or host that a user or tenant influences |
| [Files and deserialization](references/files-and-deserialization.md) | Paths from input, uploads, archive extraction, XML parsing, pickle/YAML/Java/PHP deserialization |
| [Browser and web](references/browser-and-web.md) | HTML rendering, cookie-auth state changes, CORS, redirects, `postMessage`, security headers |
| [Secrets and crypto](references/secrets-and-crypto.md) | Credentials in the repo or bundles, token generation, password hashing, encryption, webhook signatures, debug exposure |
| [Supply chain](references/supply-chain.md) | Dependency advisories, lockfiles, registries, CI workflows, release and update integrity |
| [Business logic](references/business-logic.md) | Money, credits, quotas, approvals, multi-step flows, check-then-act races, export/import abuse |
| [Data lifecycle](references/data-lifecycle.md) | Backups, restore and import, deletion, exports and download links, retention |
| [AI and LLM features](references/ai-llm.md) | The application calls a model and renders its output, passes it to tools, or retrieves data for it |
| [Agent configuration](references/agent-config.md) | The repository holds agent hooks, MCP server configs, permission allowlists, instruction files, skills or plugins, or CI agents |

Related repository files: security audit workflow (`workflows/security-audit/WORKFLOW.md` in the Axiom repository), security tools integration (`integrations/security-tools/README.md` in the Axiom repository).
