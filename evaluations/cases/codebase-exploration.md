---
skill: codebase-exploration
fixture: evaluations/fixtures/discount-bug
---

# Eval cases: codebase-exploration

## Should trigger

- "Where is the discount cap applied, and which tests cover it?"
- "Trace how apply_discount is used across this repo"
- "Map out this codebase for me: entry points, modules, tests"

## Should not trigger

- "Write release notes for 2.3.0" → `release-management`
- "Add a dark mode toggle" → `ui-ux-design`

## Behavior

### B1: Read-only answer with file references

- Prompt: "Where is the discount cap applied, and which tests cover it?"
- Fixture: `evaluations/fixtures/discount-bug`
- Expect: Cites pricing.py with the line or function where the cap is applied
- Expect: Names the test file and says which cases the tests cover
- Fail if: Edits any file
