# Contributing to Axiom

Thank you for helping improve Axiom.

## Contribution principles

- Prefer portable Agent Skills and Markdown over platform-specific formats.
- Keep canonical skills independent of a specific coding agent.
- Make workflows adaptive; do not require irrelevant stages.
- Include clear inputs, preconditions, outputs, failure behavior, and verification.
- Require evidence for quality claims.
- Keep context consumption proportional to task complexity.

## Before opening a change

1. Read [AGENTS.md](AGENTS.md), [the principles](core/PRINCIPLES.md), and the relevant contracts.
2. Search for an existing skill, workflow, template, or adapter before adding another.
3. Make the smallest coherent change.
4. Update references and evaluations affected by the change.
5. Run the repository validation scripts.

## Skills

A skill must follow the standard Agent Skills structure. Its `SKILL.md` frontmatter must contain `name` and `description`. Names must match the containing directory and use lowercase kebab-case. Keep core instructions concise; move optional detail into `references/`.

## Workflows

Workflow definitions use Markdown. Each stage must identify its purpose, skill or procedure, applicability, inputs, deliverables, dependencies, and exit criteria. Conditions must be explicit. Skipped stages must be recorded as skipped, not passed.

## Pull requests

Describe the problem, approach, affected skills/workflows/platforms, validation performed, and known limitations. Do not claim platform compatibility without testing or clearly label it as unverified.
