# Stage 2: Technical research

**Skill:** `technical-research` · **Required:** conditional · **Depends on:** stage 1

## Entry

Run this stage when correctness depends on external, current, or version-specific facts that verified project context does not cover (library APIs, platform limits, migration guides).

## Do

1. Resolve the exact library or platform versions from manifests and lockfiles.
2. Query authoritative docs one concept at a time; read the source for exact facts (signatures, defaults).
3. Record each source, version, and access date, plus the finding.

## Exit

Material external assumptions are verified or recorded as unresolved. The research brief is linked from the workflow state.
