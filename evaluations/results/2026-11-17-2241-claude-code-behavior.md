# Eval run: behavior on claude-code

- Date: 2026-11-17T22:41
- Host version: 2.1.326 (Claude Code)
- Model: host default
- Skill filter: debugging
- Max turns: 25
- Repeats per behavior case: 3; grader: separate claude-code session, model host default
- Isolation: user settings excluded
- Arms: skill,none (skill: Axiom skills installed; none: no skills, no kernel; oneliner: no skills, one generic line)
- Kernel in project instructions (skill arm): yes
- Per-run budget cap (USD): 1.5
- Runner: scripts/run_evals.py

Graded by a separate headless session with no tools and no repository context.

| Case | Tags | skill pass | none pass | Δ none vs skill | Skill invoked | Median tokens (in/out) | Seeded recall / false | Verdict |
|---|---|---|---|---|---|---|---|---|
| debugging/B2 | — | 3/3 | 1/3 | -67 pp | skill 3/3, none 0/3 | skill 167607/2015, none 68782/1042 | skill 3/3 / 0, none 3/3 / 0 | skill PASS, none FAIL |

- Tuning cases, graded runs passing: skill 3/3, none 1/3

Invalid runs (excluded from every rate above):

- none

### debugging/B2 [skill] (run 1/3): Find the seeded defect without inventing others

- Arm: skill
- Exit code: 0
- Skills invoked: debugging
- Tokens (in/out): 124341/1812
- Verdict: **PASS** (independent grader: The agent called apply_discount directly and showed wrong totals (1000, 10 -> 0), identified the // 10 divisor bug at pricing.py:13 without editing any files, and flagged a rounding mismatch with the docstring that the evidence does not show to be a non-issue.)

Tool calls in order:

```text
1. Skill: debugging
   → Launching skill: debugging
2. Read: /private/var/folders/0g/5q269b_51hj8tq4m54g45dhc0000gn/T/axiom-eval-377jgzit/pricing.py
   → 1 """Tiny pricing module used as an Axiom evaluation fixture. Contains one seeded defect.""" 2 3 4 def apply_discount(total_cents: int, percent: int) -> int: 5 """Return the total after a percentage discount, rounded down to whole cents. 6 
3. Bash: ls -a . tests .axiom 2>/dev/null; cat tests/*.py README.md
   → .: . .. .agents .claude .git AGENTS.md CLAUDE.md README.md pricing.py tests tests: . .. __init__.py test_pricing.py import unittest from pricing import apply_discount class ApplyDiscountTest(unittest.TestCase): def test_zero_percent_keeps_t
4. Bash: python3 -m unittest discover -s tests -t . 2>&1 | tail -3; python3 -I -c "
import sys; sys.path.insert(0,'.')
from prici
   → Ran 2 tests in 0.000s OK 1000 10 -> 0 1000 5 -> 500 1000 50 -> -4000 1000 100 -> -9000 1000 150 -> -9000 999 10 -> 0
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
I found one confirmed defect, on line 13. There's also a likely rounding mismatch on the same line that you'll need to rule on. I haven't changed any files.

## Defect 1 (confirmed): `pricing.py:13` divides by 10 instead of 100

```python
return total_cents - total_cents * percent // 10
```

**Cause:** `percent` is a whole-number percentage (0–100), so the discount should be `total_cents * percent // 100`. Dividing by 10 makes every discount 10 times too large. Anything above 10% gives a negative total.

**Reproduction** (I called the function directly):

| Call | Expected | Actual |
|---|---|---|
| `apply_discount(1000, 5)` | 950 | 500 |
| `apply_discount(1000, 10)` | 900 | 0 |
| `apply_discount(1000, 50)` | 500 | -4000 |
| `apply_discount(1000, 100)` | 0 | -9000 |
| `apply_discount(1000, 150)` (capped at 100) | 0 | -9000 |

The existing tests miss this. `python3 -m unittest discover -s tests -t .` prints `OK` because the two tests only cover 0% and a negative percent, which never reach the wrong divisor.

## Defect 2 (likely, needs your call): line 13 rounds the total up, not down

The docstring (lines 5 and 13) says the result is "rounded down to whole cents". The code rounds the *discount* down and then subtracts it, which rounds the *total* up. Once the divisor is fixed, `apply_discount(999, 10)` would give 999 − 99 = **900**. The exact value is 899.1, so "rounded down" means **899**. Either the code or the docstring is wrong, and only you know which rule the business wants. Rounding the discount down favors the merchant by up to 1 cent; rounding the total down favors the customer.

## What I checked and found correct
- Lines 9–10: negative percents raise `ValueError`, and an existing test covers it.
- Lines 11–12: percents above 100 are capped at 100, as documented. The results only looked wrong because of line 13.

## Not defects, but worth knowing
- `total_cents` isn't validated, so a negative total passes straight through. The contract doesn't forbid it.
- There's no test for any non-zero discount, which is how Defect 1 got through.

**Suggested fix (not applied):** write a failing regression test first, e.g. `apply_discount(1000, 10) == 900` plus one for the cap, then change `// 10` to `// 100`. Add a rounding test once you've decided Defect 2.

Not checked: how callers use `apply_discount`. This repo has only the module and its tests, so I couldn't check whether any caller compensates for the wrong values.
Risk: low for Defect 1. Defect 2 depends on which rounding rule the business intends.
```

### debugging/B2 [skill] (run 2/3): Find the seeded defect without inventing others

- Arm: skill
- Exit code: 0
- Skills invoked: debugging
- Tokens (in/out): 167607/2015
- Verdict: **PASS** (independent grader: The agent ran apply_discount and showed wrong totals such as 1000 at 10% returning 0, reported the divide-by-10 defect at pricing.py:13, and edited no files; its hedged rounding note is a real mismatch with the docstring, not one the evidence shows to be false.)

Tool calls in order:

```text
1. Skill: debugging
   → Launching skill: debugging
2. Read: /private/var/folders/0g/5q269b_51hj8tq4m54g45dhc0000gn/T/axiom-eval-uz01ambq/pricing.py
   → 1 """Tiny pricing module used as an Axiom evaluation fixture. Contains one seeded defect.""" 2 3 4 def apply_discount(total_cents: int, percent: int) -> int: 5 """Return the total after a percentage discount, rounded down to whole cents. 6 
3. Glob: {.axiom/**,tests/**}
   → tests/__init__.py tests/test_pricing.py
4. Read: /private/var/folders/0g/5q269b_51hj8tq4m54g45dhc0000gn/T/axiom-eval-uz01ambq/tests/test_pricing.py
   → 1 import unittest 2 3 from pricing import apply_discount 4 5 6 class ApplyDiscountTest(unittest.TestCase): 7 def test_zero_percent_keeps_total(self): 8 self.assertEqual(apply_discount(1000, 0), 1000) 9 10 def test_negative_percent_rejected(
5. Bash: python3 -m unittest -v 2>&1 | tail -15; python3 -c "
from pricing import apply_discount as a
for t,p in [(1000,10),(1000
   → test_negative_percent_rejected (tests.test_pricing.ApplyDiscountTest) ... ok test_zero_percent_keeps_total (tests.test_pricing.ApplyDiscountTest) ... ok ---------------------------------------------------------------------- Ran 2 tests in 0
6. Bash: python3 -c "
for t,p in [(999,10),(1,50)]: print(t,p,'fixed-divisor:',t-t*p//100,'floor-of-result:',t*(100-p)//100)"
   → 999 10 fixed-divisor: 900 floor-of-result: 899 1 50 fixed-divisor: 1 floor-of-result: 0
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
I found one definite defect in `pricing.py`, plus one possible rounding defect that depends on what "rounded down" in the docstring means. I didn't change any files.

## Defect 1 (confirmed): wrong divisor — `pricing.py:13`

```python
return total_cents - total_cents * percent // 10
```

A percentage has to be divided by **100**, not 10. As written, every discount is 10 times too large, so most totals come out wrong and many come out negative.

Running `apply_discount` directly showed:

| Call | Expected | Actual |
|---|---|---|
| `apply_discount(1000, 10)` | 900 | **0** |
| `apply_discount(1000, 50)` | 500 | **-4000** |
| `apply_discount(1000, 100)` | 0 | **-9000** |
| `apply_discount(1000, 150)` (capped at 100) | 0 | **-9000** |
| `apply_discount(1000, 0)` | 1000 | 1000 |

The negative-percent check (lines 9–10) and the cap at 100 (lines 11–12) work correctly. The bad value comes only from line 13.

## Defect 2 (possible): rounding direction — `pricing.py:13` against the docstring on `pricing.py:5`

The docstring says the result is "the total after a percentage discount, rounded down to whole cents." Even with the divisor fixed (`total_cents - total_cents * percent // 100`), the code rounds the *discount* down, which rounds the *total* up:

- `999` at 10%: the exact answer is 899.1, so rounded down is 899. The code returns 900.
- `1` at 50%: the exact answer is 0.5, so rounded down is 0. The code returns 1.

That matches the docstring only if "rounded down" means the discount, not the total. If the total should round down, the expression should be `total_cents * (100 - percent) // 100`. This is a business decision, and the difference is one cent at most.

## Why the tests didn't catch it

`python3 -m unittest -v` reports `Ran 2 tests ... OK`. The only two tests use `percent=0` and a negative percent, and the divisor bug can't show up on either. No test uses a percentage between 1 and 100, or one over 100.

## Other notes
- The file header (`pricing.py:1`) describes this as an evaluation fixture with "one seeded defect." That fits Defect 1 being the intended one.
- There's no `.axiom/` directory, so no project customizations applied.

**Next step:** with your go-ahead, I'll write failing regression tests (for example `apply_discount(1000, 10) == 900`, plus the over-100 cap). Then I'll change `// 10` to `// 100`, and change the rounding as well if you decide the total should round down.

Not checked: inputs that aren't integers (floats, `bool`, `None`). The function has type hints but doesn't check types, and the spec doesn't say what should happen with them.
Risk: I can't confirm Defect 2 until you decide how rounding should work. Fixing it would change some totals by one cent.
```

### debugging/B2 [skill] (run 3/3): Find the seeded defect without inventing others

- Arm: skill
- Exit code: 0
- Skills invoked: debugging
- Tokens (in/out): 167645/2020
- Verdict: **PASS** (independent grader: The agent ran apply_discount and got wrong totals such as 0 and -4000. It reported the divide-by-10 defect at pricing.py:13 and changed no files. Its extra rounding finding is real, since its own computation shows the result contradicts the docstring's round-down spec.)

Tool calls in order:

```text
1. Skill: debugging
   → Launching skill: debugging
2. Read: /private/var/folders/0g/5q269b_51hj8tq4m54g45dhc0000gn/T/axiom-eval-5pw6a3dt/pricing.py
   → 1 """Tiny pricing module used as an Axiom evaluation fixture. Contains one seeded defect.""" 2 3 4 def apply_discount(total_cents: int, percent: int) -> int: 5 """Return the total after a percentage discount, rounded down to whole cents. 6 
3. Glob: {tests/**,.axiom/**}
   → tests/__init__.py tests/test_pricing.py
4. Read: /private/var/folders/0g/5q269b_51hj8tq4m54g45dhc0000gn/T/axiom-eval-5pw6a3dt/tests/test_pricing.py
   → 1 import unittest 2 3 from pricing import apply_discount 4 5 6 class ApplyDiscountTest(unittest.TestCase): 7 def test_zero_percent_keeps_total(self): 8 self.assertEqual(apply_discount(1000, 0), 1000) 9 10 def test_negative_percent_rejected(
5. Bash: python3 -m unittest 2>&1 | tail -15; python3 -c "
from pricing import apply_discount as a
for t,p in [(1000,10),(1000,50
   → .. ---------------------------------------------------------------------- Ran 2 tests in 0.000s OK 1000 10 0 1000 50 -4000 1000 100 -9000 1000 150 -9000 999 33 -2297 1 50 -4
6. Bash: python3 -c "
t,p=999,33
print('fixed /100, current form:', t - t*p//100)
print('rounded-down total      :', t*(100-p)//1
   → fixed /100, current form: 670 rounded-down total : 669 exact: 669.33
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
I found two defects in `apply_discount`, both on line 13. I haven't changed any files.

## Defect 1: the divisor is 10 instead of 100 (`pricing.py:13`)

```python
return total_cents - total_cents * percent // 10
```

A percentage has to be divided by 100. Dividing by 10 makes every discount ten times too large, so most totals come out at zero or negative. This is why customers are seeing wrong totals. Calling the function directly showed:

| total_cents, percent | returned | expected |
|---|---|---|
| 1000, 10 | `0` | 900 |
| 1000, 50 | `-4000` | 500 |
| 1000, 100 (and 150, which is capped to 100) | `-9000` | 0 |
| 1, 50 | `-4` | 0 |

## Defect 2: rounding goes the wrong way (`pricing.py:13`)

The docstring (line 5) says the total after the discount is rounded down to whole cents. The code rounds the discount down and then subtracts it, which rounds the total up. This stays wrong even after defect 1 is fixed. For 999 cents at 33%, the exact total is 669.33:
- the current formula with `/100` gives **670**
- rounding the total down gives **669**

The fix that matches the docstring is `total_cents * (100 - percent) // 100`. It's a 1-cent difference, but it decides which way every fractional result rounds.

## Not defects, but worth knowing
- **Missing tests:** `tests/test_pricing.py` only checks 0% and negative percentages, and neither hits the wrong divisor. That's why `python3 -m unittest` passes (`Ran 2 tests … OK`) even with the bug.
- **Unchecked input:** a negative `total_cents` is never rejected. The docstring doesn't say whether it should be, so I'm treating it as an open question rather than a bug.
- Line 1 of the file says it holds "one seeded defect". I didn't rely on that; the second defect above is real.

**Evidence:** I called `apply_discount` with the inputs in the table and got the values shown. A separate check printed `670` from the current formula with `/100` and `669` from the rounded-down form.

**Suggested next step:** add failing regression tests for 10%, 100%, over 100%, and 999 cents at 33%. Then change line 13 to `total_cents * (100 - percent) // 100`.

Not checked: callers of `apply_discount` outside this file (there are none in the repo), and whether stored order totals were already affected.
Risk: rounding the total up instead of down may be what the business actually wants and the docstring may be the thing that's wrong. Confirm which one is meant before fixing defect 2.
```

### debugging/B2 [none] (run 1/3): Find the seeded defect without inventing others

- Arm: none
- Exit code: 0
- Skills invoked: none
- Tokens (in/out): 68782/1021
- Verdict: **FAIL** (independent grader: The agent correctly found the seeded // 10 defect on line 13 and changed no files, but it only read files with cat and never ran code or tests to show a wrong total; its rounding-versus-docstring note holds up and is not a false finding.)

Tool calls in order:

```text
1. Bash: cat -n pricing.py; ls tests; cat README.md; cat tests/*.py
   → 1 """Tiny pricing module used as an Axiom evaluation fixture. Contains one seeded defect.""" 2 3 4 def apply_discount(total_cents: int, percent: int) -> int: 5 """Return the total after a percentage discount, rounded down to whole cents. 6 
```

Expectations:

- [ ] Runs code or a test that shows a wrong total before reporting defects
- [x] Reports each defect with a `pricing.py` line reference

Failure signals:

- [x] (must be false) Edits or creates any file

Seeded defects:

- [x] (seeded) `apply_discount` divides by `10` instead of `100`, so a 10% discount removes the whole total
- False findings: 0

Final answer:

```text
I found one real defect, on line 13, plus a smaller rounding mismatch with the docstring on the same line. I haven't changed any files.

## Defect: line 13 divides by 10 instead of 100

```python
return total_cents - total_cents * percent // 10
```

To turn a percentage into a fraction you divide by 100, but this line divides by 10. That makes every discount 10 times too big:

| Call | Expected | Actual |
|---|---|---|
| `apply_discount(1000, 10)` | 900 | **0** |
| `apply_discount(1000, 5)` | 950 | 500 |
| `apply_discount(1000, 50)` | 500 | **−4000** |
| `apply_discount(1000, 100)` | 0 | **−9000** |

Any discount of 11% or more gives a negative total, so the 100% cap on lines 11–12 doesn't protect anything either. This is the bug customers are seeing, and it matches the README (`apply_discount(1000, 10)` returns `0`). The fix would be `// 100`.

## Smaller issue: rounding goes the opposite way to the docstring (line 13)

The docstring (line 5) promises the total "rounded down to whole cents". Even with `// 100`, the code rounds the *discount* down, which rounds the *total* up. For example, `apply_discount(999, 10)` would return 900, while the exact answer is 899.1, which rounds down to 899. This is at most one cent and is in the customer's favour-against direction (they pay slightly more), so it's minor. Either the docstring or the code should change, depending on which behaviour you want.

## Why the tests didn't catch it

`tests/test_pricing.py` only checks 0% and a negative percent. Neither one ever reaches the division, so both tests pass with the bug in place.

The file's own header says it "contains one seeded defect," and that's the `// 10` on line 13. The rest of the function (rejecting negative percents, capping at 100) is correct. Do you want me to fix line 13 and add tests for non-zero discounts and the 100% cap?
```

### debugging/B2 [none] (run 2/3): Find the seeded defect without inventing others

- Arm: none
- Exit code: 0
- Skills invoked: none
- Tokens (in/out): 68782/1042
- Verdict: **FAIL** (independent grader: The agent found the divide-by-10 defect at line 13 and gave line references without editing files, but it explicitly said it did not run any code or tests to show a wrong total, and its rounding-direction finding is a genuine mismatch with the docstring.)

Tool calls in order:

```text
1. Bash: cat -n pricing.py; cat README.md; ls tests; cat tests/*
   → 1 """Tiny pricing module used as an Axiom evaluation fixture. Contains one seeded defect.""" 2 3 4 def apply_discount(total_cents: int, percent: int) -> int: 5 """Return the total after a percentage discount, rounded down to whole cents. 6 
```

Expectations:

- [ ] Runs code or a test that shows a wrong total before reporting defects
- [x] Reports each defect with a `pricing.py` line reference

Failure signals:

- [x] (must be false) Edits or creates any file

Seeded defects:

- [x] (seeded) `apply_discount` divides by `10` instead of `100`, so a 10% discount removes the whole total
- False findings: 0

Final answer:

```text
I found one definite defect in `pricing.py` and one smaller rounding mismatch. I didn't change any files, and I worked these out by reading the code, not by running it.

### 1. Wrong divisor in the discount formula (line 13): this is the bug customers are seeing

```python
return total_cents - total_cents * percent // 10
```

A percentage has to be divided by **100**, but this divides by 10, so every discount comes out 10× too large:

| Call | Expected | Actual |
|---|---|---|
| `apply_discount(1000, 10)` | 900 | 1000 − 1000 = **0** |
| `apply_discount(1000, 5)` | 950 | 1000 − 500 = **500** |
| `apply_discount(1000, 50)` | 500 | 1000 − 5000 = **−4000** |

Any discount above 10% gives a negative total, and the 100% cap still allows 1000 − 10000 = −9000.

### 2. Rounding goes the wrong way (line 13, secondary)

The docstring (line 5) says the total should be "rounded down to whole cents." The formula rounds the *discount* down, which rounds the *total* up. Once the divisor is fixed:

- `apply_discount(999, 10)` gives 999 − 99 = **900**, but the exact amount is 899.1, which should round down to **899**.

It's at most one cent per call. Either the code or the docstring needs to change. `total_cents - total_cents * percent // 100` keeps the current behaviour, while `total_cents * (100 - percent) // 100` matches the docstring.

### Tests

The tests in `tests/test_pricing.py` only cover 0% and a negative percentage, and both work even with the bug. Nothing tests a non-zero discount, so the fix should come with tests for amounts like 10%, 50%, 100%, above 100%, and a case where rounding matters (999 at 10%).

The validation at lines 9–12 looks correct.
```

### debugging/B2 [none] (run 3/3): Find the seeded defect without inventing others

- Arm: none
- Exit code: 0
- Skills invoked: none
- Tokens (in/out): 105150/1324
- Verdict: **PASS** (independent grader: The agent ran the function and showed wrong totals such as 1000 at 10% returning 0. It identified the seeded divide-by-10 defect at pricing.py:13 and changed no files. Its rounding-direction note is a plausible docstring mismatch rather than a demonstrated non-issue, and it explicitly said the negative-input point was not a bug.)

Tool calls in order:

```text
1. Bash: cat -n pricing.py && cat README.md && ls tests && cat -n tests/*
   → 1 """Tiny pricing module used as an Axiom evaluation fixture. Contains one seeded defect.""" 2 3 4 def apply_discount(total_cents: int, percent: int) -> int: 5 """Return the total after a percentage discount, rounded down to whole cents. 6 
2. Bash: python3 -c "
from pricing import apply_discount as a
for t,p in [(1000,10),(1000,5),(1000,50),(1000,100),(999,10),(1000,
   → 1000 10 0 1000 5 500 1000 50 -4000 1000 100 -9000 999 10 0 1000 150 -9000 Ran 2 tests in 0.000s OK
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
I found one real defect, on line 13 of `pricing.py`, plus one place where the rounding doesn't match what the docstring says. I haven't changed any files.

### Defect: wrong divisor at `pricing.py:13`
```python
return total_cents - total_cents * percent // 10
```
The percentage is divided by `10` when it should be divided by `100`, so every discount is 10 times too large. I ran the function to confirm:

| Call | Expected | Actual |
|---|---|---|
| `apply_discount(1000, 5)` | 950 | 500 |
| `apply_discount(1000, 10)` | 900 | **0** (the case in `README.md`) |
| `apply_discount(1000, 50)` | 500 | **-4000** |
| `apply_discount(1000, 100)` | 0 | **-9000** |
| `apply_discount(1000, 150)` (capped to 100) | 0 | **-9000** |

Any discount over 10% gives a negative total. This is the cause of the customer reports.

The fix is to change `// 10` to `// 100`.

### Rounding direction differs from the docstring (lines 5 and 13)
The docstring says the result is "rounded down to whole cents". The code rounds the *discount* down, which rounds the *final total* up. With the divisor fixed, `apply_discount(999, 10)` would return `900`. The exact answer is 899.1, so rounding the total down gives `899`. It's off by at most one cent, but either the code or the docstring needs to change. Which one is right is a business decision (do customers or the shop get the extra cent?), so please confirm before I touch it.

### Gaps that let this slip through
- **Tests:** both tests pass, but they only check a 0% discount and a negative one. Nothing tests a real discount or the 100% cap, which is why this bug went unnoticed. `README.md` says the same.
- **Input checks:** nothing stops a negative `total_cents`. That's not a bug against the current docstring, but you may want it rejected.

When you want me to make changes, I'll start with a failing test for `apply_discount(1000, 10) == 900` and the 100% cap, then fix line 13.
```
