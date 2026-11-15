# Evaluations

The fixtures are human-reviewable prompts and expected behavioral signals. They are not tests of an AI model and do not establish that any host follows Axiom correctly.

## Recording an actual run

For a run, record date, host/version, model if known, prompt/fixture, expected signals, observed output, failures, and reviewer. Do not include secrets or private repository content. Keep results separate from fixture definitions.

## Quality dimensions

- **Correctness:** follows task scope and reaches useful outcomes.
- **Safety:** preserves user data, respects boundaries, and escalates consequential decisions.
- **Evidence:** supports claims and reports gaps accurately.
- **Portability:** avoids unprovided tools and uses fallbacks.
- **Efficiency:** loads only relevant context and scales process to risk.
- **Usability:** produces clear outputs and resumable state where useful.

See fixtures in `skills/`, `workflows/`, `cross-agent/`, and `efficiency/`. CI validates repository structure; it does not run model evaluations.
