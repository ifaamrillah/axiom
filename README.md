# Axiom

**Engineering skills for AI coding agents.** Axiom is a set of Markdown skills, a short always-on rule set (the *kernel*), and workflow playbooks. Together they make agents such as Claude Code, Codex, OpenCode, and Antigravity work like disciplined engineers:
- reproduce a bug before fixing it;
- write the failing test first;
- review for what is missing;
- never claim "done" without evidence.

There is nothing to run. Axiom has no runtime, server, or CLI. Your agent reads the Markdown and follows it.

> **Status:** early development (pre-1.0). Measured on Claude Code and Codex in November 2026; see [Evidence](#evidence-and-limits). Interfaces may still change.

---

## Contents

- [What you get](#what-you-get)
- [Quick start](#quick-start)
- [How it works](#how-it-works)
- [Using Axiom day to day](#using-axiom-day-to-day)
- [Skill catalog](#skill-catalog)
- [Workflows](#workflows)
- [Files Axiom creates in your project](#files-axiom-creates-in-your-project)
- [Evidence and limits](#evidence-and-limits)
- [Repository map](#repository-map)
- [For maintainers](#for-maintainers)

---

## What you get

| Piece | What it is | Where |
|---|---|---|
| **24 skills** | One folder per engineering task: debugging, TDD, code review, security audit, specs, planning, UI/UX, release, and more. Each has a short `SKILL.md` procedure plus `references/` that the agent opens only when needed: checklists, worked examples, anti-pattern catalogs, and per-language notes. | [`.agents/skills/`](.agents/skills/) |
| **Kernel** | About 50 lines of always-on rules (reproduce before fixing, evidence before claims, ask before destructive actions) and a routing table that tells the agent which skill to load for which request. | [`kernel.md`](.agents/skills/axiom-orchestrator/references/kernel.md) |
| **Workflows** | Step-by-step playbooks for larger jobs (feature development, bug fix, refactoring, audits, release) with stages and quality gates. | [`workflows/`](workflows/README.md) |
| **Templates** | Spec, plan, task, constitution, constraints, design system, ADR-style decisions, and the block you paste into `AGENTS.md`. | [`templates/`](templates/) |
| **Evals** | Runnable cases for every skill, seeded fixture projects, and recorded results. | [`evaluations/`](evaluations/README.md) |

Skills use the open [Agent Skills](https://code.claude.com/docs/en/skills) format: a folder with a `SKILL.md` that has `name` and `description` frontmatter. Any host that supports that format can load them.

---

## Quick start

Pick your agent. Every path has the same two parts:
1. Make the skills discoverable.
2. Load the kernel.

### Claude Code (recommended: plugin)

Run these inside Claude Code, one at a time:

```text
/plugin marketplace add ifaamrillah/axiom
/plugin install axiom@axiom
```

The plugin includes:
- all 24 skills, namespaced as `axiom:debugging` and so on;
- a session-start hook that loads the kernel automatically;
- four optional subagents: `reviewer`, `security-reviewer`, `researcher`, and `implementer`.

Nothing else is needed. Details and alternatives are in the [Claude Code adapter](adapters/claude-code/INSTALL.md).

### Codex, OpenCode, Antigravity, or any Agent Skills host

These hosts read skills from your project's `.agents/skills/` folder.

```bash
git clone https://github.com/ifaamrillah/axiom.git ~/axiom
```

```bash
mkdir -p .agents/skills && cp -R ~/axiom/.agents/skills/* .agents/skills/
```

Then load the kernel: open [`templates/project/agents-md-block.md`](templates/project/agents-md-block.md), copy its block into your project's `AGENTS.md` (or `CLAUDE.md`), and fill in your test and build commands.

Host-specific notes: [Codex](adapters/codex/INSTALL.md), [OpenCode](adapters/opencode/INSTALL.md), [Antigravity](adapters/antigravity/INSTALL.md), and [other hosts](adapters/generic/INSTALL.md).

### Alternative: the `skills` installer (third party)

```bash
npx skills add ifaamrillah/axiom
```

It copies the skill folders, with their bundled templates, into the agents you select. It does not install `workflows/` or the kernel, so you still need to paste the `AGENTS.md` block. See [adapter overview](adapters/README.md) for its limits.

### Check that it works

Start a new session in your project and ask:

```text
What is rule 5 of the Axiom kernel, and which skill would you use to fix a failing test?
```

A correct answer quotes "Reproduce before fixing" and names `debugging`. If the agent cannot see the kernel, the `AGENTS.md` block or the plugin hook is missing. If it does not know the skill, the skills are not in a folder your host scans.

---

## How it works

```text
your request
    │
    ▼
kernel (always loaded) ──► rules: think first · smallest change · reproduce before fixing ·
    │                       evidence before claims · ask before risky actions
    │  routing table
    ▼
skill (loaded on demand) ─► SKILL.md: the procedure, red flags, and output format
    │
    ├─► references/*.md   opened only when needed: checklists, examples, per-language notes
    └─► assets/*.md       templates the skill fills: spec, plan, prompts
    │
    ▼
your project ─► code and tests changed; optional `.axiom/` notes, plans, and workflow state
```

- **Small requests stay small.** For a typo or a one-line fix, the agent follows the kernel rules and uses no workflow files or ceremony.
- **Bigger requests escalate.** A new feature goes through `axiom-orchestrator`, which picks a workflow such as discovery → spec → plan → TDD implementation → review → verification. It records state in Markdown so work can resume later.
- **Context stays lean.** Each skill keeps its `SKILL.md` short (under 130 lines) and puts depth in references that are read on demand.

---

## Using Axiom day to day

You don't call skills by name; describe the task normally. The kernel's routing table picks the skill. Examples:

| You say | Skill the agent loads | What changes in its behavior |
|---|---|---|
| "`apply_discount(1000, 10)` returns 0, should be 900. Fix it." | `debugging` | Reproduces with a failing test first, names the root cause, and reports the test command and its output |
| "Use TDD to add a coupon code." | `tdd` | Shows a red test with the real failure message before writing code |
| "Review this PR before I merge." | `code-review` | Checks the acceptance criteria first, then defects, missing tests, and lowered quality bars, citing `file:line` |
| "Is it safe that this endpoint takes a URL?" | `security-audit` | Answers in guidance mode and reports only real trust-boundary issues, with severity and the smallest fix |
| "I want a loyalty discount, help me shape it." | `product-discovery` | Asks one question at a time, with a recommended answer to each |
| "Write a spec for it." | `requirements-analysis` | Given/When/Then scenarios, with `[NEEDS CLARIFICATION]` markers instead of guesses |
| "Plan the work, don't implement yet." | `task-planning` | Small ordered tasks with exact file paths and a verification command for each |
| "Ship it" / "go ahead and commit" | `verification-before-completion` | Runs the checks and quotes the output before claiming anything works |
| "Cut release 1.2.0 and publish." | `release-management` | Writes a readiness report, then stops and asks before tagging or publishing |
| "Where is the cap applied and what tests cover it?" | `codebase-exploration` | Answers with `file:line` evidence and makes no edits |

To force a skill, name it: "use the security-audit skill", or `axiom:security-audit` in Claude Code.

---

## Skill catalog

| Area | Skill | Use it for |
|---|---|---|
| **Orchestration** | `axiom-orchestrator` | Multi-step work: choosing the workflow, delegating to subagents, quality gates, resuming |
| **Understand** | `project-onboarding` (alias `codebase-onboarding`) | Learning a repository and writing verified project notes |
| | `codebase-exploration` | "Where is X, who calls Y, how does data flow"; impact analysis |
| | `technical-research` | Version-specific library and API facts, pinned to your lockfile and proved locally |
| **Define** | `product-discovery` | Turning a vague idea into a clear problem, outcome, and approach |
| | `requirements-analysis` | Testable specs with user stories, numbered requirements, and acceptance scenarios |
| | `spec-analysis` | Checking that spec, plan, and tasks agree, or listing what is still unimplemented |
| | `quality-constraints` | Writing the quality bar down as numbers, and catching changes that lower it |
| **Design** | `architecture-design` | Options with trade-offs, ADRs, data and API design, patterns, migrations |
| | `ui-ux-design` | Screen states, accessibility with exact thresholds, design tokens, per-stack notes |
| **Build** | `task-planning` | Ready-for-development plans: small, ordered, verifiable tasks |
| | `implementation` | Building a planned change in thin slices, each with a step → verify loop |
| | `tdd` | Red → green → refactor, with worked examples in Python, TypeScript, and Go |
| | `debugging` | Root cause before fix: a technique by symptom, bisection, and instrumentation |
| **Verify** | `testing` | Choosing test layers, fixtures, flaky tests, and commands per ecosystem |
| | `e2e-testing` | Browser journeys with Playwright: locators, waiting, traces, and flake triage |
| | `code-review` | Independent review: defect patterns, per-language checklists, and writing findings |
| | `security-audit` | Defensive audits, with 13 references covering vulnerability classes by framework |
| | `verification-before-completion` | Evidence for every "done", "fixed", or "passing" claim |
| **Ship** | `release-management` | Readiness, semver, changelog, rollout and rollback, hotfixes |
| | `project-documentation` | READMEs, ADRs, runbooks, API docs, freshness metadata |
| **Meta** | `skill-factory` | Writing new skills test-first |
| | `skill-evaluator` | Judging whether a skill triggers and works |

Every skill folder is self-contained, so you can copy just the ones you want. More detail: [skill catalog](docs/skills/README.md).

---

## Workflows

Workflows are Markdown playbooks with stages and gates. The orchestrator picks the smallest one that fits.

| Workflow | When |
|---|---|
| [Codebase Onboarding](workflows/codebase-onboarding/WORKFLOW.md) | First time in a repository |
| [Feature Development](workflows/feature-development/WORKFLOW.md) | New or substantial features (discovery through verified delivery; stage files load on demand) |
| [Bug Fix](workflows/bug-fix/WORKFLOW.md) | A defect with a clear scope |
| [Refactoring](workflows/refactoring/WORKFLOW.md) | Changing structure while keeping behavior, with a blast-radius check |
| [Security Audit](workflows/security-audit/WORKFLOW.md) | Full or scoped security review |
| [Performance Audit](workflows/performance-audit/WORKFLOW.md) | Measured performance investigation |
| [Release](workflows/release/WORKFLOW.md) | Preparing and verifying a release |

The workflows are not included in skills-only installs (`npx skills` or copied skills). Agents then follow the skills directly.

---

## Files Axiom creates in your project

All of these are optional, plain Markdown, and meant to be committed:

| Path | Purpose |
|---|---|
| `AGENTS.md` / `CLAUDE.md` block | Kernel, routing, your verified commands, and a **Pitfalls** list of mistakes agents made in this repository |
| `.axiom/project/*.md` | Onboarding notes: overview, stack, architecture, conventions, development guide (only what the repository doesn't already document) |
| `.axiom/constitution.md`, `.axiom/CONSTRAINTS.md` | Your non-negotiable principles and numeric quality bar |
| `.axiom/config.md` | Project defaults for Axiom (see the [template](templates/project/config.md)) |
| `.axiom/workflows/active/<id>/` | State, spec, plan, tasks, decisions, and handoffs for an in-progress workflow, so a later session can resume |

---

## Evidence and limits

Axiom measures itself; claims below link to recorded runs.

| What | Result | Record |
|---|---|---|
| Trigger accuracy (right skill loaded or correctly not loaded), Claude Code 2.1.325 | **110/113** prompts across 24 skills | [results](evaluations/results/2026-11-16-1500-claude-code-trigger.md) |
| Trigger accuracy, Codex CLI 0.169.0 | **107/113** | [compatibility](docs/compatibility/README.md) |
| Behavior: every skill has a case, run repeatedly | All 24 cases run. Graded by a separate Claude grader and by Codex (a non-Claude model) | [compatibility](docs/compatibility/README.md#behavior-after-the-kernel-routing-change-2026-11-16) |
| OpenCode 1.19.5 | Discovers all 24 skills; model invocation not tested | [OpenCode adapter](adapters/opencode/INSTALL.md) |
| Antigravity | Not tested | [Antigravity adapter](adapters/antigravity/INSTALL.md) |
| Dogfooding | Used on Axiom itself and on a private Laravel application; the findings changed several skills | [dogfood reports](evaluations/dogfood/README.md) |

**Known limits:**
- **Fixtures are small.** On the current fixtures, a strong model finds the seeded issues with or without the deeper references. The added depth showed a small gain only with a weaker model, on few runs ([comparison](evaluations/results/2026-11-17-depth-comparison.md)).
- **Commands are unverified.** The commands and snippets in the references come from general practice. They have not been run in every ecosystem.
- **Grading is model-only.** No human grading yet.

---

## Repository map

```text
.agents/skills/      24 canonical skills (SKILL.md, references/, assets/)
.claude-plugin/      Claude Code plugin + marketplace manifests
adapters/            per-host install guides, the Claude Code hook, and subagents
agents/              role cards, subagent prompt templates, delegation patterns
core/                architecture, principles, contracts, policies, standards
workflows/           lifecycle playbooks (Markdown)
templates/           spec, plan, task, constitution, constraints, design, AGENTS.md block
integrations/        optional tools (Playwright, documentation search, security scanners)
evaluations/         eval cases, fixtures, recorded results, dogfood reports
scripts/             maintainer tooling: validator and eval runner (Python 3 standard library)
docs/                getting started, decisions (ADRs), compatibility, roadmap, credits
```

---

## For maintainers

The scripts use only the Python 3 standard library.

```bash
python3 scripts/validate_repository.py
```

Checks skill frontmatter, links (including that skills are self-contained), bundled-asset sync, and JSON. Add `--sync` after editing a template that a skill bundles.

```bash
python3 scripts/run_evals.py --check
```

Checks that every eval case file is well formed. CI runs both commands and the unit tests (`python3 -m unittest discover -s scripts/tests`).

```bash
python3 scripts/run_evals.py --host claude-code --kind trigger --skill debugging
```

Runs live evals against an installed host. These spend model quota.
- Hosts: `--host claude-code` or `--host codex`.
- Kinds: `--kind trigger` or `--kind behavior`.
- Behavior options: `--repeat N`, `--grade`, `--grader-host codex`, and `--case B2`.
- Results are written to `evaluations/results/`.

Before contributing, read [CONTRIBUTING.md](CONTRIBUTING.md) and [AGENTS.md](AGENTS.md). Their rules are short:
- keep skills portable;
- put host-specific details in `adapters/`;
- update evals and docs when behavior changes;
- never claim a check passed without output.

Ideas adapted from other open-source projects are credited in [acknowledgements](docs/acknowledgements.md). The design history is in the [roadmap](docs/IMPLEMENTATION-ROADMAP.md), the [changelog](CHANGELOG.md), and the [decision records](docs/decisions/).

## Security

Do not commit credentials, tokens, or private keys. Report vulnerabilities privately as described in [SECURITY.md](SECURITY.md).

## License

MIT. See [LICENSE](LICENSE).
