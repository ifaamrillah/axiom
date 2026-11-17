---
skill: security-audit
---

# Eval cases: security-audit

## Should trigger

- "Is this endpoint vulnerable to IDOR?"
- "Do a full security audit of this repository"
- "Pen-test the auth module and give me a report"
- "We commit a .mcp.json and a hooks config for our coding agent. Could that be a security problem for contributors?"

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
- Seeded: `search_notes` builds its SQL query with an f-string from user input
- Seeded: `get_note` returns a note by id without checking that the caller owns it
- Seeded: `read_export` joins an unvalidated filename to the export directory (path traversal)
- Seeded: `hash_password` uses unsalted MD5
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
- Seeded: `download_invoice` looks invoices up with `find_invoice_by_number`, which is not scoped to the tenant
- Seeded: `update_profile` lets a user set any column, including `role`
- Seeded: `redeem_coupon` reads then writes `uses_left` without an atomic update or lock
- Seeded: `send_test_webhook` fetches user URLs with only a `startswith("http")` check (SSRF)
- Seeded: `verify_signature` compares HMACs with `==`
- Seeded: `new_reset_token` uses `random` instead of a secure source
- Expect: Reports that `download_invoice` (app/handlers.py) uses `find_invoice_by_number` (app/repo.py), which is not scoped to the tenant, so a user can read another tenant's invoice
- Expect: Reports that `update_profile` lets a user set arbitrary columns, including `role` (mass assignment or privilege escalation; a column-name injection report also counts)
- Expect: Reports the race in `redeem_coupon`: a read-then-write on `uses_left` without an atomic update or lock lets a coupon be redeemed more times than allowed
- Expect: Reports SSRF in `send_test_webhook`: user-supplied URLs are fetched with only a `startswith("http")` check
- Expect: Reports that `verify_signature` compares HMACs with `==` instead of a constant-time comparison
- Expect: Reports that `new_reset_token` uses `random` instead of a cryptographically secure source
- Fail if: Reports the allowlisted `ORDER BY {column}` in `list_invoices` as SQL injection
- Fail if: Reports the fixed-argument `subprocess.run` in app/backup.py as command injection
- Fail if: Modifies application code or tests

### B4: Precedent applies: escaped JSX text is not XSS

- Prompt: "Security check before I merge this React component: `export function Comment({ comment }) { return <div className=\"comment\"><b>{comment.author}</b><p>{comment.body}</p></div>; }` The author and body come straight from other users' posts via our API. Is this an XSS risk?"
- Expect: Says React escapes `{comment.body}` and `{comment.author}` as JSX text, so this is not an XSS finding
- Expect: Names the condition that would make it reportable (a raw sink such as `dangerouslySetInnerHTML`, or a user URL in `href`/`src`)
- Fail if: Reports XSS as a confirmed finding or gives it a severity
- Fail if: Creates audit artifacts or directories

### B5: Precedent does not apply: dangerouslySetInnerHTML with user input

- Prompt: "Security check before I merge this React component: `export function Comment({ comment }) { return <div className=\"comment\" dangerouslySetInnerHTML={{ __html: comment.body }} />; }` The body comes straight from other users' posts via our API and is stored as typed. Is this an XSS risk?"
- Split: held-out
- Expect: Reports stored XSS: another user's post body reaches `dangerouslySetInnerHTML` without sanitization, so script runs in the viewer's session
- Expect: Gives a severity consistent with the anchors (stored XSS affecting other users is High), or states that it is `needs_validation` and names the exact unresolved fact (for example, whether the API sanitizes the body)
- Expect: Gives the smallest fix (render as text, or sanitize with an allowlist sanitizer such as DOMPurify before rendering)
- Fail if: Dismisses the issue because React escapes output
