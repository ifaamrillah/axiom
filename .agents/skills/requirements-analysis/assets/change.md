---
status: proposed   # proposed | approved | implemented | archived
change: <change-id>
capabilities: [<capability>]
---

# Change: <one-line summary>

## Why

<problem or opportunity, 2-4 sentences>

## What changes

- <behavior change in plain words>

## Risks and migration

- <who or what relies on the old behavior; how they move>

## Deltas

Declare at least one delta below, or replace this section's body with one line: `Specs: none — <reason>` (no behavior change). Never invent a requirement to fill the format.

### Capability: <capability>

#### ADDED
- **FR-<next>**: System MUST <behavior>.
  - Scenario: Given <state>, When <action>, Then <observable result>.

#### MODIFIED
- **FR-<id>** (was: <old behavior in one line>): <full new requirement>.
  - Scenario: <full scenario set for this requirement>

#### REMOVED
- **FR-<id>**: <requirement>.
  - Reason: <why>
  - Migration: <what happens to users and data>

#### RENAMED
- **FR-<id>**: "<old name>" renamed "<new name>"; behavior unchanged.

## Clarifications

- <YYYY-MM-DD> Q: <question> → A: <answer> (affects FR-<id>)
