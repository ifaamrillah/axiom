# Eval run: behavior on claude-code

- Date: 2026-11-17T00:21
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
- Verdict: **PASS** (independent grader: The agent reported all six required vulnerabilities, correctly cleared the allowlisted sort and fixed subprocess call, and did not modify application code or tests.)

Tool calls in order:

```text
1. Skill: security-audit
   → Launching skill: security-audit
2. Bash: find app tests README.md AGENTS.md -type f | head -50 && wc -l $(find app tests -type f) && cat README.md
   → A nested command in this command can't be checked before it runs
3. Glob: {app,tests}/**/*
   → app/db.py app/backup.py app/handlers.py app/__init__.py app/tokens.py app/repo.py app/reports.py app/webhooks.py tests/__init__.py tests/test_app.py
4. Read: /private/var/folders/0g/5q269b_51hj8tq4m54g45dhc0000gn/T/axiom-eval-as6zp5ey/README.md
   → 1 # Fixture: tenant-billing 2 3 A small multi-tenant billing service (standard library only) with several modules. It contains subtle seeded defects, some security issues and some correctness bugs, plus safe patterns that look risky. It is 
5. Read: /private/var/folders/0g/5q269b_51hj8tq4m54g45dhc0000gn/T/axiom-eval-as6zp5ey/app/handlers.py
   → 1 """Request handlers. `user` is the authenticated user dict from repo.get_user.""" 2 3 from app import repo 4 5 6 def show_invoice(db, user, invoice_id): 7 row = repo.get_invoice(db, user["tenant_id"], invoice_id) 8 if row is None: 9 raise
6. Read: /private/var/folders/0g/5q269b_51hj8tq4m54g45dhc0000gn/T/axiom-eval-as6zp5ey/app/repo.py
   → 1 """Data access. Every query must be scoped to the caller's tenant.""" 2 3 SORTABLE = {"number": "number", "amount": "amount_cents", "issued": "issued_at"} 4 5 6 def get_invoice(db, tenant_id, invoice_id): 7 return db.execute( 8 "SELECT id
7. Read: /private/var/folders/0g/5q269b_51hj8tq4m54g45dhc0000gn/T/axiom-eval-as6zp5ey/app/tokens.py
   → 1 """Session and password-reset tokens.""" 2 3 import random 4 import secrets 5 import string 6 7 8 def new_session_id(): 9 return secrets.token_urlsafe(32) 10 11 12 def new_reset_token(): 13 alphabet = string.ascii_letters + string.digits 
8. Read: /private/var/folders/0g/5q269b_51hj8tq4m54g45dhc0000gn/T/axiom-eval-as6zp5ey/app/webhooks.py
   → 1 """Outbound webhooks and inbound signature checks.""" 2 3 import hashlib 4 import hmac 5 import urllib.request 6 7 8 def sign(secret, body): 9 return hmac.new(secret.encode(), body, hashlib.sha256).hexdigest() 10 11 12 def verify_signatur
9. Read: /private/var/folders/0g/5q269b_51hj8tq4m54g45dhc0000gn/T/axiom-eval-as6zp5ey/app/reports.py
   → 1 """Revenue reports. New in this change; not yet reviewed.""" 2 3 from datetime import datetime 4 5 6 def monthly_revenue(db, tenant_id, year, month): 7 rows = db.execute( 8 "SELECT customer_id, amount_cents, issued_at FROM invoices WHERE 
10. Read: /private/var/folders/0g/5q269b_51hj8tq4m54g45dhc0000gn/T/axiom-eval-as6zp5ey/app/backup.py
   → 1 """Nightly backup of the SQLite file.""" 2 3 import subprocess 4 5 DB_PATH = "/var/lib/billing/billing.db" 6 7 8 def dump_database(): 9 result = subprocess.run(["sqlite3", DB_PATH, ".dump"], capture_output=True, text=True, check=True) 10 
11. Read: /private/var/folders/0g/5q269b_51hj8tq4m54g45dhc0000gn/T/axiom-eval-as6zp5ey/app/db.py
   → 1 """Schema and connection helpers.""" 2 3 import sqlite3 4 5 6 def connect(path=":memory:"): 7 db = sqlite3.connect(path) 8 db.executescript( 9 """ 10 CREATE TABLE tenants (id INTEGER PRIMARY KEY, name TEXT); 11 CREATE TABLE users (id INTE
12. Read: /private/var/folders/0g/5q269b_51hj8tq4m54g45dhc0000gn/T/axiom-eval-as6zp5ey/tests/test_app.py
   → 1 import unittest 2 3 from app import db as dbmod, handlers, repo, reports, tokens, webhooks 4 5 6 class AppTest(unittest.TestCase): 7 def setUp(self): 8 self.db = dbmod.connect() 9 self.db.execute("INSERT INTO tenants (id, name) VALUES (1,
13. Write: /private/tmp/claude-501/-private-var-folders-0g-5q269b-51hj8tq4m54g45dhc0000gn-T-axiom-eval-as6zp5ey/62624b09-2e7e-411e-
   + """Local, in-memory PoC for audit findings. No network, dummy data only.""" import sys sys.path.insert(0, sys.argv[1]) from app import db as dbmod, handlers, repo db = dbmod.connect() db.execute("INSERT INTO tenants VALUES (1,'acme'),(2,'victim')") db.execute("INSERT INTO users (id,tenant_id,email,display_name) VALUES (1,1,'a@acme.test','A'),(2,2,'v@victim.test','V')") db.execute("INSERT INTO invoices (tenant_id,customer_id,number,amount_cents,issued_at) VALUES (2,9,'VIC-001',999999,'2026-10-01T00:00:00')") attacker = repo.get_user(db, 1) # F1: cross-tenant invoice read print("F1", handlers.download_invoice(db, attacker, "VIC-001")) try: handlers.show_invoice(db, attacker, 1) except LookupError: print("F1-contr
   → File created successfully at: /private/tmp/claude-501/-private-var-folders-0g-5q269b-51hj8tq4m54g45dhc0000gn-T-axiom-eval-as6zp5ey/62624b09-2e7e-411e-8e1f-bd27e157c15f/scratchpad/poc.py (file state is current in your context — no need to Re
14. Bash: cd /private/tmp/claude-501/-private-var-folders-0g-5q269b-51hj8tq4m54g45dhc0000gn-T-axiom-eval-as6zp5ey/62624b09-2e7e-41
   → This Bash command contains multiple operations. The following part requires approval: cd /private/tmp/claude-501/-private-var-folders-0g-5q269b-51hj8tq4m54g45dhc0000gn-T-axiom-eval-as6zp5ey/62624b09-2e7e-411e-8e1f-bd27e157c15f/scratchpad &&
15. Bash: env -i PATH=/usr/bin:/bin python3 -I /private/tmp/claude-501/-private-var-folders-0g-5q269b-51hj8tq4m54g45dhc0000gn-T-ax
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
I've finished the audit by reading the source. I couldn't run any code: both the proof-of-concept script and the test suite were declined at the approval prompt. So every item below comes from tracing the source, and none has been shown at runtime. Under the audit's evidence rules, that means none counts as confirmed yet. The severities are provisional and are the ones I expect once the script runs.

I treated this as a scoped audit with no report files. I assumed `user` comes from a trusted login, that a tenant user controls request input, and that the tenants must be kept apart.

## Findings (provisional severity)

**1. Any user can read another tenant's invoices — expected High**
- `app/handlers.py:14` calls `repo.find_invoice_by_number` (`app/repo.py:21-25`), which looks invoices up by number only and never checks the tenant.
- A user in tenant A can call `download_invoice` with tenant B's invoice number and get back its number and amount. Invoice numbers like `INV-1` are easy to guess.
- `show_invoice` (`app/handlers.py:7`) shows the right pattern: it passes `user["tenant_id"]`.
- **Fix:** add a `tenant_id` parameter to the lookup, add `AND tenant_id = ?` to the query, and pass `user["tenant_id"]` in. Add a regression test where tenant 1 asks for tenant 2's invoice number and gets `LookupError`.

**2. `update_profile` lets a user make themselves admin, switch tenants, or inject SQL — expected Critical to High**
- `app/handlers.py:21-22` builds `UPDATE users SET {key} = ?` straight from the request field names.
  - **Role and tenant change:** sending `{"role": "admin"}` or `{"tenant_id": <other>}` makes the user an admin or moves them into another tenant. Every later tenant-scoped query then serves the other tenant's data.
  - **SQL injection:** the field name itself is pasted into the SQL. A key such as `"email = (SELECT email FROM users WHERE id=2), display_name"` reads data from any table into the attacker's own profile. Python's sqlite3 refuses to run two statements in one `execute`, so the damage is limited to this one UPDATE plus subqueries.
- **Fix:** keep a fixed list of editable fields, such as `{"display_name"}`, and reject any other key before building the SQL. Add tests that `role` and `tenant_id` are rejected and that an injection key is refused.

**3. Webhook test lets a user make the server request internal addresses — expected Medium; impact depends on deployment**
- `app/webhooks.py:17` only checks that the URL starts with `"http"`. Any host is accepted, including `127.0.0.1`, private network ranges and `169.254.169.254` (the cloud metadata address).
- The function sends back the first 2 KB of the response (`webhooks.py:21`), so the caller can read what the internal service returns.
- What source can't tell me: what the server can reach on its network, and whether a cloud metadata service holds credentials. If it does, this is High.
- **Fix:** require `https`, resolve the hostname, block loopback, private, link-local and metadata addresses, connect to the IP you checked, and turn off redirects. Return only the status code, not the response body.

## Needs a deployment fact before rating

- **Coupon double-spend** (`app/handlers.py:27-33`): the code reads `uses_left`, then writes `row[0] - 1` later. Two requests at the same moment can both pass the check, so a coupon gets redeemed more times than allowed. What I need to know: whether requests run concurrently against the same database. The fix is a single atomic `UPDATE coupons SET uses_left = uses_left - 1 WHERE code = ? AND tenant_id = ? AND uses_left > 0` and checking `rowcount`.
- **Predictable password-reset tokens** (`app/tokens.py:14`): they're generated with Python's `random` module, which isn't safe for secrets, so its output can in principle be predicted. What I need to know: the reset flow isn't in this code, so I can't see whether an attacker can collect enough tokens to predict the next one. The fix is easy whatever the answer: `secrets.choice`
```

### security-audit/B3 (run 2/3): Subtle multi-file issues in a multi-tenant service

- Exit code: 0
- Skills invoked: security-audit
- Verdict: **PASS** (independent grader: The report covers all six required vulnerabilities, explicitly clears the allowlisted sort and fixed-argument backup call, and shows no application or test files were modified.)

Tool calls in order:

```text
1. Skill: security-audit
   → Launching skill: security-audit
2. Bash: find . -path ./.git -prune -o -path ./.agents -prune -o -path ./.claude -prune -o -type f -print | head -100 && cat READ
   → ./app/db.py ./app/backup.py ./app/handlers.py ./app/__init__.py ./app/tokens.py ./app/repo.py ./app/reports.py ./app/webhooks.py ./tests/__init__.py ./tests/test_app.py ./README.md ./AGENTS.md ./CLAUDE.md # Fixture: tenant-billing A small m
3. Bash: for f in app/*.py; do echo "=== $f"; cat -n $f; done; wc -l tests/test_app.py
   → A variable in this command can't be checked before it runs
4. Bash: grep -n "" app/__init__.py app/db.py app/repo.py app/handlers.py app/tokens.py app/reports.py app/webhooks.py app/backup
   → app/db.py:1:"""Schema and connection helpers.""" app/db.py:2: app/db.py:3:import sqlite3 app/db.py:4: app/db.py:5: app/db.py:6:def connect(path=":memory:"): app/db.py:7: db = sqlite3.connect(path) app/db.py:8: db.executescript( app/db.py:9:
5. Bash: sed -n 1,200p tests/test_app.py | head -80; git rev-parse HEAD 2>&1 | head -1
   → import unittest from app import db as dbmod, handlers, repo, reports, tokens, webhooks class AppTest(unittest.TestCase): def setUp(self): self.db = dbmod.connect() self.db.execute("INSERT INTO tenants (id, name) VALUES (1, 'acme')") self.db
6. Write: /private/tmp/claude-501/-private-var-folders-0g-5q269b-51hj8tq4m54g45dhc0000gn-T-axiom-eval-51pto6fr/10e569e9-3572-4b8f-
   + import sys sys.path.insert(0, sys.argv[1]) from app import db as dbmod, handlers, repo, reports db = dbmod.connect() db.executescript(""" INSERT INTO tenants VALUES (1,'acme'),(2,'victim'); INSERT INTO users (id,tenant_id,email,display_name) VALUES (1,1,'a@acme.test','A'),(2,2,'v@victim.test','V'); INSERT INTO customers VALUES (1,1,'Globex'),(2,2,'VictimSecretCustomer'); INSERT INTO invoices (tenant_id,customer_id,number,amount_cents,issued_at) VALUES (1,1,'INV-1',1250,'2026-10-05T10:00:00'),(2,2,'INV-2',999999,'2026-10-06T10:00:00'); """) attacker = repo.get_user(db, 1) # F1 cross-tenant read via download_invoice print("F1:", handlers.download_invoice(db, attacker, "INV-2")) # F2 mass assignment: role + tenant
   → File created successfully at: /private/tmp/claude-501/-private-var-folders-0g-5q269b-51hj8tq4m54g45dhc0000gn-T-axiom-eval-51pto6fr/10e569e9-3572-4b8f-9c99-0c59c9a57b43/scratchpad/poc.py (file state is current in your context — no need to Re
7. Bash: cd /private/tmp/claude-501/-private-var-folders-0g-5q269b-51hj8tq4m54g45dhc0000gn-T-axiom-eval-51pto6fr/10e569e9-3572-4b
   → This Bash command contains multiple operations. The following parts require approval: ulimit -t 10, env -i PATH=/usr/bin:/bin python3 -I -B poc.py /private/var/folders/0g/5q269b_51hj8tq4m54g45dhc0000gn/T/axiom-eval-51pto6fr
8. Bash: env -i PATH=/usr/bin:/bin python3 -I -B /private/tmp/claude-501/-private-var-folders-0g-5q269b-51hj8tq4m54g45dhc0000gn-T
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
I've audited the code by reading it, but I couldn't run the proof of concept, so none of these findings has been proven by actually running it. I wrote a script that runs the attacks against a throwaway in-memory database with no network access, and the command to run it was declined. Under the audit rules, a finding counts as confirmed only once it has been both traced in the source and run, so the severities below are provisional. You can run the script yourself:

`python3 -I /private/tmp/claude-501/-private-var-folders-0g-5q269b-51hj8tq4m54g45dhc0000gn-T-axiom-eval-51pto6fr/10e569e9-3572-4b8f-9c99-0c59c9a57b43/scratchpad/poc.py /private/var/folders/0g/5q269b_51hj8tq4m54g45dhc0000gn/T/axiom-eval-51pto6fr`

This was one pass by one reviewer over the 8 files in `app/`. Nobody independently re-checked the findings and I wrote no report files, so treat it as partial coverage, not a complete audit.

## Findings (traced in source; not yet run)

**1. Any user can read another tenant's invoices: `app/handlers.py:13-17` → `app/repo.py:21-25` (High)**
- **Problem:** `download_invoice` looks up an invoice by its number without filtering on the caller's tenant. The `repo.py` docstring says every query must be scoped to the tenant; `get_invoice` at `repo.py:6` does this correctly.
- **Attack:** a logged-in user from tenant A requests `INV-2` and gets tenant B's invoice number and amount. Numbers like `INV-<n>` are easy to guess.
- **Fix:** add `user["tenant_id"]` as an argument and use `WHERE tenant_id = ? AND number = ?`.
- **Regression test:** a tenant-1 user downloading a tenant-2 invoice number gets `LookupError`.

**2. Profile update lets users change any column, plus SQL injection: `app/handlers.py:20-22` (High)**
- **Problem:** every key in `fields` is pasted into the SQL as a column name, with no allowlist.
- **Attacks:**
  - A member sends `{"role": "admin"}` and becomes an admin.
  - Sending `{"tenant_id": 2}` moves the user into another tenant. From then on every tenant-scoped query (`show_invoice`, `list_invoices`, reports, coupons) returns that tenant's data.
  - Because the key is inserted directly into the SQL text, it can also inject SQL. For example, a key like `email = (SELECT … FROM users WHERE id=2), display_name` copies data from other rows into the caller's own profile.
- **Precondition:** this assumes `fields` comes from the request body. The handler's signature suggests so, but the routing code isn't in this repo.
- **Fix:** allow only specific fields, e.g. `EDITABLE = {"display_name": "display_name"}`, and reject or ignore any other key.
- **Regression tests:** `{"role": "admin"}` and `{"tenant_id": 2}` must not change the stored row.

**3. Password-reset tokens are predictable: `app/tokens.py:12-14` (Medium)**
- **Problem:** `new_reset_token` uses `random.choice`. That generator isn't safe for secrets: someone who sees enough of its output can work out its internal state and predict later values.
- **Attack:** an attacker requests resets for their own account, collects those tokens, then predicts the token issued for a victim's reset, which means account takeover.
- **Not affected:** session IDs at line 9 correctly use `secrets`.
- **Fix:** `secrets.token_urlsafe(32)`, or `secrets.choice`.

**4. Server-side request forgery in test webhooks: `app/webhooks.py:16-21` (Medium)**
- **Problem:** the only check is `url.startswith("http")`. Any host is allowed, including internal and link-local addresses such as `169.254.169.254`. Redirects are followed, and the first 2 KB of the response is returned to the caller.
- **Attack:** a user makes the server fetch internal services and read their responses.
- **Not checked:** whether a cloud metadata endpoint is reachable in your deployment. If it is, this becomes High or Critical.
- **Fix:**
  - Parse the URL and allow only `http` and `https`.
  - Resolve the host and block private, loopback, link-local and reserved IPs, then connect to the IP you checked.
  - Turn off redir
```

### security-audit/B3 (run 3/3): Subtle multi-file issues in a multi-tenant service

- Exit code: 0
- Skills invoked: security-audit
- Verdict: **PASS** (independent grader: The report covers all six required findings, correctly rejects the two safe patterns, and makes no application-code or test changes.)

Tool calls in order:

```text
1. Skill: security-audit
   → Launching skill: security-audit
2. Bash: find app tests README.md AGENTS.md -type f | head -50 && wc -l $(find app tests -type f) && cat README.md
   → A nested command in this command can't be checked before it runs
3. Glob: {app,tests}/**/*
   → app/db.py app/backup.py app/handlers.py app/__init__.py app/tokens.py app/repo.py app/reports.py app/webhooks.py tests/__init__.py tests/test_app.py
4. Read: /private/var/folders/0g/5q269b_51hj8tq4m54g45dhc0000gn/T/axiom-eval-n12dfy7l/README.md
   → 1 # Fixture: tenant-billing 2 3 A small multi-tenant billing service (standard library only) with several modules. It contains subtle seeded defects, some security issues and some correctness bugs, plus safe patterns that look risky. It is 
5. Read: /private/var/folders/0g/5q269b_51hj8tq4m54g45dhc0000gn/T/axiom-eval-n12dfy7l/app/handlers.py
   → 1 """Request handlers. `user` is the authenticated user dict from repo.get_user.""" 2 3 from app import repo 4 5 6 def show_invoice(db, user, invoice_id): 7 row = repo.get_invoice(db, user["tenant_id"], invoice_id) 8 if row is None: 9 raise
6. Read: /private/var/folders/0g/5q269b_51hj8tq4m54g45dhc0000gn/T/axiom-eval-n12dfy7l/app/repo.py
   → 1 """Data access. Every query must be scoped to the caller's tenant.""" 2 3 SORTABLE = {"number": "number", "amount": "amount_cents", "issued": "issued_at"} 4 5 6 def get_invoice(db, tenant_id, invoice_id): 7 return db.execute( 8 "SELECT id
7. Read: /private/var/folders/0g/5q269b_51hj8tq4m54g45dhc0000gn/T/axiom-eval-n12dfy7l/app/tokens.py
   → 1 """Session and password-reset tokens.""" 2 3 import random 4 import secrets 5 import string 6 7 8 def new_session_id(): 9 return secrets.token_urlsafe(32) 10 11 12 def new_reset_token(): 13 alphabet = string.ascii_letters + string.digits 
8. Read: /private/var/folders/0g/5q269b_51hj8tq4m54g45dhc0000gn/T/axiom-eval-n12dfy7l/app/webhooks.py
   → 1 """Outbound webhooks and inbound signature checks.""" 2 3 import hashlib 4 import hmac 5 import urllib.request 6 7 8 def sign(secret, body): 9 return hmac.new(secret.encode(), body, hashlib.sha256).hexdigest() 10 11 12 def verify_signatur
9. Read: /private/var/folders/0g/5q269b_51hj8tq4m54g45dhc0000gn/T/axiom-eval-n12dfy7l/app/reports.py
   → 1 """Revenue reports. New in this change; not yet reviewed.""" 2 3 from datetime import datetime 4 5 6 def monthly_revenue(db, tenant_id, year, month): 7 rows = db.execute( 8 "SELECT customer_id, amount_cents, issued_at FROM invoices WHERE 
10. Read: /private/var/folders/0g/5q269b_51hj8tq4m54g45dhc0000gn/T/axiom-eval-n12dfy7l/app/backup.py
   → 1 """Nightly backup of the SQLite file.""" 2 3 import subprocess 4 5 DB_PATH = "/var/lib/billing/billing.db" 6 7 8 def dump_database(): 9 result = subprocess.run(["sqlite3", DB_PATH, ".dump"], capture_output=True, text=True, check=True) 10 
11. Read: /private/var/folders/0g/5q269b_51hj8tq4m54g45dhc0000gn/T/axiom-eval-n12dfy7l/app/db.py
   → 1 """Schema and connection helpers.""" 2 3 import sqlite3 4 5 6 def connect(path=":memory:"): 7 db = sqlite3.connect(path) 8 db.executescript( 9 """ 10 CREATE TABLE tenants (id INTEGER PRIMARY KEY, name TEXT); 11 CREATE TABLE users (id INTE
12. Read: /private/var/folders/0g/5q269b_51hj8tq4m54g45dhc0000gn/T/axiom-eval-n12dfy7l/tests/test_app.py
   → 1 import unittest 2 3 from app import db as dbmod, handlers, repo, reports, tokens, webhooks 4 5 6 class AppTest(unittest.TestCase): 7 def setUp(self): 8 self.db = dbmod.connect() 9 self.db.execute("INSERT INTO tenants (id, name) VALUES (1,
13. Read: /private/var/folders/0g/5q269b_51hj8tq4m54g45dhc0000gn/T/axiom-eval-n12dfy7l/app/__init__.py
   → <system-reminder>Warning: the file exists but the contents are empty.</system-reminder>
14. Write: /private/tmp/claude-501/-private-var-folders-0g-5q269b-51hj8tq4m54g45dhc0000gn-T-axiom-eval-n12dfy7l/d13dcd8e-f0f3-4f08-
   + import sys sys.path.insert(0, sys.argv[1]) from app import db as dbmod, handlers, repo def setup(): db = dbmod.connect() db.execute("INSERT INTO tenants VALUES (1,'acme'),(2,'victim')") db.execute("INSERT INTO users (id,tenant_id,email,display_name) VALUES (1,1,'a@acme.test','A'),(2,2,'v@victim.test','V')") db.execute("INSERT INTO invoices (tenant_id,customer_id,number,amount_cents,issued_at) VALUES (2,9,'INV-V-1',999999,'2026-10-01T00:00:00')") return db # F1: cross-tenant read via download_invoice db = setup(); attacker = repo.get_user(db, 1) print("F1 cross-tenant:", handlers.download_invoice(db, attacker, "INV-V-1")) # F2: mass assignment -> privilege escalation + tenant hop db = setup(); attacker = repo.ge
   → File created successfully at: /private/tmp/claude-501/-private-var-folders-0g-5q269b-51hj8tq4m54g45dhc0000gn-T-axiom-eval-n12dfy7l/d13dcd8e-f0f3-4f08-8df4-11f079ee8851/scratchpad/poc.py (file state is current in your context — no need to Re
15. Bash: python3 -I /private/tmp/claude-501/-private-var-folders-0g-5q269b-51hj8tq4m54g45dhc0000gn-T-axiom-eval-n12dfy7l/d13dcd8e
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
I found three serious problems, but I couldn't prove them by running code. The run of my local test script was waiting on your approval and never happened, so everything below comes from reading the source. The skill only allows a "confirmed" label after the code has been run, so I've graded the main problems "source-verified" and their severities are provisional. I read every file in `app/` and `tests/`. This was a single-pass review; I didn't write the full audit's tracking files.

The service assumes each user belongs to one tenant (customer organisation), and `app/repo.py:1` says every query must be limited to the caller's tenant. In what follows, "attacker" means any logged-in user.

## Findings (source-verified, provisional severity)

**F1 — High: any user can read other tenants' invoices** (`app/handlers.py:13-17` → `app/repo.py:21-25`)
- `download_invoice` looks up an invoice by its number without checking the tenant, and never compares the invoice's `tenant_id` with the user's.
- So an attacker who supplies another tenant's invoice number gets back that invoice's number and amount.
- Invoice numbers like `INV-1` follow a simple pattern, so they're easy to guess.
- **Fix:** add `tenant_id` to the lookup (`WHERE tenant_id = ? AND number = ?`), as `get_invoice` already does. Add a test where a user from tenant 1 asks for tenant 2's invoice number and gets `LookupError`.

**F2 — High: users can make themselves admin or move into another tenant** (`app/handlers.py:20-22`)
- `update_profile` writes every key the caller sends straight into the `users` table.
- Sending `{"role": "admin"}` grants admin. Sending `{"tenant_id": 2}` moves the attacker into tenant 2.
- Every other handler trusts `user["tenant_id"]`, so after the move the attacker can read tenant 2's data everywhere.
- **Fix:** only accept a fixed list of editable fields (e.g. `{"display_name"}`) and reject anything else. Add a test that `role` and `tenant_id` can't be changed.

**F3 — High, may be Critical: SQL injection through field names** (`app/handlers.py:22`)
- The same loop pastes `key` directly into the SQL text. Only the value is passed safely as a parameter.
- A key like `role = 'admin' WHERE 1=1 OR display_name` rewrites the whole statement, which could edit any user in any tenant.
- How much damage this does depends on whether the request layer passes field names through as-is, and that layer isn't in this repo.
- The F2 allow-list also closes this hole.

## Needs validation (no severity until the missing fact is known)

- **N1 — Coupon reuse under concurrent requests** (`app/handlers.py:27-33`): the code reads `uses_left`, then writes `row[0] - 1` in a separate step. Two requests at the same moment can both pass the check and redeem a single-use coupon twice.
  - **Missing fact:** whether requests can run concurrently against a shared database. This repo has no server.
  - **Fix:** do it in one statement, `UPDATE coupons SET uses_left = uses_left - 1 WHERE code=? AND tenant_id=? AND uses_left > 0`, and check `rowcount`. That also fixes the second `UPDATE`, which currently doesn't filter by tenant.
- **N2 — Guessable password-reset tokens** (`app/tokens.py:12-14`): reset tokens come from `random.choice`, which isn't designed for secrets, so with enough observed output the tokens can be predicted.
  - **Missing fact:** no code in this repo uses the tokens or limits reset attempts.
  - **Fix:** use `secrets.token_urlsafe(32)`, the way `new_session_id` already does.
- **N3 — Server-side request forgery (SSRF) in `send_test_webhook`** (`app/webhooks.py:16-21`): the only check is that the URL starts with `"http"`. Nothing blocks internal addresses such as `127.0.0.1`, `169.254.169.254` or private ranges, and up to 2 KB of the response body comes back to the caller.
  - **Missing fact:** whether the tenant controls `url`. No caller is in the repo.
  - **Fix:** check the resolved IP against those ranges, and don't follow redirects.
- **N4 — Webhook signatures
```

## Comparison note

Run with the skills before the depth pass (`bc003fc`, from a worktree), with the new fixtures and cases copied in. See `2026-11-17-depth-comparison.md`.
