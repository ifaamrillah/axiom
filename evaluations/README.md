# Evaluations

Two kinds of evaluation material live here:

- **Runnable cases** in [`cases/`](cases/README.md): trigger prompts (positive and negative with an owner) and behavior cases with observable expectations, run by [`scripts/run_evals.py`](../scripts/run_evals.py) against an installed host. Disposable fixture projects live in [`fixtures/`](fixtures/), and recorded runs in [`results/`](results/README.md).
- **Scenario fixtures** in `skills/`, `workflows/`, `cross-agent/`, and `efficiency/`: human-reviewable prompts and expected signals.

Neither kind is evidence until it has been run and recorded. A recorded result applies only to its host version and model.

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
