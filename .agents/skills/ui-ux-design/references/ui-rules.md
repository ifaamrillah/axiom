# UI Rules (priority order)

Resolve the categories from top to bottom. Numbers are defaults; a project master may tighten them.

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

## Right-to-left interfaces

For Arabic, Hebrew, Persian, and Urdu, use logical CSS properties (`margin-inline-start`). Mirror directional icons and carousels, and keep numerals and media controls unmirrored. Check each component.

## Pre-delivery checklist

- [ ] Every state is designed and reachable: loading, empty, error, success, partial, permission-denied.
- [ ] A keyboard-only pass completes the primary flow; focus order is logical and visible.
- [ ] An automated accessibility scan (for example axe) shows no critical violations; contrast is checked in light and dark modes.
- [ ] Screenshots at about 375 px and about 1280 px widths show no overflow, clipping, or horizontal scroll.
- [ ] Touch targets and spacing meet priority 2.
- [ ] Copy is clear and errors say how to recover.
- [ ] The tokens and components used match the master, or the deviations are documented.
- [ ] Motion respects reduced-motion settings.

Report each item as checked (with evidence), failed, or not verified (with the reason).
