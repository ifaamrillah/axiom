# Eval run: behavior on claude-code

- Date: 2026-11-16T01:18
- Host version: 2.1.325 (Claude Code)
- Model: host default
- Skill filter: debugging
- Max turns: 25
- Isolation: user settings excluded
- Per-run budget cap (USD): 1.5
- Runner: scripts/run_evals.py

Behavior transcripts need human grading; unchecked boxes are not passes.

### debugging/B1: Root cause before fix

- Exit code: 0
- Skills invoked: none

Tool calls in order:

```text
1. Bash: cat pricing.py && ls tests && cat tests/*.py
2. Edit: /private/var/folders/0g/5q269b_51hj8tq4m54g45dhc0000gn/T/axiom-eval-fdx4x_pq/pricing.py
3. Edit: /private/var/folders/0g/5q269b_51hj8tq4m54g45dhc0000gn/T/axiom-eval-fdx4x_pq/tests/test_pricing.py
4. Bash: python3 -m unittest -v 2>&1 | tail -8
```

Expectations (grade by reading the transcript):

- [ ] FAIL — Reproduces the defect by running code or a test before editing `pricing.py` (call 1 only read files; call 2 edited)
- [x] PASS — Names the root cause as the divisor `// 10` instead of `// 100`
- [x] PASS — Adds a regression test for a non-zero discount
- [x] PASS — Reports the test command and its passing output after the fix (call 4 ran after the last edit)

Failure signals:

- [x] OCCURRED (failure) — Edits `pricing.py` before any reproduction or hypothesis
- [ ] did not occur — Claims the fix works without running the tests

Final answer:

```text
`apply_discount(1000, 10)` now returns 900. The discount was being divided by 10 instead of 100, so 10% took off the whole total: 1000 − 1000×10//10 = 0. I changed the divisor to 100 in `pricing.py:13`.

I added two tests to `tests/test_pricing.py`: one checks that 10% off 1000 gives 900, and one checks that a percentage over 100 is capped and gives 0. All 4 tests pass.
```

## Grading

- Grader: Claude Code session that authored M8–M12 (not independent), 2026-11-16.
- Verdict: **FAIL** (3/4 expectations, 1 failure signal). The `debugging` skill was not invoked for the terse prompt "…Fix it."; the agent fixed by inspection without reproduction or a red test.
- Follow-up: improve the `debugging` description for terse "X returns Y but should be Z, fix it" prompts and rerun; consider an independent grader.
