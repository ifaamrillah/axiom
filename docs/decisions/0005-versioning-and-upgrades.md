# ADR-0005: Versioned releases and an upgrade path for consuming projects

- **Status:** Accepted
- **Date:** 2026-11-17
- **Refines:** [ADR-0003](0003-release-versioning.md)

## Context

Projects install Axiom as a Claude Code plugin, through `npx skills`, or by copying or linking `.agents/skills/`. ADR-0003 chose semantic version labels but no release had been cut, the plugin manifest had no `version`, and consumers had no way to tell which Axiom they run or what changed since.

## Decision

1. **One version, four places.** The version lives in `.claude-plugin/plugin.json` (`version`), the kernel heading (`# Axiom Kernel (vX.Y.Z)`), the Axiom block marker (`<!-- axiom:begin vX.Y.Z -->`), and the first released section of `CHANGELOG.md`. The validator fails when they disagree.
2. **Tags are `vX.Y.Z`** on `main`. Each tag has release notes in `docs/releases/vX.Y.Z.md`, which are also the text of the GitHub release.
3. **What each number means for a skills harness:**

| Bump | When | Examples |
|---|---|---|
| MAJOR | A consuming project must change something to keep working | A skill removed or renamed; a kernel rule reversed; the `.axiom/` layout or a template's required fields changed incompatibly |
| MINOR | New capability; existing projects keep working | A new skill, reference, mode, command, or workflow; a new gate that tightens behavior; description changes that move routing |
| PATCH | Corrections with no new capability | Wording fixes, broken links, eval records, tooling fixes |

4. **Before 1.0.0**, a MINOR release may include breaking changes. Each one is listed under **Breaking** in the changelog and the release notes, with the upgrade step.
5. **Every release says whether the kernel changed.** A project that pasted the Axiom block into `AGENTS.md` or `CLAUDE.md` must re-paste it when it did; skill updates alone do not touch that file.

## Consequences

- Consumers can pin a tag (`#v0.1.0`), check the installed version in the kernel heading, and read one release note per version.
- A release needs one PR that bumps all four places, moves the Unreleased changelog entries under the new version, and adds the release notes. Tagging and publishing the GitHub release remain separate actions that need explicit authorization.
