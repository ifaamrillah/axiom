---
name: skill-evaluator
description: >
  Assess whether an agent skill triggers correctly, changes agent behavior as
  intended, and stays safe, portable, and context-efficient, using runnable eval
  cases and recorded runs. Use when reviewing a new or changed skill or deciding
  whether a skill is ready to leave Experimental status.
---

# Skill Evaluator

## Procedure

1. **Confirm intent.** Identify the intended user, triggers, non-triggers, and expected output.
2. **Static checks.** Run `python3 scripts/validate_repository.py` (frontmatter, size budget, trigger clause, references, links) and `python3 scripts/run_evals.py --check` (case structure).
3. **Trigger accuracy.** Run `python3 scripts/run_evals.py --host <host> --kind trigger --skill <name>`. Positive prompts must invoke the skill. Negative prompts must not, and should go to their owner.
4. **Behavior.** Run the behavior cases and grade every expectation and failure signal from the transcript. Compare with the baseline (without the skill) when one is recorded.
5. **Review the text.** Check for contradictions, vague steps, missing failure handling, unsafe instructions, host-specific assumptions, and duplicated reference material.
6. **Context cost.** Check the `SKILL.md` line count and which references the agent actually needed.
7. **Report** a score per dimension, with evidence: trigger precision and recall, behavior pass rate, clarity, safety, portability, and context cost. Add concrete edits and the hosts and models that remain untested.

## Gate

A skill leaves Experimental only when recorded runs on at least one host show its trigger and behavior cases passing. Fixtures are prompts, not evidence. Record actual runs in `evaluations/results/` with host, version, model, and date. Never report a dimension as passing without a recorded run or an explicit static check.

## References

See the [eval case format](../../../evaluations/cases/README.md), [evaluation guide](../../../evaluations/README.md), and [skill factory](../skill-factory/SKILL.md).
