---
name: skill-evaluator
description: >
  Assess whether an agent skill triggers correctly, changes agent behavior as
  intended, and stays safe, portable, and context-efficient, using runnable eval
  cases and recorded runs. Use when reviewing a new or changed skill, deciding
  whether a skill is ready to leave Experimental status, or diagnosing from a
  session transcript why an agent session or eval run went wrong.
---

# Skill Evaluator

## Procedure

1. **Confirm intent.** Identify the intended user, triggers, non-triggers, and expected output. Map each critical rule in the skill to a case; a rule without a case is untested ([eval design](references/eval-design.md)).
2. **Static checks.** Run `python3 scripts/validate_repository.py` (frontmatter, size budget, trigger clause, references, links), `python3 scripts/run_evals.py --check` (case structure, description collisions), and `python3 scripts/run_evals.py --routing` (offline routing proxy).
3. **Trigger accuracy.** Run `python3 scripts/run_evals.py --host <host> --kind trigger --skill <name>`. Positive prompts must invoke the skill. Negative prompts must not, and should go to their owner.
4. **Behavior.** Run the behavior cases and grade every expectation and failure signal from the transcript. Compare against arms without the skill (no skills; one generic instruction) per case. Exclude invalid runs (incomplete, or any permission denial) from rates. Repeat runs (at least 3) and report rates, not single outcomes. Grade from tool calls and output, not from the agent's claims ([grading rubric](references/grading-rubric.md)).
5. **Review the text.** Check for contradictions, vague steps, missing failure handling, unsafe instructions, host-specific assumptions, and duplicated reference material.
6. **Context cost.** Check the `SKILL.md` size, the median tokens per behavior run, and which references the agent actually needed. To test whether a section earns its place, run a [variant eval](references/eval-design.md#variant-evals-does-a-section-earn-its-place).
7. **Diagnose sessions from transcripts.** When a real session or an eval run went wrong, read its transcript before blaming or editing a skill. Analyse it per dimension and cite a transcript location for every finding ([session diagnosis](references/session-diagnosis.md)).
8. **Report** a score per dimension (0-3 scale in the [grading rubric](references/grading-rubric.md)), with evidence: trigger precision and recall, behavior pass rate, clarity, safety, portability, and context cost. Add concrete edits and the hosts and models that remain untested.

## Gate

A skill leaves Experimental only when recorded runs on at least one host show its trigger and behavior cases passing. Fixtures are prompts, not evidence. Record actual runs in `evaluations/results/` with host, version, model, and date. Never report a dimension as passing without a recorded run or an explicit static check.

## References

- [Eval design](references/eval-design.md): open when cases are missing, weak, or unobservable; covers trigger and behavior case design, pressure cases, baselines, and repeats.
- [Grading rubric](references/grading-rubric.md): open when grading transcripts or writing the report; includes a graded transcript and a full report example.
- [Session diagnosis](references/session-diagnosis.md): open when asked why a session or run went wrong; covers the per-dimension analysis, evidence citation, cause attribution, and an output template.

See also the eval case format (`evaluations/cases/README.md` in the Axiom repository), evaluation guide (`evaluations/README.md` in the Axiom repository), and [skill factory](../skill-factory/SKILL.md).
