# Learnings and Pitfalls

The learning loop turns observed agent mistakes into rules without filling the always-on instructions with one-off notes. A retro writes **learnings**. A learning that repeats or that the user confirms is **promoted** to one line in the project's Pitfalls list.

```
mistake observed → learning file (candidate) → seen again or user confirms → Pitfalls line + strongest enforcement
```

## Learning file

One file per learning: `.axiom/learnings/<yyyy-mm-dd>-<slug>.md`, dated by the first sighting. The slug names the situation (`2026-11-16-wrong-test-runner.md`).

```markdown
---
trigger: Running the test suite after editing billing code
lesson: Use `pnpm test` (vitest); `npm test` runs the legacy jest suite
evidence: 2026-11-16 session ran `npm test`; 0 tests collected for src/billing/. package.json "test:legacy".
confidence: medium        # low | medium | high
scope: project            # project | global
seen: [2026-11-16]
status: candidate         # candidate | promoted | retired
---
```

| Field | Rule |
|---|---|
| `trigger` | The concrete situation where the rule applies: a command, a file, a token, a moment. Not a mood. |
| `lesson` | One imperative rule. If you cannot write it as a rule, it is not a learning yet. |
| `evidence` | What happened and where: command, output line, path, commit. No evidence, no file. |
| `confidence` | `high`: cause verified. `medium`: cause likely. `low`: one sighting, cause unclear. |
| `scope` | `project`: true only in this repository. `global`: a skill or kernel rule may be wrong; route it to skill-factory. |
| `seen` | One date per session that hit it. Add a date; do not create a duplicate file. |

Before writing a new file, search `.axiom/learnings/` for the same trigger. A match gets a new `seen` date, not a second file.

## Promotion

Promote a learning to a Pitfalls line when either holds:

- `seen` has dates from at least 2 sessions, or
- the user confirms the lesson.

On promotion, set `status: promoted`, add the Pitfalls line, and propose the strongest enforcement that would make the line unnecessary. Remove the Pitfalls line once that enforcement exists, and set `status: retired`.

## Enforcement levels

Pick the strongest level that could prevent the mistake. Prefer proposing a stronger one over writing a stronger doc line.

| Level | Prevents by | Example |
|---|---|---|
| 1. Lint | Static rule fails on the bad pattern | ESLint `no-restricted-imports` for the legacy client |
| 2. Type | The bad call does not compile | Remove the deprecated overload |
| 3. Script or check | A repository check fails | Validator rejects a missing field |
| 4. Test | A test fails on the behavior | Regression test for the bug |
| 5. Doc | An agent reads a rule | Pitfalls line |

A Pitfalls line names its level: `(enforce: test, proposed)` or `(enforce: doc only)`. A doc-only line says why nothing stronger fits.

## Pitfalls line

```markdown
- 2026-11-16 Ran `npm test` (legacy jest) instead of `pnpm test` (vitest) → use `pnpm test` (enforce: script, proposed: remove "test:legacy")
```

Keep the Pitfalls list short: about 10 lines. Every line loads in every session. When it grows, retire lines whose enforcement landed or whose cause is gone before adding more.

## Red flags

| Thought | Do instead |
|---|---|
| "I'll add it to Pitfalls now, just in case" | Write a learning file; promote on a second sighting or user confirmation |
| "One more line in the instructions will fix it" | Propose a lint, type, check, or test first |
| "The lesson is that I should be more careful" | Not a rule. Name the trigger and the concrete act |
| Copying the session story into `evidence` | One line: what happened, where |

Sources: ideas from affaan-m/ECC (learnings with confidence; MIT) and Yeachan-Heo/oh-my-claudecode (enforcement ladder; MIT), rewritten; Axiom's own retro procedure.
