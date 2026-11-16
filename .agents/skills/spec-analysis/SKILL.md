---
name: spec-analysis
description: Check a feature's spec, plan, and tasks for consistency, coverage gaps, ambiguity, and constitution conflicts (analyze mode, read-only), or compare them with the current code and append the remaining work as new tasks (converge mode, append-only). Use when asked whether spec, plan, and tasks are consistent, or "what's left to implement compared to the spec", after task planning and before implementation, or after implementation to find what is still unmet.
---

# Spec Analysis

## Purpose

Catch drift between intent (spec), approach (plan), work (tasks), and reality (code) before it becomes rework.

## Modes

| Mode | When | Writes |
|---|---|---|
| **Analyze** | After tasks exist, before implementation | Nothing. Produces a report only. |
| **Converge** | After an implementation pass | Appends one `## Convergence N` section to the task list; nothing else |

Default to **analyze**. Use **converge** only when the user asks what is left, or when the workflow's verification stage calls for it.

## Inputs

`spec.md`, the plan, the task list, the project constitution and constraints if present, and, for converge, the current code. If a required artifact is missing, stop and name the stage that produces it.

## Analyze procedure

1. **Load progressively.** Read requirement IDs, stories, and scenarios from the spec; architecture decisions and constraints from the plan; and IDs, descriptions, and file paths from the tasks. Do not read entire files when sections suffice.
2. **Build an inventory** that maps each requirement and scenario to the tasks that cover it.
3. **Run the detection passes.** Open [detection passes](references/detection-passes.md) for the inventory commands, real findings versus non-findings for each pass, and how to phrase a finding.
   - **Duplication:** near-identical requirements or tasks.
   - **Ambiguity:** unquantified adjectives, leftover `[NEEDS CLARIFICATION]`, TODO or TBD placeholders.
   - **Underspecification:** a requirement with no measurable outcome; a task with no file path or no verification.
   - **Constitution conflicts:** plan or task choices that violate a MUST principle.
   - **Coverage gaps:** requirements with no task; tasks that map to no requirement (scope creep).
   - **Inconsistency:** terminology drift, contradictory decisions, task order that violates dependencies.
4. **Assign severity:**
   - **Critical:** a constitution MUST violation, a must-have requirement with zero coverage, or a contradiction that blocks implementation.
   - **High:** a conflicting or ambiguous requirement affecting security, data, or a P1 story.
   - **Medium:** terminology drift, a missing non-functional task, or an underspecified edge case.
   - **Low:** wording and minor redundancy.
5. **Report** (format below), then recommend next actions. The [worked analysis](references/worked-analysis.md) shows a full report and why each severity was chosen. Critical findings mean returning to requirements or planning before implementation. Offer remediation edits, but do not apply them without approval.

## Converge procedure

1. Treat spec, plan, and tasks as the only source of intent, with the constitution as governing constraints.
2. Inspect the current code and tests for each requirement and scenario. Checked boxes are claims, not evidence. Classify each one as met, partial, missing, contradicts (code conflicts with intent), or unrequested (code with no requirement), with file evidence.
3. Append one section, `## Convergence N (YYYY-MM-DD)`, to the task list. It contains new tasks for the remaining work, each traced to its requirement ID and gap type, with file paths and verification. Number new tasks after the highest existing ID. Put contradictions and constitution violations first. An unrequested item becomes a review task; converge never deletes code. See the [convergence example](references/worked-analysis.md#converge-mode-after-an-implementation-pass).
4. **Never** edit the spec or plan, rewrite, renumber, reorder, or delete existing tasks, or change application code.
5. If everything is met, leave the task list byte-for-byte unchanged and report a clean result.

## Report format

```markdown
## Spec analysis: <feature> (<date>)
| ID | Pass | Severity | Location | Finding | Recommendation |
|---|---|---|---|---|---|
| A1 | Coverage | Critical | spec FR-004 | No task implements refund limits | Add a task after T012 |

Coverage: <n>/<m> requirements have ≥1 task. Unmapped tasks: <ids>.
Constitution: <conflicts or "none found">.
Next: <proceed | resolve critical findings first>.
```

## Rules

Analysis is read-only. Do not invent requirements; report a gap instead. Prefer specific locations to general advice. Limit the findings table to about 50 rows and summarize the overflow.

## References

- [Detection passes](references/detection-passes.md): open before running analyze mode.
- [Worked analysis and convergence](references/worked-analysis.md): open to check report shape, severity calls, or the append-only convergence format.
- [Requirements analysis](../requirements-analysis/SKILL.md), [task planning](../task-planning/SKILL.md), [quality constraints](../quality-constraints/SKILL.md)
