# Phrasing and Editing Skills

Open this when you write or change wording in a skill, and before you add a line to fix an observed failure.

## Phrasing checklist

Status: these are observations reported by obra/superpowers from their skill work. Axiom has not measured them itself. Treat them as hypotheses to confirm with eval cases, not as results.

| # | Form | Reported effect | Example |
|---|---|---|---|
| 1 | Tripwire on a concrete token or situation | Works | "When the output contains `0 tests collected`, stop and report." |
| 2 | Recognition table (symptom → action) | Works | `ENOENT on .env` → "copy `.env.example`; do not create secrets" |
| 3 | Prohibition of one concrete act | Works | "Never run `git checkout <file>` on a file with uncommitted edits." |
| 4 | Prohibition about how to compose output | Tends to backfire | "Don't be verbose", "Don't over-explain" |
| 5 | Nuance clauses added to a recipe | Tend to weaken it | "Lead with the answer, unless context matters, in which case…" |

Check each line you add:

- [ ] It names a concrete trigger (token, file, command, moment), or it is a row in a symptom → action table.
- [ ] A prohibition forbids one observable act, not a style.
- [ ] A style goal is a positive recipe: "Answer in one sentence, then list the evidence" instead of "don't be verbose".
- [ ] The recipe has no "unless", "except when", or "where appropriate" clause. Handle the exception as its own tripwire, or drop it.

The repository validator prints an advisory warning for SKILL.md lines that look like composition prohibitions (form 4). The warning does not fail the build; rewrite the line as a recipe or keep it with a reason.

## Edit ladder

Work down the ladder. Stop at the first rung that fixes the observed failure.

1. **Fix below the skill.** If the failure comes from a missing project fact or tooling gap (wrong test command, missing script), record the fact in the project's instructions or fix the tooling. Do not teach around it in a skill.
2. **The section must earn its place.** Name the eval case or recorded failure that the new text fixes. No case, no text.
3. **Edit instead of append.** Change the line that failed. A new paragraph next to the old one leaves two rules that can disagree.
4. **Pick the right level.** Kernel: applies to every task in every session. Skill: applies when the skill is active. Reference: applies at one step, opened on demand. Put the rule at the lowest level that still reaches the moment it is needed.
5. **Write a rule, not a story.** "Run the baseline in a fresh session" beats a paragraph about the time a baseline leaked context. Evidence goes in the eval case or results, not the skill.

Sources: phrasing forms reported by obra/superpowers (MIT) from their skill-writing experience (not measured by Axiom); edit ladder is Axiom's own.
