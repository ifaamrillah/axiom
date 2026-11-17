# Eval run: trigger on claude-code

- Date: 2026-11-17T15:12
- Host version: 2.1.326 (Claude Code)
- Model: host default
- Skill filter: architecture-design,performance-optimization,skill-factory,spec-analysis,task-planning,tdd,technical-research,testing,ui-ux-design,verification-before-completion,writing-quality
- Max turns: 4
- Repeats per behavior case: 1; grader: none
- Isolation: user settings excluded
- Kernel in project instructions: yes
- Per-run budget cap (USD): 0.5
- Runner: scripts/run_evals.py

| Skill | Expect | Prompt | Owner | Invoked | Verdict |
|---|---|---|---|---|---|
| architecture-design | + | Should we put a Redis cache in front of apply_discount, or is that ove | architecture-design | architecture-design | pass |
| architecture-design | + | Design how discounts, coupons, and loyalty points should fit together  | architecture-design | architecture-design | pass |
| architecture-design | + | Pick an approach for storing discount rules: config file, database tab | architecture-design | architecture-design | pass |
| architecture-design | − | apply_discount returns 0 for 10%, fix it | debugging | debugging | pass |
| architecture-design | − | Review my PR | code-review | code-review | pass |
| performance-optimization | + | The monthly revenue report is slow for big tenants. Speed it up. | performance-optimization | performance-optimization | pass |
| performance-optimization | + | monthly_revenue takes forever once a tenant has thousands of invoices | performance-optimization | debugging | fail |
| performance-optimization | + | Should we add a cache in front of the reports module? It feels slow. | performance-optimization | performance-optimization | pass |
| performance-optimization | − | monthly_revenue returns the wrong total for March, fix it | debugging | debugging | pass |
| performance-optimization | − | Add a GitHub Actions workflow that runs the tests | ci-and-observability | ci-and-observability | pass |
| performance-optimization | − | Review this PR before I merge | code-review | code-review | pass |
| skill-factory | + | Create a skill that makes agents write changelog entries | skill-factory | skill-factory | pass |
| skill-factory | + | Turn our deploy checklist into an agent skill | skill-factory | skill-factory | pass |
| skill-factory | − | Is the tdd skill ready to ship? | skill-evaluator | skill-evaluator | pass |
| skill-factory | − | Write the changelog for 2.3.0 | release-management | — | pass |
| spec-analysis | + | Check whether spec.md, plan.md, and tasks.md are consistent | spec-analysis | spec-analysis | pass |
| spec-analysis | + | What's left to implement compared to the spec? | spec-analysis | spec-analysis | pass |
| spec-analysis | + | Analyze the spec and tasks for gaps before we start coding | spec-analysis | spec-analysis | pass |
| spec-analysis | − | Write the spec for a referral program | requirements-analysis | requirements-analysis | pass |
| spec-analysis | − | Fix the failing unit test | debugging | debugging | pass |
| task-planning | + | Break the coupon spec into an implementation plan with tasks | task-planning | task-planning | pass |
| task-planning | + | Plan the work to fix the discount bug and add edge-case tests | task-planning | axiom-orchestrator, task-planning | pass |
| task-planning | − | Just fix the bug | debugging | debugging | pass |
| task-planning | − | Is our spec consistent with the tasks? | spec-analysis | spec-analysis | pass |
| tdd | + | Use TDD to add a percent cap to apply_discount | tdd | tdd | pass |
| tdd | + | apply_discount(1000, 10) returns 0. Write a failing test for this bug  | tdd | tdd, debugging | pass |
| tdd | + | Make apply_discount reject negative totals, test-first please | tdd | tdd | pass |
| tdd | − | Why is the build slow? | ci-and-observability | performance-optimization | pass |
| tdd | − | Review this diff for security issues | code-review | security-audit | pass |
| technical-research | + | What does Python's round() do with 2.5, and should apply_discount use  | technical-research | — | fail |
| technical-research | + | Check the current docs: is datetime.utcnow deprecated, and what replac | technical-research | technical-research | pass |
| technical-research | − | Where is the discount cap applied? | codebase-exploration | codebase-exploration | pass |
| technical-research | − | Fix the discount bug | debugging | debugging | pass |
| testing | + | Add tests for apply_discount edge cases | testing | testing | pass |
| testing | + | What test coverage do we need for the pricing module? | testing | testing | pass |
| testing | − | Write an end-to-end browser test for checkout | e2e-testing | e2e-testing | pass |
| testing | − | Use TDD to add a coupon | tdd | tdd | pass |
| ui-ux-design | + | Design the settings page for notification preferences | ui-ux-design | ui-ux-design | pass |
| ui-ux-design | + | This form is hard to use on mobile, improve it | ui-ux-design | ui-ux-design | pass |
| ui-ux-design | + | Check the new dashboard for accessibility problems | ui-ux-design | ui-ux-design | pass |
| ui-ux-design | − | Optimize this SQL query | none | — | pass |
| ui-ux-design | − | Add an index to the orders table | none | — | pass |
| verification-before-completion | + | Ok looks done, go ahead and commit it | verification-before-completion | verification-before-completion | pass |
| verification-before-completion | + | Are we good to open the PR now? | verification-before-completion | verification-before-completion | pass |
| verification-before-completion | + | The subagent says all tests pass, mark the task complete | verification-before-completion | verification-before-completion | pass |
| verification-before-completion | − | Explain what this function does | none | — | pass |
| verification-before-completion | − | Plan the migration to Postgres 17 | task-planning | axiom-orchestrator | pass |
| writing-quality | + | Humanize this paragraph, it sounds like ChatGPT wrote it | writing-quality | — | fail |
| writing-quality | + | Tighten this PR description, it's too fluffy | writing-quality | — | fail |
| writing-quality | + | Make this README intro less salesy and more direct | writing-quality | writing-quality | pass |
| writing-quality | − | Write a spec for coupon codes | requirements-analysis | requirements-analysis | pass |
| writing-quality | − | Fix the typo 'recieve' in README.md | none | — | pass |
| writing-quality | − | Review my PR before I merge it | code-review | code-review | pass |

Summary: 49/53 pass.
