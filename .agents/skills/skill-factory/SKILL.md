---
name: skill-factory
description: Create or improve an Agent Skill test-first, by observing how an agent fails without it, writing the smallest skill that fixes those failures, and closing loopholes until runnable eval cases pass. Use when creating, splitting, or refactoring skills for Axiom or a consuming project.
---

# Skill Factory

## Purpose

Writing a skill is test-driven development applied to instructions. If you have not seen an agent fail without the skill, you do not know whether the skill teaches the right thing.

| TDD | Skill creation |
|---|---|
| Test case | Eval case: a trigger prompt or a pressure scenario |
| Red | Baseline run without the skill shows the failure or rationalization |
| Green | Run with the skill shows compliance |
| Refactor | Close new loopholes and rerun |

## The rule

```
NO SKILL.md BEFORE ITS EVAL CASE FILE EXISTS
```

Create `evaluations/cases/<skill>.md` first, in its own write, and only then create `SKILL.md`. If the skill was drafted first, delete the draft, write the cases, then rewrite the skill against them.

## When to create a skill

Create one when a technique is non-obvious, recurs across projects, and needs judgment. Do not create one for one-off fixes, project-specific conventions (put those in the project's instructions file), or mechanical rules that a linter, test, or validator can enforce. Automate those instead.

Check existing skills first. Extending or composing beats a near-duplicate.

## Red flags

| Thought | Answer |
|---|---|
| "I'll write the skill first, then the cases" | The cases define what the skill must change. Write them first. |
| "I can't run a baseline here, so I'll skip it" | Record predicted failures, label them unobserved, and report the baseline as owed. |
| "The skill is obviously right" | Unobserved failures are guesses. Keep it Experimental. |

## Procedure

1. **Define the job.** State the recurring task, the user, the activation cases, the non-activation cases, and the expected output.
2. **Write eval cases first** in `evaluations/cases/<skill>.md`: at least 2 positive triggers, 1 negative with its owner, and 1 behavior case with observable expectations and failure signals. For a discipline skill, make at least one behavior case a pressure scenario that combines three or more pressures ([pressure testing](references/pressure-testing.md)). See the case format (`evaluations/cases/README.md` in the Axiom repository).
3. **Run the baseline (red).** Run the behavior case without the skill, or with the current version, in a fresh session or subagent. Record the exact failures and the rationalizations the agent used ("this is too simple to test"), verbatim. They become the rationalization catalog. If you cannot start a fresh run here, write the failures you predict under `## Baseline` in the case file, label them **predicted, not observed**, and say in your report that the baseline is still owed.
4. **Write the minimum skill (green):**
   - Frontmatter has only `name` (equal to the directory) and `description`. The description says what the skill does and contains a "Use when/for …" trigger clause with the words users actually type. Do not list the procedure's steps in the description; agents may follow the summary and skip the body ([triggers](references/triggers.md)).
   - The body has purpose, the rule (if a discipline skill), procedure, outputs and gate, failure handling, and references.
   - Address the recorded failures directly. For discipline skills, add a red-flag or rationalization table built from the baseline, and phrase the rule as a bright line ([persuasion principles](references/persuasion.md)). Match the fix to the failure kind: discipline failures need rules and counters; shape failures need templates and examples.
   - Keep `SKILL.md` under about 200 lines. Move depth to `references/`, linked from `SKILL.md` and read on demand.
   - Keep it portable. Host tool names and configuration belong in `adapters/`.
5. **Run with the skill.** Run the trigger cases and the behavior cases. Fix description wording when triggers miss, and fix body wording when behavior fails.
6. **Refactor.** Look for new rationalizations, add counters, and rerun. Remove instructions that no case needs. Before adding text, walk the edit ladder in [phrasing](references/phrasing.md): fix below the skill if you can, and edit the failing line instead of appending.
7. **Validate.** In the Axiom repository, run `python3 scripts/validate_repository.py` and `python3 scripts/run_evals.py --check`, and record runs in `evaluations/results/`. Elsewhere, use the project's equivalent checks and keep the records next to the cases.
8. **Label maturity honestly**: Experimental until recorded runs pass on at least one host.

## Writing rules

- Imperative, specific steps with checkable results. Avoid "consider" and "as appropriate" unless you define the condition.
- One term per concept across the skill and its references.
- Prefer a table of claim → required evidence over prose.
- Use examples to clarify, not to pad.
- Never let a skill claim that it ran a tool or test.
- Phrase rules as tripwires, symptom → action tables, or prohibitions of one concrete act. State a style goal as a positive recipe, not "don't be verbose" ([phrasing checklist](references/phrasing.md)).

## Outputs and gate

The skill directory, its eval cases, and recorded baseline and post-skill results. Gate: validator passes, eval case check passes, and recorded runs show the baseline failures fixed, or the limitation is documented.

## References

Open when you reach the matching step:
- [Triggers](references/triggers.md): writing or fixing the description; collisions with sibling skills (steps 4-5).
- [Pressure testing](references/pressure-testing.md): building scenarios, running the baseline, the rationalization catalog, closing loopholes (steps 2-3, 6).
- [Persuasion principles](references/persuasion.md): wording rules in discipline skills so they hold under pressure (step 4).
- [Phrasing and editing](references/phrasing.md): which rule forms hold, and the edit ladder for fixing a failure (steps 4, 6).
- Skill contract (`core/contracts/SKILL-CONTRACT.md` in the Axiom repository)
- Skill template (`templates/skills/SKILL.template.md` in the Axiom repository)
- [Skill evaluator](../skill-evaluator/SKILL.md)
- Eval runner (`scripts/run_evals.py` in the Axiom repository)
