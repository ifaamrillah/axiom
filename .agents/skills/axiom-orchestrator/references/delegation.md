# Delegation

Delegate only when the host provides native subagents and the tasks are independent, bounded, and worth the coordination cost. Otherwise work sequentially. Never claim that parallel work happened when it did not.

## Construct the brief

A subagent does not inherit the session. Give it exactly what it needs:

- the task text, acceptance criteria, and verification commands,
- the owned files (allowed / restricted / shared),
- the relevant interfaces, conventions, and constraints, quoted or linked,
- the expected output format (see [handoff template](../../../../templates/workflows/HANDOFF.md)).

Use the prompt templates in `agents/prompts/`: [implementer](../../../../agents/prompts/implementer.md), [task reviewer](../../../../agents/prompts/task-reviewer.md), and [fix loop](../../../../agents/prompts/fix-loop.md).

## Choose the role

Role cards in `agents/roles/` declare a capability tier (`deep`, `standard`, or `fast`) and whether the role writes files. Adapters map these to host-specific models and tool permissions. Reviewers, researchers, and auditors are read-only.

## Integrate

The coordinator owns integration, shared files, conflict resolution, and evidence checks. A subagent's success report is a claim. Inspect the diff and rerun the checks before accepting it.

## Avoid

- Personas that spawn other personas. Delegation is coordinator-to-worker only.
- Two writers on overlapping files.
- Delegating work whose result you need to understand anyway, when doing it inline is cheaper.
