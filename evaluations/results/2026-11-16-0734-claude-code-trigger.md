# Eval run: trigger on claude-code

- Date: 2026-11-16T07:34
- Host version: 2.1.325 (Claude Code)
- Model: host default
- Skill filter: tdd
- Max turns: 4
- Isolation: user settings excluded
- Kernel in project instructions: yes
- Per-run budget cap (USD): 0.5
- Runner: scripts/run_evals.py

| Skill | Expect | Prompt | Owner | Invoked | Verdict |
|---|---|---|---|---|---|
| tdd | + | Use TDD to add a percent cap to apply_discount | tdd | tdd | pass |
| tdd | + | apply_discount(1000, 10) returns 0. Write a failing test for this bug  | tdd | tdd | pass |
| tdd | + | Make apply_discount reject negative totals, test-first please | tdd | tdd | pass |
| tdd | − | Why is the build slow? | none | — | pass |
| tdd | − | Review this diff for security issues | code-review | security-audit | pass |

Summary: 5/5 pass.
