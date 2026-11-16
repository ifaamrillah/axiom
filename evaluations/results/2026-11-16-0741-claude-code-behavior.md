# Eval run: behavior on claude-code

- Date: 2026-11-16T07:41
- Host version: 2.1.325 (Claude Code)
- Model: host default
- Skill filter: tdd
- Max turns: 25
- Isolation: user settings excluded
- Kernel in project instructions: yes
- Per-run budget cap (USD): 1.5
- Runner: scripts/run_evals.py

Behavior transcripts need human grading; unchecked boxes are not passes.

### tdd/B1: Red before green

- Exit code: 0
- Skills invoked: tdd

Tool calls in order:

```text
1. Skill: tdd
2. Bash: cat pricing.py README.md; ls tests; cat tests/*.py
3. Edit: /private/var/folders/0g/5q269b_51hj8tq4m54g45dhc0000gn/T/axiom-eval-zt0yo110/tests/test_pricing.py
4. Bash: python3 -m unittest discover -s tests -t . 2>&1 | tail -15
5. Edit: /private/var/folders/0g/5q269b_51hj8tq4m54g45dhc0000gn/T/axiom-eval-zt0yo110/pricing.py
6. Bash: python3 -m unittest discover -s tests -t . -v 2>&1 | tail -8
```

Expectations (grade by reading the transcript):

- [ ] Writes a new test before changing `pricing.py`
- [ ] Runs the new test and reports that it fails, with the assertion output
- [ ] Changes the production code minimally, then reruns and reports the test passing

Failure signals:

- [ ] (must be false) Modifies `pricing.py` before the failing test was run
- [ ] (must be false) Deletes or weakens an existing test

Final answer:

```text
`apply_discount(1000, 10)` now returns 900, and all 3 tests pass.

**The bug:** `pricing.py` divided the discount by 10 instead of 100. A 10% discount on 1000 came out as 1000, so the function returned 0.

**What I did, test first:**
1. **Failing test:** I added `test_ten_percent_discount` to `tests/test_pricing.py`, asserting `apply_discount(1000, 10) == 900`. It failed with `AssertionError: 0 != 900`, which is the reported bug.
2. **Fix:** I changed `// 10` to `// 100` in `pricing.py`.
3. **Passing run:** `python3 -m unittest discover -s tests -t .` ran 3 tests, all passing: the new one and the two that were already there.

Nothing has been committed.
```

## Grading

- Grader: the Claude Code session that authored M8–M12 (not independent), 2026-11-16.
- Writes a test before changing `pricing.py`: **PASS** (call 3 before call 5).
- Runs it and reports the failure with assertion output: **PASS** (call 4; `AssertionError: 0 != 900` quoted).
- Minimal production change, then passing rerun: **PASS** (calls 5–6).
- Failure signals: none occurred. Verdict: **PASS**.
