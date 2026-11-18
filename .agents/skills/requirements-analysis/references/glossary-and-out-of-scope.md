# Glossary and Out-of-Scope Records

Two small project records keep decisions from being lost between sessions: the glossary holds decided terms, and out-of-scope records hold rejected concepts. Product discovery and requirements analysis both maintain them while they work, not in a cleanup pass at the end.

## Glossary

**Where:** the project's existing glossary if it has one (for example `docs/glossary.md`). Otherwise `.axiom/project/glossary.md`, with one table row per term (columns below).

**When to write:** at the moment a term is decided, in the same turn. A term is decided when the user confirms it, or when the spec commits to it.

- Add a new domain term with its meaning in this project and the source (user answer, file, or spec ID).
- Correct an existing entry when a decision changes it, and note the change in the Notes column.
- Record code-name mappings when code and product words differ (`Ledger` in code = "balance history" in the UI).

**Do not create a glossary** only to have one. Create it when a domain term was actually decided and no glossary exists. Standard programming terms do not belong in it.

**Using it:**

- Specs and briefs use the glossary term, not a synonym. One word for one thing.
- When the request, the code, or a draft uses a different word for a glossary term, or one word for two things, flag the conflict and ask which term wins. Do not pick one silently.
- When the user's word conflicts with an entry, ask before changing the entry.

Example entry:

| Term | Definition in this project | Evidence / source | Notes |
|---|---|---|---|
| Refund request | A customer's claim for money back on one delivered order line, reviewed by a support agent | Discovery Q3 (2026-11-17); spec FR-001 | Not a "return"; returns are out of scope |

## Out-of-scope records

**Where:** the project's existing folder for rejected ideas if it has one (for example `docs/out-of-scope/`). Otherwise `.axiom/out-of-scope/`. Use one short file per concept: `<concept>.md`, with a lowercase, hyphenated name.

**When to write:** when discovery returns a `kill` verdict, or when discovery or requirements reject a concept the user or the agent proposed (a non-goal that someone is likely to suggest again). Routine scope cuts that nobody will propose again stay in the brief's non-goals only.

**Before proposing a concept,** list the folder and read any matching record. If one exists, show it and ask what has changed since. Do not propose it again as if it were new.

Format:

```markdown
# Out of scope: auto-approved refunds

- Decision: rejected
- Date: 2026-11-17
- Decided by: <owner or role>
- Reason: finance requires a human approval on every refund; no fraud data exists to set a limit.
- What would change this: three months of refund data with a fraud rate below an agreed limit, and finance sign-off.
- Source: <link to the discovery brief or spec>
```

Keep each record under about ten lines. A record that becomes wrong is updated in place with a new date, not deleted.

Sources: idea from mattpocock/skills (glossary, out-of-scope records; MIT), rewritten.
