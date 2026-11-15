# Generic Host Guidance

Use a host that supports the Agent Skills directory convention. Expose each skill folder containing `SKILL.md` in the host's documented project or global skill directory. Preserve each folder's neighboring references. If a host cannot load skills, read the relevant `SKILL.md` and workflow as ordinary Markdown; do not claim automatic discovery or orchestration.

To keep the Axiom kernel loaded, paste the [Axiom block](../../templates/project/agents-md-block.md) into the host's always-loaded instructions file.
