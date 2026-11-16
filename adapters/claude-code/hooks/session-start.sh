#!/bin/sh
# Axiom SessionStart hook for Claude Code.
# Prints the platform-neutral Axiom kernel to stdout; Claude Code adds SessionStart
# stdout to the session context. Read-only: no network, no writes, no side effects.
# Root resolution: the plugin root when installed as a plugin, otherwise this
# file's location (adapters/claude-code/hooks -> repository root).
if [ -n "${CLAUDE_PLUGIN_ROOT:-}" ]; then
  root="$CLAUDE_PLUGIN_ROOT"
else
  root="$(CDPATH= cd -- "$(dirname -- "$0")/../../.." && pwd)"
fi
kernel="$root/.agents/skills/axiom-orchestrator/references/kernel.md"
if [ -r "$kernel" ]; then
  cat "$kernel"
fi
exit 0
