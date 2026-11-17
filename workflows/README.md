# Axiom Workflows

A workflow is a Markdown playbook for the host agent. It is not an executable DSL and does not run without an agent interpreting it.

## Available workflows

- [Codebase Onboarding](codebase-onboarding/WORKFLOW.md): establish trustworthy project knowledge.
- [Feature Development](feature-development/WORKFLOW.md): take a feature from discovery to verified delivery.

## Selection

Choose the smallest workflow that safely satisfies the request. A typo or isolated low-risk bug does not require full feature development. A security-sensitive or cross-cutting change may require additional review and gates.

## Runtime state

Create workflow instances in the consuming project's `.axiom/workflows/active/<WORKFLOW-ID>/`. Keep state, plan, tasks, decisions, and handoffs in Markdown. On completion, move or archive the instance under `.axiom/workflows/completed/` while preserving evidence.

## Project customization

A project adapts a workflow without forking it. `.axiom/workflows/overlays/<workflow>.md` adds, removes, or replaces stages; `## Stage hooks` in `.axiom/config.md` runs a named check or skill before or after a stage; `.axiom/overrides/<skill>.md` adds facts and steps to one skill. Customization may tighten a workflow, never loosen a kernel rule or gate, and an entry that cannot be read is reported, not skipped. See the orchestrator's [customization reference](../.agents/skills/axiom-orchestrator/references/customization.md).

## Checkpoints and resume

Write workflow state at stage boundaries: after research, after spec approval, after plan approval, and after each verified task. On resume, trust the state file, then the ledger and decisions, then Git, then the transcript, and report any conflict before acting. See the orchestrator's [context budget reference](../.agents/skills/axiom-orchestrator/references/context-budget.md).

## Stage semantics

- **Required:** execute unless the workflow is explicitly re-scoped with an authorized reason.
- **Conditional:** execute only when its written condition is met; otherwise mark Skipped with rationale.
- **Blocked:** cannot proceed because an input, dependency, permission, or environment is unavailable.
- **Completed:** work is done; it does not imply a gate passed.
- **Gate Passed:** criteria checked with evidence.

A dependent stage can proceed after a skipped dependency only when its required inputs are independently satisfied.
