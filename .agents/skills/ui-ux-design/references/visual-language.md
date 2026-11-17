# Visual Language: Style, Color, Type, Tokens

Open this when you choose or audit the look of a new product, page, or design-system master. For an existing product, the master wins; use these tables to fill gaps, not to restyle.

## 1. Pick a style from the product, not from taste

Decide in this order: product type, then audience and context of use, then brand personality (three adjectives), then style. Data-heavy and accessibility-critical products constrain style the most.

| Style | Use for | Avoid for | Accessibility risk and guard | Status | RTL |
|---|---|---|---|---|---|
| Minimal / Swiss (grid, sans-serif, high contrast) | SaaS, admin, docs, enterprise tools | Playful consumer brands, entertainment | Low. Keep enough visual weight on primary actions | active | Good |
| Flat | MVPs, cross-platform apps, general web apps | Luxury, immersive showcases | Low. Borders or fills must still show control edges at 3:1 | active | Good |
| Soft UI (soft shadows, rounded, modern flat) | Modern SaaS, wellness, consumer productivity | Very dense data tools | Low to medium. Check card edges against background | active | Good |
| Accessible / inclusive (large type, strong contrast) | Government, health, education, finance, older users | Nothing; it fits anywhere | Lowest. Treat as the baseline for public services | active | Good |
| Data-dense dashboard (compact grid, small multiples) | BI, ops consoles, finance, monitoring | Marketing pages, casual consumers | Medium. Body text still ≥ 14 px; never color-only status | active | Good; keep numerals LTR |
| Bento grid (modular cards of mixed size) | Feature overviews, home dashboards, product pages | Long reading, dense tables, complex forms | Low. Keep a logical DOM and reading order | active | Good; mirror the grid order |
| Dark (OLED / dev-tool dark) | Code tools, media, night use, monitoring walls | Print-first content, bright outdoor use | Medium. Re-check every pair; avoid pure #000 with pure #FFF body text for long reading | active | Good |
| Glassmorphism (blur, translucent layers) | Accent surfaces in modern SaaS, OS-aligned chrome | Text over busy images, low-end devices | Conditional. Add a solid fallback; test text on worst-case backdrop | supplemental (accents only) | Good |
| Neumorphism (embossed, low contrast) | Small, simple controls in wellness apps | Forms, dashboards, anything critical | High. Controls lose their edges; add borders or avoid | deprecated → Soft UI | Good |
| Claymorphism (puffy 3D, pastel) | Kids, education, playful onboarding | Finance, health, serious tools | Medium. Pastels often fail 4.5:1 for text | supplemental | Good |
| Neubrutalism (thick borders, flat bold color, hard shadows) | Startups, creative tools, Gen Z brands | Luxury, banking, healthcare | Low. High contrast by nature; watch saturated text | active | Good; mirror offset shadows |
| Brutalism / raw | Portfolios, editorial experiments | Corporate, conversion-critical flows | Low to medium. Keep standard affordances | supplemental | Check: asymmetric layouts must mirror |
| Editorial / magazine (serif display, wide margins) | Publishing, blogs, long reads | Dense apps | Low. Measure 60-75 characters | active | Check: serif display fonts often lack Arabic and Hebrew |
| Exaggerated minimalism (huge type, few elements) | Luxury, agencies, fashion | Catalogs, forms, dashboards | Medium. Hidden navigation hurts findability | supplemental | Check: huge display type needs script coverage |
| Organic / nature (earth tones, soft shapes) | Wellness, sustainability, food | Dev tools, trading | Low to medium. Earth tones on cream often fail; check | active | Good |
| Trust and authority (navy, serif or sober sans, proof) | Legal, finance, health, B2B | Entertainment, viral consumer | Low | active | Good |
| Conversion landing (one CTA, proof, short form) | Sign-up, lead gen, product pages | Docs, complex explanations | Low. Do not hide the price or dismiss path | active | Good |
| Motion-driven / parallax / kinetic type | Brand stories, launches, portfolios | Dashboards, forms, SEO-critical pages | High. Needs `prefers-reduced-motion` path and a static final state | supplemental | Check: directional motion and parallax must mirror |
| Retro-futurism / cyberpunk / HUD / vaporwave | Games, music, sci-fi themes | Business software, public services | High. Neon on dark and glow text often fail; test | supplemental | Poor: display fonts are Latin-only |
| AI-native (chat-first, streaming, suggestion chips) | Copilots, assistants | Pure data entry | Low. Label AI output; streaming must be announced politely | active | Good; `dir="auto"` on streamed text |
| Liquid glass / spatial (Apple platform materials) | Native Apple chrome, visionOS | Dense reading surfaces | Conditional. Use system materials, which handle contrast and reduce-transparency | active (Apple platforms) | Good; system materials mirror |

Rule: one style per product. Mixing glass, clay, and brutalist cards on one page reads as a template collage.

Status: `active` styles fit as a product's main style. `supplemental` styles fit accents, single pages, or narrow product types; do not use them for a whole operate-mode product. `deprecated → X` means use X instead; a master that already records the deprecated style keeps it until a restyle. RTL: `Good` works with logical properties and mirroring; `Check` names what to test; `Poor` needs a different style or fonts for RTL products. See [RTL rules](ui-rules.md#right-to-left-interfaces).

## 2. Palette recipes by product type

Every recipe below was checked with the WCAG relative-luminance formula: primary and accent pass 4.5:1 against white text (light themes), foreground and muted text pass 4.5:1 against the background. Recheck after any edit.

| Product type | Primary | Accent / CTA | Background | Foreground | Muted text | Intent |
|---|---|---|---|---|---|---|
| General SaaS | `#2563EB` | `#C2410C` | `#F8FAFC` | `#0F172A` | `#475569` | Trust blue, warm CTA |
| Developer tool | `#4F46E5` | `#0F766E` | `#FFFFFF` | `#111827` | `#4B5563` | Indigo, calm teal |
| Fintech / banking | `#1E3A8A` | `#047857` | `#F8FAFC` | `#0F172A` | `#475569` | Navy authority, green for gains |
| Healthcare | `#0E7490` | `#047857` | `#F0FDFA` | `#134E4A` | `#475569` | Calm cyan, health green |
| E-commerce | `#047857` | `#C2410C` | `#FFFFFF` | `#1C1917` | `#57534E` | Green trust, orange buy button |
| Luxury / premium | `#1C1917` | `#A16207` | `#FAFAF9` | `#0C0A09` | `#57534E` | Near-black, gold |
| Education | `#4338CA` | `#C2410C` | `#EEF2FF` | `#1E1B4B` | `#475569` | Friendly indigo, energetic orange |
| Government / public | `#1E3A8A` | `#0369A1` | `#FFFFFF` | `#0B0F19` | `#374151` | Maximum contrast, no decoration |
| Creative / agency | `#BE185D` | `#0E7490` | `#FDF2F8` | `#500724` | `#4B5563` | Bold pink, cyan contrast |
| AI product | `#6D28D9` | `#0E7490` | `#FAF5FF` | `#1E1B4B` | `#4B5563` | Violet, cyan interaction |
| Food / restaurant | `#B91C1C` | `#A16207` | `#FFFBEB` | `#431407` | `#57534E` | Warm red, gold |
| Travel | `#0369A1` | `#C2410C` | `#F0F9FF` | `#0C4A6E` | `#475569` | Sky blue, adventure orange |
| Legal / professional | `#1E3A8A` | `#92400E` | `#F8FAFC` | `#0F172A` | `#475569` | Navy, bronze |
| Wellness / mental health | `#7C3AED` | `#047857` | `#FAF5FF` | `#3B0764` | `#57534E` | Lavender calm, green |
| Docs / knowledge base | `#334155` | `#2563EB` | `#FFFFFF` | `#0F172A` | `#475569` | Neutral chrome, blue links |
| Real estate | `#0F766E` | `#1D4ED8` | `#F0FDFA` | `#134E4A` | `#475569` | Teal trust, blue action |
| Ops dashboard (dark) | `#60A5FA` | `#4ADE80` | `#0B1120` | `#E2E8F0` | `#94A3B8` | Text on primary must be dark (`#0B1120`, 7.4:1) |
| Gaming (dark) | `#A78BFA` | `#FB7185` | `#0F0F23` | `#E2E8F0` | `#94A3B8` | Text on primary must be dark |

Palette rules:

- Status colors are separate from brand: success, warning, danger, info. Danger around `#DC2626` with white text (4.8:1). Each status needs an icon or text too.
- Light 400-level tints (`#60A5FA`, `#9CA3AF`) fail as text on white (about 2.5:1). Use them for fills and borders only.
- Dark mode is a second palette, not an inversion. Lift surfaces with lighter grays (`#0B1120` → `#111827` → `#1F2937`) instead of shadows, and desaturate brand colors one step.
- At most one saturated accent per view. The CTA should be the most saturated thing on screen.
- Check contrast with a tool, never by eye. A tiny script is enough:

```python
def lum(h):
    c = [int(h.lstrip('#')[i:i+2], 16) / 255 for i in (0, 2, 4)]
    c = [x / 12.92 if x <= 0.04045 else ((x + 0.055) / 1.055) ** 2.4 for x in c]
    return 0.2126 * c[0] + 0.7152 * c[1] + 0.0722 * c[2]
def ratio(a, b):
    hi, lo = sorted((lum(a), lum(b)), reverse=True)
    return (hi + 0.05) / (lo + 0.05)
print(round(ratio('#475569', '#F8FAFC'), 2))  # 7.24
```

## 3. Font pairings

All are free on Google Fonts. Load at most two families and four weights total. Use `font-display: swap` and a metric-matched system fallback.

| Pairing (heading / body) | Mood | Fits |
|---|---|---|
| Inter / Inter | Neutral, precise | Dashboards, admin, docs |
| Plus Jakarta Sans / Plus Jakarta Sans | Friendly modern | SaaS, B2B apps |
| Space Grotesk / DM Sans | Technical, startup | Dev tools, AI products |
| IBM Plex Sans / IBM Plex Sans (+ Plex Mono) | Sober, engineered | Banks, enterprise, fintech |
| JetBrains Mono / IBM Plex Sans | Code-first | Developer docs, CLIs |
| Lexend / Source Sans 3 | Highly legible | Government, health, accessibility-first |
| Figtree / Noto Sans | Clean, clinical | Medical, multilingual apps |
| Poppins / Open Sans | Approachable corporate | Marketing sites, small business |
| Outfit / Work Sans | Geometric, modern | Agencies, landing pages |
| Playfair Display / Inter | Elegant contrast | Luxury, fashion, editorial |
| Cormorant / Montserrat | Refined | Jewelry, high-end retail |
| Newsreader / Roboto | Journalistic | News, blogs |
| EB Garamond / Lato | Formal | Law firms, institutions |
| Lora / Raleway | Calm | Wellness, yoga, spa |
| Fredoka / Nunito | Playful, rounded | Kids, education, casual games |
| Rubik / Nunito Sans | Clean retail | E-commerce |
| Bebas Neue / Source Sans 3 | Loud display | Sports, events, posters |
| Noto Sans + script-specific Noto (Arabic, JP, KR, SC, TC, Thai, Hebrew) | Coverage first | Multilingual and RTL products |

Avoid display fonts (Bebas, Abril, Playfair) for body or UI labels. Avoid thin weights (100-300) for text under 24 px.

## 4. Type scale and spacing tokens

Use a modular scale and a 4 px spacing grid. A dense product uses the lower end of each range.

| Token | Value | Use |
|---|---|---|
| `text-xs` | 12 px / 1.4 | Captions, table meta only; never body |
| `text-sm` | 14 px / 1.5 | Dense UI labels, table cells |
| `text-base` | 16 px / 1.5-1.6 | Body, inputs (16 px stops iOS zoom on focus) |
| `text-lg` | 18-20 px / 1.5 | Lead paragraphs |
| `text-xl` … `text-4xl` | 24, 30, 36, 48 px / 1.1-1.25 | Headings; ratio about 1.2-1.25 |
| `space-1` … `space-16` | 4, 8, 12, 16, 24, 32, 48, 64 px | Gaps, padding, section rhythm |
| `radius` | 4-8 px (enterprise), 12-16 px (consumer), full (pills) | One radius family per product |
| `shadow` | 2-3 levels max | Elevation means layering, not decoration |
| `z-index` | base 0, dropdown 10, sticky 20, overlay 30, modal 40, toast 50 | Named tokens, never `9999` |

Use a three-layer token model: primitive (`--blue-600: #2563EB`), semantic (`--color-primary: var(--blue-600)`), component (`--button-bg: var(--color-primary)`). Components read semantic or component tokens only, so themes and dark mode swap one layer.

```css
:root { --color-bg: #F8FAFC; --color-fg: #0F172A; --color-primary: #2563EB; --color-on-primary: #FFFFFF; }
@media (prefers-color-scheme: dark) {
  :root:not([data-theme="light"]) { --color-bg: #0B1120; --color-fg: #E2E8F0; --color-primary: #60A5FA; --color-on-primary: #0B1120; }
}
:root[data-theme="dark"] { --color-bg: #0B1120; --color-fg: #E2E8F0; --color-primary: #60A5FA; --color-on-primary: #0B1120; }
```

### Theme migration

Use this to move an existing product to semantic tokens, add dark mode, or change the palette. Work in four passes; do not skip ahead.

1. **Audit.** List every raw color, font, spacing, radius, and shadow value in styles and components (`rg -n '#[0-9a-fA-F]{3,8}\b|rgb\(|hsl\('`). Count them per file. Note inline styles and third-party overrides.
2. **Map.** Assign each raw value to a semantic token in the master (`--color-fg`, `--color-surface`). Merge near-duplicates (`#334155` and `#333F55`). Record values that have no token yet and add the token before migrating.
3. **Migrate.** Replace values file by file with token references, one component group per change. Keep the rendered result identical in the current theme; a visual change in this pass is a bug.
4. **Verify.** Re-run the audit search: no raw values remain outside the token file. Check contrast for every pair in each theme, screenshot key screens at 375, 768, and 1280 px in each theme, and run the craft floor browser checks (V9-V14).

## 5. Icons and imagery

- One SVG icon set (Lucide, Heroicons, Phosphor, Material Symbols, SF Symbols). One stroke width and two or three sizes (16, 20, 24 px).
- No emoji as UI icons: they render differently per OS and cannot be themed.
- Decorative images get `alt=""`; meaningful ones get alt that states the purpose, not "image of".
- Always set `width` and `height` (or `aspect-ratio`) on media to prevent layout shift.

Sources: adapted from nextlevelbuilder/ui-ux-pro-max-skill (MIT) (`styles.csv`, `colors.csv`, `typography.csv`, design-system token references) and general practice.
