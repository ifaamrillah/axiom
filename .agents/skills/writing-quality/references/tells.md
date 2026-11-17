# Tell Catalog

AI writing tells are the most probable default choices: the structure or word a model reaches for when nothing pushes it elsewhere. Structural tells outlast word lists, because vocabulary shifts between model versions while habits of shape do not.

**Strong** tells (S) justify an edit on one sighting. **Weak** tells (W) need a second tell nearby.

## A. Staging instead of stating

| ID | Tell | Before | After |
|---|---|---|---|
| A1 (S) | Not X but Y, used for drama | "This isn't just a cache. It's a performance layer." | "The cache cuts p95 latency from 300 ms to 40 ms." |
| A2 (S) | One-line closer that restates the paragraph | "…In short, validation matters." | Delete the line. |
| A3 (S) | Run-up before the point | "Here's the thing: the token expires." | "The token expires after 15 minutes." |
| A4 (W) | Arguing with no one ("Some might think…") | "You might think retries are enough." | State the claim and its reason. |
| A5 (S) | Rhetorical question as a heading or opener | "So why does this matter?" | Say why it matters. |

## B. Rhythm by rule

| ID | Tell | Fix |
|---|---|---|
| B1 (W) | Lists of exactly three adjectives or clauses, again and again | Keep the items that carry information; often one |
| B2 (W) | Em dashes as the main punctuation | Use a period, comma, or colon |
| B3 (W) | Stacked hedges ("may potentially help to") | One qualifier, or none if the claim is measured |
| B4 (W) | Every paragraph the same length and shape | Let length follow content |

## C. Inflation and borrowed authority

| ID | Tell | Fix |
|---|---|---|
| C1 (S) | Stock words: delve, leverage, robust, seamless, crucial, pivotal, tapestry, landscape, elevate, unlock, empower | The plain word, or a number |
| C2 (S) | Sales register in technical text ("powerful", "cutting-edge", "game-changing") | Describe what it does |
| C3 (W) | Vague authority ("experts agree", "best practice says") | Cite the source, or drop it |
| C4 (W) | Significance claims ("plays a vital role in") | Say what it does |

## D. Formatting by rule

| ID | Tell | Fix |
|---|---|---|
| D1 (W) | Bold on phrases that are not terms or warnings | Bold only defined terms and warnings |
| D2 (W) | Headings over one-paragraph sections | Merge into the parent section |
| D3 (S) | Bullets that are full sentences forming one argument | A paragraph |
| D4 (W) | Emoji as bullets or section markers | Remove |

## E. Leftovers from chat and drafting

| ID | Tell | Fix |
|---|---|---|
| E1 (S) | "Certainly!", "Great question", "I hope this helps", "Let me know if…" | Delete |
| E2 (S) | Writing about the document ("This guide will walk you through…") | Start with the first step |
| E3 (S) | Describing the method instead of the result ("I carefully analyzed…") | State the result and its evidence |
| E4 (W) | Knowledge-cutoff or "as an AI" disclaimers in docs | Delete; state real limits concretely |

## F. Wrong reader

| ID | Tell | Fix |
|---|---|---|
| F1 (S) | Re-explaining what the title or the previous sentence said | Delete |
| F2 (W) | Defining terms the audience uses daily | Define only terms new to this reader |
| F3 (S) | Burying the decision under background | Decision first, then reasons |

## When not to act

- Quoted text, titles, names, error messages, and log lines.
- A pattern the author chose on purpose (a style guide requires headings, a list really has three items).
- Technical and reference text should stay neutral; do not add personality.

Sources: tell groups, strength thresholds, fact-preservation check, and output modes adapted from blader/humanizer (MIT), which draws on Wikipedia's "Signs of AI writing"; general editing practice. Examples are Axiom's own.
