---
description: Independent read-only review of the current diff, a branch, or a PR
argument-hint: [branch, PR, or path; default is the uncommitted diff]
disable-model-invocation: true
---

Use the `code-review` skill on: $ARGUMENTS

If no target was given, review the uncommitted diff (`git diff HEAD`).

Run the review in the `reviewer` subagent with a constructed brief. If the diff touches authentication, authorization, input parsing, secrets, or tenant data, also run the `security-reviewer` subagent. Report findings only; do not edit files.

Security pass rules (from the `security-audit` skill, guidance mode):

- Check each security candidate against the skill's precedents (`references/precedents.md`) before reporting it.
- Report a security finding only when, after an attempt to refute it, confidence that it is exploitable is at least 8/10. Score reachability from untrusted input (0-3), a concrete file:line trace past the strongest control (0-4), and the concrete impact (0-3).
- Below 8, list it under "Needs validation" with the exact unresolved fact and a safe owner check. Never drop it silently, and give it no severity.
- Severity for reported findings follows the skill's severity anchors unchanged.
