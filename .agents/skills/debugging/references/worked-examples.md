# Worked Examples

Two end-to-end cases that follow the four phases, then a bad version for contrast.

## Example 1: wrong total after a release (regression, Python)

**Report:** "Invoices for EUR customers are off by a few cents since last week."

**Phase 1: investigate**

1. Concrete case: invoice `INV-8812`, expected `€104.97`, shown `€104.96`.
2. Reproduce locally with the same line items:
   ```sh
   python -m pytest -q tests/test_invoice.py -k eur_rounding   # new test, written from the report
   # FAILED tests/test_invoice.py::test_eur_rounding - assert Decimal('104.96') == Decimal('104.97')
   ```
3. What changed: `git log --since=2.weeks -- app/pricing` shows 9 commits. Too many to read; the test is a good bisect check.
4. Bisect with the test kept outside the tree:
   ```sh
   cp tests/test_invoice.py /tmp/t.py    # untracked copy survives checkouts
   git bisect start HEAD v4.2.0
   git bisect run sh -c 'cp /tmp/t.py tests/_bisect_check.py && python -m pytest -q tests/_bisect_check.py -k eur_rounding; s=$?; rm -f tests/_bisect_check.py; exit $s'
   # 3f1c9ab is the first bad commit: "pricing: compute VAT per line"
   git bisect reset
   ```

**Phase 2: compare.** The old code summed net amounts and rounded VAT once. The new code rounds VAT per line with `round()`, which uses banker's rounding on floats.

**Phase 3: hypothesis.** "Per-line rounding with `float` and `round()` loses a cent; if true, computing with `Decimal` and `ROUND_HALF_UP` once per invoice gives `104.97`." A 5-line script with the 7 line items confirms it: `104.96` with the new code, `104.97` with the old approach.

**Phase 4: fix and verify.** Change the VAT step to `Decimal` with `quantize(Decimal("0.01"), ROUND_HALF_UP)` at invoice level, which matches the finance rule in `docs/pricing.md`.

```text
Before: python -m pytest -q tests/test_invoice.py -k eur_rounding -> 1 failed
After:  python -m pytest -q tests/test_invoice.py -k eur_rounding -> 1 passed
Broader: python -m pytest -q -> 412 passed, 0 failed
```

**Report:** cause is commit `3f1c9ab` (per-line float rounding); fix is invoice-level `Decimal` rounding; regression test added; existing invoices issued since the release are not corrected by this change and need a decision from finance.

## Example 2: flaky end-to-end test (intermittent, TypeScript)

**Report:** "`checkout.spec.ts` fails about once in ten CI runs."

1. **Measure:** `for i in $(seq 50); do npx playwright test checkout.spec.ts --reporter=line || echo FAIL; done | grep -c FAIL` → `6` of 50 locally.
2. **Read the failure:** `expect(locator).toHaveText("Order placed")` timed out; the trace shows the button clicked before the cart total finished loading.
3. **Find the cause:** the test does `await page.waitForTimeout(500)` after adding an item. The cart request sometimes takes 700 ms. The click goes to a disabled button.
4. **Hypothesis:** "Waiting on the cart response instead of a fixed delay removes the race; if true, 0 of 50 fail."
5. **Fix:** replace the sleep with `await expect(page.getByTestId("cart-total")).toHaveText("$42.00")` before clicking. See [condition-based waiting](condition-based-waiting.md).
6. **Verify:** the same loop gives `0` of 50, and the spec runs 0.4 s faster.

## Bad version (what not to do)

> "The total was off by a cent, so I added `+ 0.01` when the currency is EUR. Tests pass now."

Problems: no reproduction recorded, no root cause, a symptom patch that is wrong for other amounts, and "tests pass" with no command or output.

## The three-failed-fixes escalation

After three fixes fail, stop editing. Write this down before doing anything else, in the workflow state or in the reply to the user:

```markdown
## Debugging escalation: <symptom>

- Symptom and reproduction: <exact command> -> <decisive output line>
- Fix attempts:
  1. <change> because <hypothesis> -> <result and evidence>
  2. <change> because <hypothesis> -> <result and evidence>
  3. <change> because <hypothesis> -> <result and evidence>
- Facts established (with evidence): <what is now known to be true or false>
- Pattern across failures: <for example, each fix moved the failure to another caller>
- Current model of the system and where it may be wrong: <assumption to question>
- Options:
  - A: <narrow next experiment>, cost <x>, risk <y>
  - B: <structural change>, cost <x>, risk <y>
- Decision needed from the user: <question>
```

Signs the problem is structural, not a missing detail: each fix exposes new coupling or shared state elsewhere; a fix needs a large refactor to apply; fixes create new symptoms in unrelated places. Revert the failed attempts so the tree holds only the reproduction and evidence.

Sources: adapted from obra/superpowers (MIT) `skills/systematic-debugging/SKILL.md`, `condition-based-waiting.md`, addyosmani/agent-skills (MIT) `skills/debugging-and-error-recovery/SKILL.md`, and general practice.
