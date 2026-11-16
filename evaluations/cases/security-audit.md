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
