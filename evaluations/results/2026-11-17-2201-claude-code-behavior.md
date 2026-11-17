# Eval run: behavior on claude-code

- Date: 2026-11-17T22:01
- Host version: 2.1.326 (Claude Code)
- Model: host default
- Skill filter: debugging
- Max turns: 25
- Repeats per behavior case: 1; grader: separate claude-code session, model host default
- Isolation: user settings excluded
- Arms: skill,none (skill: Axiom skills installed; none: no skills, no kernel; oneliner: no skills, one generic line)
- Kernel in project instructions (skill arm): yes
- Per-run budget cap (USD): 1.5
- Runner: scripts/run_evals.py

- Raw host output: evaluations/results/raw/2026-11-17-2201-claude-code-behavior/

Graded by a separate headless session with no tools and no repository context.

| Case | Tags | skill pass | none pass | Δ none vs skill | Skill invoked | Median tokens (in/out) | Seeded recall / false | Verdict |
|---|---|---|---|---|---|---|---|---|
| debugging/B2 | — | 1/1 | ungraded (1 invalid) | — | skill 1/1, none 0/0 | skill 166743/1987 | skill 1/1 / 0 | skill PASS, none ungraded |

- Tuning cases, graded runs passing: skill 1/1, none ungraded

Invalid runs (excluded from every rate above):

- debugging/B2 [none] run 1: exit 0; permission denied (1): Bash; raw: evaluations/results/raw/2026-11-17-2201-claude-code-behavior/debugging-B2-none-run1.jsonl

### debugging/B2 [skill]: Find the seeded defect without inventing others

- Arm: skill
- Exit code: 0
- Skills invoked: debugging
- Tokens (in/out): 166743/1987
- Verdict: **PASS** (independent grader: The agent ran apply_discount and showed wrong totals such as 1000 at 10% returning 0, reported the divide-by-10 defect at pricing.py:13 without editing any files, and its second finding (the total rounds up, against the docstring's 'rounded down') is a real mismatch backed by the 999/15% run, so it is not a false finding.)

Tool calls in order:

```text
1. Skill: debugging
   → Launching skill: debugging
2. Read: /private/var/folders/0g/5q269b_51hj8tq4m54g45dhc0000gn/T/axiom-eval-56abmx5t/pricing.py
   → 1 """Tiny pricing module used as an Axiom evaluation fixture. Contains one seeded defect.""" 2 3 4 def apply_discount(total_cents: int, percent: int) -> int: 5 """Return the total after a percentage discount, rounded down to whole cents. 6 
3. Glob: tests/**
   → tests/__init__.py tests/test_pricing.py
4. Read: /private/var/folders/0g/5q269b_51hj8tq4m54g45dhc0000gn/T/axiom-eval-56abmx5t/tests/test_pricing.py
   → 1 import unittest 2 3 from pricing import apply_discount 4 5 6 class ApplyDiscountTest(unittest.TestCase): 7 def test_zero_percent_keeps_total(self): 8 self.assertEqual(apply_discount(1000, 0), 1000) 9 10 def test_negative_percent_rejected(
5. Bash: python3 -m unittest 2>&1 | tail -5; python3 -c "
from pricing import apply_discount as a
for t,p in [(1000,10),(1000,50)
   → .. ---------------------------------------------------------------------- Ran 2 tests in 0.000s OK 1000 10 0 1000 50 -4000 1000 100 -9000 1000 150 -9000 999 15 -499 1 50 -4
6. Bash: python3 -c "
t,p=999,15; print('with //100:', t - t*p//100, ' exact:', t*(100-p)/100, ' floor of total:', t*(100-p)//100
   → with //100: 850 exact: 849.15 floor of total: 849
```

Expectations:

- [x] Runs code or a test that shows a wrong total before reporting defects
- [x] Reports each defect with a `pricing.py` line reference

Failure signals:

- [x] (must be false) Edits or creates any file

Seeded defects:

- [x] (seeded) `apply_discount` divides by `10` instead of `100`, so a 10% discount removes the whole total
- False findings: 0

Final answer:

```text
I found one definite defect and one probable one, both on line 13 of `pricing.py`. I haven't changed any files.

## Defect 1 (definite): divides by 10 instead of 100, at `pricing.py:13`

```python
return total_cents - total_cents * percent // 10
```

The percentage is divided by 10, so every discount comes out ten times too large. Any discount above 10% makes the total negative. I ran `apply_discount` on a few inputs:

| Call | Got | Expected |
|---|---|---|
| `apply_discount(1000, 10)` | `0` | `900` |
| `apply_discount(1000, 50)` | `-4000` | `500` |
| `apply_discount(1000, 100)` | `-9000` | `0` |
| `apply_discount(1000, 150)` (capped to 100) | `-9000` | `0` |

This is almost certainly the "wrong totals" customers are reporting. The fix is to change `// 10` to `// 100`.

## Defect 2 (probable): rounding goes the wrong way, also at `pricing.py:13`

The docstring says the function returns "the total after a percentage discount, rounded down to whole cents." The code rounds the *discount* down and subtracts it, which rounds the *total* up. This still happens after fixing the divisor:

- `999` cents at 15%: the exact result is `849.15`.
- With `// 100`, the code returns `850`.
- Rounding the total down, as the docstring says, gives `849`.

This one depends on what you intend. If the docstring is right, the line should be `total_cents * (100 - percent) // 100`. If you mean to round the discount down (customers pay the extra fraction of a cent), the code is right and the docstring needs changing. Tell me which you want.

## Why the tests didn't catch it

`python3 -m unittest` passes (`Ran 2 tests ... OK`) because `tests/test_pricing.py` only checks a 0% discount and that negative percentages are rejected. No test applies a real discount or exercises the 100% cap, so both issues go unnoticed.

## Not counted as defects

- **Validation at lines 9–12:** rejecting negative percentages and capping at 100 both match the docstring.
- **Negative `total_cents`:** it isn't validated, but nothing says it should be. Only add a check if negative totals are actually invalid in your system.
- **The docstring at line 1:** it says the file "contains one seeded defect." I didn't rely on that; the rounding issue above is a separate question.

When you want the fix, I'd start by adding failing tests for 10%, 50%, 100%, over 100%, and the `999`/15% rounding case. Then I'd fix line 13 according to your answer on rounding.
```

### debugging/B2 [none]: Find the seeded defect without inventing others

- Arm: none
- Exit code: 0
- Skills invoked: none
- Tokens (in/out): 105213/1500
- Raw stream: evaluations/results/raw/2026-11-17-2201-claude-code-behavior/debugging-B2-none-run1.jsonl
- Verdict: INVALID (excluded from rates): permission denied (1): Bash

Tool calls in order:

```text
1. Bash: cat -n pricing.py && cat README.md && ls tests && cat tests/*
   → 1 """Tiny pricing module used as an Axiom evaluation fixture. Contains one seeded defect.""" 2 3 4 def apply_discount(total_cents: int, percent: int) -> int: 5 """Return the total after a percentage discount, rounded down to whole cents. 6 
2. Bash: python3 -I -c "
import sys; sys.path.insert(0,'.')
from pricing import apply_discount as a
for t,p in [(1000,10),(1000,5
   → This Bash command contains multiple operations. The following part requires approval: python3 -I -c " import sys; sys.path.insert(0,'.') from pricing import apply_discount as a for t,p in [(1000,10),(1000,50),(1000,150),(999,10)]: print(t,p
```

Expectations:

- [ ] Runs code or a test that shows a wrong total before reporting defects
- [ ] Reports each defect with a `pricing.py` line reference

Failure signals:

- [ ] (must be false) Edits or creates any file

Seeded defects:

- [ ] (seeded) `apply_discount` divides by `10` instead of `100`, so a 10% discount removes the whole total

Final answer:

```text
I found one real defect, on line 13 of `pricing.py`, plus one smaller rounding question. I tried to run the function on sample inputs and run the tests, but that command wasn't approved. The numbers below are worked out by reading the code, not from running it. I haven't changed any files.

### Defect: line 13 divides by 10 instead of 100
```python
return total_cents - total_cents * percent // 10
```
The code treats the percentage as tenths, so every discount comes out 10 times too large:
- `apply_discount(1000, 10)` returns `1000 - 1000` = **0**. It should return **900**. This matches the bug report in the README.
- `apply_discount(1000, 50)` returns `1000 - 5000` = **-4000**. It should return 500.
- Any percent over 100 is capped to 100 on line 12, so `apply_discount(1000, 150)` returns `1000 - 10000` = **-9000**. It should return 0. The cap is correct; it just feeds into the wrong formula.

Any discount above 10% therefore produces a negative total. The fix is to use `// 100`.

### Possible second issue: rounding direction (line 13, after the fix)
The docstring says the result is "rounded down to whole cents". Even with `// 100`, the code rounds the *discount* down, which rounds the *total* up:
- `apply_discount(999, 10)` with `// 100` gives `999 - 99` = **900**.
- The exact result is 899.1, so rounding the total down would give **899**.

If the docstring means the final total, the expression should be `(total_cents * (100 - percent)) // 100`. If it means the discount amount, the current form is fine. That's a business decision, so check which one customers expect.

### Not defects
- Lines 9–10 (rejecting negative percents) and lines 11–12 (capping at 100) work as documented.
- Negative or non-integer `total_cents` isn't validated, but the docstring doesn't promise that it would be.

### Why the tests didn't catch it
`tests/test_pricing.py` only covers a 0% discount and a negative percent, and line 13 gives the right answer at 0% whatever the divisor is. The README notes the same gap. Adding tests for a normal discount (`(1000, 10)` → 900), the cap (`(1000, 150)` → 0) and a rounding case (`(999, 10)`) would cover it.
```
