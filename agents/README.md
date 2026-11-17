# Optional Agent Roles and Prompts

These role cards and prompt templates help frame bounded work when a host offers native delegation. They do not define agents, grant permissions, or require a multi-agent runtime. Follow the [delegation policy](../core/policies/parallel-execution.md) and the orchestrator's [delegation guidance](../.agents/skills/axiom-orchestrator/references/delegation.md).

## Roles

Each card declares portable metadata. Adapters map it to host specifics (model choice, tool permissions):

- **capability:** `deep` (complex reasoning, review, architecture), `standard` (implementation, testing), or `fast` (search, lookup, summarization).
- **writes:** `true` if the role may edit files; `false` for read-only roles.

The orchestrator's work categories (`quick`, `deep`, `visual`, `writing`) suggest tiers named `light`, `standard`, and `strong`, which equal `fast`, `standard`, and `deep` here. See [delegation](../.agents/skills/axiom-orchestrator/references/delegation.md#work-categories).

| Role | Capability | Writes |
|---|---|---|
| [architect](roles/architect.md) | deep | false |
| [planner](roles/planner.md) | deep | true (plan files only) |
| [engineer](roles/engineer.md) | standard | true |
| [qa-engineer](roles/qa-engineer.md) | standard | true (tests only) |
| [reviewer](roles/reviewer.md) | deep | false |
| [security-engineer](roles/security-engineer.md) | deep | false |
| [researcher](roles/researcher.md) | fast | false |

## Prompt templates

- [Implementer](prompts/implementer.md): one task, constructed brief (saved as `tasks/<n>-brief.md` in a workflow instance and dispatched by path), structured status report.
- [Task reviewer](prompts/task-reviewer.md): two stages, spec compliance then code quality.
- [Fix loop](prompts/fix-loop.md): bounded rounds for resolving review findings.

These prompts are the source. Copies ship under `.agents/skills/axiom-orchestrator/assets/prompts/` for skills-only installs. After editing a prompt, run `python3 scripts/validate_repository.py --sync`.

## Delegation patterns

[Sequential](delegation/sequential.md), [parallel](delegation/parallel.md), and [review](delegation/review.md).
