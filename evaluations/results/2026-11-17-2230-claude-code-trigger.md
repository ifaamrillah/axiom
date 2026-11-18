# Eval run: trigger on claude-code

- Date: 2026-11-17T22:30
- Host version: 2.1.326 (Claude Code)
- Model: host default
- Skill filter: axiom-orchestrator,debugging,tdd,implementation,verification-before-completion
- Max turns: 4
- Repeats per behavior case: 1; grader: none
- Isolation: user settings excluded
- Arms: skill (skill: Axiom skills installed; none: no skills, no kernel; oneliner: no skills, one generic line)
- Kernel in project instructions (skill arm): yes
- Per-run budget cap (USD): 0.5
- Runner: scripts/run_evals.py

| Skill | Expect | Prompt | Owner | Invoked | Verdict |
|---|---|---|---|---|---|
| axiom-orchestrator | + | Add multi-currency support to the checkout flow | axiom-orchestrator | axiom-orchestrator | pass |
| axiom-orchestrator | + | We need to onboard onto this repo and then add an export feature | axiom-orchestrator | axiom-orchestrator | pass |
| axiom-orchestrator | + | Coordinate the work to migrate our auth to OAuth with tests and docs | axiom-orchestrator | axiom-orchestrator | pass |
| axiom-orchestrator | − | Fix the typo 'recieve' in README.md | none | — | pass |
| axiom-orchestrator | − | What does git rebase --onto do? | none | technical-research | pass |
| debugging | + | The checkout tests started failing after yesterday's merge. Can you fi | debugging | debugging | pass |
| debugging | + | apply_discount returns 0 for a 10% discount, it should be 900 | debugging | debugging | pass |
| debugging | + | This test passes alone but fails when I run the whole suite | debugging | debugging | pass |
| debugging | + | CI is red on the pricing tests since the last merge, fix pls | debugging | debugging | pass |
| debugging | + | Use the debugging skill on apply_discount: a 10% discount wipes out th | debugging | debugging | pass |
| debugging | + | Skip the formalities and just fix apply_discount, it returns 0 for 10% | debugging | debugging | pass |
| debugging | − | Add a dark mode toggle to the settings page | ui-ux-design | axiom-orchestrator | pass |
| debugging | − | Review my PR before I merge it | code-review | code-review | pass |
| debugging | − | Write release notes for 2.3.0 | release-management | release-management | pass |
| debugging | − | Write a failing test first, then make apply_discount reject totals ove | tdd | tdd | pass |
| debugging | − | Add more edge-case tests for apply_discount | testing | testing | pass |
| implementation | + | Implement task T3 from the plan: add apply_coupon to pricing.py | implementation | implementation | pass |
| implementation | + | Build the coupon function we specced, following the project's conventi | implementation | implementation | pass |
| implementation | − | Plan the coupon work into tasks | task-planning | task-planning | pass |
| implementation | − | Review the coupon diff | code-review | code-review | pass |
| tdd | + | Use TDD to add a percent cap to apply_discount | tdd | tdd | pass |
| tdd | + | apply_discount(1000, 10) returns 0. Write a failing test for this bug  | tdd | tdd | pass |
| tdd | + | Make apply_discount reject negative totals, test-first please | tdd | tdd | pass |
| tdd | + | Run this through the tdd skill: apply_discount should accept a maximum | tdd | tdd | pass |
| tdd | + | Red, green, refactor: add rounding to the nearest cent in apply_discou | tdd | tdd | pass |
| tdd | − | Why is the build slow? | ci-and-observability | performance-optimization | pass |
| tdd | − | Review this diff for security issues | code-review | security-audit | pass |
| tdd | − | apply_discount returns 0 for a 10% discount, find out why | debugging | debugging | pass |
| tdd | − | Which apply_discount edge cases do our tests miss? | testing | testing | pass |
| verification-before-completion | + | Ok looks done, go ahead and commit it | verification-before-completion | verification-before-completion | pass |
| verification-before-completion | + | Are we good to open the PR now? | verification-before-completion | verification-before-completion | pass |
| verification-before-completion | + | The subagent says all tests pass, mark the task complete | verification-before-completion | verification-before-completion | pass |
| verification-before-completion | − | Explain what this function does | none | — | pass |
| verification-before-completion | − | Plan the migration to Postgres 17 | task-planning | axiom-orchestrator | pass |

Summary: 34/34 pass.
