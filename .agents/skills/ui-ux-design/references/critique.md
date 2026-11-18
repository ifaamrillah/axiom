# Critique and Audit

Use this when asked to critique, audit, or review existing UI. Critique judges whether the design works for its users. Audit checks it against measurable rules. Both report findings; neither edits code.

## Unanchored order

Judgment that sees tool output first copies it. Do the design assessment before you look at scanner results, screenshots from tests, or another reviewer's notes.

1. **Assess the design** from the code and the rendered page: hierarchy, flow, states, copy, consistency with the master. Write the findings down.
2. **Then gather evidence:** browser snapshots at fixed widths, an accessibility scan, console errors. Add new findings and mark which earlier findings the evidence confirmed or refuted.

When the host supports subagents, give each step to a separate one and merge in the coordinator. When you do both in one context, put this line at the top of the report: `Degraded: single-context critique (assessment may be anchored).`

## Rendered review phases

Run these in order when a browser is available ([e2e-testing](../../e2e-testing/SKILL.md)). Use the same widths every time so runs are comparable: 375, 768, 1280 px.

1. **Primary flow:** complete the main task with mouse, then with keyboard only.
2. **Responsive:** each width, no horizontal scroll, no hidden primary action.
3. **States:** loading, empty, error, success, long content, and slow network where relevant.
4. **Accessibility:** contrast, names, focus order, landmarks, reduced motion.
5. **Polish:** the [craft floor](craft-floor.md) Verify and Refuse lists.
6. **Robustness:** console errors, failed requests, layout shift.

Without a browser, label the report `Not rendered: static review only` and list the phases a human must run.

### Disposition

End every rendered review handoff with exactly one disposition from this list. Check the evidence first: the disposition depends on it.

1. **Evidence check.** Every required width has a screenshot or snapshot; none is blank, cropped to the wrong viewport, or of a different page or state.
2. Then pick one:

| Disposition | When |
|---|---|
| `recapture` | Evidence is missing, blank, or at the wrong viewport. Judge nothing else until it is fixed. |
| `rebuild` | The structure or flow is wrong (the primary flow cannot be completed as designed, or the cognitive-load checklist is critical); local fixes would not converge. |
| `fix` | Specific findings to correct; the structure holds. List them. |
| `ship` | No P0 or P1 findings and the evidence check passed. |

Write it as `Disposition: fix (3 findings)`. Do not invent other words such as "mostly good" or "ship with caveats".

## Heuristic scores (critique)

Score each of Nielsen's 10 usability heuristics from 0 to 4. Use `n/a` when a heuristic does not apply, and compute the total over the applicable ones only.

| Score | Meaning |
|---|---|
| 0 | Violated across the flow |
| 1 | Major problems |
| 2 | Works with friction |
| 3 | Minor issues |
| 4 | No issues found |

Heuristics: visibility of system status; match with the real world; user control and freedom; consistency and standards; error prevention; recognition over recall; flexibility and efficiency; minimal design; error recovery; help and documentation.

Report the total as a percentage of the applicable maximum. Every score below 3 needs at least one finding that explains it.

## Cognitive-load checklist

Check each item per view. Count the failures. **4 or more failures is a critical finding (P1)** for that view, even when each item alone is minor.

| ID | Check | Fails when |
|---|---|---|
| C1 | One primary action per view | Two or more equally prominent primary buttons |
| C2 | At most 7 visible choices per group | A menu, toolbar, or option group shows 8 or more at once |
| C3 | Consistent placement | The same action or control sits in different places across views |
| C4 | Progressive disclosure | Advanced or rare options are shown up front with the common ones |
| C5 | Labels over icons only | An icon without a visible text label for a non-universal action |
| C6 | Recognition over recall | The user must remember a value, code, or step from another screen |
| C7 | Defaults chosen | Fields that have a common answer start empty or unselected |
| C8 | Errors next to the cause | An error appears only at the top, in a toast, or far from its field |

Report it as `Cognitive load: 3/8 failed (C2, C5, C7)` in the report header.

## Severity

| Level | Meaning |
|---|---|
| P0 | Blocks the task or excludes a group of users (keyboard trap, unreadable text, broken primary flow) |
| P1 | Causes errors or abandonment for many users |
| P2 | Friction, inconsistency, or a craft-floor Refuse item |
| P3 | Polish |

## Report

```markdown
## UI critique: <screen or flow> (<commit>)
Mode: critique | audit · Rendered: yes (375/768/1280) | no
Heuristics: 29/36 (81%, 1 n/a) · Cognitive load: 2/8 failed (C2, C7)
Disposition: fix (2 findings)

### Findings
1. [P0] src/checkout/Pay.tsx:44 — pay button is a <div>; not keyboard operable. Evidence: Tab skips it at 1280 px. Fix: <button type="submit">.
2. [P2] R2 hero-metric template on the dashboard header (src/Home.tsx:12). Fix: show revenue with its period only.

### Not checked
- Dark mode; RTL layout.
```

Sources: unanchored two-step critique, degraded banner, heuristic scoring with `n/a`, and P0-P3 adapted from pbakaus/impeccable (Apache-2.0); fixed-viewport phased review from nextlevelbuilder/ui-ux-pro-max-skill (MIT); Nielsen's heuristics (public method).
