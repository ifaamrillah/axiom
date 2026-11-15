# ADR-0001: Markdown and native orchestration

- **Status:** Accepted
- **Date:** 2026-11-15

## Context

Axiom must be portable across several agent hosts and easy to inspect and maintain without installing framework software.

## Decision

Use standard Agent Skills with portable `name` and `description` frontmatter, Markdown workflow definitions and state, native-first orchestration, and no custom runtime or CLI. Keep canonical skills under `.agents/skills/`; provide host-specific setup instructions as adapters.

## Consequences

People and host agents can read the source directly. CI may use optional maintainer scripts, but those scripts do not execute workflows or become user-facing tooling. Hosts differ; compatibility claims require direct evidence and adapters must explain fallbacks.
