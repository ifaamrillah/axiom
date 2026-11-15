# Eval run: trigger on claude-code

- Date: 2026-11-16T01:27
- Host version: 2.1.325 (Claude Code)
- Model: host default
- Skill filter: tdd
- Max turns: 4
- Isolation: user settings excluded
- Per-run budget cap (USD): 0.5
- Runner: scripts/run_evals.py

| Skill | Expect | Prompt | Owner | Invoked | Verdict |
|---|---|---|---|---|---|
| tdd | + | Use TDD to add a percent cap to apply_discount | tdd | tdd | pass |
| tdd | + | Write a failing test for this bug first, then fix it | tdd | — | fail |
| tdd | + | Add validation for negative quantities, test-first please | tdd | tdd | pass |
| tdd | − | Why is the build slow? | none | — | pass |
| tdd | − | Review this diff for security issues | code-review | — | pass |

Summary: 4/5 pass.
