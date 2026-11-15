# Stage 4: Requirements and acceptance

**Skill:** `requirements-analysis` · **Required:** yes · **Depends on:** stages 1–3 when applicable

## Do

1. Draft `spec.md` with prioritized stories, numbered requirements, and Given/When/Then scenarios.
2. Mark unknowns as `[NEEDS CLARIFICATION]`; run the clarification scan; ask at most 5 high-impact questions.
3. Test the requirements with the requirements-quality checklist.

## Approval gate (hard)

Nothing is built until the user or owner approves the spec (or a short design doc for smaller features). Approval covers what was shown. An idea the user said "sounds good" to is not an approved spec. Record the approval in the workflow state.

## Exit

All must-have requirements are testable, no clarification marker remains on a must-have, and the spec status is `approved`.
