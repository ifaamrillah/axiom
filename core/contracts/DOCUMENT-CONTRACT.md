# Document Contract

## Purpose

Keep project knowledge trustworthy, discoverable, and maintainable.

## Recommended metadata

For important living documents, record:
- ID or title
- Document type
- Lifecycle status: Draft, Active, Verified, Stale, Superseded, Archived
- Created and last-updated dates
- Owner, where useful
- Sources and related artifacts
- Last verification date and source revision/commit, where practical

Freshness is separate from lifecycle status. Freshness values: Current, Needs Review, Stale, Unknown.

Machine-checkable form, recommended for `.axiom/` documents:

```yaml
---
status: active
sources: [<paths or globs this document describes>]
verified_at_commit: <sha>
verified_on: <YYYY-MM-DD>
---
```

A document is **Current** when none of its `sources` changed since `verified_at_commit`, and **Needs Review** otherwise. This lets agents skip re-reading unchanged knowledge and target only the documents that drifted.

## Source-of-truth rules

- Source code and executable configuration are authoritative for implemented behavior.
- Approved specifications are authoritative for intended behavior.
- If implementation and specification differ, document the drift and seek the appropriate correction.
- Never invent evidence or mark unverified content as verified.

## Update strategy

Use targeted, change-driven updates. Update documents when behavior, architecture, dependencies, operations, conventions, risks, or decisions materially change. Avoid rewriting unrelated documents.
