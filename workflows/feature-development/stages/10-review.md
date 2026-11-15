# Stage 10: Independent code review

**Skill:** `code-review` · **Required:** yes for substantial or security-sensitive changes; a self-review for trivial ones · **Depends on:** stages 7 and 8

## Do

1. Review the whole change with a fresh, read-only reviewer: spec compliance first, then gap analysis, lenses, and bar-lowering detection.
2. Run the fix loop (at most 3 rounds) for blocking findings.

## Exit

Blocking findings are fixed or explicitly escalated.
