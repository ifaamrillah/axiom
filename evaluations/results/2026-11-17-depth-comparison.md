# Skill depth: old vs deepened skills (2026-11-17)

This record asks whether the skill depth pass (147 KB → 798 KB of skill content) changes what an agent catches. Each run used the same fixtures, the same cases, and the same runner (Claude Code 2.1.325, native CLI, kernel with routing for all 24 skills). The only variable was the skills directory:
- **old:** `origin/main` at `bc003fc`, run from a git worktree;
- **new:** `feat/skill-depth`.

Every run was graded by **Codex** (a non-Claude grader), from host-recorded tool calls and the final answer. The scores below count expectations met across 3 runs per case.

| Model | Case | Old skills | New skills | Records |
|---|---|---|---|---|
| Opus (host default) | security-audit/B2, `notes-api` (4 seeded issues) | 3/3 pass | 3/3 pass | `2026-11-17-0012-*` |
| Opus | security-audit/B3, `tenant-billing` (6 subtle issues, 2 decoys) | 18/18, 0 false-positive signals | 18/18, 0 false-positive signals | `2026-11-17-0021-*-old-skills`, `2026-11-17-0022-*` |
| Opus | code-review/B2, `tenant-billing` reports module (4 bugs) | 14/15 | 14/15 | `2026-11-17-0020-*` |
| Haiku | security-audit/B2 | 14/15 | 14/15 | `2026-11-17-0031-*` |
| Haiku | security-audit/B3 | 18/18 | 18/18 | `2026-11-17-0031-*` |
| Haiku | code-review/B2 | 10/15 (0/3 runs pass; skill invoked 1/3) | **13/15** (1/3 runs pass; skill invoked 3/3) | `2026-11-17-0031-*` |

## Reading

- **Opus:** no measurable difference. The model finds every seeded issue in both fixtures without the added detail, so these fixtures cannot show the value of depth for a strong model.
- **Haiku:** the only difference is on code review, 10/15 → 13/15. The skill was invoked in 1 of 3 old runs and 3 of 3 new runs, even though the description and kernel were identical in both. That gap is run-to-run variance, not the content. With 3 runs per side this is a hint, not a result.
- **Not measured:**
  - quality of findings beyond the rubric (severity calibration, safe validation steps, quality of fixes);
  - cost;
  - larger, real codebases.

## What would measure depth properly

- Many more runs per side, at least 10, so variance is visible.
- Fixtures whose issues need knowledge that sits in the references and is not obvious from the code alone: framework-specific sinks, tenant escape hatches, protocol details.
- A rubric that scores how good each finding is, not only whether it was found.
