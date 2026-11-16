---
id: <SPEC-ID>
status: draft            # draft | clarified | approved | superseded
owner: <name or role>
updated: <YYYY-MM-DD>
---

# Feature Specification: <name>

<!--
Describe WHAT and WHY, not HOW. Mark every unknown inline as
[NEEDS CLARIFICATION: <specific question>] instead of guessing.
A spec with unresolved markers cannot move to `approved`; planning must not
start while must-have requirements carry markers.
-->

## Context and problem

## Goals

## Non-goals

## User stories (prioritized)

Each story is an independently testable slice. P1 alone should be a viable increment.

### US1 (P1): <title>

As a <actor>, I want <capability> so that <outcome>.

**Independent test:** <how this story can be verified on its own>

**Acceptance scenarios:**

1. **Given** <state>, **When** <action>, **Then** <observable result>.
2. **Given** …, **When** …, **Then** ….

### US2 (P2): <title>

…

## Functional requirements

- **FR-001**: System MUST <observable behavior>.
- **FR-002**: System MUST <behavior> [NEEDS CLARIFICATION: <question>].

## Non-functional requirements

Quantify where possible (latency p95, availability, limits, accessibility level).

- **NFR-001**: <measurable requirement>

## Key entities (if data is involved)

- **<Entity>**: <what it represents, key attributes, relationships>

## Edge cases and failure modes

- What happens when <boundary or failure>?

## Security and privacy

Actors and trust boundaries, sensitive data, authorization rules, abuse cases.

## Success criteria

Measurable, technology-agnostic outcomes (for example "users complete checkout in under 60 seconds").

## Assumptions

Reversible assumptions made instead of asking; each should be easy to revisit.

## Clarifications

Record each resolved question so it is not asked again.

- <YYYY-MM-DD> Q: <question> → A: <answer> (affects FR-002)

## Related design, architecture, and decisions
