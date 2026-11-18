---
skill: project-documentation
fixture: evaluations/fixtures/discount-bug
---

# Eval cases: project-documentation

## Should trigger

- "Update the README to document apply_discount's behavior"
- "Our docs are stale; refresh the project documentation from the code"
- "Let's do a retro on the mistakes from this session and record what we learned"

## Should not trigger

- "Fix the discount bug" → `debugging`
- "Write a spec for loyalty discounts" → `requirements-analysis`

## Behavior

### B1: Documents the code, not the intent

- Prompt: "Update the README to document how apply_discount behaves."
- Fixture: `evaluations/fixtures/discount-bug`
- Expect: Reads pricing.py before writing
- Expect: Flags that the implementation (divides by 10) disagrees with the documented intent instead of documenting the intent as current behavior
- Fail if: States that a 10% discount on 1000 returns 900 as current behavior without noting the bug

### B2: Retro writes a learning, not a Pitfall, on first sighting

- Prompt: "Retro: earlier today you ran `pytest` from `src/` and it collected 0 tests; running it from the repository root fixed it. Record what we learned."
- Fixture: `evaluations/fixtures/discount-bug`
- Expect: Writes or proposes `.axiom/learnings/<yyyy-mm-dd>-<slug>.md` with trigger, lesson, evidence, confidence, scope, and seen fields
- Expect: Does not add a Pitfalls line yet, or asks the user to confirm before promoting, because this is the first sighting
- Fail if: Adds a Pitfalls line to the instructions file without a second sighting or user confirmation
- Fail if: The lesson is not a rule ("be more careful with paths")

### B3: Promotion names the strongest enforcement

- Prompt: "That pytest-from-src mistake happened again. I confirm the rule: run tests from the repo root. Promote it."
- Fixture: `evaluations/fixtures/discount-bug`
- Expect: Adds one dated Pitfalls line with the rule and an enforcement level
- Expect: Proposes an enforcement stronger than a doc line, such as a pytest config (`testpaths`, `rootdir`) or a test script that sets the directory
- Fail if: Adds a paragraph or a session story instead of one line
- Fail if: Labels the Pitfall doc-only without saying why no check, test, or config could prevent it
