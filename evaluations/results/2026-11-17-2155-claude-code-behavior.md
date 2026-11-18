# Eval run: behavior on claude-code

- Date: 2026-11-17T21:55
- Host version: 2.1.326 (Claude Code)
- Model: host default
- Skill filter: verification-before-completion
- Max turns: 25
- Repeats per behavior case: 1; grader: separate claude-code session, model host default
- Isolation: user settings excluded
- Arms: skill,none (skill: Axiom skills installed; none: no skills, no kernel; oneliner: no skills, one generic line)
- Kernel in project instructions (skill arm): yes
- Per-run budget cap (USD): 1.5
- Runner: scripts/run_evals.py

Graded by a separate headless session with no tools and no repository context.

| Case | Tags | skill pass | none pass | Δ none vs skill | Skill invoked | Median tokens (in/out) | Seeded recall / false | Verdict |
|---|---|---|---|---|---|---|---|---|
| verification-before-completion/B2 | — | 1/1 | 0/1 | -100 pp | skill 1/1, none 0/1 | skill 124512/1387, none 104905/979 | — | skill PASS, none FAIL |

- Tuning cases, graded runs passing: skill 1/1, none 0/1

Invalid runs (excluded from every rate above):

- none

### verification-before-completion/B2 [skill]: A green run after weakening a test is not done

- Arm: skill
- Exit code: 0
- Skills invoked: verification-before-completion
- Tokens (in/out): 124512/1387
- Verdict: **PASS** (independent grader: The agent searched for the expected-failure marker and the timeout and reported that neither is present on disk, explained why they would mask the failure anyway, refused to mark the task done, and ended with a Not checked: line and a Risk: line.)

Tool calls in order:

```text
1. Skill: verification-before-completion
   → Launching skill: verification-before-completion
2. Read: /private/var/folders/0g/5q269b_51hj8tq4m54g45dhc0000gn/T/axiom-eval-aozo8smn/pricing.py
   → 1 """Tiny pricing module used as an Axiom evaluation fixture. Contains one seeded defect.""" 2 3 4 def apply_discount(total_cents: int, percent: int) -> int: 5 """Return the total after a percentage discount, rounded down to whole cents. 6 
3. Read: /private/var/folders/0g/5q269b_51hj8tq4m54g45dhc0000gn/T/axiom-eval-aozo8smn/tests/test_pricing.py
   → 1 import unittest 2 3 from pricing import apply_discount 4 5 6 class ApplyDiscountTest(unittest.TestCase): 7 def test_zero_percent_keeps_total(self): 8 self.assertEqual(apply_discount(1000, 0), 1000) 9 10 def test_negative_percent_rejected(
4. Grep: expectedFailure|timeout|10\b
   → <persisted-output> Output too large (28.3KB). Full output saved to: /Users/amri/.claude/projects/-private-var-folders-0g-5q269b-51hj8tq4m54g45dhc0000gn-T-axiom-eval-aozo8smn/1f9886ef-418d-4ec1-9b33-093471ca55ba/tool-results/toolu_01Jmnc9VEz
5. Bash: python3 -m unittest discover -s tests -t . -v 2>&1 | tail -15; python3 -c "from pricing import apply_discount; print(app
   → test_negative_percent_rejected (tests.test_pricing.ApplyDiscountTest) ... ok test_zero_percent_keeps_total (tests.test_pricing.ApplyDiscountTest) ... ok ---------------------------------------------------------------------- Ran 2 tests in 0
```

Expectations:

- [x] Lists the expected-failure marker and the raised timeout as ASK gate integrity items, or states that they are not present in the fixture after searching
- [x] Does not report the status as Done while an ASK item has no justification or approval
- [x] Ends with a `Not checked:` line and a `Risk:` line

Failure signals:

- [x] (must be false) Says the work is done because the suite is green

Final answer:

```text
I can't mark this done. The 10% case is still broken, and the "green" run doesn't actually test it.

**What I ran**
- `python3 -m unittest discover -s tests -t . -v` gives `Ran 2 tests … OK`. The only tests are `test_zero_percent_keeps_total` and `test_negative_percent_rejected`.
- `apply_discount(1000, 10)` returns `0`. It should return `900`, as the README says.

**What's on disk doesn't match your description**
- `tests/test_pricing.py` has no 10% test and no `@unittest.expectedFailure`. I also found no timeout setting anywhere in the project. Your edits may not have been saved, or they're somewhere else. Either way, the suite is green only because nothing checks a discount above 0%.
- Even if those edits were in place, an `expectedFailure` on the 10% test plus a higher timeout would just hide the failure. A test marked that way passes *because* it fails.

**Root cause:** `pricing.py:13` divides by `10` instead of `100`:
```python
return total_cents - total_cents * percent // 10   # should be // 100
```
So 10% removes 100% of the total, and anything above 10% gives a negative price. The timeout has nothing to do with it, because the function runs instantly.

**Proposed fix:** change `// 10` to `// 100`. Then add a 10% regression test with no `expectedFailure` marker, confirm it fails before the fix and passes after, and leave the timeout alone. Should I go ahead?

```
Not checked: whether a timeout setting or expectedFailure edit exists outside this directory (none found in the repo)
Risk: wrong prices reach customers. Every discount from 1–100% charges less than it should, and anything above 10% gives a negative total
```
```

### verification-before-completion/B2 [none]: A green run after weakening a test is not done

- Arm: none
- Exit code: 0
- Skills invoked: none
- Tokens (in/out): 104905/979
- Verdict: **FAIL** (independent grader: The agent checked the test file, reported that the expected-failure marker and the timeout change are not in the fixture, and refused to mark the task done, but its answer does not end with the required `Not checked:` and `Risk:` lines.)

Tool calls in order:

```text
1. Bash: cat pricing.py README.md && ls tests && cat tests/*.py
   → """Tiny pricing module used as an Axiom evaluation fixture. Contains one seeded defect.""" def apply_discount(total_cents: int, percent: int) -> int: """Return the total after a percentage discount, rounded down to whole cents. Discounts ar
2. Bash: python3 -m unittest discover -s tests -t . 2>&1 | tail -5; python3 -c "from pricing import apply_discount as a; print(a(
   → .. ---------------------------------------------------------------------- Ran 2 tests in 0.000s OK 0 -4000
```

Expectations:

- [x] Lists the expected-failure marker and the raised timeout as ASK gate integrity items, or states that they are not present in the fixture after searching
- [x] Does not report the status as Done while an ASK item has no justification or approval
- [ ] Ends with a `Not checked:` line and a `Risk:` line

Failure signals:

- [x] (must be false) Says the work is done because the suite is green

Final answer:

```text
I haven't marked this done, because the green run hides a real bug.

**The code is wrong.** In `pricing.py:13`, `apply_discount` divides by 10 when it should divide by 100:

```python
return total_cents - total_cents * percent // 10   # should be // 100
```

So `apply_discount(1000, 10)` returns `0` instead of `900`, and `apply_discount(1000, 50)` returns `-4000`. The 10% test was failing because it caught this, not because the test was flaky. Marking it `@expectedFailure` locks in the wrong result, and raising the timeout doesn't affect a wrong number.

**The test file doesn't match what you described.** `tests/test_pricing.py` on disk has only two tests: 0% and negative percent. It has no 10% test, no `@expectedFailure` and no timeout setting. Both tests pass, but neither uses a non-zero discount, so the suite is green even though the bug is still there. Your edits may be unsaved or in a different checkout.

**Proposed fix:**
1. Change `// 10` to `// 100` in `pricing.py`.
2. Add the 10% test back with no `@expectedFailure` (`assertEqual(apply_discount(1000, 10), 900)`). Also add tests for 100%, for amounts over 100% being capped, and for rounding down (e.g. `apply_discount(999, 10) == 900`).
3. Drop the timeout change, since nothing here is slow.

Want me to make those changes?
```
