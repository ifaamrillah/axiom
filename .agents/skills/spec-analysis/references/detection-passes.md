# Detection Passes in Detail

How to run each analyze-mode pass, what a real finding looks like, and what is not a finding. Examples use the refund feature (spec `SPEC-014`, plan, and tasks from the requirements-analysis and task-planning examples). Use stable finding IDs prefixed by the pass initial: `D` duplication, `A` ambiguity, `U` underspecification, `C` constitution, `G` coverage gap, `I` inconsistency. Rerunning on unchanged artifacts must give the same IDs and counts.

## Before the passes: build the inventory

1. List every `FR-`, `NFR-`, and buildable `SC-` from the spec. Skip success criteria that are business outcomes with no buildable work ("support emails drop by half"). Keep ones that need code or tooling ("95% of refunds complete within 1 hour" needs a metric).
2. List every acceptance scenario as `US<n>/AC<m>`.
3. List every task: ID, the requirement IDs it cites, its files, its `[P]` mark, and its dependencies.
4. Map requirements to tasks. Use explicit IDs first. Fall back to keyword matching only when a task cites nothing, and say so in the finding.
5. Extract the constitution's MUST and SHOULD statements as a numbered rule list.

Quick extraction commands:

```bash
grep -noE '\b(FR|NFR|SC)-[0-9]{3}\b' spec.md | sort -u -t: -k3     # requirement IDs in spec
grep -noE '\b(FR|NFR|SC)-[0-9]{3}\b' PLAN.md | sort -u -t: -k3      # IDs the plan cites
grep -nE '^#{2,3} T[0-9]{3}|^- \[.\] T[0-9]{3}' PLAN.md              # task headings or checklist lines
grep -nE 'NEEDS CLARIFICATION|TODO|TBD|TKTK|\?\?\?' spec.md PLAN.md  # leftover markers
```

## Duplication (D)

**Look for:** two requirements or tasks that say the same thing in different words; a requirement restated in a later section with a different value.

| Finding | Not a finding |
|---|---|
| FR-002 "reject requests outside the window" and FR-009 "requests older than 30 days are refused" — same rule, two IDs | A requirement and its acceptance scenario saying the same thing; that is traceability |
| T004 and T011 both "add refund status enum" in the same file | Two tasks touching one file for different requirements |

**Recommendation pattern:** keep the clearer phrasing, retire the other ID, and update references. Severity: High when the copies disagree on a value; Low when identical.

## Ambiguity (A)

**Look for:** vague adjectives, open lists, escape-hatch phrases, placeholders, unresolved `[NEEDS CLARIFICATION]`. Use the ambiguity word list in requirements-analysis (`references/ambiguity-words.md`) for the full set.

| Finding | Not a finding |
|---|---|
| NFR-004 "The agent queue should load quickly" — no number | "Fast" in the Context section describing the user's wish |
| FR-007 still carries `[NEEDS CLARIFICATION: also on approved?]` | A marker on a P3 story that the spec lists as deferred, with the risk stated |
| Plan: "handle provider errors appropriately" | Plan: "on provider 5xx, retry 3 times at 1 s, 2 s, 4 s, then set `failed`" |

Severity: High when it touches security, money, data, or a P1 story; Medium otherwise.

## Underspecification (U)

**Look for:** a requirement verb with no object or result; a story with no failure scenario; a task with no file path, no verification command, or no expected result; a task naming a file or component that neither spec nor plan defines.

| Finding | Not a finding |
|---|---|
| FR-008 "System MUST record status changes" — where, which fields, append-only? | FR-008 that lists actor, before, after, timestamp, reason |
| T009 "Add tests for refunds" — no file, no command, no expected result | A task whose verify line is `npm test -- refunds/request.test.ts` → `4 passed` |
| T012 edits `src/notifications/sms.ts`; spec says email only | — (this is also a scope-creep coverage finding; report once, under the pass that explains it best) |

Severity: High if it blocks a P1 task from being implemented without guessing; Medium otherwise.

## Constitution conflicts (C)

**Look for:** a plan or task choice that breaks a MUST principle; a mandated section or gate missing (for example the constitution requires a migration rollback note and the plan has none). Constitution conflicts are always **Critical**. The fix is to change the spec, plan, or tasks. Changing the principle is a separate, explicit constitution amendment, never part of analysis.

| Constitution rule | Finding |
|---|---|
| "All money values MUST be integer minor units" | Plan's data model: `amount DECIMAL(10,2)` and task T003 parses `"40.00"` as float |
| "Every schema change MUST ship with a reversible migration" | T002 adds `refund_requests` table; no down migration in files or steps |
| "No new runtime dependency without an ADR" | T006 adds `bullmq` for retries; no ADR in the plan's decisions |
| "Tests first" | Tasks T007–T010 list "implement" before "write failing test" |

If the constitution file is an unfilled template, skip this pass and say so in the report.

## Coverage gaps (G)

**Look for:** a must-have requirement or scenario with zero tasks; a buildable success criterion or NFR with no task; a task with no requirement (scope creep).

| Finding | Severity |
|---|---|
| FR-003 (amount ≤ refundable balance) has no task and no test | Critical: P1 money rule with zero coverage |
| NFR-002 (idempotent provider calls) cited by no task | High: money safety |
| SC-002 (95% refunded within 1 h) needs a metric; no task emits one | Medium |
| T014 "Add CSV export of refunds" maps to no requirement | Medium: unrequested scope; ask whether to add a requirement or drop the task |
| US1/AC3 (duplicate request) has a task but no test step for it | High: P1 scenario untested |

Report coverage as a number: "11/13 requirements have at least one task (85%)".

## Inconsistency (I)

**Look for:** terminology drift across files; entities in the plan absent from the spec (or the reverse); contradictory values; task order that breaks a dependency; `[P]` on tasks that share a file or depend on each other.

| Finding | Example |
|---|---|
| Terminology drift | Spec says "support agent"; plan and tasks say "admin" and create role `admin` |
| Value conflict | Spec FR-005: reason 10–500 chars; plan validation: `max(255)` |
| Entity drift | Plan adds `RefundBatch` entity; spec has no batches |
| State drift | Spec statuses include `failed`; plan's enum omits it |
| Order violation | T005 (approve endpoint) runs before T002 (table migration) with no dependency listed |
| Wrong `[P]` | T006 [P] and T007 [P] both modify `src/refunds/service.ts` |

Severity: High when it changes behavior (value, state, permission); Medium for naming only.

## Severity quick reference

| Severity | Use when |
|---|---|
| Critical | Constitution MUST broken; P1 or must-have requirement with zero coverage; contradiction that blocks implementation |
| High | Conflict or ambiguity on security, money, data, or a P1 story; untestable acceptance criterion; wrong dependency that will break the build |
| Medium | Terminology drift; missing NFR or edge-case task; unrequested task |
| Low | Wording, minor redundancy, formatting |

## Writing a good finding

| Weak finding | Strong finding |
|---|---|
| "Some requirements are vague" | "A2 · NFR-004 'queue should load quickly' has no target. Propose ≤ 1 s p95 with 500 open requests." |
| "Coverage could be better" | "G1 · FR-003 has no task. Add task after T004: validate amount ≤ paid − completed refunds; tests from the FR-003 examples table." |
| "Plan conflicts with constitution" | "C1 · Constitution II (integer minor units) vs plan data model `DECIMAL(10,2)` at PLAN.md 'Data model'. Change to `amount_cents INTEGER`." |

A strong finding names the location, quotes or paraphrases the exact text, and gives one concrete remedy.

Sources: adapted from github/spec-kit (MIT) `templates/commands/analyze.md` and general practice.
