---
description: Independent read-only review of the current diff, a branch, or a PR
argument-hint: [branch, PR, or path; default is the uncommitted diff]
disable-model-invocation: true
---

Use the `code-review` skill on: $ARGUMENTS

If no target was given, review the uncommitted diff (`git diff HEAD`).

Run the review in the `reviewer` subagent with a constructed brief. If the diff touches authentication, authorization, input parsing, secrets, or tenant data, also run the `security-reviewer` subagent. Report findings only; do not edit files.
