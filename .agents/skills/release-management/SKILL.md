---
name: release-management
description: Prepare a software change for release by checking versioning, changelog, builds, migrations, rollout, staging evidence, rollback readiness, and post-release verification. Use when the user asks to prepare or execute a release.
---

# Release Management

## Procedure

1. Confirm release scope, target environment, owner, and approval boundaries.
2. Inspect versioning, changelog, release conventions, CI, and deployment instructions.
3. Verify required tests, builds, security checks, migrations, and configuration.
4. Prepare release notes and identify breaking changes.
5. Check staging readiness, smoke tests, observability, rollback, and incident contacts.
6. Present a readiness report with blockers and evidence.
7. Obtain explicit approval before production deployment or publishing.
8. After authorized release, verify health and key user journeys; document evidence.
9. If health checks fail, follow the approved rollback/mitigation process and notify the user.

## Rule

Preparing a release is not authorization to deploy or publish.
