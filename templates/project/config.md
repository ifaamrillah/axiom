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

## Stage hooks

Run a named check or skill before or after a workflow stage. Each entry is `before_<stage>` or `after_<stage>`, then either `check` with a command or `skill` with a skill name, then `(mandatory)` or `(optional)`. The stage is a stage ID such as `07-implementation`, or the ID without its number (`implementation`).

- before_implementation: check `<command>` (mandatory)
- after_review: skill <skill-name> (optional)

A mandatory hook that fails or cannot run blocks the stage. An optional hook reports its outcome and does not block. A hook entry that cannot be parsed is reported, never skipped silently.

## Overrides

Project-specific deviations from Axiom defaults, each with a reason and a date. An override may tighten Axiom; it never loosens a kernel rule, a quality gate, or an approval.

- <YYYY-MM-DD> <override> — <reason>

## Skill overrides and workflow overlays

Longer customization lives in its own files, read when the skill or workflow activates:

- `.axiom/overrides/<skill>.md`: persistent facts, extra steps, and stricter rules for one skill.
- `.axiom/workflows/overlays/<workflow>.md`: add, remove, or replace stages of a canonical workflow without forking it.

Formats and rules are in the `axiom-orchestrator` skill's `references/customization.md`. Reports name the layer behind each rule or template: canonical, override, overlay, or config.
