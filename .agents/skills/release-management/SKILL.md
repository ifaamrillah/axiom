---
name: release-management
description: Prepare a software change for release by checking versioning, changelog, builds, migrations, rollout, staging evidence, rollback readiness, and post-release verification. Use when the user asks to prepare or execute a release.
---

# Release Management

## Purpose

Ship changes that are reversible, observable, and incremental. Preparing a release produces evidence and a plan. It is not authorization to deploy or publish.

## When to open the references

| Need | Open |
|---|---|
| Readiness checklist, semver decision, changelog, release notes | [readiness and versioning](references/readiness-and-versioning.md) |
| Migration and rollback plans, feature flags, staged rollout, monitoring, hotfixes | [rollout, rollback, and hotfix](references/rollout-and-rollback.md) |

## Procedure

1. **Confirm the release.** Scope (commits or PRs since the last tag), target environment, release owner, approver, and the boundaries of what you may do without asking.
2. **Learn the release mechanics.** Read the existing process before inventing one:
   - Version source: `package.json`, `pyproject.toml`, `Cargo.toml`, `gradle.properties`, a `VERSION` file, or git tags only.
   - Changelog style: `CHANGELOG.md` (Keep a Changelog), changesets (`.changeset/`), release-please, semantic-release, or GitHub Releases.
   - CI/CD: `.github/workflows/`, `.gitlab-ci.yml`, deploy scripts, `RELEASING.md`.
   - Last release: `git describe --tags --abbrev=0`, then `git log <tag>..HEAD --oneline`.
3. **Classify the changes** and decide the version bump with the semver table. Flag every breaking change, migration, new config, and dependency change.
4. **Verify readiness** with the checklist: tests, build, security scan, migrations rehearsed, config present, docs updated. Record each item as passed (with evidence), failed, or not checked. A skipped item is not a passed item.
5. **Prepare artifacts**: version bump, changelog entry, release notes, migration and rollback plan, rollout plan with go/no-go thresholds. Give release notes a final pass with [writing-quality](../writing-quality/SKILL.md) in embedded mode.
6. **Check operations**: staging deploy and smoke test, dashboards and alerts for the changed paths, on-call owner and contact, communication plan for users if behavior changes.
7. **Present a readiness report** (format below) with blockers first. Stop here unless the user authorizes the next step.
8. **On explicit approval**, execute the release with the project's own tooling. Tag and publish only what was approved.
9. **Verify after release**: health checks, error rate, latency, key user journeys, and logs, against the baseline, at each rollout stage.
10. **If health fails**, follow the approved rollback or mitigation plan, notify the user, and record what happened. Do not improvise a fix in production.

## Readiness report format

```
Release: v2.4.0 (minor) - 18 commits since v2.3.2
Target: production (EU, US), owner: <name>, approver: <name>

Blockers:
- [ ] Migration 0042 not rehearsed on production-sized data

Checks:
- [x] Unit + integration: `make test` -> 1,204 passed (CI run #8812)
- [x] Build: docker image sha256:ab12... built in CI
- [x] Dependency audit: `npm audit --audit-level=high` -> 0 high/critical
- [ ] E2E on staging: not run (staging down since 10:00)
Breaking changes: none
Migrations: 0042 adds column (expand phase); rollback = drop column
Flags: `new-invoices` default off; rollout 5% -> 25% -> 100%
Rollback: redeploy v2.3.2 image (< 5 min); flag off (< 1 min)
Monitoring: dashboard "billing-api"; alert on 5xx > 1% for 5 min
Decision needed: approve deploy after blocker is cleared?
```

## Red flags

| Red flag | Do instead |
|---|---|
| "Staging passed, ship to 100%" | Stage the rollout and watch metrics at each step. |
| No rollback plan, or rollback never tested | Write it and, where possible, dry-run it before release. |
| Migration and code change that cannot run side by side | Split into expand and contract releases. |
| Breaking change in a minor or patch version | Bump major, or make the change additive. |
| Changelog generated from commit titles with no editing | Rewrite entries for the reader; group by impact. |
| Release on Friday evening or before a holiday with no on-call | Move the release or confirm coverage. |
| Flag with no owner or removal date | Add both before release. |
| Deploying because "the user said prepare the release" | Preparation is not approval. Ask. |
| Claiming a check passed without its output | Record the command and result, or mark it not run. |

## Rules

- Preparing a release is not authorization to deploy or publish.
- Production deploys, tags pushed to shared remotes, package publishing, and user announcements each need explicit user approval.
- Never skip or weaken checks to make a release date.
- Record evidence for every claim in the readiness report.
