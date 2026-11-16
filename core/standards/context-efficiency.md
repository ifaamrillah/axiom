# Context Efficiency Standard

- Inspect narrowly before reading the entire repository.
- Reuse current, verified project knowledge.
- Load references only when needed.
- Keep task handoffs concise and structured.
- Avoid repeating research and tool calls when evidence remains valid.
- Delegate only when expected benefit exceeds coordination cost.
- Prefer focused tests during iteration and broader checks at quality gates.
- Record assumptions so they need not be rediscovered.
- Load workflow stage files only when entering that stage; skip `.axiom/` documents whose `sources` are unchanged since `verified_at_commit`.
- Keep `SKILL.md` lean (validator budget: 250 lines); put depth in `references/`.
- Give subagents a constructed brief, not the session history.
- Never sacrifice correctness or safety merely to reduce tokens.
