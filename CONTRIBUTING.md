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

A skill must follow the standard Agent Skills structure. Its `SKILL.md` frontmatter must contain `name` and `description`, and the description must include a "Use when …" trigger clause. Names must match the containing directory and use lowercase kebab-case. Keep `SKILL.md` under 250 lines and move optional detail into `references/`, linked from `SKILL.md`. Links inside a skill must stay within `.agents/skills/`, because skills-only installs copy nothing else. Bundle a template the skill fills under its `assets/` (register it in `BUNDLED_ASSETS` in `scripts/validate_repository.py` and refresh copies with `--sync`), or name other repository files as plain text.

Write skills test-first with the [skill-factory](.agents/skills/skill-factory/SKILL.md) skill: add [eval cases](evaluations/cases/README.md) in `evaluations/cases/<skill>.md`, record a baseline run, then write the skill and record the post-change run in `evaluations/results/`.

## Workflows

Workflow definitions use Markdown. Each stage must identify its purpose, skill or procedure, applicability, inputs, deliverables, dependencies, and exit criteria. Conditions must be explicit. Skipped stages must be recorded as skipped, not passed.

## Pull requests

Describe the problem, approach, affected skills/workflows/platforms, validation performed, and known limitations. Do not claim platform compatibility without testing or clearly label it as unverified.

Run `python3 scripts/validate_repository.py`, `python3 scripts/run_evals.py --check`, and `python3 -m unittest discover -s scripts/tests` before submitting when Python 3 is available. These check repository structure, links, JSON, and eval-case structure. They do not exercise agent behavior. Behavior evidence comes only from recorded runs (`scripts/run_evals.py --host …`), which spend model quota and are run by maintainers. Unrun fixtures are scenarios, not test results. Keep platform guidance dated and link official references when capability details may change.
