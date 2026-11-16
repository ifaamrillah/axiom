# Eval run: behavior on claude-code

- Date: 2026-11-16T07:40
- Host version: 2.1.325 (Claude Code)
- Model: host default
- Skill filter: debugging
- Max turns: 25
- Isolation: user settings excluded
- Kernel in project instructions: no
- Per-run budget cap (USD): 1.5
- Runner: scripts/run_evals.py

Behavior transcripts need human grading; unchecked boxes are not passes.

### debugging/B1: Root cause before fix

- Exit code: 0
- Skills invoked: none

Tool calls in order:

```text
1. Read: /private/var/folders/0g/5q269b_51hj8tq4m54g45dhc0000gn/T/axiom-eval-crdz6uat/pricing.py
2. Bash: ls tests && cat tests/* README.md
3. Edit: /private/var/folders/0g/5q269b_51hj8tq4m54g45dhc0000gn/T/axiom-eval-crdz6uat/tests/test_pricing.py
4. Bash: python3 -m unittest discover -s tests -t . 2>&1 | tail -15
5. Edit: /private/var/folders/0g/5q269b_51hj8tq4m54g45dhc0000gn/T/axiom-eval-crdz6uat/tests/test_pricing.py
6. Edit: /private/var/folders/0g/5q269b_51hj8tq4m54g45dhc0000gn/T/axiom-eval-crdz6uat/pricing.py
7. Bash: python3 -m unittest discover -s tests -t . -v 2>&1 | tail -10
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
`apply_discount(1000, 10)` now returns 900. All 4 tests pass.

**The bug:** `pricing.py:13` divided by `10` instead of `100`. So a 10% discount took off the whole total, and a percentage over 100 (capped to 100) gave `-9000`.

**The fix:** `total_cents * percent // 100`.

**New tests** in `tests/test_pricing.py`:
- `apply_discount(1000, 10) == 900`
- `apply_discount(1000, 150) == 0`, which checks the 100% cap

Both failed before the fix and pass now.

**Decision for you:** the docstring and the code round differently when the discount isn't a whole number of cents. The docstring says the final total is rounded down, so `apply_discount(999, 15)` would be 849. The code rounds the discount down instead, which gives 850 and favours the customer. I left the code as it is and didn't add a test for this case, because a test would lock in one answer. Tell me which one you want and I'll make the docstring and the code agree.
```

## Grading

- Grader: the Claude Code session that authored M8–M12 (not independent), 2026-11-16.
- Control run with `--no-kernel`: no kernel block, skills only. The skill was **not** invoked, but the order still passed: failing test run (call 4) before the `pricing.py` edit (call 6).
- Verdict: **PASS** on the observable expectations. Interpretation: the earlier failures and this pass are within run-to-run variance. Do not attribute the improvement to the kernel alone; skill invocation, however, happened only with the kernel present (3/3 vs 0/1 here and 0/2 before).
