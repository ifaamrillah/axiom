---
name: project-documentation
description: >
  Create or update concise engineering documentation from verified project
  evidence, with source and commit metadata so that staleness can be detected,
  and record observed agent pitfalls in the project's instructions. Use when a
  change alters setup, behavior, architecture, APIs, or operations, or when
  onboarding knowledge needs to be recorded or refreshed, or for a retro on
  agent mistakes after a session.
---

# Project Documentation

## Purpose

Turn verified engineering knowledge into maintainable, discoverable Markdown that says where it came from and when it was last true.

## When to use / avoid

Use it when a change alters setup, behavior, architecture, APIs, operations, or durable project knowledge. Avoid duplicating code comments, temporary task notes, or existing documentation that is still accurate. Do not generate per-file narrative docs for a whole codebase; they go stale quickly and cost context. Document boundaries, decisions, and workflows instead.

## Procedure

1. **Identify** the source of truth, the audience, and the document type. Use the decision table in [doc types](references/doc-types.md) (README, ADR, API reference, runbook, how-to, architecture, comment).
2. **Check freshness before editing** ([freshness rules](references/freshness.md)). For documents with `sources:` and `verified_at_commit:` metadata, see whether the listed sources changed since that commit (`git diff --stat <commit> -- <sources>`). Unchanged sources mean the content can be trusted and skipped. Changed sources mean the document needs review.
3. **Decide** whether to update, link, or add a focused section. Prefer a targeted update over a rewrite.
4. **Draft concise content:** prerequisites, steps, expected result, caveats. Cite paths and commands; label assumptions and version-sensitive guidance. Finish prose with a [writing-quality](../writing-quality/SKILL.md) pass in file mode. Follow the type's template: [README and how-to](references/doc-types.md), [ADR](references/adrs.md), [API docs](references/api-docs.md), [runbook](references/runbooks.md).
5. **Stamp metadata** on living documents:

   ```yaml
   ---
   status: active          # draft | active | stale | superseded
   sources: [src/billing/, docs/adr/0007-invoicing.md]
   verified_at_commit: <sha>
   verified_on: <YYYY-MM-DD>
   ---
   ```

6. **Record learnings; promote pitfalls** ([learnings](references/learnings.md)). When an agent made a concrete mistake in this repository, write or update a learning file in `.axiom/learnings/<yyyy-mm-dd>-<slug>.md` (trigger, lesson, evidence, confidence, scope, seen). Promote it to one line in the **Pitfalls** section of the project's [Axiom block](assets/agents-md-block.md) only when it was seen in at least 2 sessions or the user confirms it. Each Pitfalls line names the strongest enforcement that could prevent it (lint, type, script or check, test, doc) and proposes the stronger one. Remove lines whose cause is gone or whose enforcement landed.

   **Retro** (when asked, or at the end of a long multi-step session): list each mistake, correction, or repeated friction from the session with its evidence. For each, pick one outcome: a learning file (or a new `seen` date on an existing one), a promotion, a proposed skill or kernel change (`scope: global`; route it to [skill-factory](../skill-factory/SKILL.md)), a project fact to verify and record, or nothing. Propose; do not edit skills or the kernel without approval.
7. **Check** links and consistency with the implementation.

## Outputs and gate

A focused document or update with current metadata. Gate: no unsupported claims, links resolve, metadata matches what was verified, and the intended reader can follow the content.

## Failure handling

If behavior is unclear, record the unknown or verify it with a safe check. Do not fill gaps with guesses. If a document is stale and you cannot verify it now, set `status: stale` rather than leaving it marked as current.

## References

Open the one matching the document you are writing:
- [Doc types and README](references/doc-types.md): choosing a type; README, how-to, and comment rules.
- [ADRs](references/adrs.md): recording an expensive-to-reverse decision.
- [API docs](references/api-docs.md): changing a public endpoint, library function, CLI, or event.
- [Runbooks](references/runbooks.md): alerts, manual recovery, on-call steps.
- [Freshness rules](references/freshness.md): metadata, drift checks, stale marking.
- [Learnings](references/learnings.md): retro, learning files, promotion to Pitfalls, enforcement levels.

See also the document contract (`core/contracts/DOCUMENT-CONTRACT.md` in the Axiom repository) and the documentation standard (`core/standards/documentation.md` in the Axiom repository).
