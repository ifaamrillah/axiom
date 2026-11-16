# Platform Compatibility

**Documentation reviewed: 2026-11-15/16. Live runs: Claude Code only, 2026-11-16.** This report separates documentation inspection from live runtime evidence.

| Host | Officially documented discovery | Axiom-specific status |
|---|---|---|
| Claude Code | Project `.claude/skills/`; plugin manifest `skills` paths | **Live-tested (2.1.325):** plugin validated; loaded with `--plugin-dir` and installed from the GitHub marketplace (24 skills, 4 subagents, kernel hook observed in context); trigger and behavior evals recorded (see below) |
| Codex | Project `.agents/skills/`; user `~/.agents/skills/` | Official docs inspected; live discovery and invocation not tested |
| OpenCode | `.agents/skills/` is a project compatibility source; permissions and precedence can affect loading | Official docs inspected; live discovery and invocation not tested |
| Antigravity | Workspace `.agents/skills/`; global `~/.gemini/config/skills/` | Official docs inspected; live discovery and invocation not tested |

## Claude Code live evidence (2026-11-16, Claude Code 2.1.325, host default model)

All runs used `scripts/run_evals.py` with user-level settings excluded (`--setting-sources project,local`). Each run happened in a disposable workspace with the skills copied into `.claude/skills/`. Runs from 07:30 on add the kernel block to `CLAUDE.md`/`AGENTS.md`, as a documented install does, and run code-referring prompts against the `discount-bug` fixture. Full records are in [`evaluations/results/`](../../evaluations/results/README.md).

**Plugin:** `claude plugin validate .` passed. Its only warnings were the intentionally omitted `version`, plus "no frontmatter" notices for role cards, which are not loaded as agents. A headless session with `--plugin-dir` listed all 24 `axiom:` skills and exactly 4 `axiom:` subagents, and quoted the kernel's evidence-before-claims rule (then rule 5, now rule 6) from context without reading files.

**Marketplace install:** `claude plugin marketplace add "https://github.com/ifaamrillah/axiom.git#feat/m8-m12-adoption" --scope local` followed by `claude plugin install axiom@axiom --scope local` in a scratch project succeeded. The next headless session listed 24 `axiom:` skills and 4 `axiom:` subagents, and the kernel came from the hook. Both were removed afterward.

**`npx skills` (skills@1.8.1):** installed all 24 skills for Claude Code, Codex, OpenCode, and Antigravity targets in a scratch project; Claude Code listed all 24. Only skill directories are copied. At that point 39 links in 17 skills pointed outside them; skills are now self-contained and a skills-only copy has no broken links. See the [adapter overview](../../adapters/README.md#installing-into-another-project-without-a-custom-cli).

**Native trigger accuracy, all 24 skills:** **110/113** ([record](../../evaluations/results/2026-11-16-1500-claude-code-trigger.md)).
- All 49 negative cases passed. Each positive miss went to a defensible alternative route or to a clarifying question.
- The run before it scored 56/81 on 18 skills, with every miss an under-trigger. That changed after the kernel routing table was expanded to all 24 skills and stated that loading a skill is not ceremony.
- The per-skill history below predates that change.

**Trigger accuracy** (latest run per skill; positives must invoke the skill, negatives must not):

| Skill | Result | Note |
|---|---|---|
| verification-before-completion | 5/5 | 4/5 before the description gained commit and ship phrasing |
| debugging | 7/7 | Rerun with kernel and fixture; the CI prompt was rewritten to match the Python fixture |
| tdd | 5/5 | The earlier miss was a case defect: "this bug" in an empty workspace correctly drew a clarifying question. Now run against the fixture |
| code-review | 5/5 | 3/5 before; one miss was routed to the host's built-in `simplify` skill |
| security-audit | 5/5 | |
| spec-analysis | 5/5 | 4/5 before the "what's left to implement" phrasing |

Total on the latest runs: 32/32. Not run: `axiom-orchestrator`, `quality-constraints`, `product-discovery`, `ui-ux-design`.

**Behavior** (graded by the authoring session, not an independent grader):

| Case | Kernel | Result | Note |
|---|---|---|---|
| `debugging/B1` | no (before follow-up) | FAIL ×2 | Skill not invoked; edited `pricing.py` before reproducing |
| `debugging/B1` | yes | PASS ×2 recorded (a third, identical run was overwritten by a since-fixed runner bug) | Skill invoked; failing test run before the fix |
| `debugging/B1` | no (control) | PASS ×1 | Skill not invoked, but order correct. Variance is real; one pass is not proof |
| `tdd/B1` | yes | PASS ×1 | Red quoted (`0 != 900`), then minimal fix and green |

Other behavior cases have not been run.

## Subagent harness evidence (2026-11-16, Claude Code desktop)

When the CLI account hit its usage limit, runs continued as in-session subagents. This is a different harness: skills were read from files on instruction, not discovered natively. Records: [behavior](../../evaluations/results/2026-11-16-1400-subagent-behavior.md), [routing](../../evaluations/results/2026-11-16-1400-subagent-routing.md).

- **Behavior:** 7 cases × 5 runs, graded by a separate Sonnet grader against host-recorded tool calls and workspace state. Six cases scored 5/5: debugging, release-management, task-planning, technical-research, testing, and requirements-analysis. skill-factory scored 2/5, rose to 5/5 after its cases-first rule, and still has no observed baseline.
- **Description routing:** 113/113 on both independent routers across all 24 skills. Choosing from a list of descriptions is easier than native discovery.

Earlier on the same day, CLI behavior runs with the independent grader produced these scores:
- 5/5: tdd, verification-before-completion, quality-constraints, security-audit, architecture-design, axiom-orchestrator, codebase-exploration, product-discovery, spec-analysis, codebase-onboarding, e2e-testing, implementation, project-documentation, skill-evaluator.
- 4/4 graded: ui-ux-design and project-onboarding, each with one ungraded run.
- 4/5: code-review.
- 3/5: requirements-analysis. The failures came from a runner limitation that has since been fixed.

## What has not been checked

- User-scope (global) installs with any installer.
- Any live run on Codex, OpenCode, or Antigravity. The eval runner supports only Claude Code.
- Observed baselines for skills created test-first in a subagent.
- Grading by a different model family; graders here were Claude models.
- Results may differ with other models, versions, or user settings.

## Graceful fallbacks

- If a skill is not discovered, open its `SKILL.md` directly and follow it manually.
- If host-specific metadata is rejected, keep canonical frontmatter at `name` and `description`; do not add a required Axiom extension.
- If Claude Code symlinks are unavailable, copy the skill directory or use the plugin, and treat `.agents/skills/` as the source of truth.
- If hooks are unavailable, paste the kernel block into the project's instructions file.
- If workflow state is unsupported, maintain a Markdown checklist or use the host conversation.

## Primary documentation

- [Codex skills](https://developers.openai.com/codex/skills/)
- [OpenCode skills](https://opencode.ai/docs/skills/)
- [Antigravity skills](https://antigravity.google/docs/skills)
- [Claude Code skills](https://code.claude.com/docs/en/skills), [plugin manifest](https://code.claude.com/docs/en/plugins-reference)
