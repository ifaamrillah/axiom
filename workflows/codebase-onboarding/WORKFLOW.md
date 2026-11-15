# Codebase Onboarding Workflow

## Metadata

- ID: codebase-onboarding
- Version: 1.0.0
- Status: Experimental
- Scope: understand an existing repository and establish reliable project knowledge

## Purpose

Build a concise, evidence-backed model of a repository so future tasks can begin with relevant context rather than rediscovering the system.

## Triggers

- Axiom is introduced to an existing project.
- The agent is unfamiliar with the codebase.
- Existing project knowledge is absent, stale, or contradicted by major changes.
- The user explicitly requests a codebase or architecture overview.

Do not run full onboarding for a narrow task when current, verified project knowledge already answers the questions needed.

## Inputs and preconditions

- Repository root and read access.
- User-provided context, if any.
- Existing root/nested instructions.
- Permission to create or update `.axiom/` documentation.

## Execution strategy

Use targeted exploration. Do not read every file. Prioritize manifests, entry points, architecture boundaries, tests, CI, infrastructure, and paths relevant to the user's goals. Preserve existing project-authored docs.

## Stages

### 1. Instruction and repository discovery

- **Procedure:** inspect root and nested agent instructions, repository metadata, top-level structure, manifests, lockfiles, and major configuration.
- **Required:** Yes.
- **Dependencies:** none.
- **Outputs:** repository map and instruction inventory.
- **Exit criteria:** relevant instructions and major project boundaries are identified.

### 2. Technology analysis

- **Procedure:** identify languages, frameworks, runtimes, package managers, databases, infrastructure, and major dependencies from manifests/lockfiles and observed configuration.
- **Required:** Yes.
- **Dependencies:** stage 1.
- **Outputs:** `.axiom/project/tech-stack.md`.
- **Exit criteria:** versions and sources are recorded; declared and observed versions are distinguished.

### 3. Architecture exploration

- **Procedure:** trace entry points, important modules, data/control flows, persistence, external integrations, and dependency boundaries. Use the `codebase-exploration` skill.
- **Required:** Yes.
- **Dependencies:** stages 1 and 2.
- **Outputs:** `.axiom/project/architecture.md` and a scoped repository map.
- **Exit criteria:** architecture claims have source evidence and unknowns are explicit.

### 4. Development workflow analysis

- **Procedure:** inspect local scripts, CI, tests, lint/type checks, build, migrations, and release process. Never invent commands.
- **Required:** Yes.
- **Dependencies:** stages 1 and 2.
- **Outputs:** `.axiom/project/development-guide.md`.
- **Exit criteria:** documented commands are traceable to manifests, CI, or successfully executed commands.

### 5. Conventions and domain knowledge

- **Procedure:** inspect representative code and existing product/domain docs. Capture naming, structure, error handling, testing, accessibility, security, and business vocabulary as applicable.
- **Required:** Yes.
- **Dependencies:** stages 2 and 3.
- **Outputs:** `.axiom/project/conventions.md`, `.axiom/project/glossary.md`.
- **Exit criteria:** conventions reflect observed patterns; conflicting patterns are noted.

### 6. Project knowledge synthesis

- **Procedure:** use `project-onboarding` and relevant templates to create or selectively update the overview, stack, architecture, conventions, development guide, and glossary.
- **Required:** Yes.
- **Dependencies:** stages 2–5.
- **Outputs:** `.axiom/project/` knowledge set.
- **Exit criteria:** documents are concise, linked, sourced, and explicit about freshness.

### 7. Validation

- **Procedure:** verify important paths, links, commands, and claims where feasible. Identify unexamined areas and any drift against existing docs.
- **Required:** Yes.
- **Dependencies:** stage 6.
- **Outputs:** onboarding report and validation evidence.
- **Exit criteria:** no known broken references; unverifiable claims are marked; remaining gaps are listed.

### 8. Security baseline (conditional)

- **Condition:** the user requests security posture, the repository handles sensitive data/authentication, or onboarding reveals material risk.
- **Dependencies:** stages 1 and 3.
- **Outputs:** scoped security observations or a handoff to the Security Audit workflow.
- **Exit criteria:** the scope and evidence boundary are clear; a full audit is not implied.

### 9. Performance baseline (conditional)

- **Condition:** performance is a user concern or architecture suggests a measurable bottleneck.
- **Dependencies:** stages 1–3.
- **Outputs:** safe baseline measurements or a handoff to the Performance Audit workflow.
- **Exit criteria:** measurements are reproducible and bounded, or the limitation is recorded.

### 10. Technical research (conditional)

- **Condition:** a key technical fact is version-specific or absent from repository evidence.
- **Dependencies:** stage 2.
- **Outputs:** a concise research note with authoritative sources and version scope.
- **Exit criteria:** material external assumptions are verified or left explicitly unresolved.

## Parallelization

Independent exploration of separate subsystems may be delegated after instructions and scope are understood. Assign disjoint file areas and require evidence-based handoffs. Synthesize shared architecture and project knowledge with one owner.

## Recovery

Preserve completed documents. Resume from the earliest incomplete or invalid stage. Re-run only checks invalidated by new evidence. Never label unavailable checks as passed.

## Completion criteria

Stages 1–7 are complete, required project knowledge exists, evidence and uncertainty are recorded, and the user receives a concise onboarding report.

## State semantics

Record each stage as Pending, Ready, In Progress, Completed, Blocked, Failed, Skipped, or Cancelled. Record quality gates separately as Pending, Passed, Failed, Blocked, or Waived. A skipped stage is not a passed gate. A dependent stage may proceed after a skip only when its required inputs are independently satisfied. Use the shared [workflow state template](../../templates/workflows/workflow-state.md) when retaining state is useful.
