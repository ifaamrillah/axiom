# UI Rules (priority order)

Resolve the categories from top to bottom. Numbers are defaults; a project master may tighten them. Detail lives in sibling references:

- [Visual language](visual-language.md): style catalog, palettes, font pairings, tokens.
- [Interaction patterns](interaction-patterns.md): component states, screen states, forms, feedback, motion, responsive, navigation.
- [Data display](data-display.md): chart selection, tables, dashboards.
- [Stack notes](stack-notes.md): per-framework implementation and verification commands.

| Priority | Category | Impact | Must have | Avoid |
|---|---|---|---|---|
| 1 | Accessibility | CRITICAL | Text contrast ≥ 4.5:1 (≥ 3:1 for large text and UI components); visible focus; full keyboard operation; labels or `aria-label` on controls; alt text on meaningful images; `prefers-reduced-motion` respected | Removing focus rings; icon-only buttons without labels; color as the only signal |
| 2 | Touch and interaction | CRITICAL | Targets ≥ 44×44 px (≥ 24×24 px minimum with spacing); ≥ 8 px between targets; feedback within 100 ms; disabled and loading states | Hover-only affordances; instant unexplained state jumps |
| 3 | Performance | HIGH | Reserved space for media (CLS ≤ 0.1); lazy-loaded offscreen media; modern image formats; LCP ≤ 2.5 s, INP ≤ 200 ms on key pages | Layout shift from late content; blocking web fonts without fallback |
| 4 | Style consistency | HIGH | Matches the product type and the master; one icon set (SVG); semantic tokens | Mixing visual styles at random; emoji as UI icons; raw hex values in components |
| 5 | Layout and responsive | HIGH | Mobile-first breakpoints; viewport meta; readable line length (45–80 characters); no horizontal page scroll | Fixed-pixel containers; disabled zoom |
| 6 | Navigation | HIGH | Predictable back behavior; current location shown; deep links for shareable states; at most 5 items in a bottom nav | Broken back button; state lost on refresh |
| 7 | Typography and color | MEDIUM | Body ≥ 16 px; line height around 1.5; type scale from tokens; dark mode contrast checked separately | Body text < 12 px; gray-on-gray text |
| 8 | Forms and feedback | MEDIUM | Visible labels; inline errors next to the field, plus a summary for long forms; helper text; preserved input after errors | Placeholder-only labels; errors only at the top; clearing the form on error |
| 9 | Motion | MEDIUM | Motion conveys meaning; 150–300 ms for UI transitions; animate transform and opacity only | One duration for everything; animating width, height, or top |
| 10 | Charts and data | LOW | Legends, tooltips, accessible palettes, a table alternative for key data | Meaning carried by color alone |

## Accessibility thresholds (WCAG 2.2 AA unless noted)

| Check | Threshold | How to verify |
|---|---|---|
| Body text contrast | ≥ 4.5:1 | Contrast tool or axe; check light and dark themes separately |
| Large text (≥ 24 px, or ≥ 18.66 px bold) | ≥ 3:1 | Same |
| UI component edges, icons, chart marks, focus indicator | ≥ 3:1 against adjacent colors | Manual check of borders, icons, rings |
| Placeholder and disabled text | Placeholder ≥ 4.5:1 if it carries information; disabled is exempt but should stay legible | Manual |
| Focus indicator | Visible on every focusable element; ≥ 2 px thick; not hidden by sticky headers or overlays | Keyboard pass with Tab and Shift+Tab |
| Target size | ≥ 24×24 CSS px (AA minimum); 44×44 pt iOS, 48×48 dp Android, 44×44 px recommended on touch web | Inspect computed size including padding |
| Keyboard | Every action reachable; no keyboard trap; logical order matching visual order | Unplug the mouse; complete the primary flow |
| Dragging | Every drag action has a single-pointer or button alternative | Manual |
| Reflow | Usable at 320 CSS px width and 400% zoom without two-way scrolling | Browser zoom at 1280 px width |
| Text spacing | No loss of content with line height 1.5, paragraph spacing 2×, letter spacing 0.12em, word spacing 0.16em | Text-spacing bookmarklet or injected CSS |
| Motion | Respect `prefers-reduced-motion`; nothing flashes > 3 times per second; auto-moving content > 5 s has pause | OS reduced-motion setting on, re-test |
| Names and roles | Every control has an accessible name that includes its visible label | Accessibility tree in DevTools |
| Status messages | Async results announced via `role="status"` (polite) or `role="alert"` (urgent) | Screen reader (VoiceOver, NVDA, TalkBack) |
| Headings and landmarks | One `h1`; no skipped levels; `header`, `nav`, `main`, `footer` present | axe, headings list in a screen reader |
| Language | `lang` on `<html>`; `lang` on inline foreign phrases | Source check |
| Authentication | Paste and password managers allowed; no cognitive puzzle without an alternative | Manual |
| Consistent help | Help and contact links in the same place across pages | Manual |

## Common anti-patterns and fixes

| Red flag | Why it hurts | Do instead |
|---|---|---|
| `outline: none` / `focus:outline-none` with no replacement | Keyboard users lose their place | `:focus-visible` ring, 2 px, ≥ 3:1 |
| `<div onClick>` as a button | No keyboard, no role, no focus | `<button type="button">` |
| `<a>` without `href` or `href="#"` for actions | Wrong semantics; scrolls to top | `<button>` for actions, `<a href>` for navigation |
| Placeholder as the only label | Disappears on input; low contrast; not reliably announced | Visible `<label>`; placeholder only for an example format |
| Gray `#9CA3AF` text on white | 2.5:1, fails AA | `#4B5563` (7.6:1) or darker for text |
| Red/green only for status | Invisible to color-blind users | Icon plus text ("Failed", "Passed") plus color |
| Emoji as icons | Inconsistent rendering; cannot theme; odd announcements | One SVG icon set with `aria-hidden` and a text label |
| Icon button without name | Screen readers say "button" | `aria-label` or visually hidden text |
| Hover-only menus or row actions | Unreachable on touch and keyboard | Always-visible or focus-revealed controls |
| Full-page spinner on every fetch | Layout jumps; feels slow | Skeleton matching layout; local loading per region |
| Images without dimensions | Layout shift (CLS) | `width`/`height` or `aspect-ratio` |
| `height: 100vh` on mobile | Content hidden behind browser chrome | `min-height: 100dvh` |
| `user-scalable=no` / `maximum-scale=1` | Blocks zoom for low-vision users | Plain `width=device-width, initial-scale=1` |
| Body text 12-14 px on mobile, input font < 16 px | Hard to read; iOS zooms on focus | 16 px body and inputs |
| Disabled submit with no reason | Users cannot tell what is missing | Enabled submit that shows field errors, or a visible hint |
| Clearing the form on error | Users retype everything | Preserve values; focus the first error |
| Toast as the only error | Disappears; missed by screen readers | Inline error near the cause; toast only for confirmations |
| Modal without focus trap or Escape | Focus escapes behind the overlay | Tested dialog primitive or `<dialog>` with `showModal()` |
| `z-index: 9999` arms race | Overlays collide unpredictably | Named z-index scale tokens |
| Raw hex values and one-off spacing in components | Drift; dark mode breaks | Semantic tokens from the master |
| Animating `width`, `height`, `top`, `left` | Layout thrash and jank | `transform` and `opacity` |
| Infinite decorative animation | Distracting; drains battery; vestibular risk | Animate once or on interaction only |
| Mixed styles (glass + clay + brutal cards) | Feels incoherent and untrustworthy | One style from the master |
| Truncating IDs, prices, or errors | Hides essential content | Wrap, or give a visible way to see the full text |
| Tables squeezed on mobile until text breaks per letter | Unreadable | Scroll container with sticky first column, or cards |
| Infinite scroll with a footer | Footer is unreachable | Pagination or "Load more" |

## Right-to-left interfaces

For Arabic, Hebrew, Persian, and Urdu, use logical CSS properties (`margin-inline-start`). Mirror directional icons and carousels, and keep numerals and media controls unmirrored. Check each component.

More detail:

- Set `dir="rtl"` on `<html>` (or the subtree) and `lang`; do not flip layout with transforms.
- Use `start`/`end` in Flexbox and Grid alignment, `text-align: start`, `inset-inline-*`; Tailwind `ms-*`, `me-*`, `ps-*`, `pe-*`, `start-*`, `end-*`, and the `rtl:` variant.
- Mirror arrows, back and forward chevrons, progress direction, and sliders. Do not mirror logos, clocks, checkmarks, media play buttons, or phone numbers.
- Mixed-direction text (a Latin product name in Arabic text) needs `<bdi>` or `dir="auto"`.
- Pick fonts with full script coverage (Noto Sans Arabic, Noto Sans Hebrew); Arabic usually needs line height around 1.6-1.8.

## Pre-delivery checklist

- [ ] Every state is designed and reachable: loading, empty, error, success, partial, permission-denied.
- [ ] A keyboard-only pass completes the primary flow; focus order is logical and visible.
- [ ] An automated accessibility scan (for example axe) shows no critical violations; contrast is checked in light and dark modes.
- [ ] Screenshots at about 375 px and about 1280 px widths show no overflow, clipping, or horizontal scroll.
- [ ] Touch targets and spacing meet priority 2.
- [ ] Copy is clear and errors say how to recover.
- [ ] The tokens and components used match the master, or the deviations are documented.
- [ ] Motion respects reduced-motion settings.
- [ ] Every icon-only control has an accessible name; decorative images have `alt=""`; no emoji serve as icons.
- [ ] Every interactive element has hover, focus-visible, active, and disabled styles, and clickable elements show `cursor: pointer`.
- [ ] Async actions show pending state within 100 ms and block double submission.
- [ ] Forms: visible labels, correct `type` and `autocomplete`, inline errors linked by `aria-describedby`, input preserved after errors.
- [ ] Media has reserved dimensions; no visible layout shift while loading; fonts use `font-display: swap`.
- [ ] Long and unexpected content tested: long names, long URLs, 0 items, 1 item, 1,000 items, translated strings about 30% longer.
- [ ] Browser zoom at 200% and a 320 px wide viewport keep all content and actions usable.
- [ ] Dark mode (if supported) re-checked for contrast, borders, shadows, and images.
- [ ] Back, refresh, and shared URLs restore the same view (tabs, filters, pagination).
- [ ] Destructive actions confirm or offer undo; irreversible ones name the object and the consequence.
- [ ] Charts have a text summary or data table and do not rely on color alone.
- [ ] No console errors or warnings from the UI framework's accessibility checks.

Report each item as checked (with evidence), failed, or not verified (with the reason).

## Worked review example

Bad (a typical generated card action):

```html
<div class="card" onclick="del(42)">
  <span style="color:#9CA3AF">Delete 🗑️</span>
</div>
```

Findings, in priority order: not keyboard operable and no role (P1); text at 2.5:1 (P1); emoji as icon (P4); destructive action with no confirmation or undo (P8).

Good:

```html
<button type="button" class="btn btn-danger" aria-describedby="del-hint" data-id="42">
  <svg aria-hidden="true" focusable="false" width="16" height="16"><use href="#icon-trash"/></svg>
  Delete project
</button>
<p id="del-hint" class="sr-only">Opens a confirmation dialog.</p>
```

Sources: adapted from nextlevelbuilder/ui-ux-pro-max-skill (MIT) (`ux-guidelines.csv`, ui-ux-pro-max `SKILL.md` priority categories and pre-delivery checklist) and general practice.
