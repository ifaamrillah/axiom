---
name: technical-research
description: Answer external technical questions about libraries, APIs, frameworks, migrations, and version-specific behavior from authoritative current documentation and source code, pinned to the project's actual versions and cited. Use when project knowledge is insufficient, when writing code against a library API, or when a decision depends on current external facts.
---

# Technical Research

## Purpose

Replace recalled knowledge with verified, version-matched facts. Training data and old blog posts drift. The project's lockfile and the library's own docs and source do not.

## Procedure

1. **Frame** the exact question, the decision it informs, and the constraints.
2. **Pin versions** from manifests and lockfiles (`package-lock.json`, `poetry.lock`, `go.sum`, `Cargo.lock`, …). Research the installed version, not the latest, unless the question is about upgrading.
3. **Query one concept at a time.** A combined query ("routing and auth and caching") returns shallow results for each. Ask separately unless the question is how the concepts interact.
4. **Use sources in order of authority:**
   1. Official docs, reference, release notes, and migration guides for that version.
   2. The library's source at the matching tag, for exact facts that docs often omit: signatures, defaults, option names, and where an error message comes from.
   3. Standards and specifications (RFC, W3C, language spec).
   4. A documentation index (for example a Context7-style service, see [documentation search](../../../integrations/context7/README.md)) to speed up steps 1–2, when available.
   5. Community sources only to corroborate, and labeled as such.
5. **Budget the lookups.** Most questions need 1–4 queries. Stop at about 6 per question and report what is still uncertain instead of searching indefinitely.
6. **Prove locally** when a fact is decisive and cheap to test: a tiny script or test against the installed version beats any document.
7. **Record** each finding with the source (title and URL, or repository path at a tag), the version scope, the access date, and the key fact. Summarize implications and alternatives without dumping raw documentation into the context.

## Outputs

A concise research brief: question, versions, findings with citations, local proof (if any), recommendation, alternatives, and limitations.

## Quality

Never fabricate citations, versions, APIs, or options. If the docs and the source disagree, trust the source for implemented behavior and report the drift. Label inferences as inferences. Do not include private project code or data in queries to external services.
