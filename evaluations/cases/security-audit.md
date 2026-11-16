---
skill: security-audit
---

# Eval cases: security-audit

## Should trigger

- "Is this endpoint vulnerable to IDOR?"
- "Do a full security audit of this repository"
- "Pen-test the auth module and give me a report"

## Should not trigger

- "Make the login page look nicer" → `ui-ux-design`
- "Speed up the slow orders query" → `none`

## Behavior

### B1: Guidance mode does not start a full audit

- Prompt: "Quick question: is it safe that apply_discount accepts percent values above 100?"
- Fixture: `evaluations/fixtures/discount-bug`
- Expect: Answers in guidance mode without creating audit artifacts or directories
- Expect: Does not label the behavior a vulnerability without a crossed trust boundary
- Expect: Notes the cap at 100 that the code applies
- Fail if: Creates REPORT.md, findings files, or a coverage ledger

### B2: Finds seeded vulnerabilities without inventing others

- Prompt: "Review this notes service for security vulnerabilities and report your findings."
- Fixture: `evaluations/fixtures/notes-api`
- Expect: Reports SQL injection in `search_notes` (f-string query, notes.py:51) with a file:line reference
- Expect: Reports the missing ownership check in `get_note` (any user can read any note by id; IDOR/broken object-level authorization)
- Expect: Reports path traversal in `read_export` (unvalidated filename joined to the export directory)
- Expect: Reports unsalted MD5 password hashing in `hash_password`
- Expect: Gives a severity and a fix for each reported finding
- Fail if: Reports the parameterized queries (for example `list_notes` or `login`) as SQL injection
- Fail if: Modifies notes.py or the tests

### B3: Subtle multi-file issues in a multi-tenant service

- Prompt: "Do a security audit of this billing service and report your findings."
- Fixture: `evaluations/fixtures/tenant-billing`
- Expect: Reports that `download_invoice` (app/handlers.py) uses `find_invoice_by_number` (app/repo.py), which is not scoped to the tenant, so a user can read another tenant's invoice
- Expect: Reports that `update_profile` lets a user set arbitrary columns, including `role` (mass assignment or privilege escalation; a column-name injection report also counts)
- Expect: Reports the race in `redeem_coupon`: a read-then-write on `uses_left` without an atomic update or lock lets a coupon be redeemed more times than allowed
- Expect: Reports SSRF in `send_test_webhook`: user-supplied URLs are fetched with only a `startswith("http")` check
- Expect: Reports that `verify_signature` compares HMACs with `==` instead of a constant-time comparison
- Expect: Reports that `new_reset_token` uses `random` instead of a cryptographically secure source
- Fail if: Reports the allowlisted `ORDER BY {column}` in `list_invoices` as SQL injection
- Fail if: Reports the fixed-argument `subprocess.run` in app/backup.py as command injection
- Fail if: Modifies application code or tests
