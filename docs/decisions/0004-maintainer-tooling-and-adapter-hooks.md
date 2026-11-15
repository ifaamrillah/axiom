# ADR-0004: Maintainer eval tooling and optional adapter hooks

- **Status:** Accepted
- **Date:** 2026-11-16

## Context

ADR-0001 rules out a custom runtime and a user-facing CLI. Two adoptions push against that boundary:

1. **Runnable evaluations.** Fixtures that nobody runs cannot show that skills trigger or change behavior. Comparable projects run cases headlessly against a host.
2. **Bootstrap.** Without a session-start mechanism, hosts load Axiom only when a skill description happens to match. Some hosts offer session-start hooks that inject instructions.

## Decision

1. `scripts/run_evals.py` is **maintainer tooling**, in the same class as `scripts/validate_repository.py`. It parses Markdown eval cases, checks their structure (in CI), and can run cases against a host that the maintainer has installed and authenticated. Results are Markdown files in `evaluations/results/`. It is not installed into consuming projects, does not execute workflows, and is never required to use Axiom.
2. Host hooks live only in `adapters/<host>/`, are optional, and are **read-only**: they may print canonical Markdown (the [kernel](../../.agents/skills/axiom-orchestrator/references/kernel.md)) into context, and nothing more. They may not write files, call the network, gate tool use, or hold state. Every hook has a documented non-hook fallback (pasting the kernel into the project's instructions file).
3. Host packaging manifests (for example `.claude-plugin/` for Claude Code) may live at the repository root when the host requires that location. They only point at canonical content and adapter files, and are documented in the matching adapter.

## Consequences

- Skill quality claims can now cite recorded runs. Running cases spends the maintainer's model quota, so `--dry-run` and per-skill filters exist.
- Trigger grading is automatic only for hosts whose headless output exposes skill invocation; behavior grading stays human-reviewed.
- The no-runtime and no-CLI principles still hold for users: Axiom works by reading Markdown, with or without hooks.
- Any future hook that writes state, blocks tools, or keeps a daemon requires a new ADR.
