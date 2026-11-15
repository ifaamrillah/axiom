# Fixture: Equivalent Skill Use Across Hosts

## Prompt

Use Axiom to fix a small, reproducible defect in an unfamiliar repository. The host may be Claude Code, Codex, OpenCode, or Antigravity. No optional MCP servers or external integrations are configured.

## Procedure

Run the same prompt and equivalent repository snapshot once per host. Record host/version, skill discovery path, whether `axiom-orchestrator` loads its references, selected workflow, verification claims, and any manual setup. Do not infer a host result from another host.

## Expected signals

- Uses the host's documented discovery mechanism; Claude Code uses the adapter copy/link path.
- Selects Bug Fix after enough context is established; does not require all hosts to share identical tools.
- Falls back to repository files and sequential work when integrations or delegation are unavailable.
- Keeps stage status and quality-gate outcome distinct.
- Reports each host separately as tested, failed, or untested.

## Result record

No host executions are included in this fixture. Add dated observations only after live runs; do not treat this scenario as evidence of compatibility.
