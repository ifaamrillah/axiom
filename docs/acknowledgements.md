# Acknowledgements

Axiom's M8–M12 work adapted ideas from these open-source projects. All text in Axiom is our own wording, and no files were copied. Each project is MIT-licensed unless noted.

| Project | Ideas adapted | Where in Axiom |
|---|---|---|
| [obra/superpowers](https://github.com/obra/superpowers) | Iron-law discipline skills with rationalization tables; verification before completion; root-cause debugging; fresh subagent per task with two-stage review; rulings instead of stalls; skill writing as TDD; session-start bootstrap | `verification-before-completion`, `tdd`, `debugging`, `agents/prompts/`, execution reference, `skill-factory`, Claude Code adapter hook |
| [addyosmani/agent-skills](https://github.com/addyosmani/agent-skills) | Trigger evals with positive and negative owners; constraint-driven development; doubt-driven development; definition of done; source-driven development | `evaluations/cases/`, `quality-constraints`, adversarial review, definition of done, `technical-research` |
| [multica-ai/andrej-karpathy-skills](https://github.com/multica-ai/andrej-karpathy-skills) | Compact behavioral baseline (think first, simplicity, surgical changes, goal-driven verification) | Axiom kernel |
| [github/spec-kit](https://github.com/github/spec-kit) (MIT) | Clarification markers; clarification taxonomy; checklists as unit tests for requirements; cross-artifact analysis; append-only convergence; constitution gate and complexity tracking; `[P]` task markers | `requirements-analysis`, `spec-analysis`, spec, plan, and constitution templates |
| [bmad-code-org/BMAD-METHOD](https://github.com/bmad-code-org/BMAD-METHOD) | Ready-for-Development standard; single-goal scope standard; step-file just-in-time loading; plan status frontmatter for resume; layered project customization; recording agent pitfalls | `task-planning`, feature-development `stages/`, plan template, `.axiom/config.md`, Axiom block pitfalls |
| [Yeachan-Heo/oh-my-claudecode](https://github.com/Yeachan-Heo/oh-my-claudecode) | Baseline-relative verification gates; read-only critic with gap analysis and perspectives; blast-radius classification; ambiguity-scored interviews; role capability tiers | Execution reference, `code-review` references, `product-discovery` deep mode, role metadata |
| [cloudflare/security-audit-skill](https://github.com/cloudflare/security-audit-skill) | Guidance vs full-audit modes; six-element finding requirement; severity anchors; `needs_validation` without severity; coverage ledger with fingerprints; refuting verifiers; profiles and budget; sandbox rules | `security-audit` and its references |
| [nextlevelbuilder/ui-ux-pro-max-skill](https://github.com/nextlevelbuilder/ui-ux-pro-max-skill) | Priority-ordered UI rule table with numeric checks; design-system master plus page overrides; never assume the stack | `ui-ux-design`, design master template |
| [microsoft/playwright-cli](https://github.com/microsoft/playwright-cli) (Apache-2.0) | CLI plus skill as a token-efficient alternative to MCP; visual evidence in PRs | Browser automation integration, `e2e-testing` |
| [upstash/context7](https://github.com/upstash/context7) | Resolve, then query one concept at a time, then read the source for exact facts, with a call budget | `technical-research`, documentation search integration |
| [abryant710/auto-codebase-documenter](https://github.com/abryant710/auto-codebase-documenter) | Incremental "skip what is unchanged" documentation (as freshness metadata, not per-file generation) | Document contract freshness metadata |

## Skill depth pass (2026-11-17)

A second pass deepened all 24 skills with references: checklists, worked examples, anti-pattern catalogs, and per-language or per-stack notes. All text was rewritten in Axiom's own words. Each new reference ends with a `Sources:` line naming what it adapted. A check on 12-word phrases found at most 3.7% overlap per file with these repositories, all of it short phrases. Projects without a license or with an unclear one (andrej-karpathy-skills, BMAD-METHOD) were used for ideas only.

| Project | Main source material | Axiom skills |
|---|---|---|
| cloudflare/security-audit-skill | Attack-class guides, reconnaissance, hunting, validation and reporting guides | `security-audit` (13 references) |
| nextlevelbuilder/ui-ux-pro-max-skill | Style, color, typography, UX-guideline, chart, motion, and per-stack data (condensed, not copied) | `ui-ux-design` |
| obra/superpowers | TDD and testing anti-patterns, systematic debugging and its references, verification, code-review exchange, brainstorming, plans, subagent-driven development, worktrees, skill writing and pressure testing | `tdd`, `debugging`, `verification-before-completion`, `code-review`, `product-discovery`, `task-planning`, `implementation`, `axiom-orchestrator`, `skill-factory`, `skill-evaluator` |
| addyosmani/agent-skills | Code review, constraints, doubt, security hardening, TDD and testing patterns, debugging, idea refinement, spec-driven development, planning, incremental implementation, API design, ADRs, shipping, source-driven development, context engineering | Most skills |
| github/spec-kit | Spec, plan, and tasks templates; clarify, analyze, checklist, converge, and implement commands | `requirements-analysis`, `spec-analysis`, `task-planning` |
| microsoft/playwright-cli | Snapshot, act, verify; sessions and storage state; tracing; test generation | `e2e-testing` |
| upstash/context7 | Library resolution and documentation lookup protocol | `technical-research` |
| yeachan-heo/oh-my-claudecode | Agent catalog, verifier, explore agent, deep-init, persistence loop | `axiom-orchestrator`, `codebase-exploration`, `project-onboarding`, `skill-evaluator` |
| abryant710/auto-codebase-documenter | What to document for each file and module | `project-onboarding` |


## Adoption pass (2026-11-17)

A comparison with sixteen skill and tooling projects added the ideas below, rewritten in Axiom's own words. Ideas already present in Axiom (finding format with a trigger, read-versus-inferred labels, stable requirement IDs, "Not covered" in reviews) were not added again. Tools that need a binary or CLI were not adopted; Axiom stays Markdown-only.

| Project | License | Ideas adapted | Where in Axiom |
|---|---|---|---|
| [dietrichgebert/ponytail](https://github.com/dietrichgebert/ponytail) | MIT | Reuse-first decision ladder; never-cut list; `shortcut:` markers reviewed as decisions | Kernel rule 2, `implementation/references/simplicity.md`, `code-review` rules |
| [Fission-AI/OpenSpec](https://github.com/Fission-AI/OpenSpec) | MIT | Delta specs (ADDED, MODIFIED, REMOVED, RENAMED), full-block rule for MODIFIED, archive-and-merge, reverse check for removed behavior | `requirements-analysis/references/change-proposals.md`, change template, `spec-analysis` converge |
| [pbakaus/impeccable](https://github.com/pbakaus/impeccable) | Apache-2.0 | Verify and Refuse lists with stable IDs; unanchored critique with a degraded banner; heuristic scores with `n/a`; surface modes; mode vocabulary (critique, audit, polish, harden) | `ui-ux-design` modes, `craft-floor.md`, `critique.md`, design master |
| [blader/humanizer](https://github.com/blader/humanizer) | MIT | Tell catalog ordered by strength; fact check before style check; review, file, and embedded output modes | `writing-quality` |
| [mattpocock/skills](https://github.com/mattpocock/skills) | MIT | Feedback-loop gate before hypotheses; throwaway prototypes; session retros; user-invoked commands | `debugging`, `architecture-design`, `project-documentation`, Claude Code commands |
| [bmad-code-org/BMAD-METHOD](https://github.com/bmad-code-org/BMAD-METHOD) | unclear | Claims check: treat the plan and report as testimony and try to refute them (ideas only) | Orchestrator review loop |
| [obra/superpowers](https://github.com/obra/superpowers) | MIT | Record the base commit before dispatch; never diff against `HEAD~1` | Orchestrator delegation and review loop |
| [addyosmani/agent-skills](https://github.com/addyosmani/agent-skills) | MIT | "Even when it looks obvious" description clauses; performance, CI/CD, and observability skills; `/ship` fan-out to GO or NO-GO | `debugging`, `tdd`, `verification-before-completion` descriptions; `performance-optimization`; `ci-and-observability`; `/axiom:ship` |
| [nextlevelbuilder/ui-ux-pro-max-skill](https://github.com/nextlevelbuilder/ui-ux-pro-max-skill) | MIT | Phased rendered review at fixed viewports | `ui-ux-design/references/critique.md` |
| [DeusData/codebase-memory-mcp](https://github.com/DeusData/codebase-memory-mcp) | MIT | Negative claims need a search record; coverage check before relying on graph results | `codebase-exploration` search recipes, `integrations/codebase-memory/` |
| [rtk-ai/rtk](https://github.com/rtk-ai/rtk) | Apache-2.0 | Trust condensed output except on three conditions; rerun uncondensed for evidence | `integrations/rtk/`, `verification-before-completion` reading output |
| [github/spec-kit](https://github.com/github/spec-kit) | MIT | Bug-fix verdicts: verified, partial, failed | Bug Fix workflow |
| [addyosmani/agent-skills](https://github.com/addyosmani/agent-skills) | MIT | Offline TF-IDF routing check with a collision threshold | `run_evals.py --routing`, `--check` |
| [bmad-code-org/BMAD-METHOD](https://github.com/bmad-code-org/BMAD-METHOD) | unclear | Variant evals that test whether a section earns its place (ideas only) | `skill-evaluator` eval design |
| [obra/superpowers](https://github.com/obra/superpowers) | MIT | A byte budget for skills tied to re-attachment after compaction | `validate_repository.py` |
| [Graphify-Labs/graphify](https://github.com/Graphify-Labs/graphify) | Apache-2.0 | Query an existing graph first; build-or-grep cost gate; inferred edges are hypotheses | `integrations/codebase-memory/` |
