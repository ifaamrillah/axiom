# Worked Plan: From Spec to Ready Plan

A complete plan for the refund spec (`SPEC-014`, shown in requirements-analysis `references/spec-examples.md`). It follows the [plan template](../assets/PLAN.md) and the rules in [sizing and ordering](sizing-and-ordering.md). The stack is TypeScript, Express, PostgreSQL, and Vitest; the shape is the same in any stack.

Before planning, the owner answered the open clarifications:
- FR-007: no email on `approved`. Emails on `rejected` and `refunded` only.
- Gift-card orders: excluded in v1. The form is hidden for them (new FR-009, added to the spec by the owner).

## The plan

````markdown
---
status: ready
spec: specs/014-refunds/spec.md
updated: 2026-11-17
blocked_reason: ""
---

# Plan: Self-service refund requests

## Outcome
A customer requests a refund for a delivered item; a support agent approves or
rejects it; approved refunds are paid to the original payment method; the
customer sees the status and gets emails on rejection and payout.

## Scope
- In scope: US1–US3, FR-001–FR-009, NFR-001–NFR-003, SC-002 metric.
- Out of scope: returns, auto-approval, store credit, gift-card orders (FR-009 hides them).

## Global constraints (copied from spec and constitution)
- Money is integer minor units (`amount_cents`), currency from the order.
- Window: 30 days inclusive from `order_items.delivered_at`.
- Reason: 10–500 characters. Role name: `support_agent`.
- Provider idempotency key = refund request ID.

## Constitution check
| Principle | Result | Note |
|---|---|---|
| I. Tests first | pass | Every task starts with a failing test |
| II. Integer minor units | pass | `amount_cents INTEGER`; no floats |
| III. Reversible migrations | pass | T001 has down migration and a test for it |

## File map
| Path | New/Modify | Responsibility |
|---|---|---|
| migrations/0042_refund_requests.ts | New | Tables `refund_requests`, `refund_audit`; unique open index |
| src/refunds/types.ts | New | `RefundStatus`, `RefundRequest` types |
| src/refunds/policy.ts | New | Pure rules: window, refundable balance, eligibility |
| src/refunds/repository.ts | New | DB access for requests and audit |
| src/refunds/service.ts | New | Status transitions; writes audit on every transition |
| src/refunds/routes.ts | New | Customer and agent HTTP endpoints |
| src/refunds/validation.ts | New | Request body schemas |
| src/refunds/notify.ts | New | Customer emails on status change |
| src/payments/webhooks.ts | Modify | Handle `refund.succeeded` / `refund.failed` events |
| src/web/orders/RefundForm.tsx | New | Customer form |
| src/web/orders/RefundStatus.tsx | New | Customer status view |
| src/admin/refunds/RefundQueue.tsx | New | Agent queue with approve/reject |

## Tasks

### T001 Refund tables and types — covers FR-004, FR-008, Constitution II–III
- Files: migrations/0042_refund_requests.ts (new), src/refunds/types.ts (new),
  tests/migrations/0042.test.ts (new)
- Interface: `type RefundStatus = 'requested'|'approved'|'rejected'|'refunded'|'failed'`
- Depends on: none
- Steps:
  - [ ] Write test: migrate up creates both tables; inserting two `requested` rows
        for one `order_item_id` fails on `refund_requests_one_open`; migrate down
        drops both tables.
  - [ ] Run `npx vitest run tests/migrations/0042.test.ts`; expect FAIL (no migration).
  - [ ] Write migration: `amount_cents INTEGER NOT NULL CHECK (amount_cents > 0)`;
        partial unique index on `order_item_id WHERE status IN ('requested','approved')`;
        `refund_audit` with actor_id, from_status, to_status, reason, created_at.
  - [ ] Run the test; expect 3 passed.
  - [ ] Commit `feat(refunds): add refund tables`.
- Verify: `npx vitest run tests/migrations/0042.test.ts` → 3 passed.

### T002 Customer submits a refund request (P1 slice) — covers US1, FR-001–FR-004, FR-009, NFR-003
- Files: src/refunds/policy.ts, repository.ts, validation.ts, routes.ts (new);
  src/web/orders/RefundForm.tsx (new); tests/refunds/policy.test.ts,
  tests/refunds/request.api.test.ts, tests/web/RefundForm.a11y.test.tsx (new)
- Consumes: T001 tables and `RefundStatus`.
- Produces: `isWithinWindow(deliveredAt: Date, now: Date): boolean`;
  `refundableCents(item: OrderItem, completed: Refund[]): number`;
  `POST /orders/:orderId/items/:itemId/refunds` body `{ amountCents, reason }`
  → 201 `{ id, status: 'requested' }`;
  `GET /orders/:orderId/items/:itemId/refunds` → 200 `[{ id, status, amountCents, reason }]`.
- Depends on: T001
- Steps:
  - [ ] Write policy tests from the spec's examples tables: window rows 0/29/30/31
        days and undelivered; balance rows for $40.00 paid with $0/$25/$40 refunded.
  - [ ] Run `npx vitest run tests/refunds/policy.test.ts`; expect FAIL (module missing).
  - [ ] Implement `isWithinWindow` and `refundableCents` in policy.ts.
  - [ ] Run policy tests; expect 11 passed.
  - [ ] Write API tests: 201 on valid; 422 "Refund window closed (30 days from
        delivery)"; 422 "Amount exceeds refundable balance"; 409 with existing
        request on duplicate; 404 for another customer's order; 422 for gift-card order;
        GET returns only the caller's requests.
  - [ ] Run `npx vitest run tests/refunds/request.api.test.ts`; expect FAIL (no route).
  - [ ] Implement route, validation, and repository insert. Map unique-index
        violation to 409.
  - [ ] Build RefundForm with labelled inputs and error text linked by
        `aria-describedby`.
  - [ ] Write `tests/web/RefundForm.a11y.test.tsx` with jest-axe; expect 0 violations.
  - [ ] Run `npx vitest run tests/refunds tests/web/RefundForm.a11y.test.tsx`; expect all pass.
  - [ ] Commit `feat(refunds): customer refund request`.
- Verify: `npx vitest run tests/refunds tests/web/RefundForm.a11y.test.tsx` → all pass.

### Checkpoint A (P1 shippable)
- [ ] `npm test && npm run lint && npm run build` green.
- [ ] Manual: submit a request in local env; row visible with status `requested`.
- [ ] Load test `k6 run load/refund-request.js` in staging: p95 ≤ 500 ms at 20 req/s (NFR-001).

### T003 Agent approves or rejects (P2 slice) — covers US2, FR-005, FR-008
- Files: src/refunds/service.ts (new), routes.ts (modify), validation.ts (modify),
  src/admin/refunds/RefundQueue.tsx (new), tests/refunds/review.api.test.ts (new)
- Produces: `transition(id: string, to: RefundStatus, actor: Actor, reason?: string): Promise<RefundRequest>`
  — the only function that changes status; writes one `refund_audit` row per call
  and emits event `refund.status_changed { id, from, to }`.
- Depends on: T002
- Steps:
  - [ ] Write tests: `support_agent` approves → `approved` + 1 audit row; reject
        without reason → 422; 9-char and 501-char reasons → 422; 10 and 500 → ok;
        customer role → 403; agent on own order → 403; `refunded` → `requested` → 409.
  - [ ] Run `npx vitest run tests/refunds/review.api.test.ts`; expect FAIL.
  - [ ] Implement `transition` with the spec's state table; add routes
        `POST /admin/refunds/:id/approve` and `/reject`.
  - [ ] Build RefundQueue listing `requested` items, oldest first.
  - [ ] Run tests; expect pass. Commit `feat(refunds): agent review`.
- Verify: `npx vitest run tests/refunds/review.api.test.ts` → all pass.

### T004 Pay out approved refunds (P2 slice) — covers FR-006, NFR-002, SC-002
- Files: src/refunds/service.ts (modify), src/payments/webhooks.ts (modify),
  tests/refunds/payout.test.ts (new)
- Consumes: `transition` (T003), `PaymentsClient.refund(chargeId, amountCents, { idempotencyKey })`.
- Depends on: T003
- Steps:
  - [ ] Write tests with the provider client faked: approval calls refund once with
        `idempotencyKey = request.id`; replaying approval sends the same key;
        API success leaves status `approved`; webhook `refund.succeeded` → `refunded`;
        `refund.failed` → `failed`; agent retry from `failed` reuses the key;
        histogram `refund.time_to_refunded_seconds` observed once.
  - [ ] Run `npx vitest run tests/refunds/payout.test.ts`; expect FAIL.
  - [ ] Implement payout on approval and webhook handling.
  - [ ] Run tests; expect pass. Commit `feat(refunds): payout via provider`.
- Verify: `npx vitest run tests/refunds/payout.test.ts` → all pass; provider
  sandbox run in staging shows one refund per request.

### Checkpoint B (P2 complete)
- [ ] Full gate green. Sandbox end-to-end: request → approve → webhook → `refunded`.

### T005 [P] Customer sees refund status (P3) — covers US3, NFR-003
- Files: src/web/orders/RefundStatus.tsx (new), tests/web/RefundStatus.test.tsx (new)
- Consumes: `GET /orders/:orderId/items/:itemId/refunds` (T002).
- Depends on: T004
- Steps:
  - [ ] Write render tests: one label per status ("Requested", "Approved",
        "Rejected: <reason>", "Refunded", "Failed, support will retry"); jest-axe 0 violations.
  - [ ] Run the test; expect FAIL. Implement. Run; expect pass. Commit.
- Verify: `npx vitest run tests/web/RefundStatus.test.tsx` → all pass.

### T006 [P] Status emails (P3) — covers FR-007
- Files: src/refunds/notify.ts (new), tests/refunds/notify.test.ts (new)
- Consumes: event `refund.status_changed` (T003). Does not edit service.ts.
- Depends on: T004
- Steps:
  - [ ] Write test: `rejected` and `refunded` events send one email each;
        `approved`, `requested`, `failed` send none.
  - [ ] Run the test; expect FAIL. Implement the subscriber. Run; expect pass. Commit.
- Verify: `npx vitest run tests/refunds/notify.test.ts` → all pass.

### Checkpoint C (done)
- [ ] Full gate green; spec-analysis analyze mode reports no Critical/High findings.

## Coverage map
| Requirement | Tasks |
|---|---|
| FR-001, FR-002, FR-003, FR-009 | T002 |
| FR-004 | T001, T002 |
| FR-005 | T003 |
| FR-006, NFR-002 | T004 |
| FR-007 | T006 |
| FR-008 | T001, T003 |
| NFR-001 | Checkpoint A |
| NFR-003 | T002, T005 |
| SC-002 | T004 |

## Risks and mitigations
| Risk | Impact | Mitigation | Owner |
|---|---|---|---|
| Webhook arrives before approval commit | Status stuck at `approved` | Webhook looks up by idempotency key; retries 3 times | T004 implementer |
| Provider sandbox differs from production | Payout bugs in prod | Feature flag; first week limited to staff accounts | Payments team |

## Integration order and shared files
Shared-file owner: T004 implementer owns `src/refunds/service.ts` after T003.
Integration order: T001 → T002 → (A) → T003 → T004 → (B) → T005 ∥ T006 → (C).
````

## Why it is shaped this way

| Decision | Reason |
|---|---|
| T001 is a horizontal foundation | Migrations must run in order and have their own up/down test; every slice needs the table |
| T002 bundles policy, route, and form | One vertical slice; P1 is shippable after Checkpoint A |
| `transition` is defined once in T003 | Single place for state rules and audit; T004 and T006 consume it, never duplicate it |
| T004 depends on T003 although files overlap only in service.ts | Shared file and consumed interface; not parallel |
| T005 and T006 are `[P]` | Different files; both depend only on T004; neither changes a shared contract |
| NFR-001 lives in a checkpoint | A load test proves a property of the slice, not of one task |
| Exact messages and numbers in steps | The implementer can write exactly one reasonable test from each step |

Sources: adapted from obra/superpowers (MIT) `skills/writing-plans/SKILL.md`, addyosmani/agent-skills (MIT) `skills/planning-and-task-breakdown/SKILL.md`, github/spec-kit (MIT) `templates/tasks-template.md`, and general practice.
