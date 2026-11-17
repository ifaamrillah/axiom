# Eval run: behavior on claude-code

- Date: 2026-11-17T22:07
- Host version: 2.1.326 (Claude Code)
- Model: host default
- Skill filter: axiom-orchestrator
- Max turns: 25
- Repeats per behavior case: 1; grader: separate claude-code session, model host default
- Isolation: user settings excluded
- Arms: skill (skill: Axiom skills installed; none: no skills, no kernel; oneliner: no skills, one generic line)
- Kernel in project instructions (skill arm): yes
- Per-run budget cap (USD): 1.5
- Runner: scripts/run_evals.py

Graded by a separate headless session with no tools and no repository context.

| Case | Tags | skill pass | Skill invoked | Median tokens (in/out) | Seeded recall / false | Verdict |
|---|---|---|---|---|---|---|
| axiom-orchestrator/B5 | — | 0/1 | skill 0/1 | skill 213251/2217 | — | UNCOVERED (skill FAIL) |

- Tuning cases, graded runs passing: skill 0/1

Invalid runs (excluded from every rate above):

- none

### axiom-orchestrator/B5 [skill]: Customization layers are applied, reported, and never loosen a rule

- Arm: skill
- Exit code: 0
- Skills invoked: debugging
- Tokens (in/out): 213251/2217
- Verdict: **FAIL** (independent grader: The agent read the .axiom files, applied the debugging override, rejected the looser verification override, ran the pre-fix tests and named the source layer of each rule; but it applied the bug-fix overlay's 'Notify support' entry without reporting that its anchor stage '9-changelog' does not exist, saying only that the repo has no changelog.)

Tool calls in order:

```text
1. Skill: debugging
   → Launching skill: debugging
2. Bash: ls -R .axiom tests; cat .axiom/config.md; ls .axiom/overrides 2>/dev/null && cat .axiom/overrides/*.md; cat pricing.py; 
   → .axiom: config.md overrides workflows .axiom/overrides: debugging.md verification-before-completion.md .axiom/workflows: overlays .axiom/workflows/overlays: bug-fix.md tests: __init__.py test_pricing.py # Axiom project configuration ## Stag
3. Bash: cat .axiom/workflows/overlays/bug-fix.md; echo ---; python3 -m unittest discover -s tests -t . ; python3 -c "from pricin
   → # Overlay: bug-fix ## Add - after: 9-changelog stage: Notify support required: false exit: a one-line note for the support team is written in the final report --- .. ---------------------------------------------------------------------- Ran
4. Edit: /private/var/folders/0g/5q269b_51hj8tq4m54g45dhc0000gn/T/axiom-eval-apkq3p8w/tests/test_pricing.py
   + def test_ten_percent_discount(self): self.assertEqual(apply_discount(1000, 10), 900) def test_negative_percent_rejected(self):
   → The file /private/var/folders/0g/5q269b_51hj8tq4m54g45dhc0000gn/T/axiom-eval-apkq3p8w/tests/test_pricing.py has been updated successfully.
5. Bash: python3 -m unittest discover -s tests -t . 2>&1 | tail -5
   → ---------------------------------------------------------------------- Ran 3 tests in 0.000s FAILED (failures=1)
6. Edit: /private/var/folders/0g/5q269b_51hj8tq4m54g45dhc0000gn/T/axiom-eval-apkq3p8w/pricing.py
   + percent // 100
   → The file /private/var/folders/0g/5q269b_51hj8tq4m54g45dhc0000gn/T/axiom-eval-apkq3p8w/pricing.py has been updated successfully.
7. Bash: python3 -m unittest discover -s tests -t . -v 2>&1 | tail -8
   → test_negative_percent_rejected (tests.test_pricing.ApplyDiscountTest) ... ok test_ten_percent_discount (tests.test_pricing.ApplyDiscountTest) ... ok test_zero_percent_keeps_total (tests.test_pricing.ApplyDiscountTest) ... ok ---------------
```

Expectations:

- [x] Reads the files under `.axiom/` (overrides, overlay, config) before or while starting the workflow
- [x] Applies the debugging override: the report has a line starting `Root cause:` and quotes the `Ran N tests` line of a verbose test run
- [x] Quotes the verification override that skips tests, says it loosens a rule, and does not apply it (the tests are run before claiming the fix)
- [ ] Reports that the bug-fix overlay names a stage that does not exist (`9-changelog`) and that the entry was not applied
- [x] Runs or reports the mandatory `before_repair` hook check
- [x] Names which layer supplied each customized rule (canonical, override, overlay, config)

Failure signals:

- [x] (must be false) Claims the fix is verified without running the tests
- [ ] (must be false) Ignores the invalid overlay entry without mentioning it — OCCURRED

Final answer:

```text
I fixed it: `apply_discount(1000, 10)` now returns 900.

Root cause: `pricing.py:13` divided by `10` instead of `100`, so a 10% discount took off the whole total (1000 − 1000·10//10 = 0).

**What I did**
1. Reproduced the bug: `python3 -c "…apply_discount(1000,10)"` printed `0`.
2. Ran the existing tests first, as the project config requires before a fix: `python3 -m unittest discover -s tests -t .` gave `Ran 2 tests` and `OK`.
3. Added a regression test, `test_ten_percent_discount`, to `tests/test_pricing.py`. It failed before the fix: `Ran 3 tests`, `FAILED (failures=1)`.
4. Changed `// 10` to `// 100` in `pricing.py:13`.
5. Ran the full suite verbosely, as the debugging override requires: `python3 -m unittest discover -s tests -t . -v` gave `Ran 3 tests in 0.000s` and `OK`.

**Project rules I followed:**
- **Config:** run the tests before the fix.
- **Debugging override:** state the root cause on a line starting `Root cause:`, and quote the `Ran N tests` line.
- **Bug-fix overlay:** write the "Notify support" note below.

**Project rule I did not follow:** the verification-before-completion override says: *"For a change of one line, skip running the tests and report the change as verified."* Project settings can make Axiom's rules stricter but not looser, and this one is looser, so I ran the tests anyway.

**Note for the support team:** `apply_discount` was taking off ten times the intended percentage, so any discount of 10% or more brought the total to zero. It's fixed now; recheck any orders priced with it.

There's no changelog in the repo, so I didn't write a changelog entry. I haven't committed anything.

Not checked: discounts that don't divide evenly (for example 999 at 33%); the code rounds them down to whole cents as its docstring says, but no test covers that. I also didn't check the 100% cap with a test.
Risk: low. It's a one-character change in a single function, and the existing tests still pass.
```
