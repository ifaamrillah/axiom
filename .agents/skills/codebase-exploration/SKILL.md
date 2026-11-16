---
name: codebase-exploration
description: Explore an unfamiliar or changed software repository to map its structure, stack, architecture, conventions, entry points, tests, runtime commands, dependencies, and technical risks. Use during onboarding, impact analysis, debugging, refactoring, and feature discovery.
---

# Codebase Exploration

## Purpose

Build an evidence-backed mental model of the relevant codebase without reading every file.

## Inputs

Repository root, user goal, existing project instructions, and any relevant project knowledge.

## Procedure

1. Read root and nested agent instructions relevant to the target paths.
2. Inspect top-level files, manifests, lockfiles, build configuration, and directory structure. On a large repository, size it and find hot spots first ([large codebases](references/large-codebases.md)).
3. Identify languages, frameworks, runtime versions, package managers, services, databases, and infrastructure from actual files.
4. Identify application entry points, major modules, dependency boundaries, and important data flows. Use the per-ecosystem map in [entry points](references/entry-points.md) (Node, Python, Go, Java/Spring, PHP/Laravel, Rails, mobile).
5. Locate tests, fixtures, CI workflows, linting, formatting, type checking, build scripts, and development commands.
6. Inspect the files directly related to the request and trace their callers, dependencies, and tests. Pick the recipe for the question type (where defined, who calls, data flow, config origin, history, tests, dead code) in [search recipes](references/search-recipes.md). Try naming variants; one grep is never enough.
7. Identify conventions from representative code, not assumptions.
8. Note security-sensitive boundaries, migrations, external integrations, and operational risks.
9. Reuse existing docs only after checking their source references and freshness.
10. Summarize findings with evidence and confidence, in the output format in [large codebases](references/large-codebases.md#output-format): answer, `path:line` evidence, flow, confidence, gaps, and unexamined areas.

## Outputs

- Repository map relevant to the task.
- Detected stack with source-file evidence.
- Architecture and module boundaries.
- Test/build/development commands confirmed from manifests or CI.
- Relevant files and dependency paths.
- Risks, unknowns, and stale documentation.

## Verification

Every material claim should cite a file path, command output, or observed behavior. Mark uncertain findings as unknown; do not infer missing implementation details.

## Failure handling

If repository access or tools are unavailable, state the limitation and continue only with evidence available. Never fabricate commands or stack versions.

## References

Open only the one you need:
- [Search recipes](references/search-recipes.md): when answering a specific "where / who / how / why" question.
- [Entry points](references/entry-points.md): when you do not yet know where the program starts for this stack.
- [Large codebases](references/large-codebases.md): when the repository is large or monorepo-shaped, and before writing the final report.
