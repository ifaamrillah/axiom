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

### Skill depth pass (2026-11-17)

- Deepen all 24 skills with focused references:
  - 13 vulnerability-class and method references for `security-audit`;
  - curated style, palette, typography, interaction, data-display and per-stack tables for `ui-ux-design`;
  - worked TDD cycles and a testing anti-pattern catalog;
  - layer selection, fixtures, flakiness and per-ecosystem commands for `testing`;
  - Playwright patterns, flake triage and an exploration flow;
  - debugging playbooks by symptom, bisection, instrumentation and stack traces;
  - evidence by claim and completion reports;
  - defect patterns and per-language review checklists;
  - a constraint catalog, ratchets and waivers, and bar-lowering detection;
  - elicitation techniques and a discovery example;
  - spec examples, acceptance criteria, an NFR catalog and ambiguity words;
  - detection passes and a worked analysis;
  - sizing, a worked plan, plan anti-patterns and plan execution;
  - architecture decisions and ADRs, patterns, data and API design;
  - implementation slicing, conventions and finishing a branch;
  - release readiness and versioning, rollout and rollback;
  - research sources, version pinning, local proof and citation;
  - orchestration delegation, the review loop, worktrees and context budget;
  - exploration recipes and entry points;
  - onboarding knowledge files and verification;
  - documentation types, ADRs, runbooks, API docs and freshness;
  - skill triggers, pressure testing, persuasion, eval design and grading.
- Skill content grows from 147 KB to 798 KB (5.4×). The median `SKILL.md` grows from 3.1 KB to 5.5 KB, and every `SKILL.md` stays under 130 lines. Skill descriptions are unchanged, so measured trigger accuracy is unaffected.
- All content is rewritten in Axiom's wording and attributed per file. A 12-word phrase check found at most 3.7% overlap with any source. See `docs/acknowledgements.md`.
- The plan template gains a Global constraints section.
- New `notes-api` fixture with four seeded vulnerabilities and a safe decoy, and a new `security-audit` behavior case (B2).
- New `tenant-billing` fixture (6 subtle multi-file vulnerabilities, 2 decoys, 4 correctness bugs) with `security-audit` B3 and `code-review` B2.
- `run_evals.py --case` filters behavior cases.
- Old vs deepened skills, Codex-graded: no difference with Opus (security 18/18 both; review 14/15 both). With Haiku, code review rose from 10/15 to 13/15 and security was unchanged. The sample is small. See `evaluations/results/2026-11-17-depth-comparison.md`.

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
- `run_evals.py` supports `--host codex` and `--grader-host codex` (a non-Claude grader). Codex native trigger accuracy is 107/113. OpenCode discovered all 24 skills. After the kernel routing change, every behavior case was rerun, part of it graded by Codex.
- `skill-factory`: eval case file before `SKILL.md`, and predicted baselines labeled as unobserved. This raised its graded behavior from 2/5 to 5/5.
- Skills are self-contained for skills-only installs: 16 templates and prompts are bundled under skill `assets/` (byte-identical to their repository source, enforced by the validator, refreshed with `--sync`); other repository files are named as plain text. The validator rejects links that leave `.agents/skills/`.
