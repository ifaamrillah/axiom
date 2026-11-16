---
name: project-documentation
description: >
  Create or update concise engineering documentation from verified project
  evidence, with source and commit metadata so that staleness can be detected,
  and record observed agent pitfalls in the project's instructions. Use when a
  change alters setup, behavior, architecture, APIs, or operations, or when
  onboarding knowledge needs to be recorded or refreshed.
---

# Project Documentation

## Purpose

Turn verified engineering knowledge into maintainable, discoverable Markdown that says where it came from and when it was last true.

## When to use / avoid

Use it when a change alters setup, behavior, architecture, APIs, operations, or durable project knowledge. Avoid duplicating code comments, temporary task notes, or existing documentation that is still accurate. Do not generate per-file narrative docs for a whole codebase; they go stale quickly and cost context. Document boundaries, decisions, and workflows instead.

## Procedure

1. **Identify** the source of truth and the audience.
2. **Check freshness before editing.** For documents with `sources:` and `verified_at_commit:` metadata, see whether the listed sources changed since that commit (`git diff --stat <commit> -- <sources>`). Unchanged sources mean the content can be trusted and skipped. Changed sources mean the document needs review.
3. **Decide** whether to update, link, or add a focused section. Prefer a targeted update over a rewrite.
4. **Draft concise content:** prerequisites, steps, expected result, caveats. Cite paths and commands; label assumptions and version-sensitive guidance.
5. **Stamp metadata** on living documents:

   ```yaml
   ---
   status: active          # draft | active | stale | superseded
   sources: [src/billing/, docs/adr/0007-invoicing.md]
   verified_at_commit: <sha>
   verified_on: <YYYY-MM-DD>
   ---
   ```

6. **Record pitfalls.** When an agent made a concrete, repeatable mistake in this repository, add one line to the **Pitfalls** section of the project's [Axiom block](assets/agents-md-block.md): the date, what went wrong, and the rule that prevents it. Remove entries whose cause is gone.
7. **Check** links and consistency with the implementation.

## Outputs and gate

A focused document or update with current metadata. Gate: no unsupported claims, links resolve, metadata matches what was verified, and the intended reader can follow the content.

## Failure handling

If behavior is unclear, record the unknown or verify it with a safe check. Do not fill gaps with guesses. If a document is stale and you cannot verify it now, set `status: stale` rather than leaving it marked as current.

## References

See the document contract (`core/contracts/DOCUMENT-CONTRACT.md` in the Axiom repository) and the documentation standard (`core/standards/documentation.md` in the Axiom repository).
