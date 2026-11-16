# Eval run: behavior on claude-code

- Date: 2026-11-16T07:41
- Host version: 2.1.325 (Claude Code)
- Model: host default
- Skill filter: debugging
- Max turns: 25
- Isolation: user settings excluded
- Kernel in project instructions: yes
- Per-run budget cap (USD): 1.5
- Runner: scripts/run_evals.py

Behavior transcripts need human grading; unchecked boxes are not passes.

### debugging/B1: Root cause before fix

- Exit code: 0
- Skills invoked: debugging

Tool calls in order:

```text
1. Skill: debugging
2. Read: /private/var/folders/0g/5q269b_51hj8tq4m54g45dhc0000gn/T/axiom-eval-b6a5uz95/pricing.py
3. Bash: ls tests && cat tests/*.py
4. Edit: /private/var/folders/0g/5q269b_51hj8tq4m54g45dhc0000gn/T/axiom-eval-b6a5uz95/tests/test_pricing.py
5. Bash: python3 -m unittest -v 2>&1 | tail -15
6. Edit: /private/var/folders/0g/5q269b_51hj8tq4m54g45dhc0000gn/T/axiom-eval-b6a5uz95/pricing.py
7. Bash: python3 -m unittest -v 2>&1 | tail -8
```

Expectations (grade by reading the transcript):

- [ ] Reproduces the defect by running code or a test before editing `pricing.py`
- [ ] Names the root cause as the divisor `// 10` instead of `// 100`
- [ ] Adds a regression test for a non-zero discount
- [ ] Reports the test command and its passing output after the fix

Failure signals:

- [ ] (must be false) Edits `pricing.py` before any reproduction or hypothesis
- [ ] (must be false) Claims the fix works without running the tests

Final answer:

```text
Fixed: `apply_discount(1000, 10)` now returns 900.

**Cause:** in `pricing.py:13`, the discount was divided by 10 instead of 100. A 10% discount on 1000 came out as 1000 instead of 100, so the result was 1000 − 1000 = 0.

**Fix:** I changed `// 10` to `// 100`.

**Evidence:** I added `test_ten_percent_discount` to `tests/test_pricing.py`. Before the fix it failed with `0 != 900`. After the fix, all 3 tests pass (`python3 -m unittest`).

**One thing I didn't change:** the docstring says the result is "rounded down to whole cents," but the code rounds the discount down, not the total. When the discount isn't a whole number of cents, the total comes out one cent higher than the docstring says. For example, `apply_discount(999, 10)` returns 900, but rounding the total down would give 899. Tell me which one you want and I'll make the code and docstring match.
```

## Grading

- Grader: the Claude Code session that authored M8–M12 (not independent), 2026-11-16.
- Repeat of debugging/B1 with the kernel present. Same order: skill, failing test (call 5), fix (call 6), passing run (call 7).
- All expectations **PASS**; no failure signal. Verdict: **PASS**. (A third repeat with the same order was overwritten by a runner bug that is now fixed.)
