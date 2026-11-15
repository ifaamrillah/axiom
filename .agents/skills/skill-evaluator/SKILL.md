---
name: skill-evaluator
description: >
  Assess whether an agent skill is discoverable, focused, actionable, safe,
  portable, and effective on representative scenarios. Use when reviewing a
  new or changed skill.
---

# Skill Evaluator

## Procedure

1. Confirm the skill's intended user, triggers, and expected output.
2. Check contract compliance, frontmatter, links, references, and tool assumptions.
3. Walk positive, negative, ambiguous, failure, and low-context scenarios from `evaluations/skills/`.
4. Score clarity, relevance, completeness, safety, portability, and context cost with evidence.
5. Recommend concrete edits and list untested hosts/models.

## Gate

Fixtures are evaluation prompts, not proof of model behavior. Record actual runs separately with host/model/date and outcome.

## References

See [evaluation guide](../../../evaluations/README.md), [fixtures](../../../evaluations/skills/), and [skill factory](../skill-factory/SKILL.md).
