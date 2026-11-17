# Changelog

All notable changes to Axiom are documented here. Versions follow [ADR-0005](docs/decisions/0005-versioning-and-upgrades.md); user-facing summaries and upgrade steps for each release are in [release notes](docs/releases/README.md). To update an installed copy, see [Upgrading](docs/UPGRADING.md).

New entries go under **Unreleased**, grouped as Breaking, Added, Changed, Fixed. A release moves them under its version heading.

## [Unreleased]

### Fixed

- `docs/RELEASES.md`: the publish step now rewrites the notes' relative links to absolute links at the tag. Published as-is, they broke on the GitHub release page (seen on v0.1.0, whose release text was corrected by hand).

## [0.1.0] - 2026-11-17

First versioned release. Kernel: new (paste the Axiom block). Everything below shipped in this version.

### Versioning and upgrades

- Version 0.1.0 set in the plugin manifest, the kernel heading, and the Axiom block marker; the validator keeps them and this changelog in step.
- Release notes per version in `docs/releases/`, and an upgrade guide for plugin, `npx skills`, clone, and copy installs in `docs/UPGRADING.md`.

- Establish the initial repository foundation.
- Define the skills-first, native-first, Markdown-first architecture.
- Add initial lifecycle workflows, platform adapters, contracts, and evaluation guidance.
- Complete the lifecycle skill catalog, optional native delegation roles, and handoff patterns.
- Add focused bug-fix, refactoring, security-audit, performance-audit, and release workflows.
- Add project knowledge templates, living-document rules, optional integration fallbacks, and manual install/update guidance.
- Add structural validation, CI, and human-reviewable skill, workflow, cross-agent, and context-efficiency fixtures.
- Clarify that fixture definitions and official documentation inspection are not live model or platform test results.

### Trigger run after the adoption pass (2026-11-17)

- Claude Code 2.1.326, one run per prompt: 125/131 across 27 skills; the 24 original skills hold at 110/113. Two misses predate this change (orchestrator vs onboarding on a combined request; acceptance criteria with no spec in the workspace). A rerun of the skills with new misses passed 16/16.
- The first run found a regression: a "cache or not, weigh the options" prompt went to `performance-optimization`. Its description no longer mentions caches and now hands design trade-offs to `architecture-design`; the prompt passes again.
- Two `writing-quality` trigger prompts referred to text that was not in the workspace; they now include the text.
- Run records `2026-11-17-1438` and `-1440` include host errors from a five-hour usage limit on the CLI login; they are kept as records, not counted as skill failures.

### Measurement and distribution pass (2026-11-17)

- `run_evals.py --routing`: an offline TF-IDF routing report over skill descriptions and kernel rows. `--check` now fails when two descriptions are at least 0.75 similar. First report: top-1 48/73, top-3 61/73, negatives clear 56/58, no collisions. This is a proxy; live trigger accuracy remains the evidence.
- Behavior results record tokens per run and the median per case, for Claude Code and Codex streams.
- The validator caps `SKILL.md` at 20,000 bytes in addition to 250 lines.
- `skill-evaluator` documents variant evals: test whether a section earns its tokens, with at least 10 runs per side.
- Code graph tools share one integration page (`integrations/codebase-memory/`): codebase-memory for code, Graphify only when documents must be mapped with code; never install or build without approval, and check coverage before relying on results.
- The RTK integration page now covers detection, the three cases that require an uncondensed rerun, and why a compressor summary is not verification evidence; `verification-before-completion` names compressed output as a trap.
- Native plugins for Codex, OpenCode, and Antigravity were not shipped: no host was available to test a manifest. The reason is recorded in the adapter overview.
- The test file's `unittest.main()` guard sat above two test classes, so running the file directly skipped them; it now sits at the end.

### Adoption pass (2026-11-17)

- New skills: `writing-quality` (AI writing tells, fact-preserving edits, embedded mode), `performance-optimization` (baseline, profile, re-measure), and `ci-and-observability` (pipelines from real commands; logs, metrics, traces, alerts). Each has eval cases; none has recorded runs yet.
- `requirements-analysis` gains change proposals with ADDED, MODIFIED, REMOVED, and RENAMED deltas and a bundled change template; `spec-analysis` converge checks removed requirements in reverse and uses `not verified` for unrun checks.
- `ui-ux-design` gains critique, audit, polish, and harden modes, a craft floor with Verify and Refuse lists, an unanchored critique with heuristic scores, and surface modes in the design master.
- Kernel rule 2 names what minimalism never cuts. `implementation` gains a reuse-first decision ladder and `shortcut:` markers, which `code-review` treats as decisions.
- `debugging` requires a feedback loop before hypotheses. `architecture-design` adds prototype and deprecation sections. `project-documentation` adds retros. The orchestrator records the base commit before dispatch and refutes plan claims during review. Negative search claims need a search record. Bug Fix ends with a verified, partial, or failed verdict.
- Descriptions of `debugging`, `tdd`, and `verification-before-completion` now say they apply even when the change looks obvious. Trigger accuracy after this change is not yet measured.
- Claude Code plugin adds `/axiom:spec`, `/axiom:plan`, `/axiom:review`, and `/axiom:ship`, all user-invoked only.
- Not adopted: binaries and CLIs (detectors, spec CLIs), auto-installing tools, persona agents, and moving canonical skills to host-specific `disable-model-invocation` frontmatter, which would break kernel routing and portability.

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
