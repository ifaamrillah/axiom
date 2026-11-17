# Readiness and Versioning

Use this for the release readiness checklist, the version decision, the changelog, and release notes. Back to [SKILL.md](../SKILL.md).

## Release readiness checklist

Mark every line as passed (with evidence), failed, not applicable (with reason), or not checked. Not checked is a gap, not a pass.

### Code and build

- [ ] All required CI checks green on the exact commit to release (link the run).
- [ ] Build artifact produced by CI, not a laptop. Record its digest or checksum.
- [ ] Version number set in every place the project stores it.
- [ ] No unresolved release-blocking issues or TODOs tagged for this release.

### Tests

- [ ] Unit and integration suites pass.
- [ ] E2E or smoke tests pass on staging with production-like config.
- [ ] Tests for the riskiest changes exist (name them).
- [ ] Upgrade path tested: previous version -> this version, with real-shaped data.

### Security and dependencies

- [ ] Dependency audit at high/critical: `npm audit --audit-level=high`, `pip-audit`, `cargo audit`, `govulncheck ./...`, `bundle audit`, `composer audit`, `osv-scanner -r .`.
- [ ] Secret scan clean (`gitleaks detect` or equivalent).
- [ ] New endpoints have authentication and authorization checks.
- [ ] License check for new dependencies, if the project tracks licenses.

### Data and config

- [ ] Migrations reviewed, backward compatible with the previous app version, and rehearsed on production-sized data (record duration).
- [ ] Backup taken or confirmed recent before destructive migrations.
- [ ] New config and secrets exist in every target environment.
- [ ] Feature flags created with correct defaults (usually off).

### Operations

- [ ] Health check endpoint covers new dependencies.
- [ ] Dashboards and alerts cover changed paths.
- [ ] Rollback plan written, with time-to-rollback per method.
- [ ] On-call owner named and available for the rollout window.
- [ ] Status page or user communication drafted if users will notice.

### Documentation

- [ ] Changelog entry written.
- [ ] Release notes written for the audience (users, operators, API consumers).
- [ ] Upgrade or migration guide for breaking changes.
- [ ] API docs and README updated: each changed interface mapped to its doc line; drift fixed or recorded ([doc drift](debt-and-doc-drift.md#doc-drift)).
- [ ] Debt ledger of `shortcut:` markers listed; `no-trigger` markers have an owner ([debt ledger](debt-and-doc-drift.md#debt-ledger)).

## Semver decision table

Semantic Versioning: `MAJOR.MINOR.PATCH`. The public API is whatever consumers can observe and depend on: functions, CLI flags, config keys, HTTP endpoints, event schemas, file formats.

| Change | Bump |
|---|---|
| Remove or rename a public function, endpoint, field, CLI flag, or config key | MAJOR |
| Change a type, default, or meaning of an existing public item | MAJOR |
| Make an optional input required; tighten validation that rejects previously valid input | MAJOR |
| Drop support for a runtime or platform version (for example Node 18) | MAJOR (most projects) |
| Add a new public function, endpoint, optional field, or flag | MINOR |
| Deprecate something (still works, warns) | MINOR |
| New feature behind a flag, off by default | MINOR |
| Bug fix that restores documented behavior | PATCH |
| Performance improvement with no behavior change | PATCH |
| Internal refactor, docs, tests, CI only | PATCH or no release |
| Dependency bump with no public effect | PATCH |
| Security fix | PATCH (MAJOR if the fix must break an API; say so loudly) |

Special cases:

- **`0.y.z`**: anything may change. By convention, breaking changes bump MINOR (`0.4.0` -> `0.5.0`) and others bump PATCH.
- **Pre-releases**: `2.0.0-rc.1`, `2.0.0-beta.3`. They sort before `2.0.0`.
- **Applications** (not libraries) often use date versions (`2026.03.1`) or build numbers. Follow what the project does.
- **Bug fix that someone relies on** (Hyrum's law): if the old behavior was widely used, treat the fix as breaking or provide an opt-out.

Conventional Commits mapping (when the project uses it): `fix:` -> PATCH, `feat:` -> MINOR, `!` after type or a `BREAKING CHANGE:` footer -> MAJOR.

Commands to see the range:

```bash
LAST=$(git describe --tags --abbrev=0)
git log "$LAST"..HEAD --oneline --no-merges
git log "$LAST"..HEAD --grep "BREAKING" -i --oneline
git diff "$LAST"..HEAD --stat -- migrations/ db/ "*.proto" openapi*.yaml
```

## Changelog rules

Use the project's existing format. If none exists, Keep a Changelog is a good default.

- Write for the reader of the release, not the author of the commit.
- Group by type: `Added`, `Changed`, `Deprecated`, `Removed`, `Fixed`, `Security`.
- Put breaking changes first and mark them clearly, with the migration step.
- One line per change, in the imperative or past tense, consistent within the file.
- Reference the PR or issue number.
- Leave out internal noise (refactors, CI tweaks, test changes) unless users feel them.
- Keep an `Unreleased` section at the top; move it under the version heading at release time with the date (ISO 8601).
- Never edit entries of past releases except to fix factual errors.

```markdown
## [2.4.0] - 2026-03-10

### Added
- Discount codes at checkout (#412).

### Changed
- Invoice PDFs now use the account's locale for dates (#398).

### Deprecated
- `GET /v1/invoices?page=` offset pagination; use `cursor` instead. Removal in 3.0.0 (#405).

### Fixed
- Order totals no longer round twice for JPY (#407).

### Security
- Bump `jsonwebtoken` to 9.0.2 to fix CVE-2022-23529 (#410).
```

Bad entries: "Fix bug", "Update deps", "Refactor service", "WIP", a pasted commit list.

## Release notes example

Release notes are for people deciding whether and how to upgrade. Changelog is the record; notes are the story.

```markdown
# Billing API 2.4.0

Released 2026-03-10.

## Highlights
- **Discount codes.** Send `discount_code` with `POST /checkout` to apply a
  percentage discount. Unknown or expired codes return 422 `INVALID_DISCOUNT`.

## Upgrade notes
- No breaking changes.
- Database migration `0042_add_discount_codes` adds one table. It runs in
  under a second and is safe while 2.3.x is still serving traffic.
- New optional setting `CHECKOUT_DISCOUNTS` (default `off`).

## Deprecations
- Offset pagination on `GET /v1/invoices` is deprecated. Responses now include
  `Deprecation` and `Sunset: 2026-09-01` headers. Switch to `cursor`.

## Fixes
- JPY totals are no longer rounded twice (#407).

## Security
- Updated `jsonwebtoken` to 9.0.2 (CVE-2022-23529).

Full changelog: v2.3.2...v2.4.0
```

Rules: lead with what users can do now; give every breaking change or deprecation an action and a date; state migration duration and compatibility; link the full changelog. For each upgrade note that changes data or a public contract, say whether a downgrade undoes it (two-way door) or not (one-way door), so operators know before they upgrade.

Sources: adapted from addyosmani/agent-skills (MIT) `skills/shipping-and-launch/SKILL.md`, and general practice (Semantic Versioning 2.0.0, Keep a Changelog, Conventional Commits).
