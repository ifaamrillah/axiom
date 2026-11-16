# Dogfood: Axiom maintainer tooling (2026-11-16)

**Task:** review `scripts/run_evals.py`, `scripts/validate_repository.py`, and their tests after the eval-runner changes, using the `code-review` skill. A fresh subagent ran it as a read-only reviewer with six written acceptance criteria.

**Result:** "Changes required". The review produced 2 Major findings, 4 Minor findings, and 1 Note, each with evidence the reviewer produced itself:

- **Major:** the grader accepted non-boolean verdicts (`[1, 1]`, `"false"`) as a pass. The reviewer proved this with a stubbed reply.
- **Major:** `grade()`, the result writer, and the validator checks had no tests.
- **Minor:** a race in result-file naming; aliases ignored in the behavior summary; aliases not validated; image and reference-style links bypassed the self-containment check.
- Questions led to two more fixes: a budget-capped or usage-limited run could pass a negative trigger case, and the grader had no budget cap.

All findings were fixed in the same change, and tooling tests went from 9 to 17. The usage-limit question proved real later the same day: the account hit its limit mid-run, and the old runner had scored the limit reply as a completed run (see the invalid record annotated in `evaluations/results/`).

**What the skill changed:** spec-compliance-first review against explicit acceptance criteria surfaced AC3 (malformed grader replies) as "partially met", and "do the tests fail without the change" surfaced the missing tests. Without written criteria, the grader issue would have read as a style concern.

**Pitfalls recorded** in the repository's `AGENTS.md` came from mistakes made in this session, such as discarding unstaged work with `git checkout <file>` and misreading a case defect as a skill miss.
