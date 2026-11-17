# GitHub Actions Example

**Status: untested.** This is a documented example, not a verified integration. No workflow run has been recorded. Treat every flag and input as a claim to check against the current Claude Code and GitHub docs.

[axiom-review.example.yml](axiom-review.example.yml) runs Claude Code headless (`claude -p`) with the Axiom plugin loaded through `--plugin-dir`. It asks the `axiom:reviewer` and `axiom:security-reviewer` subagents to review a pull request and posts one comment with the result.

## Prompt-injection warning

The reviewer reads the pull request: code, comments, docs, and commit messages. Anyone who can open a pull request can write text that tries to steer the model. That text runs next to an API key and a token that can comment on the repository.

- Keep the `pull_request` trigger. Never use `pull_request_target` for this job: it runs with the base repository's secrets and write token against code the author controls.
- The example skips pull requests from forks. With `pull_request`, GitHub does not pass secrets to fork runs anyway, so the job would fail without the check.
- Run it only on pull requests from trusted authors. Branch protection and required reviews still decide what merges. The model's comment is advice, not a gate.
- The allowed tools are read-only (`Read`, `Grep`, `Glob`, `git diff`/`log`/`show`, and `Agent` for the subagents). Do not add `Write`, `Edit`, or a general `Bash` permission.

## Setup

1. Copy the file to `.github/workflows/axiom-review.yml` in the target repository.
2. Replace each `<pin-sha>` with the full 40-character commit SHA of the `actions/checkout` release you trust. Do not use a tag such as `v4`. Tags can move.
3. Set `AXIOM_REF` to an Axiom tag or commit, and `CLAUDE_CODE_VERSION` to an exact Claude Code version.
4. Add the API key as the repository secret `ANTHROPIC_API_KEY` (Settings, Secrets and variables, Actions). Never write a key into the workflow file.

## What the example does

- **Once per PR.** It triggers on `opened` and `ready_for_review`, not on each push. A concurrency group per PR number stops duplicate runs. Drafts are skipped.
- **Least privilege.** The workflow grants no permissions by default. The job gets `contents: read` and `pull-requests: write`, the minimum to read code and post a comment. Checkouts set `persist-credentials: false`.
- **No expression injection.** PR values reach the shell through `env:` variables, not `${{ }}` inside `run:`. The PR title and body are never used.

## Checks before relying on it

- The subagent spawning tool is named `Agent` in recent Claude Code versions. Confirm the name for the version you pin.
- Confirm that the plugin's skills, subagents, and kernel load in headless mode on the runner (see the [Claude Code adapter](../claude-code/INSTALL.md#verify)).
- Record the first run (command, version, outcome) before calling the integration verified.

Official references: [Claude Code headless mode](https://code.claude.com/docs/en/headless), [GitHub Actions security hardening](https://docs.github.com/en/actions/security-for-github-actions/security-guides/security-hardening-for-github-actions).
