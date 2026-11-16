# Worked Analysis and Convergence

One analyze-mode report and one converge-mode pass for the refund feature. Inputs: the good spec in requirements-analysis (`references/spec-examples.md`), a plan derived from it, and the constitution rules below. The plan used here is an earlier draft with deliberate defects; the corrected plan is in task-planning (`references/worked-plan.md`).

Constitution rules in force:

- **I.** Tests first: every task writes a failing test before the code.
- **II.** Money values MUST be integer minor units.
- **III.** Every schema change MUST include a reversible migration.

## Analyze mode: the report

```markdown
## Spec analysis: Self-service refund requests (2026-11-16)

| ID | Pass | Severity | Location | Finding | Recommendation |
|---|---|---|---|---|---|
| C1 | Constitution | Critical | PLAN.md Data model; T002 | `amount DECIMAL(10,2)` breaks Constitution II | Use `amount_cents INTEGER`; update T002 and T004 |
| G1 | Coverage | Critical | spec FR-003 | Refundable-balance rule has no task or test | Add task after T004 using the FR-003 examples table |
| C2 | Constitution | Critical | T002 | Migration has no down step; breaks Constitution III | Add down migration and a rollback test step |
| G2 | Coverage | High | spec NFR-002 | Idempotent provider call not in any task | Add idempotency key = request ID to T006, with a replay test |
| I1 | Inconsistency | High | spec FR-005 vs PLAN.md Validation | Reason length 10–500 in spec, `max(255)` in plan | Follow spec: 10–500 |
| I2 | Inconsistency | High | T006 [P], T007 [P] | Both modify `src/refunds/service.ts` | Remove `[P]` from T007; depend on T006 |
| A1 | Ambiguity | High | spec FR-007 | `[NEEDS CLARIFICATION: also on approved?]` still open | Ask owner; recommended answer: no email on `approved` |
| I3 | Inconsistency | Medium | PLAN.md, T005 | Role named `admin`; spec says `support_agent` | Rename to `support_agent` |
| G3 | Coverage | Medium | T011 | "Add CSV export" maps to no requirement | Drop, or add a requirement with owner approval |
| G4 | Coverage | Medium | spec SC-002 | No task emits a time-to-refund metric | Add counter and timing to T006 |
| U1 | Underspec | Medium | T009 | "Add tests for status page": no file, no command | Name `tests/refunds/status.test.ts` and expected count |
| D1 | Duplication | Low | spec FR-002, Edge cases line 1 | Window rule stated twice | Keep FR-002; make edge case cite it |

Coverage: 10/12 requirements have ≥1 task (83%). Missing: FR-003, NFR-002.
Unmapped tasks: T011.
Constitution: 2 conflicts (II, III).
Metrics: requirements 12 · tasks 11 · ambiguity 1 · duplication 1 · critical 3.
Next: resolve critical findings first. Return to task-planning for C1, C2, G1;
ask the owner about A1.
```

### Why each severity

- C1, C2: constitution conflicts are always Critical.
- G1: a P1 money rule with zero coverage blocks a correct baseline.
- I1, I2, A1: they change behavior or break the build, but each has an obvious fix.
- I3, G3, G4, U1: they cause rework or confusion, not wrong money movement.
- D1: wording only.

### What the agent does next

It stops and offers edits. It does not apply them. A typical close:

> Three critical findings block implementation (C1, C2, G1). I can draft the plan changes for those three now. Shall I?

### A clean report

When nothing is found, still report the numbers. Silence is not evidence.

```markdown
## Spec analysis: Self-service refund requests (2026-11-20)
No findings.
Coverage: 12/12 requirements have ≥1 task (100%). Unmapped tasks: none.
Constitution: no conflicts (rules I–III checked).
Next: proceed to implementation.
```

## Converge mode: after an implementation pass

The plan was fixed and tasks T001–T012 were implemented. The user asks "what's left compared to the spec?".

### Step 1: assess each requirement against code

Completion checkboxes are claims, not evidence. Check the code and tests for every item.

| Item | Evidence checked | Result |
|---|---|---|
| FR-001 window | `src/refunds/policy.ts:isWithinWindow`, tests for 0/29/30/31 days pass | met |
| FR-002 reject outside window | `src/refunds/routes.ts` returns 422 with message; test passes | met |
| FR-003 balance rule | `policy.ts:refundableCents` exists; no test for prior completed refunds | partial |
| FR-004 one open request | Unique partial index in migration `0042`; test passes | met |
| FR-005 role and reason | Role check present; reason min 10 checked, max 500 not checked | partial |
| FR-006 refund after provider confirms | Status set to `refunded` right after the API call, before webhook confirmation | contradicts |
| FR-007 emails | `rejected` email sent; `refunded` email missing | partial |
| FR-008 audit | Audit row written on every transition; test passes | met |
| NFR-001 latency | Staging load-test report: p95 310 ms at 20 req/s | met |
| NFR-002 idempotency | Idempotency key sent; replay test passes | met |
| NFR-003 accessibility | axe-core run on refund form: 0 violations; keyboard pass recorded | met |
| SC-002 metric | No timing metric emitted | missing |
| (code) `src/refunds/export.ts` | CSV export exists; no requirement | unrequested |

### Step 2: append, never rewrite

The agent appends one section to the end of the task list. Existing tasks keep their IDs, order, and text, including checkboxes. The highest existing ID is T012, so new IDs start at T013.

```markdown
## Convergence 1 (2026-11-22)

- [ ] T013 Set status `refunded` only on provider confirmation webhook, not on API
      response, per FR-006 (contradicts). Files: src/refunds/service.ts,
      src/payments/webhooks.ts. Verify: `npm test -- refunds/webhook.test.ts` → pass,
      including "API success without webhook leaves status approved".
- [ ] T014 Add test and fix for refundable balance after prior completed refunds,
      per FR-003 (partial). Files: tests/refunds/policy.test.ts. Verify: FR-003
      examples table rows 3–4 pass.
- [ ] T015 Enforce reason max 500 characters, per FR-005 (partial). Files:
      src/refunds/validation.ts. Verify: 501-char reason returns 422.
- [ ] T016 Send email on `refunded`, per FR-007 (partial). Files:
      src/refunds/notify.ts. Verify: notify test asserts one email per transition.
- [ ] T017 Emit `refund.time_to_refunded_seconds` histogram, per SC-002 (missing).
      Files: src/refunds/service.ts. Verify: metric visible in staging.
- [ ] T018 Review `src/refunds/export.ts`: justify with a requirement or remove,
      per scope (unrequested). Owner decision needed.
```

Ordering: the `contradicts` item on money first, then partial gaps on P1 rules, then the rest. The unrequested item asks for a decision; converge never deletes code.

### Step 3: report

```markdown
Convergence 1 appended: 6 tasks (T013–T018).
Checked: 11 requirements, 1 success criterion, 3 constitution rules.
Gaps: missing 1 · partial 3 · contradicts 1 · unrequested 1.
Next: implement T013 first (money moves before confirmation).
```

### Second pass

After T013–T018 are done, converge runs again. If every item is met, the task list stays byte-for-byte unchanged and the report says so with counts. If gaps remain, a new `## Convergence 2 (date)` section goes below Convergence 1. Convergence 1 is never edited.

## Mistakes to avoid

| Mistake | Do instead |
|---|---|
| Fixing the plan while analyzing | Report and offer edits; wait for approval |
| Trusting checked boxes in converge | Check code and tests for each item |
| Renumbering tasks to fit new ones in | Append with new IDs after the highest existing ID |
| Writing an empty Convergence header when all is met | Leave the file unchanged |
| Inventing a requirement to explain unrequested code | Report it as unrequested and ask |
| Vague finding ("security could be better") | Location, exact text, one concrete remedy |

Sources: adapted from github/spec-kit (MIT) `templates/commands/analyze.md` and `templates/commands/converge.md`, and general practice.
