# Freshness Rules

A document is trustworthy only if a reader can tell when it was last true. Stamp living documents, check them before relying on them, and mark them stale when you cannot re-verify.

## Metadata

```yaml
---
status: active          # draft | active | stale | superseded
sources: [src/billing/, docs/adr/0007-invoicing.md]
verified_at_commit: 3f9c2e1
verified_on: 2026-11-16
---
```

| Field | Rule |
|---|---|
| `sources` | Files or directories whose change could make the document wrong. Specific paths beat `src/`. |
| `verified_at_commit` | The commit you checked the claims against, not the commit that adds the doc. |
| `verified_on` | Date of that check. |
| `status` | `stale` when sources changed and nobody re-verified; `superseded` with a pointer to the replacement. |

Which documents need it: project knowledge files, architecture, runbooks, how-to guides, development guides. Not needed: ADRs (they are dated records), changelogs, code comments.

## Check before trusting

```sh
git diff --stat <verified_at_commit> -- <sources...>
git log --oneline <verified_at_commit>..HEAD -- <sources...>
```

| Result | Action |
|---|---|
| No changes | Trust it. Skip re-reading the sources. |
| Changes in files the doc does not discuss | Spot-check, then update `verified_at_commit` |
| Changes in described behavior | Review the affected sections against code; update; restamp |
| Sources moved or deleted | Doc is likely wrong. Fix `sources`, re-verify, or mark `stale` |
| `verified_at_commit` not in history (rebased, squashed) | Treat as unverified; re-verify or mark `stale` |

## Quick drift checks

| Claim type | Check |
|---|---|
| Commands | Run them, or confirm they exist in `package.json`/Makefile/CI |
| Paths | `test -e <path>` for each path the doc names |
| Links | Resolve relative links; the repository validator may do this |
| Config keys | `rg -n '<KEY>'` in code and `.env.example` |
| Versions | Compare with manifests and lockfiles |
| API shapes | Compare with the schema, types, or generated spec |

A small script can check paths named in backticks:

```sh
rg -o '`[^`]+/[^`]+`' docs/architecture.md | tr -d '`' | sort -u | while read -r p; do
  [ -e "$p" ] || echo "missing: $p"
done
```

## When code changes

Update docs in the same change when it alters setup, commands, configuration, public APIs, architecture boundaries, or operations. If you cannot update a doc now, set `status: stale` and say why in the report. Never leave a known-wrong document marked `active`.

## Pitfall entries

The Pitfalls section of the project's [Axiom block](../assets/agents-md-block.md) gets one line per observed, repeatable agent mistake:

```markdown
- 2026-11-16: Ran `npm test` (jest, legacy) instead of `pnpm test` (vitest); suite is vitest since 3f9c2e1. Use `pnpm test`.
```

Remove an entry when its cause is gone (the legacy script was deleted). Do not add hypothetical pitfalls.

## Red flags

| Red flag | Do instead |
|---|---|
| Rewriting a whole doc to fix one section | Targeted edit; restamp |
| Restamping without checking | Restamp only what you verified |
| Doc says "currently" or "recently" with no date | Replace with a date or version |
| Two docs describe the same thing differently | Pick the source of truth; link the other to it |

Sources: adapted from addyosmani/agent-skills (MIT) documentation-and-adrs (drift detection), and general practice.
