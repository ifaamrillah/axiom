# Code Graph Tools (optional)

Repository indexes and code graphs can answer structural questions (who calls X, what breaks if Y changes) with fewer file reads. They are third-party tools. Axiom works without them, never installs them, and treats their answers as leads to confirm in source.

## Which one

| Tool | Builds the graph from | Fits |
|---|---|---|
| [codebase-memory-mcp](https://github.com/DeusData/codebase-memory-mcp) | Static parsing of code, no model calls; served over MCP | Call chains, impact analysis, dead-code questions. The default choice for code. |
| [Graphify](https://github.com/Graphify-Labs/graphify) | Code plus documents, PDFs, and media; documents are extracted by a model, which spends tokens | Repositories where specs and other documents must be mapped together with the code |

Use one. Running both for the same code duplicates indexing without a recorded benefit.

## Procedure

1. **Detect.** codebase-memory: its MCP tools are available in the session. Graphify: `graphify-out/graph.json` exists and `command -v graphify` succeeds. If neither is present, use the `codebase-exploration` search recipes.
2. **Check freshness.** An index older than the last change to the paths you care about gives leads, not facts. codebase-memory refreshes the session project on its own; a Graphify graph needs `graphify update .`, which you run only with the user's approval.
3. **Query before broad search.** Use the graph for structural questions. A single literal lookup is cheaper with plain search.
4. **Check coverage, then confirm in source.** With codebase-memory, run its coverage check for every file you rely on and read any reported gaps directly. Open the cited code before relying on an edge. Graphify edges marked INFERRED or AMBIGUOUS are hypotheses.
5. **Negative claims.** A graph that finds no caller is not proof of absence. The negative-claim rule in the exploration search recipes still applies: record the searches that back it.

## Cautions

- Never install a tool or build a graph without approval. A Graphify build reads the whole corpus and can spend model tokens.
- Do not enable hooks that block file reads until the graph is queried; reading source is Axiom's evidence.
- Some tools log queries on the local machine. Check before using them on sensitive code.
- Static graphs miss dynamic dispatch, reflection, and string-built calls. Both projects' token-saving figures are their own and were not reproduced here.
