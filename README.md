# Axiom

**Portable engineering skills for AI coding agents. Evidence before claims.**

Axiom packages the habits of a careful senior engineer as skills that agents load on demand:
- reproduce before fixing;
- watch the test fail first;
- review for what is missing;
- never say "done" without proof.

The same Markdown works in Claude Code, Codex, OpenCode, and Antigravity. There is nothing to run: no runtime, no server, no CLI.

```
 UNDERSTAND      DEFINE         PLAN          BUILD         VERIFY         SHIP
 ┌────────┐    ┌────────┐    ┌────────┐    ┌────────┐    ┌────────┐    ┌────────┐
 │Onboard │ ─▶ │  Idea  │ ─▶ │ Tasks  │ ─▶ │  TDD   │ ─▶ │ Review │ ─▶ │Release │
 │Explore │    │  Spec  │    │ Design │    │ Debug  │    │Security│    │  Docs  │
 └────────┘    └────────┘    └────────┘    └────────┘    └────────┘    └────────┘
        always on: the kernel (rules plus routing) · on demand: 24 skills
```

> **Status:** pre-1.0. Measured on Claude Code and Codex (November 2026). See [Evidence](#evidence).

---

## What you ask → what Axiom does

You don't need commands or skill names. Describe the task. The always-on **kernel** routes it to the right skill.

| What you're doing | Say something like | Skill | Key principle |
|---|---|---|---|
| Understand a repo | "Onboard me to this repository" | `project-onboarding` | Verified facts, not guesses |
| Shape an idea | "Help me shape a loyalty discount" | `product-discovery` | One question at a time |
| Specify it | "Write a spec for it" | `requirements-analysis` | Mark unknowns, don't invent them |
| Plan it | "Plan the work, don't implement yet" | `task-planning` | Small tasks, each with a check |
| Build it test-first | "Use TDD to add a coupon code" | `tdd` | See it fail before you make it pass |
| Fix a bug | "`apply_discount` returns 0, should be 900" | `debugging` | Reproduce before fixing |
| Review it | "Review this PR before I merge" | `code-review` | Acceptance first, then what's missing |
| Check security | "Audit this service for vulnerabilities" | `security-audit` | Only real trust-boundary issues, with evidence |
| Finish | "Ship it" / "go ahead and commit" | `verification-before-completion` | No claim without fresh output |
| Release | "Cut release 1.2.0" | `release-management` | Preparing is not permission to publish |

For multi-step work the `axiom-orchestrator` skill picks a [workflow](#workflows), delegates to subagents where safe, and keeps state in Markdown so a later session can resume. To force a skill, name it: "use the security-audit skill", or `axiom:security-audit` in Claude Code.

---

## Quick Start

**Fastest path: Claude Code plugin.** Run inside Claude Code, one line at a time:

```text
/plugin marketplace add ifaamrillah/axiom
/plugin install axiom@axiom
```

This installs:
- all 24 skills;
- the kernel, loaded automatically by a session-start hook;
- four [subagents](#subagents).

Nothing else is needed.

**Any agent, one command.** The third-party [skills CLI](https://github.com/vercel-labs/skills) copies the skills into the agents you choose:

```bash
npx skills add ifaamrillah/axiom
```

```bash
npx skills add ifaamrillah/axiom --skill debugging
```

> **Two things to know about `npx skills`.**
> - It installs skills only. Each skill carries the templates it fills, but the [workflows](#workflows) are not included.
> - It does not load the kernel. Paste the [Axiom block](templates/project/agents-md-block.md) into your `AGENTS.md` (or `CLAUDE.md`) after installing.

Prefer a manual setup? Pick your tool:

<details>
<summary><b>Claude Code: without the plugin</b></summary>

Link the skills into the project and paste the kernel into `CLAUDE.md`:

```bash
git clone https://github.com/ifaamrillah/axiom.git ~/axiom
```

```bash
mkdir -p .claude/skills && for d in ~/axiom/.agents/skills/*/; do ln -s "$d" ".claude/skills/$(basename "$d")"; done
```

Then copy the block from [`templates/project/agents-md-block.md`](templates/project/agents-md-block.md) into `CLAUDE.md`. Full guide, including the optional hook: [adapters/claude-code](adapters/claude-code/INSTALL.md).

</details>

<details>
<summary><b>Codex</b></summary>

Codex reads skills from the project's `.agents/skills/`:

```bash
git clone https://github.com/ifaamrillah/axiom.git ~/axiom
```

```bash
mkdir -p .agents/skills && cp -R ~/axiom/.agents/skills/* .agents/skills/
```

Paste the [Axiom block](templates/project/agents-md-block.md) into `AGENTS.md`. Guide: [adapters/codex](adapters/codex/INSTALL.md).

</details>

<details>
<summary><b>OpenCode</b></summary>

OpenCode also reads `.agents/skills/`. Use the same copy step as Codex, then paste the Axiom block into `AGENTS.md`. To confirm discovery, run `opencode debug skill` from the project root. Guide: [adapters/opencode](adapters/opencode/INSTALL.md).

</details>

<details>
<summary><b>Antigravity</b></summary>

Antigravity reads workspace `.agents/skills/` (and `~/.gemini/config/skills/` globally). Copy the skills, then paste the Axiom block into `AGENTS.md`. Guide: [adapters/antigravity](adapters/antigravity/INSTALL.md).

</details>

<details>
<summary><b>Any other Agent Skills host</b></summary>

Copy `.agents/skills/` to wherever your host discovers `SKILL.md` folders, and put the Axiom block in the instruction file your host always loads. If your host has no skill discovery, the agent can read `SKILL.md` files directly as Markdown. Guide: [adapters/generic](adapters/generic/INSTALL.md).

</details>

**Check the install.** In a new session, ask:

```text
What is rule 5 of the Axiom kernel, and which skill handles a failing test?
```

A correct answer quotes **"Reproduce before fixing"** and names **`debugging`**.

---

## Adoption

- **New project:** start with `project-onboarding`, then let `axiom-orchestrator` run [Feature Development](workflows/feature-development/WORKFLOW.md) for each feature.
- **Existing codebase:**
  1. Install the skills.
  2. Paste the Axiom block, filling in your verified test and build commands.
  3. Let the kernel route everyday work.
  4. Each time an agent makes a real mistake in your repository, add one line to the block's **Pitfalls** list. That list is the cheapest way to make Axiom fit your project.
- **Raising the bar:** run `quality-constraints` once to write down numeric thresholds in `.axiom/CONSTRAINTS.md`. Reviews then flag any change that quietly lowers them.

---

## All 24 Skills

Each skill is a folder with a short `SKILL.md` (the procedure, under 130 lines) and `references/` that the agent opens only when needed. The references hold checklists, worked examples, anti-pattern catalogs, and per-language notes.

### Orchestrate: route and coordinate

| Skill | What it does | Use when |
|---|---|---|
| [axiom-orchestrator](.agents/skills/axiom-orchestrator/SKILL.md) | Picks the smallest workflow, routes to skills, delegates with file ownership, enforces gates, resumes from Markdown state | Multi-step or multi-agent work |

### Understand: learn the codebase

| Skill | What it does | Use when |
|---|---|---|
| [project-onboarding](.agents/skills/project-onboarding/SKILL.md) | Verifies commands, maps stack and conventions, and writes only the project notes the repository lacks | First session in a repository |
| [codebase-exploration](.agents/skills/codebase-exploration/SKILL.md) | Search recipes per question type and entry-point maps per ecosystem; answers with `file:line` evidence | "Where is X, who calls Y", impact analysis |
| [technical-research](.agents/skills/technical-research/SKILL.md) | Pins facts to your lockfile versions, uses authoritative sources, proves facts locally, cites them | Library or API behavior questions |
| [codebase-onboarding](.agents/skills/codebase-onboarding/SKILL.md) | Alias of `project-onboarding` | Older references |

### Define: decide what to build

| Skill | What it does | Use when |
|---|---|---|
| [product-discovery](.agents/skills/product-discovery/SKILL.md) | 12 elicitation techniques, one question at a time with a recommended answer, approval before building | The idea is vague |
| [requirements-analysis](.agents/skills/requirements-analysis/SKILL.md) | User stories, numbered requirements, Given/When/Then scenarios, `[NEEDS CLARIFICATION]` markers, an NFR catalog | Writing a spec |
| [spec-analysis](.agents/skills/spec-analysis/SKILL.md) | Checks consistency across spec, plan, and tasks (read-only), or appends the remaining work after implementation | Before building, or "what's left?" |
| [quality-constraints](.agents/skills/quality-constraints/SKILL.md) | A numeric quality bar with ratchets and waivers, plus grep patterns that detect skipped tests and suppressions | Writing the bar down, or catching it being lowered |

### Design and Plan: decide how

| Skill | What it does | Use when |
|---|---|---|
| [architecture-design](.agents/skills/architecture-design/SKILL.md) | Option comparison, ADRs, a pattern catalog, data modeling, API rules (REST, GraphQL, gRPC), safe migrations | Cross-cutting or structural changes |
| [ui-ux-design](.agents/skills/ui-ux-design/SKILL.md) | Screen states, WCAG thresholds, style, palette, and type tables, design tokens, per-stack notes | Any user-facing change |
| [task-planning](.agents/skills/task-planning/SKILL.md) | Ready-for-development plans: S–M tasks, vertical slices, exact files, a check per task, checkpoints | Before multi-step or delegated work |

### Build: write the code

| Skill | What it does | Use when |
|---|---|---|
| [implementation](.agents/skills/implementation/SKILL.md) | Thin slices with a step → verify loop, convention discovery, and branch finishing | Building a planned change |
| [tdd](.agents/skills/tdd/SKILL.md) | Red → green → refactor with examples in Python, TypeScript, and Go; 13 testing anti-patterns; legacy-code seams | New behavior or a regression test |
| [debugging](.agents/skills/debugging/SKILL.md) | Technique chosen by symptom, `git bisect run`, instrumentation in 5 languages, escalation after 3 failed fixes | Bugs, failing or flaky tests, regressions |

### Verify: prove it works

| Skill | What it does | Use when |
|---|---|---|
| [testing](.agents/skills/testing/SKILL.md) | Test-layer selection, fixtures, flaky-test triage, and commands for pytest, Vitest, Jest, Go, JUnit, PHPUnit/Pest, and RSpec | Planning or running tests |
| [e2e-testing](.agents/skills/e2e-testing/SKILL.md) | Playwright locators, waiting, auth reuse, traces as evidence, flake triage, CLI exploration | Browser or user-journey checks |
| [code-review](.agents/skills/code-review/SKILL.md) | Acceptance first; defect patterns with code in 6 languages; checklists per language; checks for AI-generated code | Reviewing a diff, branch, or plan |
| [security-audit](.agents/skills/security-audit/SKILL.md) | Guidance or full-audit mode; 13 references by vulnerability class and framework; harmless validation; calibrated severity | Security questions and audits |
| [verification-before-completion](.agents/skills/verification-before-completion/SKILL.md) | The evidence each claim needs, how to read output honestly, how to verify delegated work | Before "done", commit, or PR |

### Ship: release and document

| Skill | What it does | Use when |
|---|---|---|
| [release-management](.agents/skills/release-management/SKILL.md) | Readiness checklist, semver table, changelog, staged rollout, rollback plans, hotfix steps | Preparing a release |
| [project-documentation](.agents/skills/project-documentation/SKILL.md) | Doc types, README, ADRs, runbooks, API docs, freshness metadata | Docs became stale or are missing |

### Meta: improve the skills themselves

| Skill | What it does | Use when |
|---|---|---|
| [skill-factory](.agents/skills/skill-factory/SKILL.md) | Writes skills test-first: eval cases before `SKILL.md`, pressure scenarios, rationalization tables | Creating or changing a skill |
| [skill-evaluator](.agents/skills/skill-evaluator/SKILL.md) | Eval design and a grading rubric for triggers and behavior | Judging whether a skill works |

---

## Subagents

The Claude Code plugin adds four subagents. Other hosts can follow the same [role cards](agents/roles/) as instructions.

| Agent | Model | Can edit? | Use |
|---|---|---|---|
| [reviewer](adapters/claude-code/agents/reviewer.md) | Opus | No | Spec compliance first, then quality, then what's missing |
| [security-reviewer](adapters/claude-code/agents/security-reviewer.md) | Opus | No | Trust-boundary issues only, with evidence |
| [researcher](adapters/claude-code/agents/researcher.md) | Haiku | No | Locate code, trace dependencies, check library facts |
| [implementer](adapters/claude-code/agents/implementer.md) | Inherits | Yes | One planned task with explicit file ownership |

Prompt templates for delegation (implementer, two-stage task reviewer, fix loop) live in [`agents/prompts/`](agents/prompts/).

---

## Workflows

Markdown playbooks with stages and gates. The orchestrator picks the smallest one that fits. Trivial changes use none.

| Workflow | When |
|---|---|
| [Codebase Onboarding](workflows/codebase-onboarding/WORKFLOW.md) | First time in a repository |
| [Feature Development](workflows/feature-development/WORKFLOW.md) | New features, from discovery through verified delivery |
| [Bug Fix](workflows/bug-fix/WORKFLOW.md) | A defect with understood scope |
| [Refactoring](workflows/refactoring/WORKFLOW.md) | Changing structure while keeping behavior, with a blast-radius check |
| [Security Audit](workflows/security-audit/WORKFLOW.md) | Full or scoped audits |
| [Performance Audit](workflows/performance-audit/WORKFLOW.md) | Measured performance work |
| [Release](workflows/release/WORKFLOW.md) | Preparing and verifying a release |

Workflow state lives in your project under `.axiom/workflows/active/<id>/` (spec, plan, tasks, decisions, handoffs), so work survives across sessions.

---

## How Skills Work

```
┌─ .agents/skills/<name>/ ─────────────────────────────┐
│  SKILL.md                                            │
│    frontmatter  name + description ("Use when …")    │
│    Purpose      what this skill guarantees           │
│    The rule     the non-negotiable, if any           │
│    Procedure    numbered steps with checks           │
│    Red flags    excuses agents use → the answer      │
│    Outputs      evidence required to finish          │
│  references/    depth, opened only when needed       │
│  assets/        templates the skill fills            │
└──────────────────────────────────────────────────────┘
```

- **Always-on kernel, on-demand skills.** The [kernel](.agents/skills/axiom-orchestrator/references/kernel.md) is about 50 lines: 8 behavior rules plus a routing table covering all 24 skills. Everything else loads only when needed.
- **Evidence is required.** Every completion claim names the command it ran and quotes the decisive output line. A skipped check is reported as skipped, never as passed.
- **Anti-rationalization.** Discipline skills (TDD, debugging, verification, quality bar, skill writing) include tables of the excuses agents use to cut corners, each with the answer.
- **Proportional.** A one-line fix gets no plan or workflow files. The project's own stricter rules always win.
- **Self-contained.** Skills link only within `.agents/skills/`, so copying one skill folder never leaves broken links. The validator enforces this.

---

## Project Structure

| Layer | Paths | Purpose |
|---|---|---|
| Portable core | `.agents/skills/` (24 skills) | Canonical `SKILL.md` folders used by every host |
| Always-on rules | `.agents/skills/axiom-orchestrator/references/kernel.md`, `templates/project/agents-md-block.md` | Kernel and the block you paste into `AGENTS.md` / `CLAUDE.md` |
| Playbooks | `workflows/` (7), `templates/` | Lifecycle workflows and the documents they fill |
| Delegation | `agents/` | Role cards, subagent prompt templates, parallel and sequential patterns |
| Claude Code adapter | `.claude-plugin/`, `adapters/claude-code/` | Plugin and marketplace manifests, session-start hook, 4 subagents |
| Other adapters | `adapters/{codex,opencode,antigravity,generic}/` | Per-host setup and verification notes |
| Optional tools | `integrations/` | Playwright, documentation search, security scanners, each with a fallback |
| Rules of the project | `core/` | Architecture, principles, contracts, policies, standards |
| Proof | `evaluations/` | Eval cases for every skill, seeded fixtures, recorded results, dogfood reports |
| Maintainer tooling | `scripts/`, `.github/workflows/` | Validator and eval runner (Python standard library), CI |
| Docs | `docs/` | Getting started, ADRs, compatibility, roadmap, credits |

---

## Why Axiom?

AI coding agents take the shortest path. In practice they:
- patch symptoms;
- write tests after the code, so the tests pass by construction;
- skip a failing test to "go green";
- say "fixed" without running anything.

Axiom makes the disciplined path the default, and it does that in a way you can inspect and measure:

- **Portable.** One set of skills for four hosts. Host-specific details live only in `adapters/`.
- **Measured, not asserted.** Every skill has runnable eval cases. Results are recorded per host and model version, including the failures.
- **Built to fit your project.** Verified project facts, a Pitfalls list, a constitution, and constraints make it your codebase's rules, not generic advice.
- **Synthesized.** It brings together the best ideas from obra/superpowers, addyosmani/agent-skills, github/spec-kit, cloudflare/security-audit-skill, ui-ux-pro-max, BMAD, and others, rewritten and credited in [acknowledgements](docs/acknowledgements.md).

---

## Evidence

| What | Result | Record |
|---|---|---|
| Trigger accuracy (right skill loaded or correctly not loaded), Claude Code 2.1.325 | **110/113** prompts, 24 skills | [run](evaluations/results/2026-11-16-1500-claude-code-trigger.md) |
| Trigger accuracy, Codex CLI 0.169.0 | **107/113** | [compatibility](docs/compatibility/README.md) |
| Behavior | All 24 cases run repeatedly. Graded by a separate Claude grader and by Codex (a non-Claude model) | [compatibility](docs/compatibility/README.md#behavior-after-the-kernel-routing-change-2026-11-16) |
| OpenCode 1.19.5 | All 24 skills discovered; model invocation not tested | [adapter](adapters/opencode/INSTALL.md) |
| Antigravity | Not tested | [adapter](adapters/antigravity/INSTALL.md) |
| Real projects | Used on Axiom itself and on a private Laravel application; the findings changed several skills | [dogfood](evaluations/dogfood/README.md) |

**Known limits:**
- **Fixtures are small.** A strong model finds the seeded issues with or without the deeper references. The added depth showed a small gain only with a weaker model, on few runs ([comparison](evaluations/results/2026-11-17-depth-comparison.md)).
- **Commands are unverified.** Commands in the references come from general practice. They have not been run in every ecosystem.
- **Grading is model-only.** No human grading yet.

---

## Contributing

Skills should be:
- **specific:** steps, not advice;
- **verifiable:** every step names its evidence;
- **portable:** no host-specific tool names;
- **lean:** depth goes in `references/`.

New or changed skills are written test-first: eval cases before `SKILL.md` (see [`skill-factory`](.agents/skills/skill-factory/SKILL.md)).

```bash
python3 scripts/validate_repository.py
```

```bash
python3 scripts/run_evals.py --check
```

```bash
python3 -m unittest discover -s scripts/tests
```

The first checks structure, links, and the sync of bundled assets (add `--sync` after editing a bundled template). The second checks that eval case files are well formed, and the third runs the tooling tests.

```bash
python3 scripts/run_evals.py --host claude-code --kind trigger --skill debugging
```

Runs live evals against an installed host. These spend model quota.
- Hosts: `--host claude-code` or `--host codex`.
- Kinds: `--kind trigger` or `--kind behavior`.
- Behavior options: `--repeat N`, `--grade`, `--grader-host codex`, and `--case B2`.

Read [CONTRIBUTING.md](CONTRIBUTING.md) and [AGENTS.md](AGENTS.md) first. History: [changelog](CHANGELOG.md), [roadmap](docs/IMPLEMENTATION-ROADMAP.md), [decisions](docs/decisions/).

## Security

Do not commit credentials or private keys. Report vulnerabilities privately as described in [SECURITY.md](SECURITY.md).

## License

MIT. See [LICENSE](LICENSE).
