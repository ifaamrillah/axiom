# Eval run: trigger on claude-code

- Date: 2026-11-16T01:21
- Host version: 2.1.325 (Claude Code)
- Model: host default
- Skill filter: security-audit
- Max turns: 4
- Isolation: user settings excluded
- Per-run budget cap (USD): 0.5
- Runner: scripts/run_evals.py

| Skill | Expect | Prompt | Owner | Invoked | Verdict |
|---|---|---|---|---|---|
| security-audit | + | Is this endpoint vulnerable to IDOR? | security-audit | security-audit | pass |
| security-audit | + | Do a full security audit of this repository | security-audit | security-audit | pass |
| security-audit | + | Pen-test the auth module and give me a report | security-audit | security-audit | pass |
| security-audit | − | Make the login page look nicer | ui-ux-design | — | pass |
| security-audit | − | Speed up the slow orders query | none | — | pass |

Summary: 5/5 pass.
