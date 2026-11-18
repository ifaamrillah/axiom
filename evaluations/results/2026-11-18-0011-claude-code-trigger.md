# Eval run: trigger on claude-code

- Date: 2026-11-18T00:11
- Host version: 2.1.326 (Claude Code)
- Model: host default
- Skill filter: all
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
| architecture-design | − | apply_discount returns 0 for 10%, fix it | debugging | debugging, tdd | pass |
| architecture-design | − | Review my PR | code-review | code-review | pass |
| axiom-orchestrator | + | Add multi-currency support to the checkout flow | axiom-orchestrator | axiom-orchestrator | pass |
| axiom-orchestrator | + | We need to onboard onto this repo and then add an export feature | axiom-orchestrator | axiom-orchestrator, project-onboarding | pass |
| axiom-orchestrator | + | Coordinate the work to migrate our auth to OAuth with tests and docs | axiom-orchestrator | axiom-orchestrator | pass |
| axiom-orchestrator | − | Fix the typo 'recieve' in README.md | none | — | pass |
| axiom-orchestrator | − | What does git rebase --onto do? | none | technical-research | pass |
| ci-and-observability | + | Add a GitHub Actions workflow that runs the tests on every PR | ci-and-observability | ci-and-observability | pass |
| ci-and-observability | + | Our CI takes 20 minutes, can you make the pipeline faster? | ci-and-observability | ci-and-observability | pass |
| ci-and-observability | + | Add structured logging and a latency metric to the checkout endpoint | ci-and-observability | axiom-orchestrator | fail |
| ci-and-observability | − | CI is red on the pricing tests since the last merge, fix pls | debugging | debugging | pass |
| ci-and-observability | − | Cut release 1.2.0 | release-management | release-management | pass |
| ci-and-observability | − | apply_discount is slow, speed it up | performance-optimization | performance-optimization, debugging | pass |
| code-review | + | Review this pull request before I merge it | code-review | code-review | pass |
| code-review | + | Can you do a quality pass on the changes another agent just made? | code-review | code-review | pass |
| code-review | + | Check this plan before we start implementing | code-review | code-review | pass |
| code-review | − | Deploy this to production now | release-management | release-management | pass |
| code-review | − | Write a failing test for this bug before fixing it | tdd | tdd | pass |
| codebase-exploration | + | Where is the discount cap applied, and which tests cover it? | codebase-exploration | codebase-exploration | pass |
| codebase-exploration | + | Trace how apply_discount is used across this repo | codebase-exploration | codebase-exploration | pass |
| codebase-exploration | + | Map out this codebase for me: entry points, modules, tests | codebase-exploration | codebase-exploration | pass |
| codebase-exploration | − | Write release notes for 2.3.0 | release-management | release-management | pass |
| codebase-exploration | − | Add a dark mode toggle | ui-ux-design | axiom-orchestrator | pass |
| codebase-onboarding | + | I'm new to this repo. Onboard me: what is it, how do I run the tests,  | codebase-onboarding | project-onboarding | pass |
| codebase-onboarding | + | Get familiar with this codebase and write down what a new contributor  | codebase-onboarding | project-onboarding | pass |
| codebase-onboarding | − | Fix the failing pricing test | debugging | debugging | pass |
| codebase-onboarding | − | Is it safe to accept percent above 100? | security-audit | — | pass |
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
| e2e-testing | + | Write an end-to-end browser test for the checkout discount flow | e2e-testing | e2e-testing | pass |
| e2e-testing | + | Click through the signup page in a browser and check it works | e2e-testing | e2e-testing | pass |
| e2e-testing | + | Add a Playwright test covering login and checkout | e2e-testing | e2e-testing | pass |
| e2e-testing | + | Use the e2e-testing skill to cover the checkout discount journey | e2e-testing | e2e-testing | pass |
| e2e-testing | − | Add unit tests for apply_discount edge cases | testing | testing | pass |
| e2e-testing | − | Spec out the UI for a discount input | ui-ux-design | ui-ux-design | pass |
| e2e-testing | − | The checkout unit test fails only in CI, figure out why | debugging | debugging | pass |
| implementation | + | Implement task T3 from the plan: add apply_coupon to pricing.py | implementation | implementation | pass |
| implementation | + | Build the coupon function we specced, following the project's conventi | implementation | axiom-orchestrator | fail |
| implementation | − | Plan the coupon work into tasks | task-planning | task-planning | pass |
| implementation | − | Review the coupon diff | code-review | code-review | pass |
| performance-optimization | + | The monthly revenue report is slow for big tenants. Speed it up. | performance-optimization | performance-optimization | pass |
| performance-optimization | + | monthly_revenue takes forever once a tenant has thousands of invoices | performance-optimization | performance-optimization | pass |
| performance-optimization | + | Should we add a cache in front of the reports module? It feels slow. | performance-optimization | performance-optimization | pass |
| performance-optimization | − | monthly_revenue returns the wrong total for March, fix it | debugging | debugging | pass |
| performance-optimization | − | Add a GitHub Actions workflow that runs the tests | ci-and-observability | ci-and-observability | pass |
| performance-optimization | − | Review this PR before I merge | code-review | code-review | pass |
| product-discovery | + | I have a vague idea for a loyalty feature, help me figure out what to  | product-discovery | product-discovery | pass |
| product-discovery | + | Interview me about this feature before we design anything | product-discovery | product-discovery | pass |
| product-discovery | + | Not sure exactly what we need for notifications, can you help scope it | product-discovery | product-discovery | pass |
| product-discovery | + | Before we build a referral program, is it even worth doing? Push back  | product-discovery | product-discovery | pass |
| product-discovery | − | Rename getUser to fetchUser everywhere | none | — | pass |
| product-discovery | − | Fix the null pointer in OrderService | debugging | debugging | pass |
| project-documentation | + | Update the README to document apply_discount's behavior | project-documentation | project-documentation | pass |
| project-documentation | + | Our docs are stale; refresh the project documentation from the code | project-documentation | project-documentation | pass |
| project-documentation | + | Let's do a retro on the mistakes from this session and record what we  | project-documentation | project-documentation | pass |
| project-documentation | − | Fix the discount bug | debugging | debugging | pass |
| project-documentation | − | Write a spec for loyalty discounts | requirements-analysis | requirements-analysis | pass |
| project-onboarding | + | Set up Axiom project knowledge for this repo: commands, conventions, a | project-onboarding | project-onboarding | pass |
| project-onboarding | + | Onboard this project so future agent sessions know how to build and te | project-onboarding | project-onboarding | pass |
| project-onboarding | − | Write a failing test for the discount bug | tdd | tdd | pass |
| project-onboarding | − | Shape a loyalty discount feature with me | product-discovery | product-discovery | pass |
| quality-constraints | + | Set up quality constraints for this project | quality-constraints | quality-constraints | pass |
| quality-constraints | + | The agent keeps skipping tests to get green, stop that | quality-constraints | quality-constraints | pass |
| quality-constraints | + | What coverage threshold should we enforce? | quality-constraints | quality-constraints | pass |
| quality-constraints | − | Review this PR | code-review | code-review | pass |
| quality-constraints | − | Set up GitHub Actions CI | ci-and-observability | ci-and-observability | pass |
| release-management | + | Cut release 1.0.0 and publish it | release-management | release-management | pass |
| release-management | + | Are we ready to ship 2.3.0? Prepare the release | release-management | release-management | pass |
| release-management | + | Write release notes and tag this version | release-management | release-management, verification-before-completion | pass |
| release-management | − | Add a coupon function | implementation | axiom-orchestrator, tdd | pass |
| release-management | − | Review this diff | code-review | code-review | pass |
| requirements-analysis | + | Write a spec for a loyalty discount for repeat customers | requirements-analysis | requirements-analysis | pass |
| requirements-analysis | + | Turn this idea into testable requirements: customers get 5% off after  | requirements-analysis | requirements-analysis | pass |
| requirements-analysis | + | Write the acceptance criteria for a coupon feature: 10% off orders ove | requirements-analysis | requirements-analysis | pass |
| requirements-analysis | − | Break the approved coupon spec into tasks | task-planning | task-planning | pass |
| requirements-analysis | − | Fix the failing pricing test | debugging | debugging | pass |
| security-audit | + | Is this endpoint vulnerable to IDOR? | security-audit | security-audit | pass |
| security-audit | + | Do a full security audit of this repository | security-audit | security-audit | pass |
| security-audit | + | Pen-test the auth module and give me a report | security-audit | security-audit | pass |
| security-audit | + | We commit a .mcp.json and a hooks config for our coding agent. Could t | security-audit | security-audit | pass |
| security-audit | − | Make the login page look nicer | ui-ux-design | ui-ux-design | pass |
| security-audit | − | Speed up the slow orders query | none | performance-optimization | pass |
| skill-evaluator | + | Is the tdd skill ready to leave experimental status? | skill-evaluator | skill-evaluator | pass |
| skill-evaluator | + | Evaluate whether our debugging skill actually triggers and changes beh | skill-evaluator | skill-evaluator | pass |
| skill-evaluator | + | Here is the transcript of yesterday's session where the agent went in  | skill-evaluator | skill-evaluator | pass |
| skill-evaluator | − | Create a new skill for changelog entries | skill-factory | skill-factory | pass |
| skill-evaluator | − | Review this pull request | code-review | code-review | pass |
| skill-factory | + | Create a skill that makes agents write changelog entries | skill-factory | skill-factory | pass |
| skill-factory | + | Turn our deploy checklist into an agent skill | skill-factory | skill-factory | pass |
| skill-factory | + | Agents ignore the wording in our review skill; rewrite it so they foll | skill-factory | skill-factory | pass |
| skill-factory | − | Is the tdd skill ready to ship? | skill-evaluator | skill-evaluator | pass |
| skill-factory | − | Write the changelog for 2.3.0 | release-management | release-management | pass |
| spec-analysis | + | Check whether spec.md, plan.md, and tasks.md are consistent | spec-analysis | spec-analysis | pass |
| spec-analysis | + | What's left to implement compared to the spec? | spec-analysis | spec-analysis | pass |
| spec-analysis | + | Analyze the spec and tasks for gaps before we start coding | spec-analysis | spec-analysis | pass |
| spec-analysis | − | Write the spec for a referral program | requirements-analysis | requirements-analysis | pass |
| spec-analysis | − | Fix the failing unit test | debugging | debugging | pass |
| task-planning | + | Break the coupon spec into an implementation plan with tasks | task-planning | task-planning | pass |
| task-planning | + | Plan the work to fix the discount bug and add edge-case tests | task-planning | task-planning | pass |
| task-planning | − | Just fix the bug | debugging | debugging | pass |
| task-planning | − | Is our spec consistent with the tasks? | spec-analysis | spec-analysis | pass |
| tdd | + | Use TDD to add a percent cap to apply_discount | tdd | tdd | pass |
| tdd | + | apply_discount(1000, 10) returns 0. Write a failing test for this bug  | tdd | tdd, debugging | pass |
| tdd | + | Make apply_discount reject negative totals, test-first please | tdd | tdd | pass |
| tdd | + | Run this through the tdd skill: apply_discount should accept a maximum | tdd | tdd | pass |
| tdd | + | Red, green, refactor: add rounding to the nearest cent in apply_discou | tdd | tdd | pass |
| tdd | − | Why is the build slow? | ci-and-observability | performance-optimization | pass |
| tdd | − | Review this diff for security issues | code-review | security-audit | pass |
| tdd | − | apply_discount returns 0 for a 10% discount, find out why | debugging | debugging | pass |
| tdd | − | Which apply_discount edge cases do our tests miss? | testing | testing | pass |
| technical-research | + | What does Python's round() do with 2.5, and should apply_discount use  | technical-research | technical-research | pass |
| technical-research | + | Check the current docs: is datetime.utcnow deprecated, and what replac | technical-research | technical-research | pass |
| technical-research | − | Where is the discount cap applied? | codebase-exploration | codebase-exploration | pass |
| technical-research | − | Fix the discount bug | debugging | debugging | pass |
| testing | + | Add tests for apply_discount edge cases | testing | testing | pass |
| testing | + | What test coverage do we need for the pricing module? | testing | testing | pass |
| testing | + | Use the testing skill to plan the test suite for pricing.py | testing | testing | pass |
| testing | + | Our pricing tests miss obvious cases, beef them up | testing | testing | pass |
| testing | − | Write an end-to-end browser test for checkout | e2e-testing | e2e-testing | pass |
| testing | − | Use TDD to add a coupon | tdd | tdd | pass |
| testing | − | The pricing tests started failing after the merge, find out why | debugging | debugging | pass |
| ui-ux-design | + | Design the settings page for notification preferences | ui-ux-design | ui-ux-design | pass |
| ui-ux-design | + | This form is hard to use on mobile, improve it | ui-ux-design | ui-ux-design | pass |
| ui-ux-design | + | Check the new dashboard for accessibility problems | ui-ux-design | ui-ux-design | pass |
| ui-ux-design | + | Move our hard-coded CSS colors to design tokens and add a dark theme | ui-ux-design | axiom-orchestrator | fail |
| ui-ux-design | − | Optimize this SQL query | none | — | pass |
| ui-ux-design | − | Add an index to the orders table | none | — | pass |
| verification-before-completion | + | Ok looks done, go ahead and commit it | verification-before-completion | verification-before-completion | pass |
| verification-before-completion | + | Are we good to open the PR now? | verification-before-completion | verification-before-completion | pass |
| verification-before-completion | + | The subagent says all tests pass, mark the task complete | verification-before-completion | verification-before-completion | pass |
| verification-before-completion | − | Explain what this function does | none | — | pass |
| verification-before-completion | − | Plan the migration to Postgres 17 | task-planning | axiom-orchestrator | pass |
| writing-quality | + | Humanize this, it sounds like ChatGPT wrote it: 'In today's fast-paced | writing-quality | writing-quality | pass |
| writing-quality | + | Tighten this PR description, it's too fluffy: 'This PR delves into the | writing-quality | writing-quality | pass |
| writing-quality | + | Make this README intro less salesy and more direct | writing-quality | writing-quality | pass |
| writing-quality | − | Write a spec for coupon codes | requirements-analysis | requirements-analysis | pass |
| writing-quality | − | Fix the typo 'recieve' in README.md | none | — | pass |
| writing-quality | − | Review my PR before I merge it | code-review | code-review | pass |

Summary: 147/150 pass.
