---
name: project-onboarding
description: Onboard an AI agent to an existing software repository by inspecting its instructions, stack, architecture, conventions, developer workflow, tests, risks, and documentation gaps, then creating or refreshing concise project knowledge. Use when Axiom is first introduced to a repository or when a major codebase change makes project knowledge unreliable.
---

# Project Onboarding

## Purpose

Establish a trustworthy project context so future engineering tasks do not repeatedly rediscover the same information.

## Inputs and preconditions

- Accessible repository root.
- Existing repository/agent instructions.
- User context, if supplied.
- Permission to create or update project documentation.

## Procedure

1. If the Axiom repository is available, read its onboarding workflow (`workflows/codebase-onboarding/WORKFLOW.md`). Otherwise this procedure is sufficient.
2. Choose the depth (quick, focused, or deep) from the [brownfield checklist](references/brownfield-checklist.md) and work through its items. Inspect root and relevant nested instructions, manifests, lockfiles, CI, source structure, tests, infrastructure, and documentation.
3. Use the `codebase-exploration` skill to map the system and gather evidence.
4. Detect stack and versions from manifests and lockfiles. Distinguish declared versions from observed runtime versions. Running containers or services may belong to a different checkout: check mount sources and working directories before running tests against them.
5. Trace architecture, entry points, core modules, data flows, external services, and persistence.
6. Identify development setup, commands, test layers, build and release process using scripts and CI evidence. Give every command an evidence level (verified, CI-evidenced, declared, unknown) as described in [verifying commands](references/verifying-commands.md).
7. Capture conventions and representative patterns. Avoid imposing generic conventions that conflict with the repository.
8. Record risks, unknowns, operational constraints, and security-sensitive areas.
9. If the project already documents these topics (its own instructions file, rules directory, or architecture docs), link to them instead of duplicating them. Otherwise create or selectively update the project knowledge files:
   - `.axiom/project/overview.md`
   - `.axiom/project/tech-stack.md`
   - `.axiom/project/architecture.md`
   - `.axiom/project/conventions.md`
   - `.axiom/project/development-guide.md`
   - `.axiom/project/glossary.md`

   Use the structure, module cards, and per-file rules in [knowledge files](references/knowledge-files.md). Compare your output with the [worked example](references/example-output.md) before finishing.
10. Validate links, commands, paths, and claims where practical. Mark unverified statements clearly.
11. Record onboarding state and evidence in `.axiom/workflows/` or a concise report.

## Outputs

A repository map and a concise, evidence-backed project knowledge set. Keep detail proportional to repository complexity.

## Quality gates

- Root/nested instructions inspected.
- Stack claims supported by manifests/lockfiles.
- Architecture claims supported by source structure and traced code.
- Test/development commands supported by manifests or CI.
- Unknowns and verification limits disclosed.
- No secrets copied into project documentation.

## Failure handling

Preserve existing user-authored documentation. If existing documentation conflicts with code, record drift and propose correction instead of silently overwriting. If the repository is too large for exhaustive exploration, scope the analysis and list unexamined areas.

## References

- [Brownfield checklist](references/brownfield-checklist.md): open at the start to pick depth and track coverage.
- [Knowledge files](references/knowledge-files.md): open before writing `.axiom/project/` files.
- [Verifying commands](references/verifying-commands.md): open before running or documenting any command.
- [Worked example](references/example-output.md): open to check the shape and evidence level of your output.
