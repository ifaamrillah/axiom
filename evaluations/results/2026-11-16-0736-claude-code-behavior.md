# Eval run: behavior on claude-code

- Date: 2026-11-16T07:36
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
2. Read: /private/var/folders/0g/5q269b_51hj8tq4m54g45dhc0000gn/T/axiom-eval-geh6nwff/pricing.py
3. Bash: ls tests && cat tests/*.py
4. Edit: /private/var/folders/0g/5q269b_51hj8tq4m54g45dhc0000gn/T/axiom-eval-geh6nwff/tests/test_pricing.py
5. Bash: python3 -m unittest -v 2>&1 | tail -15
6. Edit: /private/var/folders/0g/5q269b_51hj8tq4m54g45dhc0000gn/T/axiom-eval-geh6nwff/pricing.py
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
`apply_discount(1000, 10)` now returns 900.

**Cause:** in `pricing.py:13`, the discount was divided by 10 instead of 100. That made a 10% discount take off the whole amount: `1000 * 10 // 10 = 1000`, and `1000 - 1000 = 0`. Any percentage above 10 gave a negative total, so a 100% discount returned -9000.

**Fix:** I changed `// 10` to `// 100`. The existing rounding down to whole cents is unchanged.

**Test:** I added `test_ten_percent_discount` to `tests/test_pricing.py`. It failed before the fix (`AssertionError: 0 != 900`). After the fix, all 3 tests in `python3 -m unittest` pass.

Nothing is committed yet.
```

## Grading

- Grader: the Claude Code session that authored M8–M12 (not independent), 2026-11-16.
- Kernel rule 5 (reproduce before fixing) plus the debugging description; kernel present in CLAUDE.md.
- Reproduces before editing `pricing.py`: **PASS** (call 5 runs the new failing test; call 6 is the first edit to `pricing.py`).
- Root cause `// 10` named: **PASS**. Regression test: **PASS** (call 4). Tests run after fix: **PASS** (call 7, output cited).
- Failure signals: none occurred.
- Verdict: **PASS**.
