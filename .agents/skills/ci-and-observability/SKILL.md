---
name: ci-and-observability
description: >
  Set up or change CI pipelines and the logs, metrics, traces, and alerts that
  show whether software works in production. Use when adding or editing a CI
  workflow (GitHub Actions, GitLab CI, and similar), making CI faster or more
  reliable, adding logging, metrics, tracing, health checks, or alerts, or when
  a change needs to be observable before rollout.
---

# CI and Observability

## Purpose

Make every change checked automatically before merge, and make running software tell you when it breaks. A pipeline that can be skipped and a service that fails silently both hide defects.

## When to use / avoid

Use it to create or change pipelines and instrumentation. A test that fails in CI is a defect: use [debugging](../debugging/SKILL.md). Release steps and rollout gates belong to [release-management](../release-management/SKILL.md).

## Procedure: CI

1. **Read what exists.** List pipeline files (`.github/workflows/`, `.gitlab-ci.yml`, `Jenkinsfile`, `azure-pipelines.yml`) and the project's real commands from manifests. Reuse the repository's commands; do not invent new ones.
2. **Order checks cheapest first:** format and lint, type check, unit tests, build, then integration and end-to-end. Fail fast.
3. **Make it reproducible and bounded:** set a timeout on every job (`timeout-minutes` in GitHub Actions), pin tool and action versions, use the lockfile install (`npm ci`, `pip install -r` with hashes, `go mod download`), and cache dependencies by lockfile hash.
4. **Keep secrets out:** use the platform's secret store, give jobs the least permissions (`permissions:` in GitHub Actions), and never echo secrets. Workflows triggered by forks get no secrets.
5. **Never lower the bar to go green:** no `continue-on-error` on required checks, no skipped tests, no `|| true`. See [quality-constraints](../quality-constraints/SKILL.md).
6. **Validate the file** before claiming it works: the platform's linter if installed (`actionlint`), a local runner if available, or a real run on a branch. Report which one ran.

## Procedure: observability

1. **Pick the signals for the change:** what would tell an on-call engineer that this feature is broken, slow, or misused?
2. **Logs:** structured (key-value or JSON), one event per meaningful outcome, with a request or correlation ID. Never log secrets, tokens, or personal data.
3. **Metrics:** for request paths, rate, errors, and duration (RED); for resources, utilization, saturation, and errors (USE). Keep label cardinality bounded (no user IDs as labels).
4. **Traces:** propagate context across service calls when the project already uses tracing (OpenTelemetry or similar); add spans at I/O boundaries.
5. **Health and alerts:** a liveness and a readiness check where the platform uses them. Alerts on symptoms users feel (error rate, latency), each with a runbook link (see [project-documentation](../project-documentation/SKILL.md)).
6. **Verify:** trigger the path locally or in a test and show the log line, metric, or span it emits.

Patterns and examples: [pipelines and signals](references/pipelines-and-signals.md).

## Outputs and gate

The pipeline or instrumentation change, and evidence that it ran: a pipeline run link or local runner output, and the emitted signal. Gate: required checks cannot be bypassed, no secret is exposed, and every new alert has a runbook. An unrun pipeline is reported as unverified.
