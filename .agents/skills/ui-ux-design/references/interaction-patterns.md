# Interaction Patterns: States, Forms, Feedback, Motion, Responsive

Open this when you specify or review components, forms, async flows, animation, or layouts across screen sizes. Numbers are defaults; a project master may tighten them.

## 1. Component state matrix

Every interactive component needs each state below designed, not left to browser defaults.

| State | Trigger | Visual change | Semantics |
|---|---|---|---|
| Default | none | Base look; control edge visible at ≥ 3:1 against its surroundings | Native element (`button`, `a`, `input`) |
| Hover | pointer over | Small color or elevation shift; `cursor: pointer` on clickables | None; never the only way to reveal an action |
| Focus-visible | keyboard focus | Ring ≥ 2 px, ≥ 3:1 against adjacent colors, offset 2 px | Never `outline: none` without a replacement |
| Active / pressed | mouse down, touch | Darker or inset; scale ≥ 0.97 at most | `aria-pressed` for toggle buttons |
| Selected / current | chosen item, current page | Persistent marker besides color (weight, bar, check) | `aria-selected`, `aria-current="page"` |
| Disabled | not available | Reduced contrast but readable; `cursor: not-allowed` | `disabled` attribute; explain why nearby if not obvious |
| Loading / busy | async work | Spinner or progress in place; width stays fixed | `aria-busy="true"`; block double submit |
| Error / invalid | failed validation | Red border plus icon plus message | `aria-invalid="true"`, `aria-describedby` to the message |
| Read-only | viewable, not editable | No input chrome or muted chrome; text still selectable | `readonly`, not `disabled` (disabled is skipped by forms and some readers) |

When states stack, show the strongest: disabled > loading > error > active > focus > hover > default.

```css
.btn { transition: background-color 150ms ease, box-shadow 150ms ease; }
.btn:hover { background: var(--color-primary-hover); }
.btn:focus-visible { outline: 2px solid var(--color-ring); outline-offset: 2px; }
.btn:active { transform: scale(0.98); }
.btn[aria-busy="true"] { pointer-events: none; }
.btn:disabled { opacity: .55; cursor: not-allowed; }
```

## 2. Screen-state inventory

For every screen or async region, list each state and what the user sees and can do.

| State | Must show | Common miss |
|---|---|---|
| Initial loading | Skeleton matching the final layout for loads > 300 ms; nothing for < 300 ms | Full-page spinner that shifts layout when content lands |
| Empty (first use) | Why it is empty, one primary action, optional example | Blank table with headers only |
| Empty (no results) | The query or filters used, a clear-filters action, suggestions | "No data" with no way out |
| Partial | What loaded, what failed, retry for the failed part | Whole page error because one widget failed |
| Error | Plain-language cause, recovery action (retry, edit, contact), preserved input | Raw error codes or stack traces |
| Success | Confirmation near the trigger; next step | Silent success; user clicks twice |
| Offline / stale | Banner with last-updated time; queued actions marked | Spinners forever |
| Permission denied | What is blocked, who can grant access | 404 that hides the reason, or a broken page |
| Long content | Truncation with a way to see full text; wrapping for long tokens (`overflow-wrap: anywhere`) | Clipped essential text, overflowing URLs or IDs |

## 3. Forms

| Rule | Do | Do not |
|---|---|---|
| Labels | Visible `<label for>` above or beside each field | Placeholder as the only label |
| Required | Mark required or optional in text, consistently; `required` attribute | Color-only asterisk with no legend |
| Input types | `type="email"`, `tel`, `url`, `number` only for real numbers; `inputmode="numeric"` for codes | `type="number"` for card numbers or ZIP codes |
| Autofill | `autocomplete="email"`, `given-name`, `current-password`, `new-password`, `one-time-code` | Random `name` values that block password managers |
| Paste | Allow paste in all fields, including passwords and codes | Blocking paste "for security" |
| Validation timing | Validate on blur, and re-validate on input once a field shows an error | Erroring while the user is still typing the first time |
| Error message | Next to the field, says what to do: "Enter a date after 1 Jan 2024" | "Invalid input" |
| Error summary | On submit failure in long forms: summary at top, focus moved to it, links to each field | Errors only at the top, far from fields |
| Preservation | Keep all input after any error or reload where possible | Clearing the form on a server error |
| Submit | One primary button; disabled only while submitting; shows progress | Disabled submit with no hint why |
| Long forms | Group with `fieldset`/`legend`; multi-step with a progress indicator and back | One 30-field wall |
| Destructive actions | Confirm dialog naming the object and the consequence; prefer undo for reversible actions | "Are you sure?" with OK/Cancel |
| IME input | Ignore Enter while `event.isComposing` is true | Submitting half-composed Chinese or Japanese text |

```html
<label for="email">Work email</label>
<input id="email" name="email" type="email" autocomplete="email" required
       aria-invalid="true" aria-describedby="email-err">
<p id="email-err" class="field-error">Enter an address like name@company.com.</p>
```

## 4. Feedback and messaging

- Respond to every action within 100 ms (pressed state, spinner, optimistic update).
- Show progress for work over 1 s; show determinate progress or steps for work over 10 s.
- Toasts: for non-critical confirmations only. Keep visible 4-6 s, pause on hover and focus, include a close button, and announce through a polite live region (`role="status"`). Never put the only copy of an error or a required action in a toast.
- Errors that block progress use `role="alert"` or move focus to the message.
- Confirm irreversible actions; offer undo (5-10 s) for reversible ones instead of a dialog.
- Label AI-generated content and give a way to retry or report it.

## 5. Motion

| Use | Duration | Easing |
|---|---|---|
| Hover, color, focus | 100-150 ms | `ease` or `ease-out` |
| Small transitions (dropdown, tooltip, toggle) | 150-200 ms | `ease-out` entering, `ease-in` leaving |
| Medium (modal, drawer, card expand) | 200-300 ms | `cubic-bezier(0.2, 0, 0, 1)` |
| Page or large layout change | 300-400 ms max | Same; exit faster than enter |
| Skeleton shimmer, spinners | Loop while loading only | `linear` |

- Animate `transform` and `opacity` only. Animating `width`, `height`, `top`, or `left` causes layout work and jank.
- One or two animated elements per view. Motion must explain a change (origin, destination, relation).
- Interruptible: a new interaction cancels the running animation and sets the final state directly.
- Auto-rotating content (carousels) needs pause and previous/next controls and stops on hover and focus.
- Nothing flashes more than 3 times per second.
- Respect reduced motion; keep the final state, drop the travel:

```css
@media (prefers-reduced-motion: reduce) {
  *, *::before, *::after { animation-duration: 0.01ms !important; animation-iteration-count: 1 !important;
    transition-duration: 0.01ms !important; scroll-behavior: auto !important; }
}
```

## 6. Responsive layout

| Breakpoint | Width | Typical layout |
|---|---|---|
| Base (mobile) | 320-639 px | Single column, bottom or hamburger nav, full-width buttons |
| `sm` | ≥ 640 px | Two-column forms, wider cards |
| `md` | ≥ 768 px | Sidebars appear as drawers; tables may keep columns |
| `lg` | ≥ 1024 px | Persistent sidebar, multi-column dashboards |
| `xl` / `2xl` | ≥ 1280 / 1536 px | Cap content width (about 1200-1440 px); do not stretch text |

- Write mobile-first: base styles for small screens, `min-width` queries upward.
- Test widths: 320, 375, 414, 768, 1024, 1280, 1440. Also test 200% browser zoom and 400% zoom at 1280 px (WCAG reflow at 320 CSS px).
- `<meta name="viewport" content="width=device-width, initial-scale=1">`; never `maximum-scale=1` or `user-scalable=no`.
- Use `min-height: 100dvh`, not `100vh`, on mobile. Respect safe areas with `env(safe-area-inset-*)`.
- Text measure 45-80 characters (`max-width: 65ch` for prose).
- Tables on small screens: horizontal scroll inside the table container with a sticky first column, or a card per row. The page itself never scrolls sideways.
- Flex and grid children that hold text need `min-width: 0` so long words can wrap.
- Prefer container queries for components that live in different column widths.

## 7. Navigation

- Show where the user is: highlighted nav item plus `aria-current="page"`; breadcrumbs for 3+ levels.
- Back must work: every view the user can reach and share has its own URL; filters, tabs, and pagination sit in the query string.
- Bottom tab bar: 3-5 items, each with icon and text label.
- Sticky headers must not hide focused elements: `scroll-padding-top` equal to header height.
- Provide a "Skip to main content" link as the first focusable element.
- Modals trap focus, close on Escape, and return focus to the trigger.

Sources: adapted from nextlevelbuilder/ui-ux-pro-max-skill (MIT) (`ux-guidelines.csv`, `motion.csv`, design-system `states-and-variants.md`) and general practice.
