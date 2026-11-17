#!/bin/sh
# Axiom SubagentStart hook for Claude Code.
# SessionStart context does not reach subagents, so this hook gives each subagent the
# platform-neutral Axiom kernel. SubagentStart ignores plain stdout; it reads context
# from JSON `hookSpecificOutput.additionalContext`, so the kernel is JSON-escaped here.
# Read-only: no network, no writes, no side effects. Prints nothing if the kernel is missing.
if [ -n "${CLAUDE_PLUGIN_ROOT:-}" ]; then
  root="$CLAUDE_PLUGIN_ROOT"
else
  root="$(CDPATH= cd -- "$(dirname -- "$0")/../../.." && pwd)"
fi
kernel="$root/.agents/skills/axiom-orchestrator/references/kernel.md"
if [ -r "$kernel" ]; then
  awk '
    BEGIN { bs = sprintf("%c", 92) }
    {
      line = ""
      for (i = 1; i <= length($0); i++) {
        c = substr($0, i, 1)
        if (c == bs) c = bs bs
        else if (c == "\"") c = bs "\""
        else if (c == "\t") c = bs "t"
        else if (c == "\r") c = ""
        line = line c
      }
      out = out (NR > 1 ? bs "n" : "") line
    }
    END {
      printf "{\"hookSpecificOutput\":{\"hookEventName\":\"SubagentStart\",\"additionalContext\":\"%s\"}}\n", out
    }
  ' "$kernel"
fi
exit 0
