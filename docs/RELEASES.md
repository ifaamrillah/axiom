# Release Guidance

Versions follow [ADR-0005](decisions/0005-versioning-and-upgrades.md): tags `vX.Y.Z` on `main`, one release-notes page per tag. Consumers update with [Upgrading](UPGRADING.md).

## Cutting a release

1. **Pick the number** from the Unreleased changelog entries: anything Breaking means MAJOR (MINOR before 1.0.0), new capability means MINOR, fixes only mean PATCH.
2. **Bump it in all four places** in one PR: `.claude-plugin/plugin.json` `version`, the kernel heading `# Axiom Kernel (vX.Y.Z)`, the block marker in `templates/project/agents-md-block.md`, then run `python3 scripts/validate_repository.py --sync`.
3. **Move the changelog:** rename the Unreleased entries into `## [X.Y.Z] - YYYY-MM-DD` and leave an empty Unreleased section above it.
4. **Write the notes** in `docs/releases/vX.Y.Z.md` from [the template](../templates/releases/notes.md), and add a row to the [index](releases/README.md). State whether the kernel changed: compare `kernel.md` with the previous tag (`git diff vPREV -- .agents/skills/axiom-orchestrator/references/kernel.md`), ignoring the heading line.
5. **Verify:** validator, `run_evals.py --check`, tooling tests, and a live trigger run when skills or descriptions changed. Link the records in the notes.
6. **Merge the PR.**
7. **Tag and publish** (needs explicit authorization each time):

   ```bash
   git tag -a vX.Y.Z -m "Axiom vX.Y.Z" && git push origin vX.Y.Z
   ```

   The notes page uses links relative to `docs/releases/`, which break on the GitHub release page. Publish a copy with absolute links to the tag:

   ```bash
   B=https://github.com/ifaamrillah/axiom/blob/vX.Y.Z; sed -e "s#](\.\./\.\./#]($B/#g" -e "s#](\.\./#]($B/docs/#g" docs/releases/vX.Y.Z.md > /tmp/axiom-vX.Y.Z-notes.md
   ```

   ```bash
   gh release create vX.Y.Z --title "Axiom vX.Y.Z" --notes-file /tmp/axiom-vX.Y.Z-notes.md --verify-tag
   ```

   Check that `grep -c '](\.\.' /tmp/axiom-vX.Y.Z-notes.md` prints `0` before publishing. Links within `docs/releases/` (such as `](v0.1.0.md)`) are not rewritten; avoid them in notes pages.

The validator fails when the four version places or the newest changelog heading disagree, or when the notes page for the current version is missing.

Before any release, also review compatibility status, the license, and unresolved security or migration concerns.
