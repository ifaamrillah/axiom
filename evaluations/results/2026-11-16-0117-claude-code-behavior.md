# Eval run: behavior on claude-code

- Date: 2026-11-16T01:17
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
I fixed it: `apply_discount(1000, 10)` now returns 900.

**Cause:** the formula in `pricing.py:13` divided by 10 instead of 100, so a 10% discount took off 100% of the total.

```python
return total_cents - total_cents * percent // 100
```

I also added two tests to `tests/test_pricing.py`: one checks that 10% off 1000 gives 900, and one checks that discounts above 100% are capped and give 0. All 4 tests pass.
```

## Grading

- Not gradeable for sequencing: this run predates tool-call tracing in the runner. Final answer names the root cause and adds tests. Superseded by `2026-11-16-0118-claude-code-behavior.md`.
