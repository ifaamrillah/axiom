# Delegation

Delegate only when the host provides native subagents and the tasks are independent, bounded, and worth the coordination cost. Otherwise work sequentially. Never claim that parallel work happened when it did not.

Related references: [review loop](review-loop.md) for accepting delegated work and handling stuck workers, [worktree isolation](worktrees.md) for parallel writers, and [context budget](context-budget.md) for deciding what stays in the coordinator.

## Decide: inline, sequential, or parallel

Answer the questions in order. The first row that matches decides.

| # | Question | If yes |
|---|---|---|
| 1 | Is the task under ~15 minutes of work, or do you need to understand the result in detail anyway? | Do it inline. A brief costs more than the work. |
| 2 | Do you not yet know what is broken or what the design is? | Investigate inline first. Delegate only after the problem splits into known pieces. |
| 3 | Does task B need A's output (types, schema, API shape, migration)? | Sequential. Run A, review it, then brief B with A's real interface. |
| 4 | Would two tasks write the same file, lockfile, migration sequence, generated code, or shared config? | Sequential, or one owner for the shared file and the others read-only. |
| 5 | Do the tasks share mutable runtime state (one dev database, one port, one emulator, global caches)? | Sequential, or isolate the state per worker (separate DB name, port, worktree). |
| 6 | Could fixing one failure plausibly fix the others (same stack trace, same recent commit)? | One worker investigates all of them together. |
| 7 | None of the above, and each task has its own acceptance check? | Parallel. One worker per independent domain. |

Read-only work (exploration, review, audit of separate areas) parallelizes safely because no one writes. Writing work parallelizes only with disjoint write sets and, when the host allows, [separate worktrees](worktrees.md).

### Signals in practice

| Situation | Decision | Why |
|---|---|---|
| Three test files fail after a refactor, each with a different error and module | Parallel, one worker per file | Separate domains, separate checks |
| Five tests fail with the same `undefined is not a function` from one helper | One worker | One root cause |
| Add an endpoint, then the UI that calls it | Sequential | UI brief needs the real response shape |
| Audit auth, audit payments, audit logging (read-only) | Parallel | No writes, separate scopes |
| Rename a type used in 40 files | Inline or one worker | Single coherent change; splitting causes merge conflicts |
| Two features both add a migration | Sequential | Migration ordering is shared state |
| Map an unfamiliar repo: backend, frontend, infra | Parallel read-only explorers | Fan-out search; coordinator synthesizes |

## Construct the brief

A subagent does not inherit the session. Give it exactly what it needs and nothing else:

- the task text, acceptance criteria, and verification commands,
- the owned files (allowed / restricted / shared),
- the relevant interfaces, conventions, and constraints, quoted or linked,
- the baseline (known pre-existing failures) so it does not chase them,
- what to do when stuck, and the expected output format (see [handoff template](../assets/handoff.md)).

Use the bundled prompt templates: [implementer](../assets/prompts/implementer.md), [task reviewer](../assets/prompts/task-reviewer.md), and [fix loop](../assets/prompts/fix-loop.md).

### Brief template

```markdown
## Task <ID>: <one-line goal>

Context: <2-5 sentences: why this task exists, where it fits>
Spec excerpt: <quote only the relevant requirement lines, or path#section>

Acceptance:
- <observable result 1>
- <observable result 2>

Files:
- Allowed (write): <paths or globs>
- Restricted (do not touch): <paths>
- Shared (read only; ask coordinator to change): <paths>

Interfaces and conventions:
- <signature, type, endpoint shape, or pattern file to copy>

Verify with: <exact commands>
Baseline: <pre-existing failures to ignore, or "clean">

Constraints: <no new dependencies / no schema change / keep public API>
If blocked: stop and report BLOCKED or NEEDS_CONTEXT with what is missing. Do not guess.
Return: status (DONE | DONE_WITH_CONCERNS | NEEDS_CONTEXT | BLOCKED), changed files,
commands run with output summary, open concerns. Keep it under 40 lines.
```

### Worked example

Bad brief:

```text
Fix the failing tests in the billing module.
```

The worker does not know which tests, which files it may change, what "fixed" means, or whether to change tests or code. It may "fix" tests by loosening assertions.

Good brief:

```markdown
## Task T3: Make invoice rounding tests pass

Context: Commit 4f2a1c switched money values from float to integer cents.
Two tests in tests/billing/test_invoice.py now fail. Other billing tests pass.
Spec excerpt: docs/spec/billing.md#rounding says "round half to even, per line item".

Acceptance:
- test_line_item_rounding and test_invoice_total_mixed_currency pass
- No other test in tests/billing/ changes status

Files:
- Allowed: src/billing/invoice.py, src/billing/money.py
- Restricted: tests/ (do not edit assertions), migrations/
- Shared: src/billing/__init__.py (ask first)

Interfaces: Money(cents: int, currency: str); keep the constructor signature.
Verify with: pytest tests/billing -q
Baseline: tests/billing/test_tax.py::test_vat_eu is known flaky; ignore it.

Constraints: no new dependencies. Do not use float anywhere in the fix.
If blocked: report NEEDS_CONTEXT with the question. Do not edit tests.
Return: status, changed files, pytest summary line, concerns.
```

## Choose the role

Role cards (`agents/roles/` in the Axiom repository) declare a capability tier (`deep`, `standard`, or `fast`) and whether the role writes files. Adapters map these to host-specific models and tool permissions. Reviewers, researchers, and auditors are read-only.

| Work | Tier |
|---|---|
| Mechanical edit with a clear spec, 1-2 files | `fast` |
| Multi-file integration, debugging, pattern matching | `standard` |
| Architecture, final whole-change review, a task that failed twice | `deep` |

## Integrate

The coordinator owns integration, shared files, conflict resolution, and evidence checks. A subagent's success report is a claim. Inspect the diff and rerun the checks before accepting it. Follow the [review loop](review-loop.md).

## Avoid

| Red flag | Do instead |
|---|---|
| Personas that spawn other personas | Delegation is coordinator-to-worker only |
| Two writers on overlapping files | One owner per file; others read-only |
| "Fix all the tests" as a brief | One domain per worker, with test names and errors pasted |
| Pasting the whole conversation into the brief | Quote only the spec lines and interfaces the task needs |
| Delegating work whose result you must understand anyway | Do it inline |
| Re-dispatching the same brief to the same tier after BLOCKED | Change something: context, tier, or task size |
| Accepting "all tests pass" with no output | Rerun the command yourself |

Sources: adapted from obra/superpowers (MIT) dispatching-parallel-agents and subagent-driven-development, yeachan-heo/oh-my-claudecode (MIT) agent catalog, and general practice.
