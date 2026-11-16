# Data Display: Charts, Tables, Dashboards

Open this when a screen shows numbers, trends, comparisons, or lists of records. Start from the question the user asks of the data, then pick the form.

## 1. Chart selection

| Question | Best form | Alternatives | Do not use when | Accessible fallback |
|---|---|---|---|---|
| How does it change over time? | Line | Area (one series), sparkline | Fewer than 4 points (use a stat); more than 6 series | Data table plus one-line trend summary |
| Which category is bigger? | Bar (horizontal for long labels) | Column, dot plot | More than 15-20 categories (use a sorted table) | Sortable table |
| What share of the whole? | Stacked bar or 100% bar | Donut (2-5 slices), waffle | More than 5 parts, or slices differ by < 5% | Percentage table |
| One number vs a target? | Bullet chart or KPI tile with delta | Gauge (single hero KPI only) | No target exists | Text "72% of 80% target" |
| Two numeric variables related? | Scatter | Bubble (third variable) | Fewer than about 20 points | Table plus correlation summary |
| How is it distributed? | Histogram | Box plot (comparing groups) | Fewer than about 20 values per group | Statistics table (min, median, max) |
| Where does flow drop off? | Funnel (sequential steps) | Sankey (branching flows) | Steps are not sequential | Stage table with conversion rates |
| What adds up to the total? | Waterfall | Stacked bar | More than about 12 steps | Running-total table |
| Intensity across two dimensions? | Heatmap | Calendar heatmap | Fewer than about 20 cells; exact values matter | Grid table |
| Where geographically? | Choropleth (rates) | Bubble map (counts) | Region size misleads; mobile-first | Sortable region table |
| Part of a hierarchy? | Treemap (2-3 levels) | Sunburst, indented tree | Depth > 3 | Collapsible tree table |
| Forecast with uncertainty? | Line with confidence band | Fan chart | No historical baseline | Table with ranges |
| Live stream? | Rolling line or area with pause | Periodic refresh line | Updates slower than once a minute | Live value with `role="status"` throttled |
| Price over time (OHLC)? | Candlestick | Line of close price | Non-financial audience | OHLC table |

Avoid by default: 3D charts, radar charts with more than 6-8 axes, dual y-axes (use two aligned charts), pie charts with more than 5 slices, word clouds for anything quantitative.

## 2. Chart rules

- Start bar and area axes at zero. Line charts may zoom the axis but must label it.
- Label directly on the chart when you have 4 or fewer series; otherwise use a legend in series order.
- Sort categorical bars by value unless the category has a natural order (time, rating).
- Color: one hue for one series; a categorical palette of at most 6-8 distinct hues; sequential (light to dark) for magnitude; diverging (two hues around a neutral midpoint) for above/below a baseline.
- Never encode meaning in color alone: add labels, patterns, markers, or dash styles. About 8% of men have a red-green color vision deficiency.
- Non-text marks (lines, bars, points) need ≥ 3:1 contrast against the background.
- Tooltips work on hover, focus, and tap. Every value shown in a tooltip is also reachable from the keyboard or in the table view.
- Give each chart a title that states the finding ("Sign-ups doubled after the March launch"), not only the metric.
- Format numbers for people: thousand separators, units, sensible precision, locale-aware dates (`Intl.NumberFormat`, `Intl.DateTimeFormat`).
- Volume: SVG up to about 1,000 points; Canvas or WebGL above; aggregate or downsample above about 10,000.
- Wrap charts as `<figure>` with a `<figcaption>`; give the SVG `role="img"` and an `aria-label` with the summary, or link a visible table.

## 3. Tables

| Rule | Detail |
|---|---|
| Semantics | Real `<table>` with `<th scope="col">`, a `<caption>`; not a grid of `div`s |
| Alignment | Text left, numbers right with tabular figures (`font-variant-numeric: tabular-nums`), dates consistent |
| Density | Row height 40-48 px (comfortable) or 32-36 px (compact toggle); body text ≥ 14 px |
| Sorting | Sortable headers are buttons; show direction; set `aria-sort` |
| Long lists | Paginate, or virtualize above about 100-200 rows; keep the header sticky |
| Selection and bulk actions | Checkbox column; a bulk bar shows the count selected and the actions |
| Row actions | Visible, or in an overflow menu that is keyboard reachable; never hover-only |
| Empty and loading | Skeleton rows while loading; an empty state with an action |
| Small screens | Scroll inside the table container with a sticky first column, or switch to cards |
| Truncation | Truncate long cells with an ellipsis plus a tooltip or expand; never truncate IDs users must copy |

## 4. Dashboards

- Lead with 3-5 KPI tiles: value, unit, change vs a stated period, and direction in text or icon (not color alone).
- Put the most important view top-left. Group related charts; align their time ranges and scales.
- One global time filter, shown clearly; persist filters in the URL.
- Show freshness ("Updated 2 min ago") and loading state per widget so one slow query does not blank the page.
- Prefer small multiples over one chart with many series.
- Dense dashboards: 8-16 px gaps, 14 px body, compact tables; keep target sizes for interactive parts.

Sources: adapted from nextlevelbuilder/ui-ux-pro-max-skill (MIT) (`charts.csv`, `ux-guidelines.csv`, dashboard rows of `styles.csv`) and general practice.
