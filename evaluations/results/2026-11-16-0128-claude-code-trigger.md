# Eval run: trigger on claude-code

- Date: 2026-11-16T01:28
- Host version: 2.1.325 (Claude Code)
- Model: host default
- Skill filter: code-review
- Max turns: 4
- Isolation: user settings excluded
- Per-run budget cap (USD): 0.5
- Runner: scripts/run_evals.py

| Skill | Expect | Prompt | Owner | Invoked | Verdict |
|---|---|---|---|---|---|
| code-review | + | Review this pull request before I merge it | code-review | code-review | pass |
| code-review | + | Can you do a quality pass on the changes another agent just made? | code-review | code-review | pass |
| code-review | + | Check this plan before we start implementing | code-review | code-review | pass |
| code-review | − | Deploy this to production now | release-management | — | pass |
| code-review | − | Write a failing test for this bug before fixing it | tdd | — | pass |

Summary: 5/5 pass.
