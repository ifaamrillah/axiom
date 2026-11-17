# Change Proposals (Delta Specs)

Use this when behavior that already has a spec changes. A new spec describes a whole feature; a change proposal describes only the difference, so reviewers see what moves and the living spec stays the single source of truth.

## When to use

| Situation | Use |
|---|---|
| New feature, no spec exists | A full spec ([template](../assets/spec.md)) |
| Existing spec, behavior changes, is added, or is removed | A change proposal ([template](../assets/change.md)) |
| Brownfield code with no spec | Write a spec only for the slice you change, then use proposals from then on |

## Layout

```
.axiom/specs/<capability>/spec.md          living spec: current intended behavior
.axiom/changes/<change-id>/proposal.md     why, what, affected capabilities
.axiom/changes/<change-id>/delta.md        the requirement deltas below
.axiom/changes/archive/<YYYY-MM-DD>-<change-id>/   after the change ships
```

Plans and tasks for the change sit beside the proposal (`plan.md`, `tasks.md`). Reuse existing capability names; create a new capability only when no existing one fits.

## Delta operations

Group deltas by capability. Each requirement keeps its existing ID (`FR-003`); never renumber.

```markdown
## Capability: checkout

### ADDED
- **FR-012**: System MUST reject coupon codes after their expiry date.
  - Scenario: Given coupon "TEN" expired yesterday, When it is applied, Then the total is unchanged and the error "Coupon expired" is shown.

### MODIFIED
- **FR-004** (was: discount capped at 50%): System MUST cap a combined discount at 30% of the subtotal.
  - Scenario: …

### REMOVED
- **FR-007**: Guest checkout with a saved card.
  - Reason: card storage moved to accounts only.
  - Migration: guests are asked to sign in; saved guest cards are deleted after 30 days.

### RENAMED
- **FR-009** → **FR-009**: "Promo code" renamed "Coupon code"; behavior unchanged.
```

Rules:

- **MODIFIED copies the whole new requirement and its scenarios**, not only the changed words. A partial block silently drops the rest when it is merged.
- **REMOVED needs a reason and a migration** (what happens to users and data that relied on it).
- A delta with no ADDED, MODIFIED, REMOVED, or RENAMED entry is not a behavior change. Say so in the proposal and skip the delta file.
- New IDs continue after the highest ID in the living spec.

## Lifecycle

1. **Propose:** `proposal.md` (why, what changes, affected capabilities, risks) plus `delta.md`. Apply the normal procedure steps 3-8 to the delta: markers, clarification, scenarios, checklist.
2. **Approve:** the user or owner accepts the proposal before implementation.
3. **Implement and verify:** `spec-analysis` converge mode compares code to the delta. Removed requirements are checked in reverse: the old behavior must be gone.
4. **Archive:** merge each delta into the living spec (add, replace the whole block, delete, rename), move the change folder to `archive/` with the date, and record the commit. Ask before archiving if tasks remain open.

Two open changes that modify the same requirement conflict. Resolve which lands first before either is approved.

Sources: delta operations, archive-and-merge, and the full-block rule adapted from Fission-AI/OpenSpec (MIT); stable IDs and replan from BMAD-METHOD (ideas only); general practice.
