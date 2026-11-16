# Task Sizing, Slicing, and Ordering

Rules for drawing task boundaries, choosing slice direction, ordering by dependency, and marking parallel work. The [worked plan](worked-plan.md) applies all of them to one spec.

## Task sizing

A task is the smallest unit that has its own test cycle and that a reviewer could reject while approving its neighbors. Fold setup, config, and docs into the task that needs them.

| Size | Files touched | Typical content | Verdict |
|---|---|---|---|
| XS | 1 | One validation rule, one config value | Fine; consider folding into a neighbor |
| S | 1–2 + tests | One function, one endpoint, one component | Ideal |
| M | 3–5 + tests | One thin vertical slice | Ideal |
| L | 6–8 | Several components | Split |
| XL | 9+ | A subsystem | Split; maybe a separate plan |

### Split a task when

- Its acceptance needs more than 3 bullet points.
- Its title contains "and" joining two outcomes ("add table and build admin list").
- It touches two independent subsystems (billing and notifications).
- It would take more than one focused session (about 2 hours of agent work).
- A reviewer could approve half of it and reject the other half.
- Its verification needs more than one kind of check to be meaningful (unit tests and a manual UI pass and a load test).

### Merge tasks when

- One task is pure setup that no test can exercise alone ("create empty folder", "add dependency").
- One task only renames what the previous task created.
- Two tasks always change the same lines.
- A "write docs" task describes a single function delivered by another task.

## Vertical slices vs horizontal layers

**Default to vertical slices:** each task delivers one behavior through every layer it needs (schema, logic, API, UI) and can be tested end to end.

| Horizontal (avoid as default) | Vertical (prefer) |
|---|---|
| T1 Create all tables | T1 Customer can submit a refund request (table + policy + endpoint + form) |
| T2 Write all services | T2 Agent can approve or reject (role check + endpoint + admin list) |
| T3 Write all endpoints | T3 Approved refund is paid out (provider call + webhook + status) |
| T4 Build all UI | T4 Customer sees status (query + page + emails) |
| T5 Wire it together | — |

Why vertical wins: each task proves something real; integration bugs show up in task 1, not task 5; the plan can stop after any task and still ship value; reviewers see behavior, not scaffolding.

**When a horizontal task is right:**

- A shared foundation that several slices need and that has its own test (a migration with up/down tests, a shared money type).
- A contract that parallel slices consume (define the API schema or interface first, then parallelize).
- Cross-cutting setup the constitution demands before any feature (feature flag, audit table).

Keep such foundation tasks small, put them first, and give them their own verification.

## Dependency ordering

1. **Map the graph first.** For each task, list what it consumes (tables, types, functions, endpoints) and what it produces. A task depends on every task that produces something it consumes.
2. **Order:** setup → foundations → P1 slice(s) → P2 → P3 → polish and cross-cutting. P1 alone should be shippable.
3. **Risk first within a priority level.** Put the task most likely to fail or change the design early (an unfamiliar provider API, a tricky migration). Fail fast.
4. **Each task leaves the system working:** tests pass and the build is green after every task. If a task leaves things broken until the next one, merge them or reorder.
5. **No forward references.** A task never uses a name defined in a later task.
6. **Checkpoints** after every 2–4 tasks and at the end of each priority level: full test suite, build, and one end-to-end check of the slice.

Example dependency sketch:

```text
T001 migrations ──> T002 request slice (P1) ──> T003 approve/reject (P2) ──> T004 payout (P2) ──┬─> T005 [P] status page (P3)
                                                                                               └─> T006 [P] status emails (P3)
```

## Parallel markers `[P]`

Mark a task `[P]` only when **all** of these hold:

- It modifies no file that another unfinished task modifies.
- All its dependencies are done before the parallel group starts.
- It does not change a shared contract (schema, public interface, config file) that a sibling consumes.
- Its tests can run without the sibling's code.

| Situation | Mark |
|---|---|
| Two slices touch different modules, both depend only on T001 | Both `[P]` |
| Two tasks edit `src/refunds/service.ts` | Not `[P]`; order them |
| Task adds a column; sibling reads it | Not `[P]`; dependency |
| Two tasks each add a route to one shared `routes.ts` | Not `[P]`, or name one shared-file owner who merges both |
| Docs or tests for code that is already merged | `[P]` |
| Two migrations | Never `[P]`; migration order matters |

When work must run in parallel but shares a file, name a **shared-file owner** in the plan. Only that owner edits the file; others hand over their changes.

## Interfaces between tasks

When a task produces something a later task consumes, write the exact interface in the producing task and repeat it in the consuming task's "Consumes" line. Examples:

```ts
// TypeScript
export function refundableCents(item: OrderItem, completedRefunds: Refund[]): number
```

```python
# Python
def refundable_cents(item: OrderItem, completed_refunds: list[Refund]) -> int: ...
```

```go
// Go
func RefundableCents(item OrderItem, completed []Refund) int64
```

A name that differs between tasks (`refundableCents` in T002, `getRefundable` in T004) is a plan bug. Check it in the self-review.

## Verification commands by stack

Name the narrowest command that proves the task, plus the expected result. Use the repository's own scripts when they exist (`package.json`, `Makefile`, `pyproject.toml`, `justfile`).

| Stack | Focused test | Full gate |
|---|---|---|
| Node (Vitest/Jest) | `npx vitest run tests/refunds/policy.test.ts` | `npm test && npm run lint && npm run build` |
| Python (pytest) | `pytest tests/refunds/test_policy.py -q` | `pytest -q && ruff check . && mypy .` |
| Go | `go test ./internal/refunds -run TestRefundable -v` | `go test ./... && go vet ./...` |
| Java (Maven) | `mvn -q test -Dtest=RefundPolicyTest` | `mvn -q verify` |
| Ruby (RSpec) | `bundle exec rspec spec/refunds/policy_spec.rb` | `bundle exec rspec && bundle exec rubocop` |
| Rust | `cargo test refunds::policy` | `cargo test && cargo clippy -- -D warnings` |

Expected result must be specific: "FAIL: `refundableCents is not defined`" before the code, "4 passed" after.

Sources: adapted from addyosmani/agent-skills (MIT) `skills/planning-and-task-breakdown/SKILL.md`, obra/superpowers (MIT) `skills/writing-plans/SKILL.md`, github/spec-kit (MIT) `templates/tasks-template.md` and `templates/commands/tasks.md`, and general practice.
