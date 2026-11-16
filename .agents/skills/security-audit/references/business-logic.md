# Business Logic, Race Conditions, and Feature Abuse

Open this file for workflows with money, credits, quotas, inventory, approvals, invitations, coupons, voting, or multi-step state; for anything that does check-then-act on shared state; and for export, import, search, and notification features that legitimate users can bend. Scanners rarely find these, and they often carry the highest real impact.

## Core rule

Write the business invariant in one sentence, then try to break it with inputs and orderings the UI never sends. Examples: "a coupon is redeemed at most once per account", "a user's balance never goes negative", "an order cannot ship before payment is captured", "only the document owner can change sharing". A finding is a reachable path that violates the invariant for another principal or for the operator.

## Classes

### Race conditions (check-then-act)

Two concurrent requests both pass a check before either one writes.

```python
# Vulnerable: both requests read balance=100 and both withdraw 100
acct = Account.objects.get(pk=pk)
if acct.balance >= amount:
    acct.balance -= amount
    acct.save()

# Safe: atomic conditional update
updated = Account.objects.filter(pk=pk, balance__gte=amount).update(balance=F("balance") - amount)
if updated == 0:
    raise InsufficientFunds()
# Or: select_for_update() inside transaction.atomic()
```

```js
// Vulnerable: redeem coupon
const c = await db.coupon.findUnique({ where: { code } });
if (c.usedAt) throw new Error('used');
await db.coupon.update({ where: { code }, data: { usedAt: new Date(), userId } });
// Safe: conditional update returns count
const { count } = await db.coupon.updateMany({ where: { code, usedAt: null }, data: { usedAt: new Date(), userId } });
if (count !== 1) throw new Error('used');
```

Equivalents: Rails `with_lock`, `lock!`, or `update_all` with conditions plus unique indexes; Spring `@Version` optimistic locking, `PESSIMISTIC_WRITE`, or conditional `UPDATE`; Laravel `lockForUpdate()` inside `DB::transaction`; Go `SELECT ... FOR UPDATE` in a `tx`, or `UPDATE ... WHERE ... RETURNING`.

Where to look: balance and credit changes, coupon and gift-card redemption, invite acceptance with seat limits, vote/like counters with "once per user" rules, rate-limit counters read then written, file quota checks before upload, idempotency keys checked but not reserved atomically, `INSERT` after `SELECT` existence checks without a unique constraint.

Transaction isolation: `READ COMMITTED` (Postgres default) does not prevent lost updates in read-modify-write. A transaction alone is not a lock.

Red flags: `get` then `save` on counters; `if not exists: create` with no unique index; Redis `GET` then `SET` instead of `INCR`/`SETNX`/Lua; in-memory locks (`Mutex`, `synchronized`) in a multi-instance deployment.

### State machine violations

- Skip steps: call `POST /orders/:id/ship` before `/pay`. Check that each transition validates the **current** state server-side.
- Replay: re-submit a completed step (confirm payment twice, accept an invite after it was revoked).
- Go backwards: cancel after fulfilment to get a refund while keeping the goods.
- Partial failure: step 2 of 3 fails; is step 1 rolled back or left granting value?
- Parallel flows: two checkout sessions for one cart.

### Numeric and quantity manipulation

- Negative quantities or amounts (`qty: -5` producing a credit), zero-price items, and transfers to yourself.
- Floating-point money (`0.1 + 0.2`), rounding each line vs the total, currency mismatch between cart and payment.
- Integer overflow in languages with fixed-width integers (Go `int32`, Java `int`), or unchecked casts.
- String/number coercion: `"10" + 5` in JS, PHP loose comparison (`"0e123" == "0e456"` is true, `0 == "abc"` was true before PHP 8), `in_array` without strict mode.
- Client-supplied price, discount, or total accepted by the server. The server must recompute from its own catalog.

### Trusting client or intermediate state

- Hidden form fields or JWT claims carrying `price`, `role`, `plan`, `tenantId`, or `approved: true`.
- Multi-step wizards that carry decisions in client state between steps.
- Server-side data assumed validated because another path validated it on the way in (import, admin API, and migration paths may skip validation).

### Feature abuse

| Feature | Abuse to check |
|---|---|
| Export / backup / report | Includes other tenants, deleted records, hidden fields, or data above the requester's role |
| Import / restore | Overwrites existing records, sets owner or tenant fields, bypasses validation |
| Search, filter, sort | Filters on fields the user cannot see (`?filter[salary][gt]=100000`) reveal values through result sets; sort order leaks hidden values |
| Invitations and sharing | Invite yourself into another org; share links that grant more than intended or never expire; accept an invite meant for another email |
| Notifications and webhooks | User-set URL becomes SSRF (see the SSRF reference); notification content leaks private data to removed members |
| Referral, trial, and free-tier | Unlimited trials by email aliases; self-referral; credits granted before verification |
| Undo, restore, revision history | Restores a version with permissions the user no longer has |
| Preview and draft | Preview tokens unlock more than one item; drafts visible via API listing, RSS, or sitemap |
| Account deletion | Leaves sessions, API keys, or memberships working |

### Time-based logic

Expiry compared with the client's clock, timezone mismatches between services, boundary checks using `<` vs `<=`, and windows where a revoked permission stays cached.

### Fail-open defaults

What happens when a feature flag is off, config is missing, the auth provider times out, or a dependency is down? Look for `try { check() } catch { /* allow */ }`, `if (!policy) return true`, and permissive defaults in config loaders.

## Search commands

```bash
rg -n -e 'balance|credit|quota|coupon|voucher|redeem|refund|payout|inventory|stock|seats?' -g '!*.test.*' -l
rg -n -e 'select_for_update|lockForUpdate|with_lock|FOR UPDATE|@Version|LockModeType|SETNX|WATCH\s' 
rg -n -e 'catch\s*(\(\w*\))?\s*\{\s*(return\s+true|next\(\)|\}|//)' -e 'except\s*(Exception)?\s*:\s*(pass|return True)'
rg -n -e 'req\.body\.(price|amount|total|discount|role|plan)' -e 'params\[:(price|amount|role|plan)\]' -e '\$request->(price|amount|role)'
```

## Validate without harm

- Races: use a **deterministic** local harness rather than flooding. Two threads or async tasks against a local test database, or a test that injects a pause between check and write (a hook, mock, or debugger breakpoint). Show the invariant broken once with dummy accounts. Never race a shared or production system.
- State machine: call transitions out of order in an integration test against a local instance.
- Numeric: submit the boundary value (negative, zero, max) for a dummy cart and read the resulting dummy balance.
- Feature abuse: two dummy tenants, one export or import operation, and a check of the produced artifact.

## False-positive traps

| Looks bad | Check before reporting |
|---|---|
| Read-modify-write on a counter | A unique index, DB constraint, or serializable isolation may still prevent the bad state. Check schema and migrations |
| Negative quantity accepted by the API | Downstream validation or a DB `CHECK` constraint may reject it |
| Race window exists | Impact must be a violated invariant with value (double redemption, overdraft), not a duplicate log line |
| Self-abuse of free features | Unlimited trials or self-referral are often product decisions. Report as business risk only if the product states the limit |
| Client sends price | Server may ignore it and recompute. Trace what is persisted and charged |

## Severity guidance

Business-logic severity follows the value at stake.

| Result | Typical severity |
|---|---|
| Unbounded creation of money or credits; purchase without payment; cross-tenant export | High to Critical |
| Double-redemption of single-use value with limited amounts; approval bypass for a sensitive workflow | Medium to High |
| Quota bypass with operator cost; limited inventory oversell | Medium |
| Extra trials, self-referral, or races producing harmless duplicates | Low or business note |

Fix pattern: enforce the invariant in one atomic operation in the data store (conditional update, unique constraint, row lock), recompute prices server-side, validate state transitions server-side, and add a concurrency regression test.

Sources: adapted from cloudflare/security-audit-skill (MIT) and general practice.
