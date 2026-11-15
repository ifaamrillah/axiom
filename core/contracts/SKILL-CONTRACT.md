# Skill Contract

## Purpose

Define the minimum quality and portability requirements for every canonical Axiom skill.

## Required structure

- A directory named in lowercase kebab-case.
- A `SKILL.md` file.
- YAML frontmatter containing standard `name` and `description` fields.
- `name` matches the directory name.
- Description explains the skill's purpose and when it should be used.

Optional directories include `references/`, `scripts/`, `assets/`, and `examples/`. Add them only when useful.

## Required instruction content

A skill must make clear:
1. Purpose and activation conditions.
2. Inputs and preconditions.
3. Actionable procedure and decision rules.
4. Expected outputs.
5. Verification or quality criteria.
6. Failure handling and limitations.

Delegation, integrations, and references are included when relevant.

## Portability

Do not require undocumented platform-specific metadata. Keep native tool names and host configuration in adapter guidance or clearly marked optional integration sections. Provide a fallback when optional capabilities are unavailable.

## Quality

Instructions must be actionable, non-contradictory, proportionate, safe, and context-efficient. Do not duplicate large reference documents in the main skill body. Do not claim that a skill executed a tool or test unless it did.

## Completion

A skill is ready when its structure validates, referenced files exist, activation is unambiguous, expected outputs are defined, and its evaluation cases pass or limitations are documented.
