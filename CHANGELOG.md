# Changelog

All notable changes to Axiom are documented here.

## Unreleased

- Establish the initial repository foundation.
- Define the skills-first, native-first, Markdown-first architecture.
- Add initial lifecycle workflows, platform adapters, contracts, and evaluation guidance.
- Complete the lifecycle skill catalog, optional native delegation roles, and handoff patterns.
- Add focused bug-fix, refactoring, security-audit, performance-audit, and release workflows.
- Add project knowledge templates, living-document rules, optional integration fallbacks, and manual install/update guidance.
- Add structural validation, CI, and human-reviewable skill, workflow, cross-agent, and context-efficiency fixtures.
- Clarify that fixture definitions and official documentation inspection are not live model or platform test results.

### M8–M12: adoption pass (2026-11-16)

- **M8 Behavior:** add the always-on Axiom kernel and a project instructions block with Pitfalls; add `verification-before-completion`; rewrite `tdd`, `debugging` (with root-cause tracing, condition-based waiting, and test-pollution bisection references), and `code-review` (spec-first, gap analysis, lenses, bar-lowering detection, blast radius, adversarial review). Add an optional read-only Claude Code SessionStart hook that prints the kernel.
- **M9 Evaluation:** add runnable Markdown eval cases (`evaluations/cases/`), a seeded fixture, `scripts/run_evals.py` (structure check in CI; headless trigger and behavior runs for Claude Code), recorded results, unit tests, and test-first `skill-factory`/`skill-evaluator`. The validator now enforces trigger clauses, a 250-line `SKILL.md` budget, linked references, and valid JSON. ADR-0004 bounds maintainer tooling and adapter hooks.
- **M10 Specification and execution:** add `spec-analysis` (read-only analyze, append-only converge) and `quality-constraints`; add clarification markers, a clarification taxonomy, and a requirements-quality checklist; add constitution, constraints, and definition-of-done templates; add the Ready-for-Development plan standard with status frontmatter; add implementer, task-reviewer, and fix-loop prompts; add rulings, stop conditions, and baseline-relative gates; split Feature Development into on-demand stage files.
- **M11 Domain depth:** rewrite `security-audit` (guidance vs full audit, six-element findings, severity anchors, `needs_validation`, coverage ledger, refuting verifiers, profiles and budget); add elicitation to `product-discovery`; add priority UI rules and a design-system master to `ui-ux-design`; add concrete browser automation and documentation-search protocols; add freshness metadata and pitfalls to documentation; add role capability and write metadata and `.axiom/config.md`.
- **M12 Distribution:** add Claude Code plugin and marketplace manifests (skills from `.agents/skills/`, kernel hook, read-only reviewer, security-reviewer, and researcher subagents); document `npx skills` installation and AGENTS.md bootstrap for Codex, OpenCode, and Antigravity.
- Credit adapted ideas in `docs/acknowledgements.md`.

### M8–M12 follow-up: eval fixes (2026-11-16)

- Kernel gains rule 5, **Reproduce before fixing**; later rules are renumbered (evidence before claims is now rule 6). Routing names the "X returns Y, should be Z" and "failing test first" phrasings.
- `tdd` description names the "failing test for this bug first" request.
- `run_evals.py`: workspaces receive the kernel in `CLAUDE.md`/`AGENTS.md` like a documented install (`--no-kernel` to measure skills alone); case files may set a `fixture:` for trigger runs; result files are never overwritten.
- `tdd` and `debugging` trigger cases that referred to code now run against the `discount-bug` fixture.
- Evidence: trigger 5/5 (`tdd`) and 7/7 (`debugging`); behavior `debugging/B1` passes 2/2 recorded runs and `tdd/B1` 1/1; marketplace install from GitHub verified; `npx skills` install verified.
- Eval cases for all 24 skills; `run_evals.py` gains `--repeat`, `--grade` (separate tool-less grader with strict verdicts), written content in traces, and host-error detection (budget caps, usage limits). Repeated, independently graded behavior runs recorded on the CLI and, after a usage limit, on an in-session subagent harness.
- Kernel routing covers all 24 skills and states that loading a skill is not ceremony. Native trigger accuracy went from 56/81 (18 skills) to 110/113 (all 24), with no negative-case regressions.
- `skill-factory`: eval case file before `SKILL.md`, and predicted baselines labeled as unobserved. This raised its graded behavior from 2/5 to 5/5.
- Skills are self-contained for skills-only installs: 16 templates and prompts are bundled under skill `assets/` (byte-identical to their repository source, enforced by the validator, refreshed with `--sync`); other repository files are named as plain text. The validator rejects links that leave `.agents/skills/`.
