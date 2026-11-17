# Eval run: trigger on claude-code

- Date: 2026-11-17T14:40
- Host version: 2.1.326 (Claude Code)
- Model: host default
- Skill filter: skill-factory,spec-analysis,task-planning,tdd,technical-research,testing,ui-ux-design,verification-before-completion,writing-quality
- Max turns: 4
- Repeats per behavior case: 1; grader: none
- Isolation: user settings excluded
- Kernel in project instructions: yes
- Per-run budget cap (USD): 0.5
- Runner: scripts/run_evals.py

| Skill | Expect | Prompt | Owner | Invoked | Verdict |
|---|---|---|---|---|---|
| skill-factory | + | Create a skill that makes agents write changelog entries | skill-factory | skill-factory | pass |
| skill-factory | + | Turn our deploy checklist into an agent skill | skill-factory | — | error (exit 1) |
| skill-factory | − | Is the tdd skill ready to ship? | skill-evaluator | — | error (exit 1) |
| skill-factory | − | Write the changelog for 2.3.0 | release-management | — | error (exit 1) |
| spec-analysis | + | Check whether spec.md, plan.md, and tasks.md are consistent | spec-analysis | — | error (exit 1) |
| spec-analysis | + | What's left to implement compared to the spec? | spec-analysis | — | error (exit 1) |
| spec-analysis | + | Analyze the spec and tasks for gaps before we start coding | spec-analysis | — | error (exit 1) |
| spec-analysis | − | Write the spec for a referral program | requirements-analysis | — | error (exit 1) |
| spec-analysis | − | Fix the failing unit test | debugging | — | error (exit 1) |
| task-planning | + | Break the coupon spec into an implementation plan with tasks | task-planning | — | error (exit 1) |
| task-planning | + | Plan the work to fix the discount bug and add edge-case tests | task-planning | — | error (exit 1) |
| task-planning | − | Just fix the bug | debugging | — | error (exit 1) |
| task-planning | − | Is our spec consistent with the tasks? | spec-analysis | — | error (exit 1) |
| tdd | + | Use TDD to add a percent cap to apply_discount | tdd | — | error (exit 1) |
| tdd | + | apply_discount(1000, 10) returns 0. Write a failing test for this bug  | tdd | — | error (exit 1) |
| tdd | + | Make apply_discount reject negative totals, test-first please | tdd | — | error (exit 1) |
| tdd | − | Why is the build slow? | ci-and-observability | — | error (exit 1) |
| tdd | − | Review this diff for security issues | code-review | — | error (exit 1) |
| technical-research | + | What does Python's round() do with 2.5, and should apply_discount use  | technical-research | — | error (exit 1) |
| technical-research | + | Check the current docs: is datetime.utcnow deprecated, and what replac | technical-research | — | error (exit 1) |
| technical-research | − | Where is the discount cap applied? | codebase-exploration | — | error (exit 1) |
| technical-research | − | Fix the discount bug | debugging | — | error (exit 1) |
| testing | + | Add tests for apply_discount edge cases | testing | — | error (exit 1) |
| testing | + | What test coverage do we need for the pricing module? | testing | — | error (exit 1) |
| testing | − | Write an end-to-end browser test for checkout | e2e-testing | — | error (exit 1) |
| testing | − | Use TDD to add a coupon | tdd | — | error (exit 1) |
| ui-ux-design | + | Design the settings page for notification preferences | ui-ux-design | — | error (exit 1) |
| ui-ux-design | + | This form is hard to use on mobile, improve it | ui-ux-design | — | error (exit 1) |
| ui-ux-design | + | Check the new dashboard for accessibility problems | ui-ux-design | — | error (exit 1) |
| ui-ux-design | − | Optimize this SQL query | none | — | error (exit 1) |
| ui-ux-design | − | Add an index to the orders table | none | — | error (exit 1) |
| verification-before-completion | + | Ok looks done, go ahead and commit it | verification-before-completion | — | error (exit 1) |
| verification-before-completion | + | Are we good to open the PR now? | verification-before-completion | — | error (exit 1) |
| verification-before-completion | + | The subagent says all tests pass, mark the task complete | verification-before-completion | — | error (exit 1) |
| verification-before-completion | − | Explain what this function does | none | — | error (exit 1) |
| verification-before-completion | − | Plan the migration to Postgres 17 | task-planning | — | error (exit 1) |
| writing-quality | + | Humanize this paragraph, it sounds like ChatGPT wrote it | writing-quality | — | error (exit 1) |
| writing-quality | + | Tighten this PR description, it's too fluffy | writing-quality | — | error (exit 1) |
| writing-quality | + | Make this README intro less salesy and more direct | writing-quality | — | error (exit 1) |
| writing-quality | − | Write a spec for coupon codes | requirements-analysis | — | error (exit 1) |
| writing-quality | − | Fix the typo 'recieve' in README.md | none | — | error (exit 1) |
| writing-quality | − | Review my PR before I merge it | code-review | — | error (exit 1) |

Summary: 1/42 pass.
