---
name: ui-ux-design
description: >
  Shape user-facing flows, states, accessibility, and visual decisions for a
  software change using a priority-ordered rule set with measurable checks and a
  persisted design-system master. Use when a feature changes screens, navigation,
  forms, components, layout, styling, motion, or user feedback, or when reviewing
  UI for usability and accessibility.
---

# UI/UX Design

## Purpose

Make interfaces usable, accessible, and consistent before and after implementation. Decide things in priority order: an accessible, usable plain screen beats a beautiful inaccessible one.

## When to use / avoid

Use it whenever a change affects how something looks, feels, moves, or is interacted with. Skip it for pure backend, infrastructure, or non-visual work.

## Procedure

1. **Detect, never assume, the stack.** Check `package.json` dependencies (react, next, vue, svelte, angular), `pubspec.yaml` (Flutter), `Package.swift` or `*.xcodeproj` (SwiftUI), `composer.json` (Laravel), and React Native markers. Ask if the stack is unclear and it matters. Then open the [stack notes](references/stack-notes.md) for that framework's UI rules and verification commands.
2. **Load the design system.** If `.axiom/design/MASTER.md` exists, it is the source of truth for tokens, components, and patterns. A page override (`.axiom/design/pages/<page>.md`) wins for that page only. If neither exists and the work is a new product or page, propose a master (see [design-system master](assets/master.md)). Choose style, palette, fonts, and tokens from the product type with the [visual language](references/visual-language.md) tables, and check every color pair's contrast.
3. **Map the flow and the states.** Cover the primary path and alternates, plus loading, empty, error, success, partial, and offline states, and the permission-denied state where relevant. Use the state matrices in [interaction patterns](references/interaction-patterns.md); for numbers, charts, or tables, pick forms with [data display](references/data-display.md).
4. **Apply the rules in priority order** from the [UI rules](references/ui-rules.md). Resolve CRITICAL and HIGH categories before styling details. Use its accessibility thresholds table for exact numbers and its anti-pattern table when reviewing existing UI.
5. **Reuse established components and patterns.** Document any deviation and why.
6. **Specify** using the [design brief](assets/brief.md): flows, a state inventory, responsive behavior, accessibility notes, and mockups where useful.
7. **Verify the rendered result** when browser tooling is available ([e2e-testing](../e2e-testing/SKILL.md)): screenshots at mobile and desktop widths, keyboard pass, contrast and accessibility scan. Run the [pre-delivery checklist](references/ui-rules.md#pre-delivery-checklist). Label unverified visual claims.

## Outputs and gate

Flow notes, a state inventory, a design spec or mockups, and an updated master or override when design decisions change. Gate: all CRITICAL rules pass or carry an approved exception, every state is specified, and visual checks are either evidenced or labeled unverified.

## Fallback

Without design or browser tooling, produce a textual interaction spec. Implement it with the repository's established patterns, and list the visual checks that a human must perform.

## References

- [UI rules, accessibility thresholds, anti-patterns, pre-delivery checklist](references/ui-rules.md): every task.
- [Visual language](references/visual-language.md): new product, page, or master; restyling; palette or font choice.
- [Interaction patterns](references/interaction-patterns.md): component and screen states, forms, feedback, motion, breakpoints, navigation.
- [Data display](references/data-display.md): charts, tables, dashboards.
- [Stack notes](references/stack-notes.md): framework-specific implementation and verification commands.
- [Design-system master template](assets/master.md), [design brief](assets/brief.md)
- Feature Development workflow (`workflows/feature-development/WORKFLOW.md` in the Axiom repository)
