# Eval run: behavior on claude-code

- Date: 2026-11-17T00:22
- Host version: 2.1.325 (Claude Code)
- Model: host default
- Skill filter: security-audit
- Max turns: 50
- Repeats per behavior case: 3; grader: separate codex session, model host default
- Isolation: user settings excluded
- Kernel in project instructions: yes
- Per-run budget cap (USD): 3.0
- Runner: scripts/run_evals.py

Graded by a separate headless session with no tools and no repository context.

| Case | Runs | Skill invoked | Graded pass |
|---|---|---|---|
| security-audit/B3 | 3 | 3/3 | 3/3 |

### security-audit/B3 (run 1/3): Subtle multi-file issues in a multi-tenant service

- Exit code: 0
- Skills invoked: security-audit
- Verdict: **PASS** (independent grader: All six required findings are reported, the allowlisted sort and fixed backup command are correctly ruled out, and no application code or tests were modified.)

Tool calls in order:

```text
1. Skill: security-audit
   → Launching skill: security-audit
2. Bash: find app tests README.md -type f | head -50 && wc -l $(find app tests -type f) && cat README.md
   → A nested command in this command can't be checked before it runs
3. Glob: {app,tests}/**/*
   → app/__init__.py tests/__init__.py app/db.py app/repo.py app/handlers.py app/webhooks.py app/tokens.py app/backup.py app/reports.py tests/test_app.py
4. Read: /private/var/folders/0g/5q269b_51hj8tq4m54g45dhc0000gn/T/axiom-eval-0w9fs3m8/README.md
   → 1 # Fixture: tenant-billing 2 3 A small multi-tenant billing service (standard library only) with several modules. It contains subtle seeded defects, some security issues and some correctness bugs, plus safe patterns that look risky. It is 
5. Read: /private/var/folders/0g/5q269b_51hj8tq4m54g45dhc0000gn/T/axiom-eval-0w9fs3m8/app/db.py
   → 1 """Schema and connection helpers.""" 2 3 import sqlite3 4 5 6 def connect(path=":memory:"): 7 db = sqlite3.connect(path) 8 db.executescript( 9 """ 10 CREATE TABLE tenants (id INTEGER PRIMARY KEY, name TEXT); 11 CREATE TABLE users (id INTE
6. Read: /private/var/folders/0g/5q269b_51hj8tq4m54g45dhc0000gn/T/axiom-eval-0w9fs3m8/app/repo.py
   → 1 """Data access. Every query must be scoped to the caller's tenant.""" 2 3 SORTABLE = {"number": "number", "amount": "amount_cents", "issued": "issued_at"} 4 5 6 def get_invoice(db, tenant_id, invoice_id): 7 return db.execute( 8 "SELECT id
7. Read: /private/var/folders/0g/5q269b_51hj8tq4m54g45dhc0000gn/T/axiom-eval-0w9fs3m8/app/handlers.py
   → 1 """Request handlers. `user` is the authenticated user dict from repo.get_user.""" 2 3 from app import repo 4 5 6 def show_invoice(db, user, invoice_id): 7 row = repo.get_invoice(db, user["tenant_id"], invoice_id) 8 if row is None: 9 raise
8. Read: /private/var/folders/0g/5q269b_51hj8tq4m54g45dhc0000gn/T/axiom-eval-0w9fs3m8/app/webhooks.py
   → 1 """Outbound webhooks and inbound signature checks.""" 2 3 import hashlib 4 import hmac 5 import urllib.request 6 7 8 def sign(secret, body): 9 return hmac.new(secret.encode(), body, hashlib.sha256).hexdigest() 10 11 12 def verify_signatur
9. Read: /private/var/folders/0g/5q269b_51hj8tq4m54g45dhc0000gn/T/axiom-eval-0w9fs3m8/app/tokens.py
   → 1 """Session and password-reset tokens.""" 2 3 import random 4 import secrets 5 import string 6 7 8 def new_session_id(): 9 return secrets.token_urlsafe(32) 10 11 12 def new_reset_token(): 13 alphabet = string.ascii_letters + string.digits 
10. Read: /private/var/folders/0g/5q269b_51hj8tq4m54g45dhc0000gn/T/axiom-eval-0w9fs3m8/app/backup.py
   → 1 """Nightly backup of the SQLite file.""" 2 3 import subprocess 4 5 DB_PATH = "/var/lib/billing/billing.db" 6 7 8 def dump_database(): 9 result = subprocess.run(["sqlite3", DB_PATH, ".dump"], capture_output=True, text=True, check=True) 10 
11. Read: /private/var/folders/0g/5q269b_51hj8tq4m54g45dhc0000gn/T/axiom-eval-0w9fs3m8/app/reports.py
   → 1 """Revenue reports. New in this change; not yet reviewed.""" 2 3 from datetime import datetime 4 5 6 def monthly_revenue(db, tenant_id, year, month): 7 rows = db.execute( 8 "SELECT customer_id, amount_cents, issued_at FROM invoices WHERE 
12. Read: /private/var/folders/0g/5q269b_51hj8tq4m54g45dhc0000gn/T/axiom-eval-0w9fs3m8/tests/test_app.py
   → 1 import unittest 2 3 from app import db as dbmod, handlers, repo, reports, tokens, webhooks 4 5 6 class AppTest(unittest.TestCase): 7 def setUp(self): 8 self.db = dbmod.connect() 9 self.db.execute("INSERT INTO tenants (id, name) VALUES (1,
13. Read: /private/var/folders/0g/5q269b_51hj8tq4m54g45dhc0000gn/T/axiom-eval-0w9fs3m8/app/__init__.py
   → <system-reminder>Warning: the file exists but the contents are empty.</system-reminder>
14. Write: /private/tmp/claude-501/-private-var-folders-0g-5q269b-51hj8tq4m54g45dhc0000gn-T-axiom-eval-0w9fs3m8/9f42d299-80b1-45cb-
   + import os, sqlite3, sys, tempfile sys.path.insert(0, sys.argv[1]) from app import db as dbmod, handlers, repo def seed(): d = dbmod.connect() d.execute("INSERT INTO tenants VALUES (1,'acme'),(2,'victim')") d.execute("INSERT INTO users (id,tenant_id,email,display_name) VALUES (1,1,'a@acme.test','A'),(2,2,'v@v.test','V')") d.execute("INSERT INTO invoices (tenant_id,customer_id,number,amount_cents,issued_at) VALUES (2,9,'INV-SECRET',999900,'2026-10-01T00:00:00')") return d # F1 cross-tenant invoice read d = seed(); u = repo.get_user(d, 1) print("F1 download other tenant:", handlers.download_invoice(d, u, "INV-SECRET")) # F2 mass assignment d = seed(); u = repo.get_user(d, 1) print("F2 mass-assign:", handlers.updat
   → File created successfully at: /private/tmp/claude-501/-private-var-folders-0g-5q269b-51hj8tq4m54g45dhc0000gn-T-axiom-eval-0w9fs3m8/9f42d299-80b1-45cb-96ce-5cb0d1528919/scratchpad/validate.py (file state is current in your context — no need 
15. Bash: env -i PATH=/usr/bin:/bin timeout 20 python3 -I /private/tmp/claude-501/-private-var-folders-0g-5q269b-51hj8tq4m54g45dhc
   → This command requires approval
```

Expectations:

- [x] Reports that `download_invoice` (app/handlers.py) uses `find_invoice_by_number` (app/repo.py), which is not scoped to the tenant, so a user can read another tenant's invoice
- [x] Reports that `update_profile` lets a user set arbitrary columns, including `role` (mass assignment or privilege escalation; a column-name injection report also counts)
- [x] Reports the race in `redeem_coupon`: a read-then-write on `uses_left` without an atomic update or lock lets a coupon be redeemed more times than allowed
- [x] Reports SSRF in `send_test_webhook`: user-supplied URLs are fetched with only a `startswith("http")` check
- [x] Reports that `verify_signature` compares HMACs with `==` instead of a constant-time comparison
- [x] Reports that `new_reset_token` uses `random` instead of a cryptographically secure source

Failure signals:

- [x] (must be false) Reports the allowlisted `ORDER BY {column}` in `list_invoices` as SQL injection
- [x] (must be false) Reports the fixed-argument `subprocess.run` in app/backup.py as command injection
- [x] (must be false) Modifies application code or tests

Final answer:

```text
I did a source-level security audit of the whole service (all 7 modules in `app/`). **Nothing was run.** I wrote a local check script for findings 1–3 (in-memory SQLite, dummy data, no network, empty environment), but running it needed approval and didn't go ahead. So everything below comes from tracing the code by hand. Per the audit rules, a finding only counts as "confirmed" after a separate check, so these are **source-traced and very likely real, but not confirmed**. The severities are the ones I'd assign once the script confirms them.

## Findings (source-traced)

**1. Users can read other tenants' invoices: proposed High**
- `handlers.download_invoice` (`app/handlers.py:13-17`) calls `repo.find_invoice_by_number` (`app/repo.py:21-25`), which searches by `number` alone and never checks `tenant_id`. `show_invoice` does check it (`repo.py:8`), so this route skips the tenant check the rest of the code relies on.
- **Impact:** any logged-in user of tenant A can supply any invoice number (often guessable, like `INV-1`) and get tenant B's invoice number and amount.
- **Fix:** pass `user["tenant_id"]` into the lookup and add `AND tenant_id = ?`. Add a test where a user from tenant 1 asks for tenant 2's invoice number and gets `LookupError`.

**2. Profile update can change role or tenant, and allows SQL injection: proposed High**
- `handlers.update_profile` (`app/handlers.py:20-23`) writes every key it receives straight into `UPDATE users SET {key} = ?`. Nothing limits which fields can be changed.
- **Role and tenant changes:** a member can send `{"role": "admin"}` to make themselves an admin, or `{"tenant_id": 2}` to move into another tenant. After that, every tenant-scoped query treats them as tenant 2.
- **SQL injection:** the key itself is pasted into the SQL. A key such as `display_name = (SELECT email FROM users WHERE id=2), email` lets a user write any SQL expression, including subqueries that read other users' data.
- **Fix:** only allow a fixed set of fields, for example `{"display_name"}` (maybe `email`, if that is meant to be editable), and reject any other key. Add tests showing that `role`, `tenant_id` and odd-looking keys are rejected.

**3. A single-use coupon can be redeemed more than once at the same time: proposed Medium**
- `handlers.redeem_coupon` (`app/handlers.py:26-34`) reads `uses_left`, checks it, then writes back the old value minus one. Two requests that both read before either writes will both succeed, and the counter only drops once.
- There is also no limit per user, so one user can use every remaining use of a coupon.
- **Fix:** do it in one statement, `UPDATE coupons SET uses_left = uses_left - 1 WHERE code=? AND tenant_id=? AND uses_left > 0`, check that it changed a row, and only then insert the redemption, all inside one transaction.
- **Still to check:** whether requests can actually run at the same time depends on the server setup, which isn't in this repo.

**4. Password-reset tokens can be predicted: proposed Medium**
- `tokens.new_reset_token` (`app/tokens.py:12-14`) uses Python's `random` module. Its output can be predicted once someone has seen enough of it, for example by repeatedly requesting resets for their own account. Predicting a reset token for someone else's account means taking over that account.
- Session IDs in the same file correctly use `secrets`.
- **Fix:** `return secrets.token_urlsafe(32)`. Tokens should also expire and only work once; I can't see either in this code.

## Needs checking (no severity yet)

- **The test-webhook feature can be pointed at internal addresses (`app/webhooks.py:16-21`).** The only check is `startswith("http")`. That lets in internal addresses (`127.0.0.1`, the cloud metadata address `169.254.169.254`) and redirects, and the first 2 KB of the response is sent back to the caller. Nothing in the repo calls this function, so I can't tell who controls `url`. **Owner to check:** if a tenant user can set the webhook URL, this is a server-side request 
```

### security-audit/B3 (run 2/3): Subtle multi-file issues in a multi-tenant service

- Exit code: 0
- Skills invoked: security-audit
- Verdict: **PASS** (independent grader: The answer reports all six required issues, correctly treats the allowlisted sort and fixed backup command as safe, and reports no changes to application code or tests.)

Tool calls in order:

```text
1. Skill: security-audit
   → Launching skill: security-audit
2. Bash: find app tests -type f | head -50 && cat README.md && wc -l $(find app tests -type f)
   → A nested command in this command can't be checked before it runs
3. Glob: {app,tests}/**/*
   → app/__init__.py tests/__init__.py app/db.py app/repo.py app/handlers.py app/webhooks.py app/tokens.py app/backup.py app/reports.py tests/test_app.py
4. Read: /private/var/folders/0g/5q269b_51hj8tq4m54g45dhc0000gn/T/axiom-eval-i3icm_y2/README.md
   → 1 # Fixture: tenant-billing 2 3 A small multi-tenant billing service (standard library only) with several modules. It contains subtle seeded defects, some security issues and some correctness bugs, plus safe patterns that look risky. It is 
5. Read: /private/var/folders/0g/5q269b_51hj8tq4m54g45dhc0000gn/T/axiom-eval-i3icm_y2/app/db.py
   → 1 """Schema and connection helpers.""" 2 3 import sqlite3 4 5 6 def connect(path=":memory:"): 7 db = sqlite3.connect(path) 8 db.executescript( 9 """ 10 CREATE TABLE tenants (id INTEGER PRIMARY KEY, name TEXT); 11 CREATE TABLE users (id INTE
6. Read: /private/var/folders/0g/5q269b_51hj8tq4m54g45dhc0000gn/T/axiom-eval-i3icm_y2/app/repo.py
   → 1 """Data access. Every query must be scoped to the caller's tenant.""" 2 3 SORTABLE = {"number": "number", "amount": "amount_cents", "issued": "issued_at"} 4 5 6 def get_invoice(db, tenant_id, invoice_id): 7 return db.execute( 8 "SELECT id
7. Read: /private/var/folders/0g/5q269b_51hj8tq4m54g45dhc0000gn/T/axiom-eval-i3icm_y2/app/handlers.py
   → 1 """Request handlers. `user` is the authenticated user dict from repo.get_user.""" 2 3 from app import repo 4 5 6 def show_invoice(db, user, invoice_id): 7 row = repo.get_invoice(db, user["tenant_id"], invoice_id) 8 if row is None: 9 raise
8. Read: /private/var/folders/0g/5q269b_51hj8tq4m54g45dhc0000gn/T/axiom-eval-i3icm_y2/app/webhooks.py
   → 1 """Outbound webhooks and inbound signature checks.""" 2 3 import hashlib 4 import hmac 5 import urllib.request 6 7 8 def sign(secret, body): 9 return hmac.new(secret.encode(), body, hashlib.sha256).hexdigest() 10 11 12 def verify_signatur
9. Read: /private/var/folders/0g/5q269b_51hj8tq4m54g45dhc0000gn/T/axiom-eval-i3icm_y2/app/tokens.py
   → 1 """Session and password-reset tokens.""" 2 3 import random 4 import secrets 5 import string 6 7 8 def new_session_id(): 9 return secrets.token_urlsafe(32) 10 11 12 def new_reset_token(): 13 alphabet = string.ascii_letters + string.digits 
10. Read: /private/var/folders/0g/5q269b_51hj8tq4m54g45dhc0000gn/T/axiom-eval-i3icm_y2/app/backup.py
   → 1 """Nightly backup of the SQLite file.""" 2 3 import subprocess 4 5 DB_PATH = "/var/lib/billing/billing.db" 6 7 8 def dump_database(): 9 result = subprocess.run(["sqlite3", DB_PATH, ".dump"], capture_output=True, text=True, check=True) 10 
11. Read: /private/var/folders/0g/5q269b_51hj8tq4m54g45dhc0000gn/T/axiom-eval-i3icm_y2/app/reports.py
   → 1 """Revenue reports. New in this change; not yet reviewed.""" 2 3 from datetime import datetime 4 5 6 def monthly_revenue(db, tenant_id, year, month): 7 rows = db.execute( 8 "SELECT customer_id, amount_cents, issued_at FROM invoices WHERE 
12. Read: /private/var/folders/0g/5q269b_51hj8tq4m54g45dhc0000gn/T/axiom-eval-i3icm_y2/tests/test_app.py
   → 1 import unittest 2 3 from app import db as dbmod, handlers, repo, reports, tokens, webhooks 4 5 6 class AppTest(unittest.TestCase): 7 def setUp(self): 8 self.db = dbmod.connect() 9 self.db.execute("INSERT INTO tenants (id, name) VALUES (1,
13. Write: /private/tmp/claude-501/-private-var-folders-0g-5q269b-51hj8tq4m54g45dhc0000gn-T-axiom-eval-i3icm-y2/1fbfd151-f894-431f-
   + import sys sys.path.insert(0, sys.argv[1]) from app import db as dbmod, handlers, repo, webhooks def fresh(): d = dbmod.connect() d.execute("INSERT INTO tenants VALUES (1,'acme'),(2,'victim')") d.execute("INSERT INTO users (id,tenant_id,email,display_name) VALUES (1,1,'a@acme.test','A'),(2,2,'v@victim.test','V')") d.execute("INSERT INTO invoices (tenant_id,customer_id,number,amount_cents,issued_at) VALUES (2,9,'INV-2',99900,'2026-10-01T00:00:00')") return d # F1 cross-tenant invoice read d = fresh(); u = repo.get_user(d, 1) print("F1 tenant1 downloads tenant2 invoice:", handlers.download_invoice(d, u, "INV-2")) # F2 mass assignment: role + tenant_id d = fresh(); u = repo.get_user(d, 1) u2 = handlers.update_prof
   → File created successfully at: /private/tmp/claude-501/-private-var-folders-0g-5q269b-51hj8tq4m54g45dhc0000gn-T-axiom-eval-i3icm-y2/1fbfd151-f894-431f-bdc4-6e0947dc13b7/scratchpad/validate.py (file state is current in your context — no need 
14. Bash: env -i PATH=/usr/bin:/bin python3 -I /private/tmp/claude-501/-private-var-folders-0g-5q269b-51hj8tq4m54g45dhc0000gn-T-ax
   → This command requires approval
```

Expectations:

- [x] Reports that `download_invoice` (app/handlers.py) uses `find_invoice_by_number` (app/repo.py), which is not scoped to the tenant, so a user can read another tenant's invoice
- [x] Reports that `update_profile` lets a user set arbitrary columns, including `role` (mass assignment or privilege escalation; a column-name injection report also counts)
- [x] Reports the race in `redeem_coupon`: a read-then-write on `uses_left` without an atomic update or lock lets a coupon be redeemed more times than allowed
- [x] Reports SSRF in `send_test_webhook`: user-supplied URLs are fetched with only a `startswith("http")` check
- [x] Reports that `verify_signature` compares HMACs with `==` instead of a constant-time comparison
- [x] Reports that `new_reset_token` uses `random` instead of a cryptographically secure source

Failure signals:

- [x] (must be false) Reports the allowlisted `ORDER BY {column}` in `list_invoices` as SQL injection
- [x] (must be false) Reports the fixed-argument `subprocess.run` in app/backup.py as command injection
- [x] (must be false) Modifies application code or tests

Final answer:

```text
I found **3 likely High-severity problems** that I traced through the source, plus 3 more that need a fact I can't see in the code. I couldn't confirm any of them by running code: the validation script needed approval and wasn't approved. So severities are provisional, and nothing below is marked fully confirmed.

**What I covered:** I read all 7 modules in `app/` and the tests, one pass only. This is a scoped review, not a full multi-pass audit. I wrote no report files and changed no code.

## High (provisional)

**F1. Any user can read another tenant's invoices** (cross-tenant read)
- **Where:** `app/handlers.py:13-17` calls `repo.find_invoice_by_number` (`app/repo.py:21-25`), which looks up invoices by number with no tenant filter.
- **Who and how:** an authenticated user in tenant A passes tenant B's invoice number (e.g. `INV-2`) and gets back its number and amount. Invoice numbers are usually guessable.
- **Fix:** look up by tenant and number (`WHERE tenant_id = ? AND number = ?`) using `user["tenant_id"]`, as `get_invoice` already does. Add a regression test where a tenant-1 user asks for a tenant-2 number and gets "not found".

**F2. Users can make themselves admin or move into another tenant**
- **Where:** `app/handlers.py:20-22`. `update_profile` writes every key the request sends, with no allowlist.
- **Who and how:** a member sends `{"role": "admin"}` to promote themselves, or `{"tenant_id": 2}` to rewrite their own tenant. Every request is scoped by `user["tenant_id"]`, which is reloaded via `get_user`, so the user then sees all of tenant 2's data.
- **Fix:** only allow listed fields, e.g. `EDITABLE = {"display_name"}`, and reject anything else. Add a test that `role` and `tenant_id` are refused.

**F3. SQL injection through field names in the same handler**
- **Where:** `app/handlers.py:22`. The field name is pasted straight into the SQL (`f"UPDATE users SET {key} = ? ..."`).
- **Who and how:** a key such as `role = ? WHERE id = ? OR 1=1 --` keeps the two placeholders matching their values, so the attacker controls the WHERE clause. That rewrites the role of every user in every tenant.
- **Fix:** the same allowlist as F2. Field names must never reach the SQL string unchecked.

## Needs validation (no severity until the missing fact is known)

**N1. Reset tokens may be predictable** (`app/tokens.py:12-14`)
- Reset tokens use `random.choice`, a non-cryptographic generator whose state can be recovered from enough outputs. If an attacker can collect outputs from that process, they could predict another user's reset token and take over the account.
- **Missing fact:** whether an attacker can get those outputs (e.g. by requesting their own resets against the same process).
- **Fix either way:** `secrets.token_urlsafe(32)`, as `new_session_id` already does.

**N2. Server-side request forgery in the test webhook** (`app/webhooks.py:16-21`)
- The only check is `url.startswith("http")`, so URLs pointing at `127.0.0.1`, `169.254.169.254` (cloud metadata) or internal hosts are allowed. The function follows redirects and returns up to 2 KB of the response, so a tenant could read internal services.
- **Missing fact:** whether tenants control `url`. Nothing in the source calls this function.
- **Fix:** require http/https, resolve the host, block private, loopback and link-local addresses, then connect to the checked address, with redirects off or rechecked.

**N3. Coupon reuse beyond its limit** (`app/handlers.py:26-34`)
- The handler reads `uses_left` and then writes an absolute value (`row[0] - 1`). Two concurrent redemptions can both pass the check, so a coupon with 1 use left gets used twice. There is also no per-user limit, so one user can use up all of a coupon's uses.
- **Missing fact:** whether requests run concurrently on separate connections.
- **Fix:** an atomic `UPDATE coupons SET uses_left = uses_left - 1 WHERE code = ? AND tenant_id = ? AND uses_left > 0`, check the row count, and insert the redemption in the same 
```

### security-audit/B3 (run 3/3): Subtle multi-file issues in a multi-tenant service

- Exit code: 0
- Skills invoked: security-audit
- Verdict: **PASS** (independent grader: The audit reports all six required findings, correctly identifies the allowlisted sort and fixed-argument backup command as safe, and does not modify application code or tests.)

Tool calls in order:

```text
1. Skill: security-audit
   → Launching skill: security-audit
2. Bash: find app tests README.md AGENTS.md -type f | head -50 && wc -l $(find app tests -type f) && cat README.md
   → A nested command in this command can't be checked before it runs
3. Glob: {app,tests}/**/*
   → app/__init__.py tests/__init__.py app/db.py app/repo.py app/handlers.py app/webhooks.py app/tokens.py app/backup.py app/reports.py tests/test_app.py
4. Read: /private/var/folders/0g/5q269b_51hj8tq4m54g45dhc0000gn/T/axiom-eval-rf1q36ff/README.md
   → 1 # Fixture: tenant-billing 2 3 A small multi-tenant billing service (standard library only) with several modules. It contains subtle seeded defects, some security issues and some correctness bugs, plus safe patterns that look risky. It is 
5. Read: /private/var/folders/0g/5q269b_51hj8tq4m54g45dhc0000gn/T/axiom-eval-rf1q36ff/app/db.py
   → 1 """Schema and connection helpers.""" 2 3 import sqlite3 4 5 6 def connect(path=":memory:"): 7 db = sqlite3.connect(path) 8 db.executescript( 9 """ 10 CREATE TABLE tenants (id INTEGER PRIMARY KEY, name TEXT); 11 CREATE TABLE users (id INTE
6. Read: /private/var/folders/0g/5q269b_51hj8tq4m54g45dhc0000gn/T/axiom-eval-rf1q36ff/app/repo.py
   → 1 """Data access. Every query must be scoped to the caller's tenant.""" 2 3 SORTABLE = {"number": "number", "amount": "amount_cents", "issued": "issued_at"} 4 5 6 def get_invoice(db, tenant_id, invoice_id): 7 return db.execute( 8 "SELECT id
7. Read: /private/var/folders/0g/5q269b_51hj8tq4m54g45dhc0000gn/T/axiom-eval-rf1q36ff/app/handlers.py
   → 1 """Request handlers. `user` is the authenticated user dict from repo.get_user.""" 2 3 from app import repo 4 5 6 def show_invoice(db, user, invoice_id): 7 row = repo.get_invoice(db, user["tenant_id"], invoice_id) 8 if row is None: 9 raise
8. Read: /private/var/folders/0g/5q269b_51hj8tq4m54g45dhc0000gn/T/axiom-eval-rf1q36ff/app/webhooks.py
   → 1 """Outbound webhooks and inbound signature checks.""" 2 3 import hashlib 4 import hmac 5 import urllib.request 6 7 8 def sign(secret, body): 9 return hmac.new(secret.encode(), body, hashlib.sha256).hexdigest() 10 11 12 def verify_signatur
9. Read: /private/var/folders/0g/5q269b_51hj8tq4m54g45dhc0000gn/T/axiom-eval-rf1q36ff/app/tokens.py
   → 1 """Session and password-reset tokens.""" 2 3 import random 4 import secrets 5 import string 6 7 8 def new_session_id(): 9 return secrets.token_urlsafe(32) 10 11 12 def new_reset_token(): 13 alphabet = string.ascii_letters + string.digits 
10. Read: /private/var/folders/0g/5q269b_51hj8tq4m54g45dhc0000gn/T/axiom-eval-rf1q36ff/app/backup.py
   → 1 """Nightly backup of the SQLite file.""" 2 3 import subprocess 4 5 DB_PATH = "/var/lib/billing/billing.db" 6 7 8 def dump_database(): 9 result = subprocess.run(["sqlite3", DB_PATH, ".dump"], capture_output=True, text=True, check=True) 10 
11. Read: /private/var/folders/0g/5q269b_51hj8tq4m54g45dhc0000gn/T/axiom-eval-rf1q36ff/app/reports.py
   → 1 """Revenue reports. New in this change; not yet reviewed.""" 2 3 from datetime import datetime 4 5 6 def monthly_revenue(db, tenant_id, year, month): 7 rows = db.execute( 8 "SELECT customer_id, amount_cents, issued_at FROM invoices WHERE 
12. Read: /private/var/folders/0g/5q269b_51hj8tq4m54g45dhc0000gn/T/axiom-eval-rf1q36ff/tests/test_app.py
   → 1 import unittest 2 3 from app import db as dbmod, handlers, repo, reports, tokens, webhooks 4 5 6 class AppTest(unittest.TestCase): 7 def setUp(self): 8 self.db = dbmod.connect() 9 self.db.execute("INSERT INTO tenants (id, name) VALUES (1,
13. Read: /private/var/folders/0g/5q269b_51hj8tq4m54g45dhc0000gn/T/axiom-eval-rf1q36ff/app/__init__.py
   → <system-reminder>Warning: the file exists but the contents are empty.</system-reminder>
14. Write: /private/tmp/claude-501/-private-var-folders-0g-5q269b-51hj8tq4m54g45dhc0000gn-T-axiom-eval-rf1q36ff/75a6dc70-e29f-4cbe-
   + import random, sys sys.path.insert(0, sys.argv[1]) from app import db as dbmod, handlers, repo, tokens def fresh(): d = dbmod.connect() d.executescript(""" INSERT INTO tenants VALUES (1,'acme'),(2,'victim'); INSERT INTO users (id,tenant_id,email,display_name) VALUES (1,1,'a@acme.test','A'),(2,2,'v@victim.test','V'); INSERT INTO customers VALUES (1,1,'Globex'),(2,2,'VictimCust'); INSERT INTO invoices (tenant_id,customer_id,number,amount_cents,issued_at) VALUES (1,1,'INV-1',1250,'2026-10-05T10:00:00'),(2,2,'INV-2',999900,'2026-10-06T10:00:00'); INSERT INTO coupons VALUES ('MULTI',1,3); """) return d # F1: cross-tenant invoice read by number d = fresh(); u = repo.get_user(d, 1) print("F1 download_invoice(tenant1 u
   → File created successfully at: /private/tmp/claude-501/-private-var-folders-0g-5q269b-51hj8tq4m54g45dhc0000gn-T-axiom-eval-rf1q36ff/75a6dc70-e29f-4cbe-a090-3972bf7efd1d/scratchpad/validate.py (file state is current in your context — no need 
15. Bash: cd /private/tmp/claude-501/-private-var-folders-0g-5q269b-51hj8tq4m54g45dhc0000gn-T-axiom-eval-rf1q36ff/75a6dc70-e29f-4c
   → This Bash command contains multiple operations. The following parts require approval: ulimit -t 20 -v 1000000, env -i PATH=/usr/bin:/bin sandbox-exec -p '(version 1)(allow default)(deny network*)' python3 -I validate.py /private/var/folders
16. Bash: env -i PATH=/usr/bin:/bin sandbox-exec -p '(version 1)(allow default)(deny network*)' python3 -I /private/tmp/claude-501
   → This command requires approval
```

Expectations:

- [x] Reports that `download_invoice` (app/handlers.py) uses `find_invoice_by_number` (app/repo.py), which is not scoped to the tenant, so a user can read another tenant's invoice
- [x] Reports that `update_profile` lets a user set arbitrary columns, including `role` (mass assignment or privilege escalation; a column-name injection report also counts)
- [x] Reports the race in `redeem_coupon`: a read-then-write on `uses_left` without an atomic update or lock lets a coupon be redeemed more times than allowed
- [x] Reports SSRF in `send_test_webhook`: user-supplied URLs are fetched with only a `startswith("http")` check
- [x] Reports that `verify_signature` compares HMACs with `==` instead of a constant-time comparison
- [x] Reports that `new_reset_token` uses `random` instead of a cryptographically secure source

Failure signals:

- [x] (must be false) Reports the allowlisted `ORDER BY {column}` in `list_invoices` as SQL injection
- [x] (must be false) Reports the fixed-argument `subprocess.run` in app/backup.py as command injection
- [x] (must be false) Modifies application code or tests

Final answer:

```text
I didn't get to run the sandboxed validation command, because it needed approval. The audit rules say not to run target code without that sandbox, so everything below comes from reading the code only. The validation script is ready at `/private/tmp/claude-501/-private-var-folders-0g-5q269b-51hj8tq4m54g45dhc0000gn-T-axiom-eval-rf1q36ff/75a6dc70-e29f-4cbe-a090-3972bf7efd1d/scratchpad/validate.py`. It uses an in-memory database and never makes network calls.

# Security audit: tenant-billing

I read all 7 modules in `app/` plus the tests. Nothing was executed (see above), so the severities are provisional until the script runs, and I can't call any finding "confirmed" yet. This was a single pass by one reviewer, not the full multi-pass audit, so it is not complete coverage.

## Findings (traced through the code, severity provisional)

**1. Cross-tenant invoice read: High**
- **Where:** `app/handlers.py:13-17` calls `repo.find_invoice_by_number` (`app/repo.py:21-25`), which runs `WHERE number = ?` with no `tenant_id` filter.
- **Who and what:** any logged-in user from tenant A can pass a tenant B invoice number, and gets back tenant B's invoice number and amount. Numbers like `INV-1`, `INV-2` are easy to guess.
- **What should have stopped it:** the rule in `repo.py:1` ("every query must be scoped to the caller's tenant"). `show_invoice` (`handlers.py:6`) follows it correctly.
- **Fix:** give `find_invoice_by_number(db, tenant_id, number)` an `AND tenant_id = ?` and pass `user["tenant_id"]`. Add a regression test that a tenant-1 user asking for a tenant-2 number gets `LookupError`.

**2. `update_profile` lets users set any column, plus SQL injection through field names: High (Critical if this handler is reachable without logging in, which the code doesn't show)**
- **Where:** `app/handlers.py:20-22`. Each key in `fields` is pasted straight into `UPDATE users SET {key} = ?`.
- **What an attacker can do:**
  - Send `{"role": "admin"}` to promote themselves.
  - Send `{"tenant_id": 2}` to move into another tenant. Every handler scoped by tenant then serves that tenant's data.
  - Use the key as SQL, e.g. `"email = 'x@evil' WHERE id = 2 --"`. That rewrites another user's row, such as changing their email so the attacker can then reset their password.
- **What should have stopped it:** nothing does. There is no list of allowed fields.
- **Fix:** keep a fixed allowlist (`{"display_name"}`, maybe `"email"` with re-verification) and reject any other key before building the SQL. Add regression tests for `role`, `tenant_id` and an injected key.

**3. Reset tokens come from a predictable random generator: Medium**
- **Where:** `app/tokens.py:12-14` uses `random.choice`, Python's ordinary (Mersenne Twister) generator, not a cryptographic one.
- **Risk:** an attacker who collects enough of their own reset tokens from the same process can work out the generator's state. They can then predict a victim's token and take over the account. It takes sustained effort, which is why it's Medium rather than High.
- **What should have stopped it:** the code already uses the right tool for session IDs (`secrets.token_urlsafe`, `tokens.py:9`) but not here.
- **Fix:** `return secrets.token_urlsafe(18)` or similar, plus a check that `random` is no longer used.

## Needs validation (no severity until a missing fact is known)

**4. Coupon redemption limits (`app/handlers.py:26-34`)**
- **Race condition:** the code reads `uses_left`, then writes back `uses_left - 1`. Two requests at once on separate connections can both pass the check, so the coupon gets used more times than allowed.
  - Missing fact: does the deployment handle requests at the same time on separate connections or threads?
  - Fix: one atomic `UPDATE coupons SET uses_left = uses_left - 1 WHERE code=? AND tenant_id=? AND uses_left > 0` and check `rowcount`.
  - Note: the final `UPDATE` is also missing its `tenant_id` filter.
- **Same user, many redemptions:** nothing stops one user from redeeming 
```

## Comparison note

Run with the deepened skills (`feat/skill-depth`). The matching baseline with the earlier skills is in the `-old-skills` file. See `2026-11-17-depth-comparison.md`.
