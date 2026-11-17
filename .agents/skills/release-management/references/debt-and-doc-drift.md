# Debt Ledger and Doc Drift

Two readiness checks that look past the tests: the deliberate shortcuts the release carries, and the docs that still describe the old behavior. Back to [SKILL.md](../SKILL.md).

## Debt ledger

Implementation marks deliberate limits with a `shortcut:` comment that states the limit and when to upgrade (see [simplicity](../../implementation/references/simplicity.md)). At release time, list every marker so the team ships its debt knowingly.

1. Search the whole tree at the release commit, not only the diff. Markers from earlier releases still count.

   ```bash
   git grep -n "shortcut:" <release-commit> -- . ':!*.lock'
   ```

   If the project has no git, use `rg -n "shortcut:"` or `grep -rn "shortcut:" .`. Record the command and the hit count.
2. For each hit, record the location, the ceiling (the stated limit), and the upgrade trigger.
3. Mark a hit `no-trigger` when it has no upgrade trigger. Mark it `new` when it was added since the last release (`git diff <last-tag>..<release-commit> | grep '^+.*shortcut:'`).
4. Check each trigger against what you know about the release. A trigger already met (for example "upgrade above 10k rows" and production has 50k) is a blocker or an explicit owner decision.

```markdown
Debt ledger (`git grep -n "shortcut:" v1.4.0-rc1` -> 3 hits):
| Location | Ceiling | Upgrade trigger | Flag |
|---|---|---|---|
| app/export.py:41 | loads all rows into memory, fine below ~10k orders | exports exceed 10k orders | |
| app/search.py:88 | linear scan of tags | more than 200 tags per account | new |
| app/mail.py:12 | sends synchronously | — | no-trigger |
```

A `no-trigger` marker is not a release blocker by itself, but it goes in the report with an owner who will add the trigger. Zero hits is a valid result; write it with the command, not as an empty section.

## Doc drift

Docs that describe old behavior mislead users as much as a bug does.

1. List what the release changed that a reader can observe: public functions, CLI flags, config keys, endpoints, defaults, error messages, file formats, install or upgrade steps. Use the release diff (`git diff <last-tag>..<release-commit> --stat`, then the changed public files).
2. For each item, search the docs for the old name, value, or behavior:

   ```bash
   git grep -n -e "<old name>" -e "<old default>" -- README* docs/ '*.md' CHANGELOG*
   ```

3. Read each hit. Mark it **drift** when it still describes the old behavior, and **ok** when it describes the new one or is history (a past changelog entry is history, not drift).
4. Check the other direction: every item from step 1 is in the changelog entry for this release.
5. Before a GO, each drift item is either fixed in the release or recorded in the readiness report with an owner and a reason it can wait. An item neither fixed nor recorded blocks GO.

```markdown
Doc drift (3 changed interfaces checked):
- drift: README.md:52 still shows `--format csv` as the default; release changed it to `json`. Fixed in a1b2c3d.
- drift: docs/config.md:18 documents `RETRY_LIMIT=3`; release default is 5. Recorded: owner Dana, fix in 1.4.1.
- ok: CHANGELOG.md has entries for all 3 items.
```

"Docs updated" without the mapping from each change to the line that describes it is not evidence.

Sources: ideas from dietrichgebert/ponytail (shortcut ledger; MIT) and garrytan/gstack (doc drift at release; MIT), rewritten.
