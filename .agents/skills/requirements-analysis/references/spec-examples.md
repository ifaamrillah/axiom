# Spec Examples: Weak vs Good

Two specs for the same feature: self-service refund requests (the feature from the product-discovery worked example). The weak spec is typical of a first draft. The good spec is what this skill should produce. Annotations explain each difference.

## Weak spec (do not imitate)

```markdown
# Refunds

Customers should be able to easily request refunds. Support will review them
quickly. The system should be secure and fast.

## Requirements
1. Add a refund button on the order page.            <!-- W1 -->
2. Customers can request refunds for their orders.   <!-- W2 -->
3. Admins approve or reject refunds.                 <!-- W3 -->
4. Use the Stripe API to refund.                     <!-- W4 -->
5. Send notifications.                               <!-- W5 -->
6. Handle errors appropriately.                      <!-- W6 -->
7. Should be fast and scalable.                      <!-- W7 -->

## Acceptance
- Refunds work.                                      <!-- W8 -->
```

| Mark | Problem | Why it hurts |
|---|---|---|
| Intro | "easily", "quickly", "secure", "fast" | Untestable adjectives. Nobody can fail this spec. |
| W1 | UI solution, not behavior | Locks in a design. Says nothing about what happens after the click. |
| W2 | "their orders": all orders? Undelivered ones? Any age? | Missing the 30-day window, the delivered condition, and the per-item scope. |
| W3 | "Admins" vs "support agents" elsewhere | Terminology drift. Which role? Can agents approve their own requests? |
| W3 | No rejection reason, no states | The pre-mortem risk from discovery is lost. |
| W4 | Vendor detail as a requirement | An implementation choice. Fine as a constraint only if it is real; the code wraps the provider already. |
| W5 | Who is notified, when, through which channel? | Three interpretations at least. |
| W6 | "appropriately" | Decides nothing. Every error path is unspecified. |
| W7 | No numbers, no conditions | Cannot be measured or tested. |
| W8 | Single acceptance line | No scenarios, no failure paths, no traceability. |
| Missing | Amount limits, duplicates, money rounding, audit, permissions, non-goals | The two hard rules from discovery (never over-refund, one open request) do not appear at all. |

## Good spec (excerpt)

```markdown
---
id: SPEC-014
status: clarified
owner: payments team
updated: 2026-11-16
---

# Feature Specification: Self-service refund requests

## Context and problem
Support handles ~120 refund emails a week (~10 min each). Slow refunds cause
chargebacks ($15 each). See discovery brief.

## Goals
- Customers request refunds for damaged or wrong items without emailing support.
- Every refund is reviewed by a support agent before money moves.

## Non-goals
Physical returns, automatic approval, store credit, partial-quantity refunds.

## User stories (prioritized)

### US1 (P1): Customer requests a refund for a delivered item
As a customer, I want to request a refund for a damaged or wrong item so that I
get my money back without emailing support.

**Independent test:** with a delivered order seeded, a customer submits a request
and it appears as `requested` in the agent queue.

**Acceptance scenarios:**
1. **Given** an order item delivered 10 days ago and paid $40.00, **When** the
   customer requests a refund of $40.00 with reason "damaged", **Then** a request
   is created with status `requested` and the customer sees "Request received".
2. **Given** an order item delivered 31 days ago, **When** the customer opens the
   refund form, **Then** the form is not offered and the page shows "Refund window
   closed (30 days from delivery)".
3. **Given** an item with an open request, **When** the customer requests again,
   **Then** no new request is created and the page shows the existing request.

### US2 (P2): Agent approves or rejects a request
...

### US3 (P3): Customer sees request status
...

## Functional requirements
- **FR-001**: System MUST allow a customer to request a refund for an order item
  they own whose `deliveredAt` is at most 30 days before the request time.
- **FR-002**: System MUST reject requests outside the window and show the reason.
- **FR-003**: Requested amount MUST be > 0 and ≤ (price paid for the item − sum of
  completed refunds for that item), in the order's currency, in minor units.
- **FR-004**: System MUST allow at most one open request (`requested` or
  `approved`) per order item.
- **FR-005**: Only users with role `support_agent` MUST be able to approve or
  reject. Rejection MUST include a reason of 10–500 characters.
- **FR-006**: On approval, System MUST issue the refund to the original payment
  method and set status `refunded` only after the provider confirms.
- **FR-007**: System MUST email the customer when status becomes `rejected` or
  `refunded`. [NEEDS CLARIFICATION: also on `approved`?]
- **FR-008**: System MUST record an audit entry (actor, old status, new status,
  timestamp, reason) for every status change.

## Non-functional requirements
- **NFR-001**: Request submission responds in ≤ 500 ms p95 server time at 20
  requests/second sustained, measured in staging.
- **NFR-002**: Provider refund calls MUST be idempotent: retrying an approval
  never refunds twice (idempotency key = request ID).
- **NFR-003**: Refund form meets WCAG 2.2 AA.

## Key entities
- **RefundRequest**: order item, customer, amount (minor units), currency,
  reason, status (requested | approved | rejected | refunded | failed),
  timestamps. One open request per order item.

## Edge cases and failure modes
- Provider call fails or times out after approval: status `failed`, agent can
  retry; no double refund (NFR-002).
- Order paid partly by gift card: [NEEDS CLARIFICATION: refund gift-card share to
  gift card, or exclude these orders in v1?]
- Customer and agent act at the same moment (agent approves while customer
  cancels): see Clarifications.

## Security and privacy
Customers see only their own requests. Agents cannot approve requests on orders
they placed themselves. Reason text is user input: escape on display.

## Success criteria
- SC-001: Refund emails to support < 60/week within 8 weeks of launch (baseline ~120).
- SC-002: 95% of approved refunds reach `refunded` within 1 hour of approval.

## Assumptions
- Refunds go to the original payment method only.

## Clarifications
- 2026-11-16 Q: Can customers cancel an open request? → A: Not in v1 (affects US1, FR-004).
```

## What makes the good spec good

| Property | Where you see it |
|---|---|
| Behavior, not UI design | FR-001 says what is allowed; no button is mentioned |
| Exact values | 30 days, `deliveredAt`, minor units, 10–500 characters |
| One term per concept | "support agent" and `support_agent` everywhere; "order item", never "product" |
| Failure paths specified | Scenarios 2 and 3; provider failure; concurrency |
| Hard rules from discovery kept | FR-003 (never over-refund), FR-004 (one open request), FR-005 (reason) |
| Unknowns marked, not guessed | Two `[NEEDS CLARIFICATION]` markers; both on non-P1 behavior |
| Measurable NFRs | Percentile, load, environment; idempotency stated as a rule |
| Non-goals stated | Stops scope creep in planning |
| Success criteria separate from requirements | SC-001 is a business outcome; SC-002 needs buildable monitoring |
| Traceability | Clarification names the affected IDs |

## Rewrite patterns

| Weak phrasing | Rewrite |
|---|---|
| "Customers can request refunds" | "System MUST allow a customer to request a refund for an order item they own, delivered ≤ 30 days ago" |
| "Admins approve refunds" | "Only `support_agent` users MUST be able to approve or reject; rejection requires a 10–500 character reason" |
| "Send notifications" | "System MUST email the customer when status becomes `rejected` or `refunded`" |
| "Handle errors appropriately" | One edge-case line per named failure, each with the resulting state and message |
| "Use Stripe" | Move to plan, or keep as a constraint with the reason ("existing provider contract") |
| "Fast" | "≤ 500 ms p95 server time at 20 req/s in staging" |
| "Secure" | Name the actor, the asset, and the rule: "Customers see only their own requests" |

Sources: adapted from github/spec-kit (MIT) `templates/spec-template.md` and `templates/commands/specify.md`, addyosmani/agent-skills (MIT) `skills/spec-driven-development/SKILL.md`, and general practice.
