# Dogfood: private Laravel/Livewire application (2026-11-16)

**Project:** a private multi-tenant Laravel 13 + Livewire + Pest application with its own detailed agent instructions (an instructions file, a rules directory, ADRs, and documented gates). This is a copy of the project used with the owner's permission. Rules: local only, no push, no commit, no credentials.

**Agent:** a fresh subagent loaded the kernel and followed `project-onboarding`, then `tdd`, `verification-before-completion`, and a `code-review` self-review. The project's own rules took precedence.

## What happened

- **Onboarding:** found that PHP exists only in containers. The copy had no `.env`, and the running dev containers mounted a *different* checkout (the original repository). The agent then ran tests in a throwaway, network-less container against the copy, with the original's `vendor/` mounted read-only (identical lockfile).
- **Baseline:** the unit suite had 72 failures, all environmental (no database, no app key, no Vite manifest), recorded before any edit. Drift found: the project's rules say unit tests need no database, but 61 tests under `tests/Unit` do.
- **Task:** there were no failing or skipped tests and no provable defect, so the agent added a missing unit test for a pure service class (3 tests).
  - Each test was shown to fail against a temporary mutation of the production code. The code was then restored and the restore confirmed with `git status`.
  - The full unit suite afterward had the identical 72 failures, and 3 more tests passed.
- **Independently re-run by the maintainer session:** `Tests: 3 passed (7 assertions)`. The branch held one untracked test file, with no commits.

## Skill assessment

| Skill | Effect |
|---|---|
| Kernel | Helped. "Name the command and its decisive output line" led to a recorded baseline and a comparison of failure sets, instead of dismissing the failures as "pre-existing". |
| project-onboarding | Mixed. Separating declared from observed runtime led the agent to notice that the containers belonged to another checkout. Creating `.axiom/project/*` would have duplicated the project's richer docs, so it was skipped. The step-1 workflow path did not exist in a skills-only install. |
| tdd | Partly ceremony: the red step has no natural form for tests on existing code. The red flag "test passed on the first run" led to the mutation technique, which the skill did not name. |
| verification-before-completion | Helped. Gates relative to the baseline, and "Blocked, not Passed" for feature and end-to-end tests that could not run. |
| code-review | Helped. "Predict first" caught a false comment the agent had written itself; fixing it also removed warnings. A separate subagent was ceremony for one test file. |

**Conflicts with project rules (the project won):**
- The project's stricter gates (an approved plan before feature code, end-to-end tests per acceptance criterion) were not acknowledged by the kernel's proportionality section.
- A formatter hook rule (keep each import and its use in one edit) has no counterpart in Axiom.

## Axiom changes that followed

1. `project-onboarding`:
   - The workflow reference is optional when the Axiom repository is absent.
   - Link to existing project docs instead of duplicating them.
   - Check container mount sources before running tests.
2. `tdd`: a characterization-test section (red by temporary mutation, then restore and confirm).
3. Kernel: proportionality never skips a gate the project itself defines.
4. `code-review`: a self-review is acceptable for small diffs if it predicts first and is labeled.
5. Orchestrator and routing: workflow, core, and agents paths are labeled as Axiom-repository paths, with a fallback for skills-only installs.

## Not verified

- Feature, integration, and end-to-end tests: there were no database credentials, by instruction.
- Coverage.
- Parallel runs in the project's real container setup.
