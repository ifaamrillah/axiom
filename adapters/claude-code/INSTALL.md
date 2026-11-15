# Claude Code Adapter

## Project-level use

Claude Code documents project skills under `.claude/skills/<skill-name>/SKILL.md`; Axiom's canonical source remains `.agents/skills/` for the other selected hosts. To expose Axiom skills to Claude Code, create a symlink for each selected skill directory under `.claude/skills/`, or copy the directories when symlinks are unsuitable. Do not edit the canonical copy through a generated duplicate without checking the source.

Example from the repository root (review the target before running):

```sh
mkdir -p .claude/skills
ln -s ../../.agents/skills/axiom-orchestrator .claude/skills/axiom-orchestrator
```

The relative link target above assumes `.claude/skills/` is two levels below repository root; validate it with `readlink` or directory listing on the target system. Filesystem and Windows symlink permissions vary, so copying is a fallback.

## Verify

Start/refresh Claude Code and confirm the skill appears and its references resolve. Host-specific invocation and permission behavior may vary by version. Axiom has not been live-tested in Claude Code here.

Official reference: [Claude Code skills](https://docs.anthropic.com/en/docs/claude-code/skills).
