# Slicing and the Verify Loop

Use this to split work into safe slices, run each slice through the step and verify loop, and decide when a refactor belongs in the task. Back to [SKILL.md](../SKILL.md).

## Slicing strategies

| Strategy | Shape | Use when |
|---|---|---|
| Vertical slice | One thin path through all layers (DB, API, UI) per slice | Default for features; each slice is demoable |
| Risk-first | Prove the most uncertain piece first (a library, a protocol, a perf limit) | An unknown could kill the plan |
| Contract-first | Slice 0 defines types, schema, or OpenAPI; then producer and consumer in parallel | Two sides develop at once |
| Walking skeleton | End-to-end stub that does nothing useful, then fill in | New service or pipeline with many moving parts |
| Expand and contract | Add new path beside old, migrate callers, remove old | Changing a shared interface or schema |
| Behind a flag | Merge incomplete slices with the feature off | Long work on a trunk-based team |

## Rules for a good slice

1. **Builds and passes on its own.** Never leave the tree red between slices.
2. **One logical change.** Feature, refactor, rename, dependency bump, and config change are separate slices.
3. **Has a check.** A test, a type check, or a command whose output proves it. No check, no slice.
4. **Revertable alone.** Additive changes first; deletions in their own slice.
5. **Safe default.** New behavior off by default or opt-in until the last slice wires it.
6. **Small.** Roughly under 100-200 changed lines including tests. Larger means split.

Bad slicing: "Slice 1: all models. Slice 2: all services. Slice 3: all controllers. Slice 4: tests." Nothing works until slice 4, and tests come last.

Good slicing: "Slice 1: create order (model + service + endpoint + test). Slice 2: list orders. Slice 3: cancel order."

## The step and verify loop

For each step, know the expected result before you run the command.

```
Step: add OrderTotal.compute with tax
Command: pytest tests/orders/test_total.py -q
Expected before code: 1 failed (AttributeError: compute)
Expected after code: 3 passed
```

Three outcomes after each run:

| Outcome | Action |
|---|---|
| Output matches expected | Next step |
| The code is wrong | Debug the cause (see [debugging](../../debugging/SKILL.md)). Do not patch the symptom to match. |
| The plan is wrong (interface missing, step contradicts spec) | Choose the smallest change that meets the spec. Record "Deviation: <finding> -> <decision> because <reason>". Continue. Stop and ask if it changes scope or a public contract. |

Verification order per slice, cheapest first:

1. The focused test for the slice.
2. Type check for the touched package (`npx tsc --noEmit -p .`, `mypy src/orders`, `go vet ./orders/...`).
3. Lint for touched files (`npx eslint <files>`, `ruff check <files>`, `golangci-lint run ./orders/...`).
4. The test file or package around the change.
5. At the end of the task: the full suite, build, and any integration tests.

Do not re-run a command on unchanged code to feel safer. Do re-run after any edit.

Keep long output out of your context: redirect to a file and read the tail.

```bash
npm test > /tmp/test.log 2>&1; echo "exit=$?"; tail -30 /tmp/test.log
```

## Worked example

Task: "Add a `discount_code` to checkout. Valid codes reduce the total by their percentage. Invalid codes return 422." Stack: Python, FastAPI, SQLAlchemy, pytest.

**Discovery.** `app/orders/` holds `models.py`, `service.py`, `router.py`. Tests in `tests/orders/`. Existing errors use `raise DomainError(code="...")`, mapped to 422 in `app/errors.py`. Commands from `Makefile`: `make test`, `make lint` (ruff), `make typecheck` (mypy). Baseline: `make test` -> `212 passed`.

**Slice 1: domain rule, no I/O.**

```python
# tests/orders/test_discount.py
def test_applies_percentage_discount():
    assert apply_discount(Money(10_000), Discount(percent=15)) == Money(8_500)

def test_rejects_percent_over_100():
    with pytest.raises(DomainError) as e:
        Discount(percent=120)
    assert e.value.code == "INVALID_DISCOUNT"
```

Run: `pytest tests/orders/test_discount.py -q` -> `2 failed (ImportError)`. Expected. Implement `Discount` and `apply_discount` in `app/orders/discount.py` using integer cents (the codebase's `Money` type). Run -> `2 passed`. `make typecheck` -> clean.

**Slice 2: lookup.** Add `DiscountCode` model and migration (additive, new table). Test `find_active(code)` with the existing DB fixture. Run focused test -> pass. Run the migration down then up locally -> clean.

**Slice 3: wire into checkout.** Add optional `discount_code: str | None = None` to the request schema (optional keeps old clients working). Service applies the discount when present. Router test: valid code -> total reduced; unknown code -> 422 with `code: "INVALID_DISCOUNT"`; no code -> unchanged total.

**Deviation.** The plan said to add a new `InvalidDiscountError` class. `DomainError(code=...)` already maps to 422. Decision: reuse it. Recorded in the report.

**Final.** `make test` -> `219 passed` (212 + 7 new). `make lint` and `make typecheck` clean. Diff review found a leftover `print(total)`; removed. Noticed but not changed: `checkout` recomputes tax twice (separate perf ticket).

## Refactoring while implementing

Refactor inside the task only when at least one is true:

- The change cannot be made cleanly without it (preparatory refactor: "make the change easy, then make the easy change").
- The code you must touch has no seam for a test, and a small extraction creates one.
- The refactor removes duplication your change would otherwise add a third copy of.

Limits:

| Allowed | Not allowed |
|---|---|
| Extract a function or class you then use | Rename across the codebase |
| Move code within the files you own | Reorganize directories |
| Add a parameter with a default | Change a public signature used by other teams |
| Replace a copy you would otherwise duplicate | "Modernize" syntax in untouched code |

Procedure:

1. Tests green before the refactor. If coverage of the area is missing, add a characterization test first that pins current behavior.
2. Refactor in its own slice and commit. Behavior must not change; tests stay green without edits to assertions.
3. Then do the feature slice.

If the refactor grows past about one slice, stop. Propose it as a separate task (see [quality-constraints](../../quality-constraints/SKILL.md)).

## Feature flags for incomplete work

When slices merge before the feature is complete:

```ts
// TypeScript
if (flags.isEnabled("checkout-discounts", { userId })) {
  total = applyDiscount(total, discount);
}
```

```python
# Python
if settings.FEATURE_CHECKOUT_DISCOUNTS:
    total = apply_discount(total, discount)
```

Rules: default off; test both states; give the flag an owner and a removal date; remove it in a follow-up once fully rolled out.

Sources: adapted from addyosmani/agent-skills (MIT) `skills/incremental-implementation/SKILL.md`, obra/superpowers (MIT) `skills/executing-plans/SKILL.md`, and general practice.
