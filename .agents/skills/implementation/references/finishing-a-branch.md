# Finishing a Branch

Use this when implementation is done and the work must be checked, cleaned, and handed off as a commit, PR, or merge. Back to [SKILL.md](../SKILL.md).

## 1. Final checks on the current tree

Run on the exact tree you will hand off. Earlier green runs do not count after later edits.

- [ ] Full relevant test suite (or all affected packages in a monorepo).
- [ ] Type check, lint, and format check as CI runs them.
- [ ] Build (`npm run build`, `go build ./...`, `cargo build`, `./gradlew assemble`).
- [ ] Migrations apply and roll back locally, if any were added.
- [ ] Results compared with the baseline. New failures are yours until proven otherwise.

If anything fails, stop and fix or report. Do not offer to merge or open a PR on a red suite.

## 2. Diff review

```bash
git status --porcelain
git diff --stat <base>...HEAD
git diff <base>...HEAD
```

Look for:

| Look for | Action |
|---|---|
| Files outside the task scope | Revert or explain |
| Debug output (`console.log`, `print`, `dbg!`, `var_dump`) | Remove |
| Commented-out code, stray `TODO` | Remove or link a ticket |
| Secrets, tokens, `.env` files, personal data | Remove; rotate if already committed or pushed |
| Generated or build artifacts | Remove; check `.gitignore` |
| Lockfile changed without a manifest change | Explain or revert |
| Whitespace-only or formatting churn in untouched code | Revert |
| Tests skipped, deleted, or loosened; timeouts raised; snapshots regenerated; suppressions added | Restore, or list each as ASK with its justification ([gate integrity](../../code-review/references/gate-integrity.md)); an unjustified one blocks handoff |
| New `shortcut:` markers | Check each has a limit and an upgrade trigger |

Secret scan if the project has one (`gitleaks detect`, `trufflehog git file://.`), or at least `git diff <base>...HEAD | rg -i "api[_-]?key|secret|password|token"`.

## 3. Commit hygiene

- Follow the repository's commit style (`git log --oneline -20`).
- One logical change per commit. Conventional Commits example: `feat(checkout): apply percentage discount codes`.
- The message body says why, not a list of files.
- Do not rewrite history that others already pulled. Do not force-push without explicit user approval.
- Commit only when the user or workflow asked for commits.

## 4. Choose the integration path (user decides)

Integration is the user's decision. Present the options and wait:

1. Push the branch and open a pull request against the base branch.
2. Merge locally into the base branch (then re-run tests on the merged result).
3. Keep the branch as is.

Confirm the base branch before merging; merging into the wrong base is costly to undo. Discarding work happens only on an explicit user request, after listing exactly what will be deleted. Pushing, opening a PR, and merging are external or consequential actions: do them only with the user's authorization.

After a local merge, run the tests on the merged result. If they fail, stop and leave the branch in place.

## 5. Clean up

- Remove temporary files, scratch scripts, and local debug config.
- Remove worktrees you created only after the work has landed or the user chose to discard it. Never force-remove a worktree with uncommitted files; show the files and ask.
- Delete a merged local branch with `git branch -d` (safe delete), not `-D`.

## 6. PR description

Use the repository's PR template if one exists (`.github/pull_request_template.md`). Give the final text a pass with `writing-quality` in embedded mode. Otherwise:

```markdown
## Summary
Adds percentage discount codes to checkout. Valid codes reduce the order
total; unknown or expired codes return 422 INVALID_DISCOUNT.

## Why
Marketing campaign in March needs codes (TICKET-412).

## Changes
- New `discount_codes` table and migration (additive).
- `apply_discount` domain rule using integer cents.
- Optional `discount_code` field on `POST /checkout` (backward compatible).

## Verification
- `make test` -> 219 passed (baseline 212)
- `make lint`, `make typecheck` -> clean
- Migration up/down run locally on Postgres 15
- Not run: e2e suite (needs staging data)

## Merge danger
- Reversibility: two-way door. Flag off undoes the behavior; the additive
  migration can stay.
- Blast radius: data (new table in the shared database).
- Before: `curl -X POST /checkout -d '{"discount_code":"SPRING10"}'` ->
  `400 unknown field discount_code`
- After: same command -> `200 {"total_cents": 900}`; expired code -> `422 INVALID_DISCOUNT`

## Risk and rollout
Behind `CHECKOUT_DISCOUNTS` flag, default off. Rollback: turn flag off;
migration is additive and safe to leave.

## Notes for reviewers
Reused `DomainError` instead of a new error class (plan deviation).
Noticed, not changed: tax computed twice in checkout (TICKET-415).
```

Rules: list the commands actually run and their results; list what was not run; call out breaking changes, migrations, and new config; keep it short enough to read in two minutes.

The **Merge danger** section is required. It tells the person merging what they risk:

| Line | Write |
|---|---|
| Reversibility | `two-way door` when a revert or flag fully undoes the change; `one-way door` when it cannot be fully undone (data rewritten or deleted, a published API or package, messages sent to users, a destructive migration). Say what makes it one-way. |
| Blast radius | One word: `local` (this module's internals), `module` (callers in this codebase), `service` (other services or consumers), `data` (stored data or schemas), `users` (behavior users see). Pick the widest that applies. |
| Before / after | The commands that show the change, each with its decisive output line before and after. A test name alone is not evidence of behavior. |

A one-way door needs a sentence on how the change was rehearsed, and it is a reason to ask for review even on a small diff.

## 7. Handoff report

```
Branch: feat/checkout-discounts (3 commits, base main)
Checks on final tree: make test 219 passed; lint and typecheck clean
Integration: awaiting user choice (PR / merge / keep)
Deviations: 1 (reused DomainError)
Follow-ups: TICKET-415
Merge danger: two-way door; blast radius data
Not checked: e2e suite (needs staging data)
Risk: discount and tax interaction covered by unit tests only
```

The handoff ends with `Not checked:` and `Risk:`, as in the [report format](../SKILL.md#report-format).

Sources: adapted from obra/superpowers (MIT) `skills/finishing-a-development-branch/SKILL.md` and `skills/executing-plans/SKILL.md`, and general practice.
