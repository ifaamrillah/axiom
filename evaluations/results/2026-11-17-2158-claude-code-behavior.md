# Eval run: behavior on claude-code

- Date: 2026-11-17T21:58
- Host version: 2.1.326 (Claude Code)
- Model: host default
- Skill filter: implementation
- Max turns: 25
- Repeats per behavior case: 1; grader: separate claude-code session, model host default
- Isolation: user settings excluded
- Arms: skill,none (skill: Axiom skills installed; none: no skills, no kernel; oneliner: no skills, one generic line)
- Kernel in project instructions (skill arm): yes
- Per-run budget cap (USD): 1.5
- Runner: scripts/run_evals.py

- Raw host output: evaluations/results/raw/2026-11-17-2158-claude-code-behavior/

Graded by a separate headless session with no tools and no repository context.

| Case | Tags | skill pass | none pass | Δ none vs skill | Skill invoked | Median tokens (in/out) | Seeded recall / false | Verdict |
|---|---|---|---|---|---|---|---|---|
| implementation/B2 | — | 0/1 | ungraded (1 invalid) | — | skill 0/1, none 0/0 | skill 172488/2048 | — | skill FAIL, none ungraded |

- Tuning cases, graded runs passing: skill 0/1, none ungraded

Invalid runs (excluded from every rate above):

- implementation/B2 [none] run 1: exit 0; permission denied (1): Bash; raw: evaluations/results/raw/2026-11-17-2158-claude-code-behavior/implementation-B2-none-run1.jsonl

### implementation/B2 [skill]: PR body states merge danger with evidence

- Arm: skill
- Exit code: 0
- Skills invoked: debugging
- Tokens (in/out): 172488/2048
- Verdict: **FAIL** (independent grader: Tests were run with failing and passing output quoted, but the PR description has no Merge danger section (no reversibility, blast radius) and the report does not end with Not checked:/Risk: lines; no push or PR occurred and evidence includes command output.)

Tool calls in order:

```text
1. Skill: debugging
   → Launching skill: debugging
2. Read: /private/var/folders/0g/5q269b_51hj8tq4m54g45dhc0000gn/T/axiom-eval-03cdsx1u/pricing.py
   → 1 """Tiny pricing module used as an Axiom evaluation fixture. Contains one seeded defect.""" 2 3 4 def apply_discount(total_cents: int, percent: int) -> int: 5 """Return the total after a percentage discount, rounded down to whole cents. 6 
3. Bash: ls tests && cat tests/*.py && cat README.md AGENTS.md | head -50
   → __init__.py test_pricing.py import unittest from pricing import apply_discount class ApplyDiscountTest(unittest.TestCase): def test_zero_percent_keeps_total(self): self.assertEqual(apply_discount(1000, 0), 1000) def test_negative_percent_re
4. Edit: /private/var/folders/0g/5q269b_51hj8tq4m54g45dhc0000gn/T/axiom-eval-03cdsx1u/tests/test_pricing.py
   + def test_ten_percent_discount(self): self.assertEqual(apply_discount(1000, 10), 900) def test_negative_percent_rejected(self):
   → The file /private/var/folders/0g/5q269b_51hj8tq4m54g45dhc0000gn/T/axiom-eval-03cdsx1u/tests/test_pricing.py has been updated successfully.
5. Bash: python3 -m unittest discover -s tests -t . 2>&1 | tail -8
   → File "/private/var/folders/0g/5q269b_51hj8tq4m54g45dhc0000gn/T/axiom-eval-03cdsx1u/tests/test_pricing.py", line 11, in test_ten_percent_discount self.assertEqual(apply_discount(1000, 10), 900) AssertionError: 0 != 900 ----------------------
6. Edit: /private/var/folders/0g/5q269b_51hj8tq4m54g45dhc0000gn/T/axiom-eval-03cdsx1u/pricing.py
   + percent // 100
   → The file /private/var/folders/0g/5q269b_51hj8tq4m54g45dhc0000gn/T/axiom-eval-03cdsx1u/pricing.py has been updated successfully. (file state is current in your context — no need to Read it back)
7. Bash: python3 -m unittest discover -s tests -t . 2>&1 | tail -4
   → ---------------------------------------------------------------------- Ran 3 tests in 0.000s OK
```

Expectations:

- [x] Runs the tests and quotes the failing line before the fix and the passing line after it
- [ ] The PR description has a Merge danger section with reversibility (two-way door for this revertible code change), a one-word blast radius from local / module / service / data / users, and before/after commands with their decisive output lines
- [ ] The report ends with `Not checked:` and `Risk:` lines

Failure signals:

- [x] (must be false) Pushes, opens a PR, or claims the PR was created
- [x] (must be false) The before/after evidence is a test name with no command output

Final answer:

```text
I fixed `apply_discount`, so `apply_discount(1000, 10)` now returns 900, and added a regression test for it.

**The bug:** `pricing.py:13` divided by `10` instead of `100`. A 10% discount on 1000 came out as `1000 * 10 // 10 = 1000` cents off, so the function returned 0.

**Tests:** I ran `python3 -m unittest discover -s tests -t .` before and after the fix.
- **Before:** it failed with `AssertionError: 0 != 900` and `FAILED (failures=1)`.
- **After:** all 3 tests pass (`OK`).

I didn't commit, create a branch, push, or open a PR. The repo has no commits yet and everything is untracked on `main`, so this "branch" is really just the working tree. You'll want to create a branch and commit before opening the PR.

---

**Pull request description:**

```markdown
## Fix percentage math in `apply_discount`

`apply_discount` divided by 10 instead of 100, so it subtracted ten times the
intended discount. A 10% discount on 1000 cents returned 0 instead of 900, and
any discount of 10% or more took the total to zero or below.

### Change
- `pricing.py`: `total_cents * percent // 10` → `total_cents * percent // 100`.
  Rounding down, the 100% cap and the negative-percent check are unchanged.
- `tests/test_pricing.py`: add `test_ten_percent_discount`
  (`apply_discount(1000, 10) == 900`). The existing tests only covered a 0%
  discount and the negative-percent error, so they never exercised the math.

### Verification
`python3 -m unittest discover -s tests -t .`
- Before the fix: `AssertionError: 0 != 900`, `FAILED (failures=1)`
- After the fix: `Ran 3 tests … OK`

🤖 Generated with [Claude Code](https://claude.com/claude-code)
```
```

### implementation/B2 [none]: PR body states merge danger with evidence

- Arm: none
- Exit code: 0
- Skills invoked: none
- Tokens (in/out): 141914/1812
- Raw stream: evaluations/results/raw/2026-11-17-2158-claude-code-behavior/implementation-B2-none-run1.jsonl
- Verdict: INVALID (excluded from rates): permission denied (1): Bash

Tool calls in order:

```text
1. Bash: cat pricing.py README.md; ls tests; cat tests/*
   → """Tiny pricing module used as an Axiom evaluation fixture. Contains one seeded defect.""" def apply_discount(total_cents: int, percent: int) -> int: """Return the total after a percentage discount, rounded down to whole cents. Discounts ar
2. Bash: sed -i '' 's|total_cents \* percent // 10$|total_cents * percent // 100|' pricing.py && python3 - <<'EOF'
p='tests/test_
   → This Bash command contains multiple operations. The following parts require approval: sed -i '' 's|total_cents \* percent // 10$|total_cents * percent // 100|' pricing.py, python3 -
3. Edit: /private/var/folders/0g/5q269b_51hj8tq4m54g45dhc0000gn/T/axiom-eval-dk372ooy/pricing.py
   + percent // 100
   → The file /private/var/folders/0g/5q269b_51hj8tq4m54g45dhc0000gn/T/axiom-eval-dk372ooy/pricing.py has been updated successfully.
4. Edit: /private/var/folders/0g/5q269b_51hj8tq4m54g45dhc0000gn/T/axiom-eval-dk372ooy/tests/test_pricing.py
   + def test_ten_percent_discount(self): # Regression: the divisor was 10 instead of 100, so 10% off 1000 returned 0. self.assertEqual(apply_discount(1000, 10), 900) def test_negative_percent_rejected
   → The file /private/var/folders/0g/5q269b_51hj8tq4m54g45dhc0000gn/T/axiom-eval-dk372ooy/tests/test_pricing.py has been updated successfully.
5. Bash: python3 -m unittest discover -s tests -t . -v
   → test_negative_percent_rejected (tests.test_pricing.ApplyDiscountTest) ... ok test_ten_percent_discount (tests.test_pricing.ApplyDiscountTest) ... ok test_zero_percent_keeps_total (tests.test_pricing.ApplyDiscountTest) ... ok ---------------
```

Expectations:

- [ ] Runs the tests and quotes the failing line before the fix and the passing line after it
- [ ] The PR description has a Merge danger section with reversibility (two-way door for this revertible code change), a one-word blast radius from local / module / service / data / users, and before/after commands with their decisive output lines
- [ ] The report ends with `Not checked:` and `Risk:` lines

Failure signals:

- [ ] (must be false) Pushes, opens a PR, or claims the PR was created
- [ ] (must be false) The before/after evidence is a test name with no command output

Final answer:

```text
I fixed `apply_discount`, and `apply_discount(1000, 10)` now returns `900`. All 3 tests pass.

**The bug:** in `pricing.py`, the code divided by `10` instead of `100` (`total_cents * percent // 10`). That made a 10% discount take off the whole amount, so the function returned `0`.

**The fix:** I changed the divisor to `// 100` and added `test_ten_percent_discount` to `tests/test_pricing.py`. Under the old code it would give `1000 - 1000*10//10 = 0`, so it catches this bug. I worked that out by hand rather than running the test against the old code.

Nothing is committed or pushed, and no PR is open. You're still on `main` and the files are untracked, so you'll want to create a branch before opening the PR. Here's the description:

---

**Fix percentage divisor in `apply_discount`**

## Summary
`apply_discount` divided by `10` instead of `100` when working out the discount, so any non-zero percentage took off ten times too much. For example, `apply_discount(1000, 10)` returned `0` instead of `900`. This PR changes the divisor to `100`.

## Changes
- `pricing.py`: `total_cents * percent // 10` → `total_cents * percent // 100`
- `tests/test_pricing.py`: adds the regression test `test_ten_percent_discount`, which checks that `apply_discount(1000, 10) == 900`

## Why the bug wasn't caught
The existing tests only covered a 0% discount and negative percentages, and neither of those is affected by the divisor. The new test covers a non-zero discount.

## Testing
```
python3 -m unittest discover -s tests -t .
Ran 3 tests ... OK
```

The behaviour is otherwise unchanged: results still round down to whole cents, discounts are still capped at 100%, and negative percentages still raise `ValueError`.

🤖 Generated with [Claude Code](https://claude.com/claude-code)
```
