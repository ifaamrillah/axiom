# Craft Floor

Open this right before editing or generating UI, and again when reviewing it. The [UI rules](ui-rules.md) make a screen usable; this list keeps it from looking generated. Each item has a stable ID so findings can cite it.

## Verify (every UI change)

| ID | Check |
|---|---|
| V1 | Text and controls meet the contrast thresholds in [UI rules](ui-rules.md#accessibility-thresholds-wcag-22-aa-unless-noted). |
| V2 | Spacing comes from the token scale; no one-off values. Related items sit closer than unrelated ones. |
| V3 | Body line length is about 45-75 characters; headings are not wider than their content needs. |
| V4 | Every interactive element has hover, focus-visible, active, disabled, and loading states. |
| V5 | Loading, empty, and error states exist and are specific to the content ("No invoices yet. Create one" beats "No data"). |
| V6 | Copy is concrete and from the product: real labels, real units, no lorem ipsum, no invented numbers. |
| V7 | The layout holds at 375 px, 768 px, and 1280 px with no horizontal scroll. |
| V8 | One visual hierarchy per screen: one primary action, one main heading. |

### Browser surfaces

Add these for web pages and webviews. Check each in light and dark themes.

| ID | Check |
|---|---|
| V9 | `::selection` uses token colors with readable contrast, not the browser default clashing with the brand. |
| V10 | `caret-color` in inputs is visible against the field background. |
| V11 | Scrollbars (`scrollbar-color`, `scrollbar-width`, or `::-webkit-scrollbar`) match the theme; no light scrollbar on a dark surface. |
| V12 | A visible focus ring on every focusable element (`:focus-visible`), meeting the focus indicator threshold in [UI rules](ui-rules.md#accessibility-thresholds-wcag-22-aa-unless-noted). |
| V13 | Underlined links use `text-underline-offset` so the line clears descenders; links in body text stay underlined. |
| V14 | Number columns and changing numbers use tabular numerals (`font-variant-numeric: tabular-nums`) so digits align and do not jitter. |

## Refuse (generated-looking patterns)

Do not produce these unless the master or the user explicitly asks for them. In a review, each one is a finding at severity P2 unless it also breaks a UI rule.

| ID | Pattern | Instead |
|---|---|---|
| R1 | A grid of identical cards (icon, title, two lines) for unrelated content | Vary the form to the content: list, table, a single feature with detail |
| R2 | The hero-metric template: three big numbers with tiny labels and no source | Show the one number that matters, with its unit and source, or none |
| R3 | Gradient text on headings | Solid color from the tokens; emphasis through size or weight |
| R4 | Small uppercase "eyebrow" labels above every heading | Use them at most once, where they carry information |
| R5 | Decorative glass, blur, or glow with no purpose | Flat surfaces with the master's elevation tokens |
| R6 | Colored side-stripe borders on every card or alert | Reserve accent borders for one meaning (for example, status) |
| R7 | Emoji as icons or bullet points | One SVG icon set with text labels |
| R8 | Monospace type used to look "technical" for non-code text | Monospace only for code, IDs, and aligned numbers |
| R9 | Everything centered, including body text and forms | Left-align text and forms; center only short, isolated content |
| R10 | A default purple-to-blue gradient as the brand | The palette chosen for this product in the master |
| R11 | Filler copy: "Unlock the power of", "Seamless", "Elevate your workflow" | Say what the product does, in the user's words |
| R12 | Animation on every element on load | Motion only for state changes and feedback, within the master's durations |

A pattern is acceptable when the master records it as a deliberate choice. Cite the master line in that case.

Sources: Verify and Refuse lists adapted from pbakaus/impeccable (Apache-2.0) craft floor and anti-pattern guidance; nextlevelbuilder/ui-ux-pro-max-skill (MIT) anti-pattern columns; general practice. Wording is Axiom's own.
