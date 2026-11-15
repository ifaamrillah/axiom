# Axiom Project Configuration

Save as `.axiom/config.md` in the consuming project. Project-level defaults and persistent facts that adjust Axiom's behavior without forking skills. Skills and the orchestrator read this file when present. Everything here is optional, and absent keys use Axiom defaults.

## Persistent facts

Facts that every Axiom workflow in this project should keep in context. Prefer links to `.axiom/` documents over long text.

- <fact or link>

## Defaults

| Setting | Value | Options |
|---|---|---|
| Default execution mode | inline | inline · delegated (subagent per task) |
| Task review depth | two-stage | none · quick (spec only) · two-stage |
| Security review mode | guidance | guidance · full audit (only when requested) |
| Security audit profile | standard | quick · standard · deep |
| Clarification question budget | 5 | number per round |
| Discovery deep mode threshold | 0.8 | 0–1 |
| Fix-loop round limit | 3 | number |
| Workflow state location | `.axiom/workflows/active/` | path |

## Extra steps

Additional instructions to run at given points. Keep them short and verifiable.

- Before planning: <e.g. "check docs/runbooks/ for affected services">
- Before completion: <e.g. "run `make verify`">

## Overrides

Project-specific deviations from Axiom defaults, each with a reason and a date.

- <YYYY-MM-DD> <override> — <reason>
