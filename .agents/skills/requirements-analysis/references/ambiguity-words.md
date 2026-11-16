# Ambiguity Word List

Words that let a requirement mean different things to different readers. When one appears in a requirement, either replace it with a measurable statement or mark it `[NEEDS CLARIFICATION: ...]`. The words are fine in context and problem sections, where they describe intent. They are not fine in requirements, scenarios, or NFRs.

Quick scan (case-insensitive):

```bash
grep -nEi '\b(fast|quick(ly)?|slow|easy|easily|simple|intuitive|user-friendly|seamless|robust|scalable|secure|safe|reliable|flexible|efficient|appropriate(ly)?|adequate|reasonable|sufficient|minimal|optimal|large|small|many|few|several|some|most|various|etc|and/or|as needed|if possible|where applicable|should|may|might|could|ideally|normally|typically|usually|support[s]?|handle[s]?|manage[s]?|process(es)?|TBD|TODO|TKTK)\b' spec.md
grep -nF '???' spec.md   # placeholder that word boundaries miss
```

Treat each hit as a question, not as an automatic defect.

## Vague quality adjectives

| Word | Ask | Example rewrite |
|---|---|---|
| fast, quick, responsive, performant | What percentile, what time, under what load? | "≤ 500 ms p95 at 20 req/s" |
| easy, simple, intuitive, user-friendly | Who, doing what, in how long, how measured? | "8 of 10 test users finish unaided in ≤ 2 min" |
| secure, safe | Against which actor and which threat? | "Customers can read only their own requests" |
| reliable, robust, resilient | Which failure, what behavior, what rate? | "Retries 3 times; after that, status `failed` and alert" |
| scalable | To what volume, by when? | "200 orders/min with < 0.1% errors" |
| flexible, extensible, configurable | Which change, by whom, without what? | "Window length set in config without deploy" |
| efficient, optimal, minimal | Which resource, compared with what? | "≤ 1 DB query per request" |
| seamless, smooth | Which steps disappear? | "No re-login when moving from order page to refund form" |
| modern, clean, nice | Usually a design note. Move to design or delete. | — |

## Vague quantities

| Word | Ask | Example rewrite |
|---|---|---|
| large, small, big, long, short | What number and unit? | "≤ 500 characters" |
| many, few, several, some, most | How many exactly, or what threshold? | "Up to 50 items per page" |
| frequently, rarely, periodically | How often? | "Every 15 minutes" |
| recent, old, soon, later | Measured from what date, how long? | "Delivered ≤ 30 days before the request" |

## Weak or escape-hatch phrases

| Phrase | Problem | Do instead |
|---|---|---|
| appropriate(ly), adequate, reasonable, sufficient, proper | The writer deferred the decision to the reader | State the decision or mark it |
| as needed, if possible, where applicable, when necessary | Makes the requirement optional with no rule | State the condition, or make it a SHOULD with the condition |
| etc., and so on, such as | Open list; readers cannot tell what is in scope | List the full set, or write "only these: ..." |
| and/or | Two readings | Write "A, B, or both", or split |
| support(s), handle(s), manage(s), process(es) | Verb with no observable result | Name the action and its result: "rejects with message X" |
| ideally, normally, typically, usually | What happens in the other cases? | Specify the exception path |
| including but not limited to | Open scope | Close the list |
| user | Which role? | Name the role: customer, support agent |
| it, this, they (across sentences) | Unclear referent | Repeat the noun |

## Modal verbs

Use the RFC 2119 meanings consistently.

| Word | Meaning in a spec |
|---|---|
| MUST, MUST NOT | Required. The release fails without it. |
| SHOULD, SHOULD NOT | Expected unless a stated reason applies. Name the reason when you skip it. |
| MAY | Optional. No test required. |
| will, shall, should (lowercase), could, might | Ambiguous strength. Replace with MUST, SHOULD, or MAY. |

## Placeholders

`TBD`, `TODO`, `TKTK`, `???`, `<placeholder>`, `[fill in]`, `XXX`, and empty sections are always findings. In a requirement or scenario they block the `clarified` status. Convert each into `[NEEDS CLARIFICATION: <specific question>]` so it can be tracked.

## Terminology drift

Ambiguity also comes from using two words for one thing, or one word for two things. Build a short glossary when you see drift.

| Drift seen | Fix |
|---|---|
| "admin", "agent", "support", "staff" for one role | Pick `support agent`; use it everywhere |
| "order" meaning both the order and one line item | Use "order" and "order item" |
| "cancel" and "reject" for the same transition | Pick one status name |

Sources: adapted from github/spec-kit (MIT) `templates/commands/analyze.md` and `templates/commands/clarify.md`, and general practice (RFC 2119, requirements-engineering ambiguity guidance).
