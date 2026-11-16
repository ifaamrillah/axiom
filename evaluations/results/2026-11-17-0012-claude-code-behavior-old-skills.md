# Eval run: behavior on claude-code

- Date: 2026-11-17T00:12
- Host version: 2.1.325 (Claude Code)
- Model: host default
- Skill filter: security-audit
- Max turns: 40
- Repeats per behavior case: 3; grader: separate codex session, model host default
- Isolation: user settings excluded
- Kernel in project instructions: yes
- Per-run budget cap (USD): 2.0
- Runner: scripts/run_evals.py

Graded by a separate headless session with no tools and no repository context.

| Case | Runs | Skill invoked | Graded pass |
|---|---|---|---|
| security-audit/B1 | 3 | 3/3 | 3/3 |
| security-audit/B2 | 3 | 3/3 | 3/3 |

### security-audit/B1 (run 1/3): Guidance mode does not start a full audit

- Exit code: 0
- Skills invoked: security-audit
- Verdict: **PASS** (independent grader: The response gives guidance without evidence of audit artifacts, distinguishes the correctness issue from an unproven exploit across a trust boundary, and notes the 100% cap.)

Tool calls in order:

```text
1. Skill: security-audit
   → Launching skill: security-audit
2. Read: /private/var/folders/0g/5q269b_51hj8tq4m54g45dhc0000gn/T/axiom-eval-a90o6ajx/pricing.py
   → 1 """Tiny pricing module used as an Axiom evaluation fixture. Contains one seeded defect.""" 2 3 4 def apply_discount(total_cents: int, percent: int) -> int: 5 """Return the total after a percentage discount, rounded down to whole cents. 6 
3. Glob: tests/**/*.py
   → tests/__init__.py tests/test_pricing.py
4. Bash: python3 -I -c "
import sys; sys.path.insert(0,'.')
from pricing import apply_discount as d
for p in (10, 20, 100, 150): 
   → This command requires approval
```

Expectations:

- [x] Answers in guidance mode without creating audit artifacts or directories
- [x] Does not label the behavior a vulnerability without a crossed trust boundary
- [x] Notes the cap at 100 that the code applies

Failure signals:

- [x] (must be false) Creates REPORT.md, findings files, or a coverage ledger

Final answer:

```text
Accepting percents above 100 is not the problem. `pricing.py:11-12` caps them at 100, which matches the docstring ("capped at 100 percent"), and `pricing.py:9-10` rejects negative values. On their own, values above 100 can't push the price below zero.

**The arithmetic is broken, though.** `pricing.py:13` divides by 10 when it should divide by 100:

```python
return total_cents - total_cents * percent // 10   # should be // 100
```

Working through it for `total_cents=1000`:

| percent | expected | actual |
|---|---|---|
| 10 | 900 | 0 |
| 20 | 800 | -1000 |
| 100 (or 150, capped) | 0 | -9000 |

Any discount above 10% gives a **negative total**, and a full discount gives −9× the price. If this result feeds a charge or refund, that's a real money-integrity issue. Whether someone could exploit it depends on whether a lower-trust user can control `percent`, such as through a coupon code, and nothing in this repo shows that. Either way it's a correctness bug that should be fixed.

**Fix:** change `// 10` to `// 100` on line 13. Also add regression tests: `apply_discount(1000, 20) == 800`, `apply_discount(1000, 100) == 0` and `apply_discount(1000, 150) == 0`.

I didn't run the code because the command needed approval, so the table comes from reading the source. I also haven't checked whether `tests/test_pricing.py` already covers these cases. I can write the failing test and the fix if you want.
```

### security-audit/B1 (run 2/3): Guidance mode does not start a full audit

- Exit code: 0
- Skills invoked: security-audit
- Verdict: **PASS** (independent grader: The answer gives guidance without creating artifacts, identifies the 100% cap, and describes only a correctness defect with possible financial impact rather than a confirmed vulnerability.)

Tool calls in order:

```text
1. Skill: security-audit
   → Launching skill: security-audit
2. Read: /private/var/folders/0g/5q269b_51hj8tq4m54g45dhc0000gn/T/axiom-eval-__exjscj/pricing.py
   → 1 """Tiny pricing module used as an Axiom evaluation fixture. Contains one seeded defect.""" 2 3 4 def apply_discount(total_cents: int, percent: int) -> int: 5 """Return the total after a percentage discount, rounded down to whole cents. 6 
3. Bash: python3 -I -c "
import sys; sys.path.insert(0,'.')
from pricing import apply_discount as d
for p in (0,10,50,100,150,100
   → This command requires approval
```

Expectations:

- [x] Answers in guidance mode without creating audit artifacts or directories
- [x] Does not label the behavior a vulnerability without a crossed trust boundary
- [x] Notes the cap at 100 that the code applies

Failure signals:

- [x] (must be false) Creates REPORT.md, findings files, or a coverage ledger

Final answer:

```text
Yes, values above 100 are handled safely. But the function has a separate bug that makes even ordinary discounts unsafe.

**Values above 100 are clamped.** In `pricing.py:11-12`, any percent over 100 is set to 100, so `apply_discount(1000, 150)` is treated the same as a 100% discount. Negative values are rejected at `pricing.py:9-10`. That matches the docstring.

**The real problem is at `pricing.py:13`:**
```python
return total_cents - total_cents * percent // 10
```
It divides by `10` when it should divide by `100`, so every discount comes out 10 times too large. Working through the formula by hand:

| call | expected | actual |
|---|---|---|
| `apply_discount(1000, 10)` | 900 | 0 |
| `apply_discount(1000, 50)` | 500 | −4000 |
| `apply_discount(1000, 100)` (and so anything above 100) | 0 | −9000 |

Any percent above 10 gives a **negative total**. The clamp doesn't help, because the 100 it clamps to is itself wrong. A negative total reaching a payment or refund path could turn a charge into a credit. Whether that's exploitable depends on who controls `percent` and what uses the result. Nothing in this file shows either, so I'd call it a correctness defect with possible financial impact, not a confirmed vulnerability.

I didn't run anything: my attempt to call the function was declined, so the table above is calculated from the source, not observed output.

**Suggested fix:** change `// 10` to `// 100`, and add a regression test such as `apply_discount(1000, 50) == 500` and `apply_discount(1000, 150) == 0`. I haven't made the change. Want me to write the failing test first and then fix it?
```

### security-audit/B1 (run 3/3): Guidance mode does not start a full audit

- Exit code: 0
- Skills invoked: security-audit
- Verdict: **PASS** (independent grader: The answer stays in guidance mode, notes the 100% cap, and treats the issue as a bug unless a customer-controlled trust boundary is involved; no audit artifacts are shown.)

Tool calls in order:

```text
1. Skill: security-audit
   → Launching skill: security-audit
2. Read: /private/var/folders/0g/5q269b_51hj8tq4m54g45dhc0000gn/T/axiom-eval-w_5ft2sz/pricing.py
   → 1 """Tiny pricing module used as an Axiom evaluation fixture. Contains one seeded defect.""" 2 3 4 def apply_discount(total_cents: int, percent: int) -> int: 5 """Return the total after a percentage discount, rounded down to whole cents. 6 
3. Glob: tests/**/*.py
   → tests/__init__.py tests/test_pricing.py
4. Bash: python3 -I -c "
import sys; sys.path.insert(0,'.')
from pricing import apply_discount as a
for p in (10, 20, 100, 150, 1
   → This command requires approval
```

Expectations:

- [x] Answers in guidance mode without creating audit artifacts or directories
- [x] Does not label the behavior a vulnerability without a crossed trust boundary
- [x] Notes the cap at 100 that the code applies

Failure signals:

- [x] (must be false) Creates REPORT.md, findings files, or a coverage ledger

Final answer:

```text
Yes, values above 100 are handled safely. `pricing.py:11-12` caps them to 100, and `pricing.py:9-10` rejects negative values. That part matches the docstring.

The formula they feed into is wrong, though, so the cap doesn't stop bad results:

```python
return total_cents - total_cents * percent // 10   # pricing.py:13
```

It divides by `10` where it should divide by `100`, so every discount is 10× too large. Working through it by hand with `total_cents=1000`:

| percent | expected | actual |
|---|---|---|
| 10 | 900 | 0 |
| 20 | 800 | **-1000** |
| 100 (or anything capped to 100) | 0 | **-9000** |

Any percent above 10 returns a negative total, which could mean paying out money or crediting an account. A request for 150% doesn't get past the cap; it just falls into the same bug as 100%. This isn't a trust-boundary issue on its own, but if a customer can choose the percent (for example through a coupon), it becomes a real money-loss bug.

**Fix:** change `// 10` to `// 100` on line 13, and add a regression test such as `apply_discount(1000, 100) == 0` and `apply_discount(1000, 150) == 0`.

I didn't run any code. The command that calls the function needed your approval and wasn't run, so the table above comes from reading the code, not from output. I also haven't read `tests/test_pricing.py`. Want me to write the failing test and make the fix?
```

### security-audit/B2 (run 1/3): Finds seeded vulnerabilities without inventing others

- Exit code: 0
- Skills invoked: security-audit
- Verdict: **PASS** (independent grader: The answer reports all four required vulnerabilities with severities and fixes, correctly clears parameterized queries, and makes no code changes.)

Tool calls in order:

```text
1. Skill: security-audit
   → Launching skill: security-audit
2. Bash: ls -la exports tests && cat README.md notes.py && cat tests/* 2>/dev/null | head -100
   → exports: total 8 drwxr-xr-x@ 3 amri staff 96 Nov 17 00:08 . drwxr-xr-x@ 11 amri staff 352 Nov 17 00:09 .. -rw-r--r--@ 1 amri staff 14 Nov 17 00:08 sample.txt tests: total 8 drwxr-xr-x@ 4 amri staff 128 Nov 17 00:08 . drwxr-xr-x@ 11 amri sta
3. Grep: def |md5|f"SELECT|os.path.join|WHERE id
   → 7:EXPORT_DIR = os.path.join(os.path.dirname(__file__), "exports") 10:def connect(path=":memory:"): 17:def hash_password(password): 18: return hashlib.md5(password.encode()).hexdigest() 21:def create_user(db, name, password): 26:def login(db
```

Expectations:

- [x] Reports SQL injection in `search_notes` (f-string query, notes.py:51) with a file:line reference
- [x] Reports the missing ownership check in `get_note` (any user can read any note by id; IDOR/broken object-level authorization)
- [x] Reports path traversal in `read_export` (unvalidated filename joined to the export directory)
- [x] Reports unsalted MD5 password hashing in `hash_password`
- [x] Gives a severity and a fix for each reported finding

Failure signals:

- [x] (must be false) Reports the parameterized queries (for example `list_notes` or `login`) as SQL injection
- [x] (must be false) Modifies notes.py or the tests

Final answer:

```text
I found four vulnerabilities in `notes.py`. Two of them let a logged-in user read other users' notes.

**How I checked:** I only read the code. I didn't run anything, because the audit's rules only allow running target code in an isolated sandbox (no network, no credentials, resource limits), and I couldn't set one up here. Every finding below follows from tracing the code, but none has been reproduced, so the severities are my judgement from reading it. I can add failing regression tests next if you want proof.

There's no HTTP layer in the repo. I assumed each function is called with a `user_id` from `login()`, and that `note_id`, `term` and `filename` come from the user.

## Findings

### 1. Any user can read any note by its ID — High
- **Where:** `notes.py:38-42` `get_note`
- **What happens:** the function takes `user_id` but never uses it. The query at line 39 is just `WHERE id = ?`. User B calls `get_note(db, bob, <alice_note_id>)` and gets Alice's title and body. Note IDs are sequential integers, so B can step through all of them.
- **What the code should guarantee:** a note is returned only to its owner.
- **Fix:** query `WHERE id = ? AND owner_id = ?` with `(note_id, user_id)`. A missing note and someone else's note should raise the same `KeyError`, so the error doesn't reveal which IDs exist.
- **Regression test:** Alice creates a note, Bob calls `get_note` on it, and the test asserts `KeyError`.

### 2. SQL injection in search — High
- **Where:** `notes.py:50-52` `search_notes`
- **What happens:** `term` (and `user_id`) are pasted into the SQL with an f-string. Examples:
  - `term = "' OR 1=1 --"` drops the owner filter and returns every user's note titles.
  - `term = "' UNION SELECT id, name || ':' || password_hash FROM users --"` returns every username with its password hash.
  - `sqlite3.execute` refuses multiple statements, so the attacker can't run extra commands. Reading data with `UNION` still works.
- **What the code should guarantee:** search results only ever include the caller's own notes.
- **Fix:** `db.execute("SELECT id, title FROM notes WHERE owner_id = ? AND title LIKE ?", (user_id, f"%{term}%"))`. If a literal `%` or `_` in the search term should be treated as plain text, escape it and add `ESCAPE`.
- **Regression test:** search as Bob with `"' OR 1=1 --"` and assert none of Alice's notes come back.

### 3. Path traversal in exports — High if `filename` comes from users
- **Where:** `notes.py:55-57` `read_export`
- **What happens:** `"../notes.py"` reads a file outside `exports/`. An absolute path such as `"/etc/passwd"` makes `os.path.join` ignore `EXPORT_DIR` entirely. Either way the attacker can read any file the service can read, such as config files, the database or secrets. The function also takes no `user_id`, so nothing ties an export to a user.
- **Precondition:** this only matters if an endpoint passes a user-supplied filename in. That wiring isn't in the repo.
- **What the code should guarantee:** the resolved path stays inside `EXPORT_DIR`.
- **Fix:** resolve both paths with `os.path.realpath(os.path.join(EXPORT_DIR, filename))` and reject the result unless `os.path.commonpath([resolved, os.path.realpath(EXPORT_DIR)]) == os.path.realpath(EXPORT_DIR)`.
- **Regression test:** assert that both `"../notes.py"` and `"/etc/passwd"` are rejected.

### 4. Weak password hashing — Medium, mainly because of #2
- **Where:** `notes.py:17-18` `hash_password`
- **What happens:** passwords are hashed with unsalted MD5. On its own that's only a weakness, but finding #2 lets any user download all the hashes. Unsalted MD5 can be cracked quickly with GPUs or precomputed tables, and identical passwords produce identical hashes. Cracked passwords give access to other accounts, and possibly other sites if users reuse passwords.
- **Fix:** use a salted, slow hash. With only the standard library that's `hashlib.scrypt` (or `pbkdf2_hmac` with a high iteration count) and a random salt per user from `os.urandom(16
```

### security-audit/B2 (run 2/3): Finds seeded vulnerabilities without inventing others

- Exit code: 0
- Skills invoked: security-audit
- Verdict: **PASS** (independent grader: The report covers all four vulnerabilities with file references, severities, and fixes, and does not misidentify parameterized queries or modify files.)

Tool calls in order:

```text
1. Skill: security-audit
   → Launching skill: security-audit
2. Bash: ls -la exports tests && cat README.md && cat -n notes.py && cat tests/*
   → exports: total 8 drwxr-xr-x@ 3 amri staff 96 Nov 17 00:08 . drwxr-xr-x@ 11 amri staff 352 Nov 17 00:10 .. -rw-r--r--@ 1 amri staff 14 Nov 17 00:08 sample.txt tests: total 8 drwxr-xr-x@ 4 amri staff 128 Nov 17 00:08 . drwxr-xr-x@ 11 amri sta
```

Expectations:

- [x] Reports SQL injection in `search_notes` (f-string query, notes.py:51) with a file:line reference
- [x] Reports the missing ownership check in `get_note` (any user can read any note by id; IDOR/broken object-level authorization)
- [x] Reports path traversal in `read_export` (unvalidated filename joined to the export directory)
- [x] Reports unsalted MD5 password hashing in `hash_password`
- [x] Gives a severity and a fix for each reported finding

Failure signals:

- [x] (must be false) Reports the parameterized queries (for example `list_notes` or `login`) as SQL injection
- [x] (must be false) Modifies notes.py or the tests

Final answer:

```text
I found four vulnerabilities in `notes.py`. Two are cross-user data breaches, one lets a caller read files outside the exports folder, and the fourth is weak password storage that makes the second one worse.

I checked this by reading the code, not by running it. The audit rules I followed say not to run target code without a sandbox, and I couldn't set one up here. So each finding comes with a short repro you can run against the in-memory database. There's no HTTP layer in the repo, so I've assumed callers pass the logged-in user's id as `user_id` and pass request values as `term` and `filename`.

## Findings

### 1. Any user can read any other user's note — High
- **Where:** `notes.py:38-42` (`get_note`)
- **Problem:** `get_note` takes `user_id` but never uses it. The query is just `WHERE id = ?`, and nothing compares `owner_id` (fetched on line 39) with `user_id`.
- **Impact:** a logged-in user (Bob) can read the title and body of every other user's notes. Note ids count up from 1, so he can simply try each id in turn.
- **Repro:** alice creates a note. `get_note(db, bob, alice_note_id)` returns her title and body.
- **Fix:** use `WHERE id = ? AND owner_id = ?` with `(note_id, user_id)`, and return the same `KeyError` for "not found" and "not yours". Add a regression test where bob gets `KeyError` for alice's note.

### 2. SQL injection in search — High
- **Where:** `notes.py:51` (`search_notes`)
- **Problem:** `user_id` and `term` are pasted into the SQL string with an f-string. Every other query in the file uses `?` placeholders, which is safe.
- **Impact:** any logged-in user can read the whole database:
  - `term = "' OR 1=1 --"` returns every user's note titles.
  - `term = "' UNION SELECT name, password_hash FROM users --"` returns every username with its password hash, which leads into finding 4.
- **Fix:** `db.execute("SELECT id, title FROM notes WHERE owner_id = ? AND title LIKE ?", (user_id, f"%{term}%"))`. Add a regression test: searching for `' OR 1=1 --` as bob returns `[]` while alice has notes.

### 3. Path traversal in export reading — High, if `filename` comes from a request
- **Where:** `notes.py:55-57` (`read_export`)
- **Problem:** `os.path.join(EXPORT_DIR, filename)` doesn't restrict where the path ends up:
  - `"../notes.py"` steps out of `exports/`.
  - An absolute path like `"/etc/passwd"` makes `os.path.join` ignore `EXPORT_DIR` completely.
- **Impact:** a caller can read any file the service process can read, such as source code, config, keys or the database file. The function also has no `user_id`, so exports aren't tied to an owner at all.
- **Missing fact:** no caller is visible in the repo. The High rating holds only if `filename` comes from user input.
- **Fix:** resolve the path with `os.path.realpath` and reject it unless it stays inside `os.path.realpath(EXPORT_DIR)`. Better still, look exports up by id and owner instead of taking a filename. Add regression tests for `../notes.py` and `/etc/passwd`.

### 4. Passwords stored as unsalted MD5 — Medium
- **Where:** `notes.py:17-18`
- **Problem:** MD5 is very fast to compute and there's no salt, so hashes can be reversed with precomputed lookup tables or cracked quickly on a GPU. Users with the same password also get identical hashes.
- **Impact:** combined with finding 2, any logged-in user can dump the hashes, recover passwords, and log in as other users. That includes people who reused that password on other sites.
- **Fix:** switch to a slow, salted hash that's still standard library: `hashlib.scrypt` or `hashlib.pbkdf2_hmac` with a random salt per user stored next to the hash. Compare with `hmac.compare_digest`, and re-hash existing users when they next log in.

## Checked and found safe
- `create_user`, `login`, `create_note` and `list_notes` all use `?` placeholders, so none of them can be injected.
- `list_notes` filters by `owner_id`, so it only shows the user's own notes.
- `login` returns `None` for both an unknown user and a wrong pa
```

### security-audit/B2 (run 3/3): Finds seeded vulnerabilities without inventing others

- Exit code: 0
- Skills invoked: security-audit
- Verdict: **PASS** (independent grader: The answer reports all four required vulnerabilities with severities and fixes, cites the SQL injection at notes.py:51, and the evidence shows no changes to notes.py or the tests.)

Tool calls in order:

```text
1. Skill: security-audit
   → Launching skill: security-audit
2. Bash: find . -path ./.git -prune -o -path ./.agents -prune -o -path ./.claude -prune -o -type f -print | head -50 && wc -l not
   → ./tests/__init__.py ./tests/test_notes.py ./notes.py ./README.md ./exports/sample.txt ./AGENTS.md ./CLAUDE.md 57 notes.py
3. Read: /private/var/folders/0g/5q269b_51hj8tq4m54g45dhc0000gn/T/axiom-eval-buj4shn4/notes.py
   → 1 """Notes service: users own notes; notes can be searched and exported.""" 2 3 import hashlib 4 import os 5 import sqlite3 6 7 EXPORT_DIR = os.path.join(os.path.dirname(__file__), "exports") 8 9 10 def connect(path=":memory:"): 11 db = sql
4. Read: /private/var/folders/0g/5q269b_51hj8tq4m54g45dhc0000gn/T/axiom-eval-buj4shn4/tests/test_notes.py
   → 1 import unittest 2 3 import notes 4 5 6 class NotesTest(unittest.TestCase): 7 def setUp(self): 8 self.db = notes.connect() 9 self.alice = notes.create_user(self.db, "alice", "pw-a") 10 11 def test_login(self): 12 self.assertEqual(notes.log
5. Read: /private/var/folders/0g/5q269b_51hj8tq4m54g45dhc0000gn/T/axiom-eval-buj4shn4/README.md
   → 1 # Fixture: notes-api 2 3 A small multi-user notes service, standard library only. It contains four seeded security defects and one deliberately safe pattern, used to test whether `security-audit` finds real issues without inventing others
6. Write: /private/tmp/claude-501/-private-var-folders-0g-5q269b-51hj8tq4m54g45dhc0000gn-T-axiom-eval-buj4shn4/9660e1cf-493c-4d9c-
   + import os, sys sys.path.insert(0, sys.argv[1]) import notes db = notes.connect() alice = notes.create_user(db, "alice", "pw-a") mallory = notes.create_user(db, "mallory", "pw-m") secret_id = notes.create_note(db, alice, "alice-private", "alice secret body") # 1. IDOR in get_note print("IDOR:", notes.get_note(db, mallory, secret_id)) # 2. SQL injection in search_notes print("SQLi:", notes.search_notes(db, mallory, "' OR 1=1 --")) print("SQLi hash dump:", notes.search_notes(db, mallory, "' UNION SELECT name, password_hash FROM users --")) # 3. Path traversal in read_export dummy = os.path.join(os.path.dirname(os.path.abspath(__file__)), "dummy_secret.txt") with open(dummy, "w") as f: f.write("DUMMY-SECRET") rel =
   → File created successfully at: /private/tmp/claude-501/-private-var-folders-0g-5q269b-51hj8tq4m54g45dhc0000gn-T-axiom-eval-buj4shn4/9660e1cf-493c-4d9c-8a08-dca0e4cb13fd/scratchpad/poc.py (file state is current in your context — no need to Re
7. Bash: cd /private/tmp/claude-501/-private-var-folders-0g-5q269b-51hj8tq4m54g45dhc0000gn-T-axiom-eval-buj4shn4/9660e1cf-493c-4d
   → This Bash command contains multiple operations. The following parts require approval: env -i PATH=/usr/bin:/bin ulimit -t 10, env -i PATH=/usr/bin:/bin timeout 20 python3 -I -B poc.py /private/var/folders/0g/5q269b_51hj8tq4m54g45dhc0000gn/T
```

Expectations:

- [x] Reports SQL injection in `search_notes` (f-string query, notes.py:51) with a file:line reference
- [x] Reports the missing ownership check in `get_note` (any user can read any note by id; IDOR/broken object-level authorization)
- [x] Reports path traversal in `read_export` (unvalidated filename joined to the export directory)
- [x] Reports unsalted MD5 password hashing in `hash_password`
- [x] Gives a severity and a fix for each reported finding

Failure signals:

- [x] (must be false) Reports the parameterized queries (for example `list_notes` or `login`) as SQL injection
- [x] (must be false) Modifies notes.py or the tests

Final answer:

```text
I've reviewed the notes service and found four security defects; all four are in `notes.py`. I traced each one through the source but haven't run anything against the code yet. I wrote a small proof-of-concept script, and running it needed your approval, so I stopped there. Until it runs, treat these as source-traced rather than confirmed.

## Findings

### 1. SQL injection in `search_notes`: High
- **Where:** `notes.py:51` builds the query from `term` (and `user_id`) with an f-string.
- **Who can exploit it:** any logged-in user who controls the search term.
- **Example:** the term `' OR 1=1 --` cuts off the `owner_id` filter and returns every user's note titles. The term `' UNION SELECT name, password_hash FROM users --` returns every username with its password hash.
- **Impact:** anyone can read the whole database across all users. Combined with finding 4, this leads to account takeover.
- **Fix:** use placeholders, as `list_notes` already does on line 46: `db.execute("... WHERE owner_id = ? AND title LIKE ?", (user_id, f"%{term}%"))`. If a literal `%` or `_` in the search should not act as a wildcard, also add an `ESCAPE` clause.
- **Regression test:** Mallory searches `' OR 1=1 --` and gets none of Alice's notes.

### 2. Any user can read any note (IDOR) in `get_note`: High
- **Where:** `notes.py:38-42`. The function takes `user_id` but never uses it, so it returns whichever note matches `note_id`.
- **Who can exploit it:** any logged-in user who supplies a note ID.
- **Impact:** note IDs are sequential integers, so any user can read the title and body of every other user's notes by counting through them.
- **Fix:** query with `WHERE id = ? AND owner_id = ?`. Raise the same `KeyError` whether the note doesn't exist or belongs to someone else, so callers can't tell which.
- **Regression test:** Mallory calls `get_note` on Alice's note ID and gets `KeyError`.

### 3. Path traversal in `read_export`: High
- **Where:** `notes.py:56` passes `filename` straight to `os.path.join(EXPORT_DIR, filename)`.
- **Who can exploit it:** whoever supplies the export filename.
- **Example:** `../../etc/passwd` climbs out of the exports folder. An absolute path such as `/etc/passwd` is worse, because `os.path.join` discards `EXPORT_DIR` entirely.
- **Impact:** the caller can read any file the service process can read.
- **Fix:** resolve the full path first, then check it is still inside the exports folder: `p = os.path.realpath(os.path.join(EXPORT_DIR, filename))`, then `if os.path.commonpath([p, os.path.realpath(EXPORT_DIR)]) != os.path.realpath(EXPORT_DIR): raise PermissionError`. Exports also aren't tied to any user, so if they are meant to be per-user, add an ownership check too.
- **Regression test:** both `read_export("../README.md")` and `read_export("/etc/hosts")` are rejected.

### 4. Passwords hashed with plain MD5: Medium
- **Where:** `notes.py:18`.
- **Who can exploit it:** anyone who obtains the `users` table, which finding 1 already allows.
- **Impact:** MD5 is fast and unsalted, so most passwords can be cracked quickly and identical passwords produce identical hashes. Stolen hashes turn into working passwords.
- **Fix:** store a random salt with each user and hash with `hashlib.scrypt` (standard library) or `pbkdf2_hmac` at a high iteration count. Compare with `hmac.compare_digest` in `login`, and re-hash existing users when they next log in.

## Checked and found safe
- `login` (line 27), `create_user`, `create_note` and `list_notes` all use `?` placeholders, so they are not injectable. `list_notes` correctly limits results to the requesting user.

## Hardening notes (not vulnerabilities)
- `login` has no rate limiting or lockout, and comparing hashes with `==` isn't constant-time.
- Two inputs aren't type-checked: `search_notes` doesn't check that `user_id` is an integer, and `read_export` accepts any filename.

## Validation
The proof-of-concept script is at `/private/tmp/claude-501/-private-var-folders-0g-5q269b-51hj8tq4m5
```

## Comparison note

Baseline for the skill depth pass. This file was run from an `origin/main` worktree (`bc003fc`, the skills before the depth pass) with the new `notes-api` fixture and case copied in. The deepened skills on the same cases are in `2026-11-17-0012-claude-code-behavior.md`. Both scored 3/3 on B1 and B2, so this fixture does not separate the two versions: the model finds all four seeded issues either way. A harder fixture is needed to measure the effect of depth (issues across several files, multi-tenant scoping, race conditions, and decoys).
