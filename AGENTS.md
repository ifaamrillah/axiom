# Repository Instructions

## Mission

Build Axiom as a universal, skills-first software engineering harness. Keep the repository portable, understandable, evidence-driven, and usable without a custom runtime or CLI.

## Authoritative decisions

- Standard Agent Skills format: every skill directory has a `SKILL.md` with standard `name` and `description` frontmatter.
- Canonical skills live in `.agents/skills/`.
- Workflow definitions and workflow execution state are Markdown-first.
- Orchestration is native-first; do not build a custom agent runtime.
- There is no CLI.
- Initial platform targets: Claude Code, Codex, OpenCode, and Antigravity.
- Full lifecycle scope; workflows cover onboarding, feature development, bug fixes, refactoring, security/performance audits, and release readiness.
- Balance quality, speed, and context/token efficiency.

## Working rules

1. Inspect relevant repository instructions and existing files before editing.
2. Prefer the smallest complete solution; avoid speculative abstractions and unnecessary dependencies.
3. Keep platform-specific details in `adapters/`; keep canonical skills platform-neutral.
4. Treat source code as the source of truth for implemented behavior and specs as the source of intended behavior. Surface drift; do not silently falsify either.
5. Never claim tests, commands, integrations, screenshots, or deployments ran unless there is evidence.
6. A skipped stage is not a passed stage. A completed task is not automatically a passed quality gate.
7. Require explicit user authorization before production deployment, destructive data operations, publishing, or other consequential external actions.
8. Delegate only independent tasks with explicit deliverables and non-overlapping write scopes. Use sequential work when ownership conflicts.
9. Keep handoffs concise and evidence-based.
10. Update affected documentation and evaluation cases when behavior or interfaces change.

## Documentation conventions

- Use clear Markdown headings and relative links.
- State status and verification date where freshness matters.
- Distinguish normative requirements from examples and recommendations.
- Avoid platform capability claims unless the adapter documents their evidence and limitations.

## Project facts (verified 2026-11-16 at 096adb1)

- Structure and links: `python3 scripts/validate_repository.py` (`--sync` refreshes bundled skill assets after editing their source)
- Eval case structure: `python3 scripts/run_evals.py --check`
- Tooling tests: `python3 -m unittest discover -s scripts/tests`
- Live evals (spend model quota; maintainers only): `python3 scripts/run_evals.py --host claude-code --kind trigger|behavior [--repeat N --grade]`

## Pitfalls

Observed agent mistakes in this repository and the rule that prevents each.

- 2026-11-16 Reverted a temporary test edit with `git checkout <file>` and silently discarded unrelated unstaged edits in that file → undo a temporary edit by editing it back (or stash first); never `git checkout` a file that has uncommitted work.
- 2026-11-16 Several eval runs finishing in the same minute overwrote each other's result file, losing a record → result writers must never overwrite; check that a record exists after each run.
- 2026-11-16 A trigger case said "this bug" in an empty workspace; the agent correctly asked which bug, and the case was misread as a skill miss → prompts that refer to code need a `fixture:`; before blaming a skill, read what the agent actually did.
- 2026-11-16 Claimed that "installing the whole skill set" kept repository links working, without checking → verify install claims by inspecting the installed tree.
