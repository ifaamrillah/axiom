---
description: Pre-merge GO / NO-GO check with verification, review, and a rollback plan (does not push or publish)
argument-hint: [branch or PR; default is the current branch]
disable-model-invocation: true
---

Decide whether this is ready to merge: $ARGUMENTS (if empty, the current branch). Do not push, tag, merge, deploy, or publish.

1. Record the base commit and the diff range.
2. In one turn, dispatch in parallel, read-only:
   - the `reviewer` subagent with the `code-review` skill;
   - the `security-reviewer` subagent, only if the diff crosses a trust boundary (auth, input parsing, secrets, tenant data, file or network access); otherwise record "security: skipped, no boundary touched";
   - the `researcher` subagent to list affected callers, migrations, config, and docs.
3. Meanwhile, apply `verification-before-completion` yourself: run the project's full checks and record each command with its decisive output line.
4. Merge the results:

```markdown
## Ship check: <branch> (<base>..<head>)
Verdict: GO | NO-GO
Checks: <command → result>, …
Blocking findings: <list or none>
Skipped: <what and why>
Rollback: <exact steps to revert, including migrations and flags>
```

Verdict is NO-GO if any check fails, any Blocking finding is open, or no rollback plan can be written. Skips are listed, never counted as passes.
