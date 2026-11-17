# Project Customization

A project can adjust Axiom without forking skills or workflows. It uses three layers under `.axiom/`, all optional and all Markdown. Open this reference when any of these paths exist, or when the user asks to customize a skill or workflow.

| Layer | Path | Use it for |
|---|---|---|
| Skill override | `.axiom/overrides/<skill>.md` | Persistent project facts and extra steps for one skill |
| Workflow overlay | `.axiom/workflows/overlays/<workflow>.md` | Adding, removing, or replacing stages of a canonical workflow |
| Stage hooks | `## Stage hooks` in `.axiom/config.md` | Running a named check or skill before or after a stage |

## The tightening rule

Customization may tighten Axiom, never loosen it. An override, overlay, or hook can add steps, add checks, and narrow scope. It cannot:

- remove or weaken a kernel rule (evidence before claims, human control, reproduce before fixing, and the rest),
- skip or waive a quality gate, an approval, or a hard gate such as spec approval before build,
- turn a skipped stage into a passed one.

When an entry tries to loosen a rule or gate, do not apply that entry. Report it, quote it, and continue with the canonical behavior. Removing a stage through an overlay is allowed only when the stage is not a gate the workflow or project requires, and the stage is then recorded as Skipped with the overlay as the reason.

## Skill overrides

When a skill activates, check for `.axiom/overrides/<skill>.md` (the skill's `name`). If it exists, read it once and apply it on top of the skill. Suggested sections:

```markdown
# Override: <skill>

## Facts
- <persistent project fact this skill needs, e.g. "integration tests need `make db-up` first">

## Extra steps
- <when> : <step>   (e.g. "before the final report: run `make lint-docs`")

## Stricter rules
- <rule that tightens the skill, e.g. "every finding needs a file:line">
```

## Workflow overlays

When a workflow starts or resumes, check for `.axiom/workflows/overlays/<workflow-id>.md`. Apply its operations to the canonical stage list before recording stages in the workflow state. A stage ID is the stage file name without `.md` (`08-verification`), or the stage name as the workflow writes it when it has no stage files. Hooks may use the ID or the ID without its number (`before_implementation` matches `07-implementation`).

```markdown
# Overlay: feature-development

## Add
- after: 08-verification
  stage: Contract tests
  skill: testing
  required: true
  exit: consumer contract suite passes against the new API

## Replace
- stage: 12-delivery
  with: Internal release via `docs/runbooks/release.md`
  reason: <why>

## Remove
- stage: 03-design
  reason: backend-only service, no user interface
```

Record each applied operation as a decision in the workflow instance, so a later resume sees the same stage list.

## Stage hooks

Declare hooks in `.axiom/config.md` under `## Stage hooks`. Each entry names a stage, a timing, a check or skill, and whether it is mandatory:

```markdown
## Stage hooks
- before_implementation: check `make verify` (mandatory)
- after_review: skill security-audit (optional)
```

- `before_<stage>` runs on entering the stage; `after_<stage>` runs before the stage is marked Completed.
- A **mandatory** hook that fails or cannot run blocks the stage. Record Blocked or Failed with the evidence.
- An **optional** hook that fails or cannot run is reported with its outcome; it does not block.
- A hook result is evidence like any other check: name the command and its decisive output line.

## Read failures are reported, never skipped

If an override, overlay, or hook entry cannot be read or parsed (missing file named in config, unknown stage, unknown skill, malformed entry), stop applying that entry and report it:

```text
Customization problem: .axiom/workflows/overlays/feature-development.md "after: 08-verify" — no stage with that ID. Entry not applied; canonical stages used.
```

Continue with the canonical behavior for that entry. For a mandatory hook that cannot be parsed, treat the stage as Blocked until the user fixes or confirms it. Silently ignoring a project rule is a failure.

## Artifact inventory in reports

When a report, plan, or workflow state depends on customized behavior, name the layer that supplied each template or rule:

```text
Layers: stages = canonical + overlay (added "Contract tests"); task template = canonical;
extra step "make lint-docs" = override (project-documentation); hook before_implementation = config.
```

Use the names `canonical`, `override`, `overlay`, and `config`. A reviewer can then tell project rules from Axiom defaults without reading every file.

Sources: ideas from github/spec-kit (overlays, stage hooks; MIT) and bmad-code-org/BMAD-METHOD (per-skill overrides; ideas only), rewritten.
