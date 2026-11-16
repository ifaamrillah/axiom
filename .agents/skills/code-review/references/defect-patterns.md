# Defect Pattern Catalog

Common defects that pass tests and look reasonable in a diff. Each entry gives the shape to look for, a bad snippet, a fixed snippet, and a review question. Use it during procedure step 3 (correctness) when the diff touches the named area.

Snippets are minimal. The language is the one where the defect is most common; the pattern applies across languages.

## How to use

1. Classify each changed hunk by the areas it touches (shared state, I/O, money, time, queries, user input).
2. Open only the matching sections below.
3. For each match, confirm the defect against the real code path before reporting. A pattern match is a lead, not a finding.

## 1. Concurrency and shared state

**Check-then-act race.** Two requests both pass the check, then both act.

```python
# Bad: two concurrent redemptions both see remaining > 0
coupon = Coupon.objects.get(code=code)
if coupon.remaining > 0:
    coupon.remaining -= 1
    coupon.save()

# Good: let the database enforce it atomically
updated = Coupon.objects.filter(code=code, remaining__gt=0).update(remaining=F("remaining") - 1)
if updated == 0:
    raise CouponExhausted(code)
```

**Unsynchronized map or counter.**

```go
// Bad: concurrent map writes panic in Go
var cache = map[string]int{}
func Hit(k string) { cache[k]++ }

// Good
var (mu sync.Mutex; cache = map[string]int{})
func Hit(k string) { mu.Lock(); defer mu.Unlock(); cache[k]++ }
```

**Async fire-and-forget.** A promise is not awaited, so errors vanish and ordering breaks.

```ts
// Bad: forEach ignores returned promises; the function returns before saves finish
items.forEach(async (i) => { await save(i); });

// Good
await Promise.all(items.map((i) => save(i)));   // or a for...of loop if order matters
```

Review questions: What shared state does this touch? What happens when two callers run it at once? Is there a unique constraint, lock, or atomic update that makes it safe? Are goroutines, threads, or tasks ever joined and their errors collected?

## 2. Error handling

**Swallowed error.**

```java
// Bad: failure becomes silent success
try { repo.save(order); } catch (Exception e) { log.debug("save failed"); }

// Good: handle what you can, rethrow what you cannot
try { repo.save(order); }
catch (OptimisticLockException e) { throw new ConflictException(order.id(), e); }
```

**Lost cause.** Wrapping without the original error destroys the stack trace.

```go
// Bad
if err != nil { return errors.New("load failed") }
// Good
if err != nil { return fmt.Errorf("load user %d: %w", id, err) }
```

**Partial failure without compensation.** The second of two writes fails and the first is not rolled back.

```python
# Bad
charge = payments.charge(card, total)
db.insert_order(order)          # if this raises, the customer is charged with no order

# Good: write the intent first, then reconcile; or use one transaction when both live in one DB
order = db.insert_order(order, status="pending")
charge = payments.charge(card, total, idempotency_key=order.id)
db.mark_paid(order.id, charge.id)
```

Review questions: Which errors can each call raise? Which are caught, and is the handler correct for every one? Does the caller learn about the failure? Is a retry safe (idempotent)?

## 3. Resource leaks

```python
# Bad: file handle leaks if parse() raises
f = open(path); data = parse(f.read()); f.close()
# Good
with open(path) as f:
    data = parse(f.read())
```

```go
// Bad: response body never closed; connection pool drains
resp, err := http.Get(url)
if err != nil { return err }
return json.NewDecoder(resp.Body).Decode(&out)
// Good
resp, err := http.Get(url)
if err != nil { return err }
defer resp.Body.Close()
```

```java
// Bad: connection not closed on exception
Connection c = ds.getConnection(); PreparedStatement ps = c.prepareStatement(sql); ...
// Good
try (Connection c = ds.getConnection(); PreparedStatement ps = c.prepareStatement(sql)) { ... }
```

Also look for: timers and listeners never removed (`setInterval`, `addEventListener`, `useEffect` without cleanup), goroutines blocked forever on a channel nobody reads, temp files never deleted, HTTP clients with no timeout.

## 4. N+1 queries and unbounded work

```python
# Bad: one query per order
for order in Order.objects.filter(user=u):
    print(order.customer.name)
# Good
for order in Order.objects.filter(user=u).select_related("customer"):
    print(order.customer.name)
```

```php
// Bad (Laravel)
foreach (Post::all() as $post) { echo $post->author->name; }
// Good
foreach (Post::with('author')->get() as $post) { echo $post->author->name; }
```

```ts
// Bad: sequential awaits inside a loop, one round trip each
for (const id of ids) results.push(await api.get(id));
// Good: batch endpoint, or bounded concurrency
const results = await api.getMany(ids);
```

Also flag: `findAll()` or `SELECT *` without `LIMIT` on a growing table, loading a whole table into memory to count it, list endpoints without pagination, regexes with nested quantifiers on user input (catastrophic backtracking).

## 5. Off-by-one and boundaries

```ts
// Bad: skips the last page when total is an exact multiple
const pages = Math.floor(total / size);
// Good
const pages = Math.ceil(total / size);
```

```python
# Bad: inclusive end silently drops the last day
rows = db.query("... WHERE created_at BETWEEN %s AND %s", (start, end_date))  # end_date at 00:00
# Good: half-open interval
rows = db.query("... WHERE created_at >= %s AND created_at < %s", (start, end_date + timedelta(days=1)))
```

Check: `<` vs `<=` at each limit, slice ends (`[a:b]` excludes `b`), loop bounds over `len - 1`, empty collection, single element, exactly-at-limit values, and fencepost counts (n items have n-1 gaps).

## 6. Time and time zones

```python
# Bad: naive local time; wrong on servers in other zones and around DST
expires = datetime.now() + timedelta(hours=24)
# Good: store and compare in UTC; convert at display time
expires = datetime.now(timezone.utc) + timedelta(hours=24)
```

```ts
// Bad: "2026-03-08" parses as UTC midnight, which is the previous day in the Americas
new Date("2026-03-08").getDate();
// Good: treat calendar dates as dates, not instants (a date library or explicit parts)
```

Check: naive vs aware timestamps mixed, "add one day" implemented as +24h across a DST change, `LocalDateTime` stored for an instant, cron schedules in local time, expiry compared with `>` vs `>=`, client clock trusted for ordering, durations measured with wall clock instead of a monotonic clock (`time.monotonic()`, `performance.now()`, `System.nanoTime()`).

## 7. Money and rounding

```js
// Bad: binary floats
0.1 + 0.2 === 0.3            // false
const total = price * qty * 1.11;
// Good: integer minor units, round once at a defined point
const totalCents = Math.round(priceCents * qty * 111 / 100);
```

```python
# Good: Decimal with explicit rounding mode
from decimal import Decimal, ROUND_HALF_EVEN
tax = (subtotal * Decimal("0.11")).quantize(Decimal("0.01"), rounding=ROUND_HALF_EVEN)
```

Check: floats for currency, rounding per line vs per total (results differ; the spec must say which), split payments whose parts do not sum to the whole, currency missing from the value (amount without currency code), currencies with 0 or 3 decimal places (JPY has 0, KWD has 3; IDR is 2 in ISO 4217 but often 0 in practice).

## 8. Null and missing values

```ts
// Bad: 0 and "" are valid but falsy
const limit = req.query.limit || 50;
// Good
const limit = req.query.limit ?? 50;
```

```kotlin
// Bad: !! turns a known-nullable into a crash
val email = user.profile!!.email
// Good: decide what absence means
val email = user.profile?.email ?: return Result.failure(MissingProfile(user.id))
```

```java
// Bad: Optional.get() without a check is a NullPointerException with a different name
String name = repo.findName(id).get();
```

Check: optional chaining that hides a bug (`a?.b?.c` where `a` must exist), `None` default arguments that are mutable (`def f(x=[])`), JSON fields that may be absent vs null vs empty, SQL `NULL` in comparisons (`col <> 'x'` excludes NULL rows), and `NOT IN` with a subquery that can return NULL (matches nothing).

## 9. Injection

```python
# Bad: SQL built from input
cur.execute(f"SELECT * FROM users WHERE email = '{email}'")
# Good
cur.execute("SELECT * FROM users WHERE email = %s", (email,))
```

```js
// Bad: shell injection
exec(`convert ${file} out.png`);
// Good: no shell, argument array
execFile("convert", [file, "out.png"]);
```

```php
// Bad: raw expression with input
User::whereRaw("name = '$name'")->get();
// Good
User::whereRaw('name = ?', [$name])->get();
```

Also: XSS through `innerHTML`, `dangerouslySetInnerHTML`, `{!! !!}` in Blade, `|safe` in Jinja; path traversal (`../`) when joining user input to a path; SSRF when fetching a user-supplied URL; template injection; LDAP and NoSQL operator injection (`{"$ne": null}`); log injection via newlines. Sort columns and table names cannot be parameterized: allow-list them.

## 10. State, caching, and idempotency

- Cache key missing a dimension (tenant, locale, permissions), so one user sees another's data.
- Cache not invalidated on write, or invalidated before the write commits.
- Retried webhook or job processed twice because there is no idempotency key or unique constraint.
- State machine allows an invalid transition (refund a pending order, ship a cancelled one).
- Mutable default or module-level state shared across requests.

## Red flags in a diff

| Red flag | Look for |
|---|---|
| `catch`/`except` broadened | Errors that used to surface now vanish |
| New loop containing an `await`, a query, or an HTTP call | N+1 or serial latency |
| `float`/`double`/`number` near a price or balance | Rounding defects |
| `now()` without a zone | Time zone defects |
| String concatenation or interpolation building SQL, shell, HTML, or a path | Injection |
| New global, static, or module-level mutable variable | Cross-request leakage, races |
| Read, modify, write on a row without a lock or condition | Lost update |
| Timeout, retry, or limit removed or set to 0 | Hangs and unbounded work |

Sources: adapted from addyosmani/agent-skills (MIT) (`skills/code-review-and-quality`, `skills/performance-optimization`) and general practice.
