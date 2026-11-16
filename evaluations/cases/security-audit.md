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
