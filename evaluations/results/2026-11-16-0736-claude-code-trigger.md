# Eval run: trigger on claude-code

- Date: 2026-11-16T07:36
- Host version: 2.1.325 (Claude Code)
- Model: host default
- Skill filter: debugging
- Max turns: 4
- Isolation: user settings excluded
- Kernel in project instructions: yes
- Per-run budget cap (USD): 0.5
- Runner: scripts/run_evals.py

| Skill | Expect | Prompt | Owner | Invoked | Verdict |
|---|---|---|---|---|---|
| debugging | + | The checkout tests started failing after yesterday's merge. Can you fi | debugging | debugging | pass |
| debugging | + | apply_discount returns 0 for a 10% discount, it should be 900 | debugging | debugging | pass |
| debugging | + | This test passes alone but fails when I run the whole suite | debugging | debugging | pass |
| debugging | + | build is broken on CI with 'undefined is not a function', fix pls | debugging | — | fail |
| debugging | − | Add a dark mode toggle to the settings page | ui-ux-design | — | pass |
| debugging | − | Review my PR before I merge it | code-review | code-review | pass |
| debugging | − | Write release notes for 2.3.0 | release-management | — | pass |

Summary: 6/7 pass.
