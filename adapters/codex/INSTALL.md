# Codex Adapter

## Project-level use

Codex discovers repository skills from `.agents/skills/`. Keep the canonical directories in that location and open the project root in Codex. For portable reuse in another repository, copy or link the desired skill directories into that repository's `.agents/skills/`.

## Global use

Codex documentation lists `~/.agents/skills/` for user-wide skills. Copy selected skill directories there only if global availability is desired.

## Verify

Start or refresh the Codex session and ask it to list or use `axiom-orchestrator`. Confirm a known instruction is applied. If not discovered, inspect the working root, exact `SKILL.md` path, frontmatter, and host version. The docs were checked; Axiom's behavior has not been live-tested here.

Official reference: [Codex skills](https://developers.openai.com/codex/skills).
