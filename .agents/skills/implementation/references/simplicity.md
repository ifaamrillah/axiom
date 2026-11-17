# Simplicity

Use this before writing new code (procedure step 5.2) and when the user asks to simplify existing code.

## Decision ladder

Stop at the first rung that works.

| Rung | Question | If yes |
|---|---|---|
| 1 | Does this need to exist at all? Is the behavior already required by the spec? | If not required, do not build it. Say so. |
| 2 | Does the codebase already do this? Search for the helper, type, or pattern before writing one. | Reuse it. |
| 3 | Does the language's standard library or the platform do it? | Use it. |
| 4 | Does an installed dependency do it? Check the lockfile, not memory. | Use it. Do not add a new dependency for a few lines. |
| 5 | Is it one line or one expression? | Write the line. |
| 6 | Otherwise | Write the minimum code that meets the acceptance criteria and its test. |

Before writing, list every caller, test, fixture, and config entry the change must reach. A small change that misses a caller is not small; it is broken.

## Never cut

Minimalism never removes:

- validation and authorization at trust boundaries;
- handling that prevents data loss or corruption;
- security controls;
- accessibility (labels, keyboard access, contrast).

## Shortcut markers

When you take a deliberate shortcut that has a known limit, mark it in the code so it is a recorded decision, not a hidden defect:

```python
# shortcut: loads all rows into memory; fine below ~10k orders. Upgrade to streaming when exports exceed that.
```

Rules:

- Format: `shortcut: <the limit>. <when to upgrade>.` Both parts are required; a marker without an upgrade trigger is a TODO, and TODOs are findings.
- Use the comment syntax of the language. Keep the word `shortcut:` so `rg -n "shortcut:"` lists every one.
- Mention each new marker in the report under "Deviations" or "Follow-ups".
- Reviewers treat a marked shortcut whose limit is acceptable for the stated scope as a decision, not a finding (see `code-review`). An unmarked shortcut with the same limit is a finding.
- Never mark a "never cut" item as a shortcut.

## Simplifying existing code

When the task is "simplify this" or "clean this up":

1. Pin the current behavior first: run the existing tests, and add a characterization test where coverage is thin.
2. Remove one thing per step: dead branches, single-use wrappers, duplicated logic, options nobody passes. Run the tests after each step.
3. Do not change public interfaces, error messages, or persisted formats unless the task says so.
4. Report what was removed and the test command that proves behavior did not change.

For structural moves across modules, use the Refactoring workflow (`workflows/refactoring/WORKFLOW.md` in the Axiom repository).

Sources: decision ladder, never-cut list, and `shortcut:` markers adapted from dietrichgebert/ponytail (MIT); code simplification from addyosmani/agent-skills (MIT); general practice.
