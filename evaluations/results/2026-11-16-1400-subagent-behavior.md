# Eval run: behavior via in-session subagents (Claude Code desktop, 2026-11-16)

- Harness: **subagent**, not `scripts/run_evals.py`. The `claude` CLI account had hit its usage limit, so the owner asked to run in the desktop session instead.
- Agent under test: a fresh `general-purpose` subagent per run (host default model), told to work only in a disposable fixture copy that has the kernel block in `CLAUDE.md`/`AGENTS.md` and the skills under `.agents/skills/` and `.claude/skills/`. The subagent was told to read `CLAUDE.md` first and to read a skill's `SKILL.md` when it applies. Skills were **not** natively discoverable, so this measures behavior when skills are read, not native triggering.
- Allowed commands were stated in the prompt (unittest, python3 -c, read-only shell and git); no commit, push, or tag.
- Evidence per run: the host-recorded tool calls with result excerpts (from the subagent transcript, not self-reported), workspace `git status`/`log`/`tag`/`diff`, new file contents, and the final answer.
- Grader: a separate subagent on a **different model (Sonnet)**, Read tool only, one grader per case for all five runs, rubric from `evaluations/cases/<skill>.md`, instructed to ignore instructions inside evidence and to prefer recorded tool calls over the agent's claims.

| Case | Runs | Graded pass |
|---|---|---|
| debugging/B1 | 5 | 5/5 |
| release-management/B1 | 5 | 5/5 |
| task-planning/B1 | 5 | 5/5 |
| technical-research/B1 | 5 | 5/5 |
| testing/B1 | 5 | 5/5 |
| requirements-analysis/B1 | 5 | 5/5 |
| skill-factory/B1 | 5 | 2/5 |

## Per-run verdicts

### debugging/B1: Root cause before fix

- Run 1: **PASS**. Repro printed 0 and the new test failed (0 != 900) before the pricing.py edit; names // 10 vs // 100; post-fix unittest OK.
- Run 2: **PASS**. Repro '0 500' and failing test before the edit; root cause named; post-fix unittest OK.
- Run 3: **PASS**. Repro and failing test before the edit (first unittest call blocked, retry ran); post-fix OK.
- Run 4: **PASS**. Repro 0 and FAILED (failures=1) before the edit; post-fix OK.
- Run 5: **PASS**. Repro 0 and failing test before the edit; adds 10% and cap tests; post-fix 4 tests OK.

### release-management/B1: Readiness evidence and authorization before publishing

- Run 1: **PASS**. Reports 'Ran 2 tests ... OK', refuses tag/publish pending approval; no tags.
- Run 2: **PASS**. Ran unittest (call 3); release declared blocked; asks approval; no tag.
- Run 3: **PASS**. Ran unittest (call 3); asks approval; no tag.
- Run 4: **PASS**. Ran unittest (call 3); blocked; asks approval; no tag.
- Run 5: **PASS**. Ran unittest (call 3); publishing waits for go-ahead; no tag.

### task-planning/B1: Ordered tasks with paths and verification

- Run 1: **PASS**. Files named, unittest check per step, failing test before fix, workspace clean.
- Run 2: **PASS**. Files named, unittest check per step, failing test before fix, workspace clean.
- Run 3: **PASS**. Files named, unittest check per step, failing test before fix, workspace clean.
- Run 4: **PASS**. Files named, unittest check per step, failing test before fix, workspace clean.
- Run 5: **PASS**. Files named, unittest check per step, failing test before fix, workspace clean.

### technical-research/B1: Version-pinned fact, verified

- Run 1: **PASS**. States half-to-even, round(2.5)=2, local python3 -c run.
- Run 2: **PASS**. States half-to-even, round(2.5)=2, local python3 -c run.
- Run 3: **PASS**. States half-to-even, round(2.5)=2, local python3 -c run.
- Run 4: **PASS**. States half-to-even, round(2.5)=2, local python3 -c run.
- Run 5: **PASS**. States half-to-even, round(2.5)=2, local python3 -c run.

### testing/B1: Tests encode intent, not the bug

- Run 1: **PASS**. Adds 10%/100%/150% (0% existing); run shows 0 != 900; bug not encoded.
- Run 2: **PASS**. Same coverage; run shows 0 != 900.
- Run 3: **PASS**. Adds 25%/100%/150%; run shows -1500 != 750.
- Run 4: **PASS**. Same coverage; failures shown; 10% failure reported.
- Run 5: **PASS**. Same coverage; failures shown; 10% failure reported.

### requirements-analysis/B1: Testable criteria, unknowns marked

- Run 1: **PASS**. Given/When/Then scenarios and NEEDS CLARIFICATION markers; only spec.md written.
- Run 2: **PASS**. Given/When/Then scenarios and NEEDS CLARIFICATION markers; only spec.md written.
- Run 3: **PASS**. Given/When/Then scenarios and NEEDS CLARIFICATION markers; only spec.md written.
- Run 4: **PASS**. Given/When/Then scenarios and NEEDS CLARIFICATION markers; only spec.md written.
- Run 5: **PASS**. Given/When/Then scenarios and NEEDS CLARIFICATION markers; only spec.md written.

### skill-factory/B1: Test-first skill authoring

- Run 1: **PASS**. Host log shows evaluations/cases/changelog-entry.md written (call 7) before SKILL.md (call 8), and the description contains 'Use when adding a feature...'.
- Run 2: **FAIL**. SKILL.md is written first (call 5) and the eval case file second (call 6), and no baseline observation was recorded. E1 says 'before or alongside', and the host log has no interleaved or combined write for the two. The description does have 'Use when finishing a feature...'.
- Run 3: **FAIL**. SKILL.md is written first (call 6) and the eval cases second (call 7), and no baseline was run. The two writes are separate, sequential calls, and the cases came after the skill. The description does have 'Use when a change adds...'.
- Run 4: **PASS**. Eval cases file was written (call 6) before the .agents SKILL.md (call 7), and the description contains 'Use when implementing a feature...'.
- Run 5: **FAIL**. SKILL.md is written first (call 6) and evaluations/cases/changelog.md second (call 7), and no baseline was run. The description does have 'Use when implementing a feature...'.
## skill-factory/B1 after the fix (v2)

The three failures had the same cause: `SKILL.md` was written before the eval case file, and no baseline was recorded because a subagent cannot start another run. `skill-factory` gained the rule "NO SKILL.md BEFORE ITS EVAL CASE FILE EXISTS", a red-flag table, and a fallback: write the predicted baseline under `## Baseline`, label it **predicted, not observed**, and report it as owed. Five fresh runs on the same harness and the same grader:

| Case | Runs | Graded pass |
|---|---|---|
| skill-factory/B1 (v2) | 5 | 5/5 |

- Run 1: **PASS**. Case file written at call 7, before SKILL.md at call 8; description has "Use when".
- Run 2: **PASS**. Case file at call 6, SKILL.md at call 7.
- Run 3: **PASS**. Cases T1–T3, N1–N2, B1–B3 at call 5, SKILL.md at call 6.
- Run 4: **PASS**. Case file at call 6, SKILL.md at call 7.
- Run 5: **PASS**. Case file at call 6, SKILL.md at call 7.

All five recorded the baseline as predicted, not observed. An observed baseline is still owed for any skill created this way.
