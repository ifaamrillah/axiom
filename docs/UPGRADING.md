# Upgrading Axiom

How to see which Axiom a project runs, update it, and pin a version. Versions follow [ADR-0005](decisions/0005-versioning-and-upgrades.md). Each release has a page in [release notes](releases/README.md).

## 1. Check what you have

| Install | Check |
|---|---|
| Any | Ask the agent: "Which Axiom version is loaded?" It reads the kernel heading, `# Axiom Kernel (vX.Y.Z)`. |
| Copied or `npx skills` | `head -1 .agents/skills/axiom-orchestrator/references/kernel.md` (or `.claude/skills/…` when `npx skills` installed for Claude Code only) |
| Pasted Axiom block | The marker in `AGENTS.md` or `CLAUDE.md`: `<!-- axiom:begin vX.Y.Z -->` |
| Claude Code plugin | `claude plugin list` |

No version in the heading or marker means the copy predates v0.1.0.

## 2. Read the release notes

Open every [release note](releases/README.md) between your version and the target. For each one, note:

- **Kernel changed: yes** means re-pasting the Axiom block (step 4).
- **Breaking** entries list a step you must take: a renamed skill, a moved template, a changed `.axiom/` file.

## 3. Update the skills

### Claude Code plugin

```bash
claude plugin marketplace update axiom
```

```bash
claude plugin update axiom@axiom
```

Restart Claude Code to apply. The plugin hook loads the new kernel on its own; skip step 4.

To stay on one version, add the marketplace at a tag instead: `claude plugin marketplace add "https://github.com/ifaamrillah/axiom.git#v0.1.0"`.

### `npx skills`

```bash
npx skills check
```

```bash
npx skills update
```

`skills-lock.json` records the source and commit, so commit it with the update. `#ref` accepts a branch or tag, not a commit SHA. To pin a version, install from a tag: `npx skills add ifaamrillah/axiom#v0.1.0`.

### Clone with symlinks

If `.claude/skills/` or `.agents/skills/` link into a clone of Axiom, update the clone:

```bash
git -C ~/axiom fetch --tags
```

```bash
git -C ~/axiom checkout v0.1.0
```

Use the target tag in place of `v0.1.0`. Links pick up the change; check that no skill you link was removed (see the Breaking section of the notes).

### Copied skills

Commit or stash your project first, so the update is one reviewable diff. Then replace each Axiom skill directory with the release's copy. This touches only directories that exist in Axiom; your own skills stay.

```bash
git -C ~/axiom fetch --tags && git -C ~/axiom checkout v0.1.0
```

```bash
test -f ~/axiom/.agents/skills/axiom-orchestrator/SKILL.md && for d in ~/axiom/.agents/skills/*/; do [ -f "$d/SKILL.md" ] || continue; n="$(basename "$d")"; rm -rf ".agents/skills/$n" && cp -R "$d" ".agents/skills/$n"; done
```

The `test -f` guard stops the loop when the clone path is wrong, and each directory is replaced only if it is an Axiom skill.

Review `git diff --stat .agents/skills`. If you had edited an Axiom skill locally, re-apply that edit from the diff, or better, move it to your project instructions so the next update keeps it. Delete any skill the release notes list as removed.

## 4. Re-paste the kernel when it changed

Only when a release note between your version and the target says **Kernel changed: yes**, and only if you pasted the Axiom block (the Claude Code plugin does not need this):

1. Open `AGENTS.md` or `CLAUDE.md` and find the block between `<!-- axiom:begin … -->` and `<!-- axiom:end -->`.
2. Replace its Behavior, Routing, and Proportionality sections with the new ones from `.agents/skills/axiom-orchestrator/references/kernel.md`.
3. Update the marker to the new version.
4. Keep your **Project facts** and **Pitfalls** sections as they are.

## 5. Check the result

In a new session, ask: "Which Axiom version is loaded, and which skill handles a failing test?" The answer should name the new version and `debugging`.

## Let the agent do it

Paste this into your agent, with the target version:

```text
Update Axiom in this project to v0.1.0 by following
https://github.com/ifaamrillah/axiom/blob/main/docs/UPGRADING.md.
Read the release notes between our current version and v0.1.0 first.
Keep my Project facts and Pitfalls. Show me the diff before committing.
```

The agent runs the commands above. Network access and any install commands still need your approval.
