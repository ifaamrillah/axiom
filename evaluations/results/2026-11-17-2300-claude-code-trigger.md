# Eval run: trigger on claude-code

- Date: 2026-11-17T23:00
- Host version: 2.1.326 (Claude Code)
- Model: host default
- Skill filter: product-discovery,architecture-design,verification-before-completion
- Max turns: 4
- Repeats per behavior case: 1; grader: none
- Isolation: user settings excluded
- Arms: skill (skill: Axiom skills installed; none: no skills, no kernel; oneliner: no skills, one generic line)
- Kernel in project instructions (skill arm): yes
- Per-run budget cap (USD): 0.5
- Runner: scripts/run_evals.py

| Skill | Expect | Prompt | Owner | Invoked | Verdict |
|---|---|---|---|---|---|
| architecture-design | + | Should we put a Redis cache in front of apply_discount, or is that ove | architecture-design | architecture-design | pass |
| architecture-design | + | Design how discounts, coupons, and loyalty points should fit together  | architecture-design | architecture-design | pass |
| architecture-design | + | Pick an approach for storing discount rules: config file, database tab | architecture-design | architecture-design | pass |
| architecture-design | − | apply_discount returns 0 for 10%, fix it | debugging | debugging | pass |
| architecture-design | − | Review my PR | code-review | code-review | pass |
| product-discovery | + | I have a vague idea for a loyalty feature, help me figure out what to  | product-discovery | product-discovery | pass |
| product-discovery | + | Interview me about this feature before we design anything | product-discovery | product-discovery | pass |
| product-discovery | + | Not sure exactly what we need for notifications, can you help scope it | product-discovery | product-discovery | pass |
| product-discovery | + | Before we build a referral program, is it even worth doing? Push back  | product-discovery | product-discovery | pass |
| product-discovery | − | Rename getUser to fetchUser everywhere | none | — | pass |
| product-discovery | − | Fix the null pointer in OrderService | debugging | debugging | pass |
| verification-before-completion | + | Ok looks done, go ahead and commit it | verification-before-completion | verification-before-completion | pass |
| verification-before-completion | + | Are we good to open the PR now? | verification-before-completion | verification-before-completion | pass |
| verification-before-completion | + | The subagent says all tests pass, mark the task complete | verification-before-completion | verification-before-completion | pass |
| verification-before-completion | − | Explain what this function does | none | — | pass |
| verification-before-completion | − | Plan the migration to Postgres 17 | task-planning | axiom-orchestrator | pass |

Summary: 16/16 pass.
