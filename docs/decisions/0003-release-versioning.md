# ADR-0003: Use semantic version labels for releases

- **Status:** Accepted; refined by [ADR-0005](0005-versioning-and-upgrades.md)
- **Date:** 2026-11-15

## Context

The initial versioning policy was not specified, while a versioned changelog and release guidance are part of the repository foundation.

## Decision

Use semantic version labels (`MAJOR.MINOR.PATCH`) for tagged releases and maintain a top-level changelog with an Unreleased section. This is documentation guidance only; no release automation is introduced.

## Consequences

Breaking contract changes should increment MAJOR, backward-compatible additions MINOR, and corrections PATCH. The project owner can revise this policy before its first public release.
