# Worked Discovery Example

A full discovery session for a vague request, followed by the approach comparison and the approved brief. Use it as a model for pacing, question choice, and the shape of the output. The same feature continues in the requirements-analysis, task-planning, and spec-analysis examples.

## The request

> "Customers keep emailing us about refunds. Can we add some kind of self-service refund thing?"

## Step 1: check context before asking

The agent reads the repository first and notes what it already knows:

- `src/orders/order.ts` has `status` and `deliveredAt`. Orders have line items with `pricePaidCents`.
- `src/payments/client.ts` wraps the payment provider and already has `refund(chargeId, amountCents)`, used only by an internal script.
- `docs/support.md` says support refunds through the provider dashboard by hand.
- No refund table exists. No admin UI exists; staff use a small internal tool at `src/admin/`.

These facts remove at least four questions. The agent will not ask "which payment provider?" or "do orders have a delivery date?".

## Step 2: the dialogue

Each turn shows the technique and why that question came next.

**Q1 (5 whys, highest impact):**
> Agent: Before options, what hurts most today: support time spent on refund emails, slow refunds annoying customers, or chargebacks? I'd guess support time.
>
> User: Support time. About 120 refund emails a week, each takes 10 minutes. And some customers file chargebacks when we're slow, which cost us $15 each.

*Why this first:* the problem decides everything else. Two costs now exist: support time and chargeback fees.

**Q2 (jobs to be done):**
> Agent: When a customer asks for a refund, what do most of them want: money back for a damaged or wrong item, or to return an unwanted item? I'd scope version one to damaged or wrong items, with no physical return.
>
> User: Mostly damaged or wrong. Returns are a separate process with the warehouse. Leave returns out.

*Why:* this cut removes a warehouse integration. Returns become a non-goal.

**Q3 (user journey, decision point):**
> Agent: Who decides whether a refund goes through? Options: (a) automatic for everything, (b) a support agent approves each one, (c) automatic under a threshold, agent above it. I recommend (b) for version one, because we have no fraud data yet.
>
> User: (b). Finance would never accept automatic yet.

*Why:* the approval model changes the data model, the UI, and the risk profile.

**Q4 (edge-case sweep, policy):**
> Agent: Is there a time window? I'd propose 30 days from delivery, counted from `deliveredAt`.
>
> User: 30 days, yes.

**Q5 (constraint inversion):**
> Agent: If this had to ship in two weeks, I'd skip a new admin screen and add an "approve / reject" list to the existing internal tool in `src/admin/`. OK?
>
> User: Fine, the internal tool is what support lives in anyway.

**Q6 (success signal):**
> Agent: How will we know it worked? I suggest: refund emails drop from about 120 a week to under 60 within 8 weeks of launch, and chargebacks for "refund not processed" drop. Do you track chargeback reasons?
>
> User: We get a monthly report with reasons. Use both.

**Q7 (pre-mortem, last question):**
> Agent: Imagine we roll this back in three months. The most likely reason I see: customers request refunds above what they paid, or twice for the same item, and finance loses money. I'll make "never refund more than was paid" and "one open request per item" hard rules. Anything else that would make you roll it back?
>
> User: Agents forgetting why they rejected something. Make them give a reason.

*Stop:* seven questions asked. Problem, outcome, users, scope, constraints, and the top risk are now Clear. Remaining unknowns become assumptions.

## Step 3: approach comparison

Use this template whenever you propose approaches. Keep to 2–3 real options. A strawman option does not count.

| | A. Request form + agent approval in internal tool | B. Request form + auto-approve under $50 | C. Email-based: form emails support with approve and reject links |
|---|---|---|---|
| **Value** | Removes most email back-and-forth; full control | Fastest refunds for small amounts | Removes form-to-email typing only |
| **Cost** | Medium: new table, form, admin list | Medium plus fraud rules | Low |
| **Risk** | Low: every refund reviewed | Fraud with no data to tune the threshold | Links in email can be forwarded; weak audit |
| **Reversibility** | High: can add auto-approve later | Medium: customers get used to instant refunds | High |
| **Time to first value** | ~2 weeks | ~3 weeks | ~1 week |
| **Fits constraints** | Yes | Conflicts with finance (Q3) | Weak audit trail |

**Recommendation:** A. It meets the finance constraint, keeps an audit trail, and leaves auto-approve as a later, data-driven step. C is cheaper but fails the pre-mortem concern about rejection reasons and audit.

Present the recommendation first, then the table. Ask for a choice in one question: "Go with A?"

## Step 4: the brief the user approved

```markdown
# Discovery Brief: Self-service refund requests

## Problem and affected users
Support handles ~120 refund emails a week at ~10 minutes each. Slow refunds cause
chargebacks at $15 each. Affected: customers with damaged or wrong items; support agents.

## Desired outcomes and success signals
- Refund emails drop from ~120/week to under 60/week within 8 weeks of launch.
- "Refund not processed" chargebacks drop (baseline: monthly chargeback report).

## Current behavior and evidence
Support refunds by hand in the provider dashboard (docs/support.md).
`PaymentsClient.refund` exists but only an internal script uses it.

## Constraints and dependencies
Finance requires a human approval on every refund (v1). Existing internal tool in src/admin/.

## Assumptions and open decisions
- Assumption: refunds go to the original payment method only.
- Assumption: email is the only customer notification channel.
- Open: gift-card-paid orders (deferred to requirements).

## Options considered
A (chosen), B (rejected: conflicts with finance), C (rejected: weak audit). See table.

## Scope and non-goals
In: request form for delivered items within 30 days; agent approve/reject with reason;
refund via provider; status visible to customer.
Out: physical returns, auto-approval, store credit, partial-quantity refunds.

## Approval
Approved by: <owner> on <YYYY-MM-DD> (covers this brief as written)

## Recommended next step
Requirements analysis: write spec.md for US1 (request), US2 (approve/reject), US3 (status).
```

## What made this session work

- The agent read the code first and never asked what it could see.
- Each question carried a recommendation, so most answers were one word.
- Every answer either cut scope or set a hard rule.
- The pre-mortem turned two vague fears into testable rules.
- The session stopped at seven questions and wrote the rest down as assumptions.

## Common discovery failures

| Failure | Do instead |
|---|---|
| Asking a list of ten questions in one message | Ask one, update, choose the next |
| Accepting "make it easy to use" as an outcome | Ask for a number with a baseline |
| Designing the database during discovery | Stay at problem, outcome, scope; design comes later |
| Presenting one option | Present 2–3 with a recommendation |
| Treating "sounds good" to an idea as approval | Write the brief; get approval on the brief |
| Continuing to ask after the user says "just build it" | Stop, list assumptions, continue |

Sources: adapted from obra/superpowers (MIT) `skills/brainstorming/SKILL.md`, addyosmani/agent-skills (MIT) `skills/idea-refine/examples.md` and `skills/idea-refine/refinement-criteria.md`, and general practice.
