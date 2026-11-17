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
Heuristics: 29/36 (81%, 1 n/a)

### Findings
1. [P0] src/checkout/Pay.tsx:44 — pay button is a <div>; not keyboard operable. Evidence: Tab skips it at 1280 px. Fix: <button type="submit">.
2. [P2] R2 hero-metric template on the dashboard header (src/Home.tsx:12). Fix: show revenue with its period only.

### Not checked
- Dark mode; RTL layout.
```

Sources: unanchored two-step critique, degraded banner, heuristic scoring with `n/a`, and P0-P3 adapted from pbakaus/impeccable (Apache-2.0); fixed-viewport phased review from nextlevelbuilder/ui-ux-pro-max-skill (MIT); Nielsen's heuristics (public method).
