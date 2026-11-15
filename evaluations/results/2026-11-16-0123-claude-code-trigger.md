# Eval run: trigger on claude-code

- Date: 2026-11-16T01:23
- Host version: 2.1.325 (Claude Code)
- Model: host default
- Skill filter: spec-analysis
- Max turns: 4
- Isolation: user settings excluded
- Per-run budget cap (USD): 0.5
- Runner: scripts/run_evals.py

| Skill | Expect | Prompt | Owner | Invoked | Verdict |
|---|---|---|---|---|---|
| spec-analysis | + | Check whether spec.md, plan.md, and tasks.md are consistent | spec-analysis | spec-analysis | pass |
| spec-analysis | + | What's left to implement compared to the spec? | spec-analysis | — | fail |
| spec-analysis | + | Analyze the spec and tasks for gaps before we start coding | spec-analysis | spec-analysis | pass |
| spec-analysis | − | Write the spec for a referral program | requirements-analysis | requirements-analysis | pass |
| spec-analysis | − | Fix the failing unit test | debugging | debugging | pass |

Summary: 4/5 pass.
