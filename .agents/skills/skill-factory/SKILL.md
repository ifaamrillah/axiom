---
name: skill-factory
description: Design or improve an Agent Skill by defining its activation criteria, procedure, inputs, outputs, verification, references, and portability, then validating its structure and behavior. Use when creating or refactoring skills for Axiom or a consuming project.
---

# Skill Factory

## Procedure

1. Define the recurring task and the problem a reusable skill solves.
2. Identify activation and non-activation cases.
3. Define inputs, preconditions, procedure, decision rules, outputs, failure handling, and verification.
4. Check for overlap with existing skills; prefer extending or composing before creating duplicates.
5. Write standard Agent Skills frontmatter with `name` and `description`.
6. Keep portable instructions in `SKILL.md`; move optional detail to references.
7. Add examples and evaluation cases for important behaviors.
8. Validate name/path consistency, references, clarity, safety, and token efficiency.
9. Label maturity honestly and document limitations.

## Quality

A skill is not ready merely because its prose is plausible. It needs clear triggers, actionable steps, defined outputs, and evaluation evidence.
