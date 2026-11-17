---
status: draft            # draft | active
updated: <YYYY-MM-DD>
verified_at_commit: <sha>
---

# Design System Master: <product>

Global source of truth for visual and interaction decisions. Save it as `.axiom/design/MASTER.md` in the consuming project. Page-specific deviations go in `.axiom/design/pages/<page>.md`; an override wins for its page only and never edits the master.

## Product and audience

Product type, audience, usage context, and brand personality (3 adjectives).

Surface mode, which sets how much visual ambition fits: **persuade** (marketing, landing), **operate** (dashboards, admin, forms), **read** (docs, articles), or **experience** (games, media). Pages may override it.

Product facts here come from the user or the repository only. Never invent claims such as customer counts, metrics, or testimonials; leave a placeholder and ask.

## Stack

Detected framework, styling system (Tailwind, CSS modules, …), and component library, with the evidence (file paths).

## Tokens

| Token | Value | Use |
|---|---|---|
| color.primary | | Primary actions |
| color.surface | | Backgrounds |
| color.text | | Body text (contrast vs surface: ≥ 4.5:1) |
| color.danger / success / warning | | Feedback |
| font.body / font.heading | | Typography pairing |
| space.scale | 4/8 px base | Spacing |
| radius / shadow | | Elevation |
| motion.duration | 150–300 ms | Transitions |

## Components and patterns

Buttons, inputs, cards, navigation, modals, toasts: the existing component path for each, and its rules.

## Accessibility commitments

WCAG level, focus style, reduced-motion behavior, and the minimum target size.

## Anti-patterns for this product

Styles and patterns to avoid, with the reason.

## Page overrides

| Page | File | Deviates in |
|---|---|---|
