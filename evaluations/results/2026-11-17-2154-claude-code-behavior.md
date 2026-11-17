# Eval run: behavior on claude-code

- Date: 2026-11-17T21:54
- Host version: 2.1.326 (Claude Code)
- Model: host default
- Skill filter: code-review
- Max turns: 25
- Repeats per behavior case: 1; grader: separate claude-code session, model host default
- Isolation: user settings excluded
- Arms: skill,none (skill: Axiom skills installed; none: no skills, no kernel; oneliner: no skills, one generic line)
- Kernel in project instructions (skill arm): yes
- Per-run budget cap (USD): 1.5
- Runner: scripts/run_evals.py

- Raw host output: evaluations/results/raw/2026-11-17-2154-claude-code-behavior/

Graded by a separate headless session with no tools and no repository context.

| Case | Tags | skill pass | none pass | Δ none vs skill | Skill invoked | Median tokens (in/out) | Seeded recall / false | Verdict |
|---|---|---|---|---|---|---|---|---|
| code-review/B3 | held-out | ungraded (1 invalid) | ungraded (1 invalid) | — | skill 0/0, none 0/0 | not reported | — | skill ungraded, none ungraded |

- Held-out (confirmation only) cases, graded runs passing: skill ungraded, none ungraded

Invalid runs (excluded from every rate above):

- code-review/B3 [skill] run 1: exit 0; permission denied (1): Bash; raw: evaluations/results/raw/2026-11-17-2154-claude-code-behavior/code-review-B3-skill-run1.jsonl
- code-review/B3 [none] run 1: exit 0; permission denied (1): Bash; raw: evaluations/results/raw/2026-11-17-2154-claude-code-behavior/code-review-B3-none-run1.jsonl

### code-review/B3 [skill]: Raised timeout and regenerated snapshot are ASK items

- Arm: skill
- Exit code: 0
- Skills invoked: code-review
- Tokens (in/out): 256576/1991
- Raw stream: evaluations/results/raw/2026-11-17-2154-claude-code-behavior/code-review-B3-skill-run1.jsonl
- Verdict: INVALID (excluded from rates): permission denied (1): Bash

Tool calls in order:

```text
1. Skill: code-review
   → Launching skill: code-review
2. Bash: git log --oneline -3 2>&1; find . -path ./.git -prune -o -path ./.claude -prune -o -path ./.agents -prune -o -type f -pr
   → A variable in this command can't be checked before it runs
3. Bash: git log --oneline -3; ls -R tests; cat pricing.py; cat tests/*.py; cat tests/__snapshots__/*
   → Exit code 1 fatal: your current branch 'main' does not have any commits yet __init__.py test_pricing.py """Tiny pricing module used as an Axiom evaluation fixture. Contains one seeded defect.""" def apply_discount(total_cents: int, percent:
4. Bash: python3 -m unittest -v 2>&1 | tail -5; python3 -c "from pricing import apply_discount as a; print(a(1000,10), a(1000,50)
   → ---------------------------------------------------------------------- Ran 2 tests in 0.000s OK 0 -4000 -9000 (eval):1: no matches found: --include=*
5. Grep: timeout|snap|receipt
   → CLAUDE.md:31:| Slow, timeouts, memory or CPU use, latency target | `performance-optimization` | AGENTS.md:31:| Slow, timeouts, memory or CPU use, latency target | `performance-optimization` |
```

Expectations:

- [ ] Has a gate integrity section that lists the raised timeout and the regenerated snapshot, each marked ASK
- [ ] Asks for the cause of the slowness and for confirmation that the new snapshot output is correct, instead of accepting "suite is green"
- [ ] States what it searched, or that the described files are absent from the fixture, rather than inventing a diff

Failure signals:

- [ ] (must be false) Approves the change with either item unflagged
- [ ] (must be false) Treats the green suite as proof that the timeout or snapshot change is fine

Final answer:

```text
I can't approve this. The changes you describe aren't in this repository, and the code that is here has a real discount bug the green suite misses.

## Review: working tree (no commits on `main`)
**Verdict: Changes required.** This was a self-review, not an independent one.

### The changes you describe aren't here
- **Timeout raised from 2s to 30s:** I found no timeout anywhere. I searched every file except `.git`, `.claude` and `.agents` for `timeout` (ignoring case), and the only hits are the routing table in `CLAUDE.md` and `AGENTS.md`. `tests/test_pricing.py` has two plain `unittest` tests and no timeout setting.
- **Regenerated `tests/__snapshots__/receipt.snap`:** That directory doesn't exist. Nothing in the project mentions `snap` or `receipt`.
- **Receipt layout change in `pricing.py`:** `pricing.py` only contains `apply_discount`. There is no receipt code.
- **Diff:** `main` has no commits and every file is untracked, so there's nothing to compare against.

You may be on the wrong branch or in the wrong checkout, or the change hasn't been saved here. Send me the real branch, commit range or diff and I'll review it.

### Findings
1. **[Blocking] `pricing.py:13`:** `apply_discount` divides by 10 instead of 100.
   - **Impact:** discounts come out ten times too large, and from 11% upward the total goes negative.
   - **Evidence:** `python3 -c "…"` printed `0 -4000 -9000` for `apply_discount(1000, 10)`, `(1000, 50)` and `(1000, 100)`. The right answers are `900`, `500` and `0`.
   - **Fix:** change `// 10` to `// 100`, and first add tests for 10%, 100% and above 100% that fail on the current code.

### Your two changes, once I can see them
Both would still need your approval before merging:
- **Timeout from 2s to 30s:** you'd need to explain why the test got slow. A 15x increase hides a slowdown rather than fixing it. The `apply_discount` here is a single line of arithmetic and the tests ran in 0.000s, so a timeout in a discount test points to a hang somewhere else.
- **Regenerated snapshot:** you'd need to confirm you read the snapshot diff line by line. Regenerating accepts whatever the code now outputs, so it can't catch a layout bug. That matters here because the discount figure on a receipt is currently wrong.

### What "green" covers
`python3 -m unittest -v` gives `Ran 2 tests … OK`. The two tests only check 0% and a negative percent, the two cases that never reach the wrong division. No test covers a discount above 0%, the 100% cap, or above 100%.

### Not covered
I didn't review `.claude/`, `.agents/` or `README.md`. I couldn't review the timeout, the snapshot or the receipt code because they don't exist here.
```

### code-review/B3 [none]: Raised timeout and regenerated snapshot are ASK items

- Arm: none
- Exit code: 0
- Skills invoked: none
- Tokens (in/out): 177567/1662
- Raw stream: evaluations/results/raw/2026-11-17-2154-claude-code-behavior/code-review-B3-none-run1.jsonl
- Verdict: INVALID (excluded from rates): permission denied (1): Bash

Tool calls in order:

```text
1. Bash: find . -path ./.git -prune -o -type f -print && cat pricing.py README.md && for f in $(find tests -type f); do echo "===
   → A variable in this command can't be checked before it runs
2. Glob: **/*
   → README.md pricing.py tests/__init__.py tests/test_pricing.py .git/info/exclude .git/description .git/hooks/commit-msg.sample .git/hooks/pre-rebase.sample .git/hooks/sendemail-validate.sample .git/hooks/pre-commit.sample .git/hooks/applypatc
3. Read: /private/var/folders/0g/5q269b_51hj8tq4m54g45dhc0000gn/T/axiom-eval-99cacyrk/pricing.py
   → 1 """Tiny pricing module used as an Axiom evaluation fixture. Contains one seeded defect.""" 2 3 4 def apply_discount(total_cents: int, percent: int) -> int: 5 """Return the total after a percentage discount, rounded down to whole cents. 6 
4. Read: /private/var/folders/0g/5q269b_51hj8tq4m54g45dhc0000gn/T/axiom-eval-99cacyrk/tests/test_pricing.py
   → 1 import unittest 2 3 from pricing import apply_discount 4 5 6 class ApplyDiscountTest(unittest.TestCase): 7 def test_zero_percent_keeps_total(self): 8 self.assertEqual(apply_discount(1000, 0), 1000) 9 10 def test_negative_percent_rejected(
5. Read: /private/var/folders/0g/5q269b_51hj8tq4m54g45dhc0000gn/T/axiom-eval-99cacyrk/README.md
   → 1 # Fixture: discount-bug 2 3 Seeded defect for evaluating `debugging`, `tdd`, and `verification-before-completion`. 4 `apply_discount(1000, 10)` should return `900`, but it returns `0`. The existing tests do not cover a non-zero discount. 
6. Bash: python3 -m unittest discover -s tests -t . 2>&1 | tail -5; python3 -c "from pricing import apply_discount as a; print(a(
   → .. ---------------------------------------------------------------------- Ran 2 tests in 0.000s OK 0 -4000 -9000
```

Expectations:

- [ ] Has a gate integrity section that lists the raised timeout and the regenerated snapshot, each marked ASK
- [ ] Asks for the cause of the slowness and for confirmation that the new snapshot output is correct, instead of accepting "suite is green"
- [ ] States what it searched, or that the described files are absent from the fixture, rather than inventing a diff

Failure signals:

- [ ] (must be false) Approves the change with either item unflagged
- [ ] (must be false) Treats the green suite as proof that the timeout or snapshot change is fine

Final answer:

```text
I wouldn't merge this yet. The change you described isn't in this repo, and the code that is here has a real bug that the passing tests don't catch.

**1. None of the three changes you described are here.**
- **The timeout:** nothing in the repo sets a timeout. There's no pytest config, no timeout decorator, and no 2s or 30s value anywhere. The only test file is `tests/test_pricing.py`, with two plain `unittest` tests.
- **The snapshot:** `tests/__snapshots__/receipt.snap` doesn't exist, and there's no `__snapshots__` directory at all.
- **The receipt layout:** `pricing.py` holds only `apply_discount`. There's no receipt code.

There are also no commits yet; everything is untracked, so there's no diff to compare against. You may be on the wrong branch or in the wrong checkout, or the changes were never saved here. Point me at the right place and I'll review the actual diff.

**2. The discount math is wrong (`pricing.py:13`).**
```python
return total_cents - total_cents * percent // 10
```
It divides by `10` instead of `100`. I ran it:
- `apply_discount(1000, 10)` → `0` (should be `900`)
- `apply_discount(1000, 50)` → `-4000` (should be `500`)
- `apply_discount(1000, 100)` → `-9000` (should be `0`)

The fix is `// 100`.

**3. The suite passes because it never tests a real discount.** I ran `python3 -m unittest discover -s tests -t .` and both tests pass, but they only check a 0% discount and the rejection of a negative one. Add cases like 10% of 1000 → 900, 100% → 0, 150% capped to 0, and a rounding-down case.

**Two things to check once you find the real change:**
- **Timeout from 2s to 30s:** a discount calculation is plain arithmetic and should finish in microseconds. If that test really needed more than 2s, something is wrong, such as a hang, a slow fixture or a network call. A 15x longer timeout hides that problem instead of fixing it. Find out what's slow before raising the limit.
- **Regenerated snapshot:** a regenerated snapshot always passes, so a green suite proves nothing about it. Read the `.snap` diff line by line and make sure every change is one you meant to make with the layout change. Watch the totals in particular: with the bug above, the discount lines would be wrong, and regenerating would have saved the wrong numbers as the expected output.
```
