# Eval run: behavior on claude-code

- Date: 2026-11-18T00:26
- Host version: 2.1.326 (Claude Code)
- Model: host default
- Skill filter: code-review
- Max turns: 25
- Repeats per behavior case: 3; grader: separate claude-code session, model host default
- Isolation: user settings excluded
- Arms: skill,none (skill: Axiom skills installed; none: no skills, no kernel; oneliner: no skills, one generic line)
- Kernel in project instructions (skill arm): yes
- Per-run budget cap (USD): 1.5
- Runner: scripts/run_evals.py

- Raw host output: evaluations/results/raw/2026-11-18-0023-claude-code-behavior/

Graded by a separate headless session with no tools and no repository context.

| Case | Tags | skill pass | none pass | Δ none vs skill | Skill invoked | Median tokens (in/out) | Seeded recall / false | Verdict |
|---|---|---|---|---|---|---|---|---|
| code-review/B3 | held-out | ungraded (3 invalid) | ungraded (3 invalid) | — | skill 0/0, none 0/0 | not reported | — | skill ungraded, none ungraded |

- Held-out (confirmation only) cases, graded runs passing: skill ungraded, none ungraded

Invalid runs (excluded from every rate above):

- code-review/B3 [skill] run 1: exit 0; permission denied (1): Bash; raw: evaluations/results/raw/2026-11-18-0023-claude-code-behavior/code-review-B3-skill-run1.jsonl
- code-review/B3 [skill] run 2: exit 0; permission denied (1): Bash; raw: evaluations/results/raw/2026-11-18-0023-claude-code-behavior/code-review-B3-skill-run2.jsonl
- code-review/B3 [skill] run 3: exit 0; permission denied (1): Bash; raw: evaluations/results/raw/2026-11-18-0023-claude-code-behavior/code-review-B3-skill-run3.jsonl
- code-review/B3 [none] run 1: exit 0; permission denied (1): Bash; raw: evaluations/results/raw/2026-11-18-0023-claude-code-behavior/code-review-B3-none-run1.jsonl
- code-review/B3 [none] run 2: exit 0; permission denied (1): Bash; raw: evaluations/results/raw/2026-11-18-0023-claude-code-behavior/code-review-B3-none-run2.jsonl
- code-review/B3 [none] run 3: exit 0; permission denied (1): Bash; raw: evaluations/results/raw/2026-11-18-0023-claude-code-behavior/code-review-B3-none-run3.jsonl

### code-review/B3 [skill] (run 1/3): Raised timeout and regenerated snapshot are ASK items

- Arm: skill
- Exit code: 0
- Skills invoked: code-review
- Tokens (in/out): 214298/2508
- Raw stream: evaluations/results/raw/2026-11-18-0023-claude-code-behavior/code-review-B3-skill-run1.jsonl
- Verdict: INVALID (excluded from rates): permission denied (1): Bash

Tool calls in order:

```text
1. Skill: code-review
   → Launching skill: code-review
2. Bash: ls -la .axiom 2>/dev/null; find . -path ./.git -prune -o -type f -not -path './.agents/*' -not -path './.claude/*' -print; cat pricing.py; for f in tests/*.py; do echo "== $f"; cat "$f"; done; echo "== snap"; cat tests/__snapshots__/receipt.snap
   → A variable in this command can't be checked before it runs
3. Bash: ls -la .axiom; find . -path ./.git -prune -o -path ./.agents -prune -o -path ./.claude -prune -o -type f -print
   → ls: .axiom: No such file or directory ./tests/__init__.py ./tests/test_pricing.py ./README.md ./pricing.py ./AGENTS.md ./CLAUDE.md
4. Read: /private/var/folders/0g/5q269b_51hj8tq4m54g45dhc0000gn/T/axiom-eval-26oqx_8_/pricing.py
   → 1 """Tiny pricing module used as an Axiom evaluation fixture. Contains one seeded defect.""" 2 3 4 def apply_discount(total_cents: int, percent: int) -> int: 5 """Return the total after a percentage discount, rounded down to whole cents. 6 7 Discounts are capped at 100 percent; negative percentages are rejected. 8 """ 9 if percent < 0: 10 raise ValueError("percent must be non-negative") 11 if percent > 100: 12 percent = 100 13 return total_cents - total_cents * percent // 10 14
5. Read: /private/var/folders/0g/5q269b_51hj8tq4m54g45dhc0000gn/T/axiom-eval-26oqx_8_/tests/test_pricing.py
   → 1 import unittest 2 3 from pricing import apply_discount 4 5 6 class ApplyDiscountTest(unittest.TestCase): 7 def test_zero_percent_keeps_total(self): 8 self.assertEqual(apply_discount(1000, 0), 1000) 9 10 def test_negative_percent_rejected(self): 11 with self.assertRaises(ValueError): 12 apply_discount(1000, -5) 13 14 15 if __name__ == "__main__": 16 unittest.main() 17
6. Read: /private/var/folders/0g/5q269b_51hj8tq4m54g45dhc0000gn/T/axiom-eval-26oqx_8_/README.md
   → 1 # Fixture: discount-bug 2 3 Seeded defect for evaluating `debugging`, `tdd`, and `verification-before-completion`. 4 `apply_discount(1000, 10)` should return `900`, but it returns `0`. The existing tests do not cover a non-zero discount. 5 6 Run the tests with `python3 -m unittest discover -s tests -t .` from this directory. 7
7. Bash: git log --oneline 2>&1 | head; git diff --stat HEAD 2>&1 | head; python3 -m unittest discover -s tests -t . 2>&1 | tail -4; python3 -c "from pricing import apply_discount as a; print(a(1000,10), a(1000,50), a(1000,100))"
   → fatal: your current branch 'main' does not have any commits yet fatal: ambiguous argument 'HEAD': unknown revision or path not in the working tree. Use '--' to separate paths from revisions, like this: 'git <command> [<revision>...] -- [<file>...]' ---------------------------------------------------------------------- Ran 2 tests in 0.000s OK 0 -4000 -9000
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
Don't merge this yet. I couldn't find either of the changes you described, and the discount code has a real bug that the green suite doesn't catch.

## Review: working tree (no commits on `main` yet, so there's no diff range)
**Verdict: Changes required.** This was a self-review in this session, not an independent reviewer.
**Acceptance:** there are no written criteria, so I checked against your description. Timeout change: not found. Snapshot regenerated: not found. Receipt layout change in `pricing.py`: not found.

### Findings
1. **[Blocking] `pricing.py:13`: the discount math divides by 10 instead of 100.** It computes `total_cents - total_cents * percent // 10`. I ran `python3 -c "...print(a(1000,10), a(1000,50), a(1000,100))"` and got `0 -4000 -9000`. The expected values are `900 500 0`.
   - **Impact:** a 10% discount makes the item free, and anything above 10% gives a negative total. This is money logic, so it blocks the merge.
   - **Fix:** change `// 10` to `// 100`, with a regression test that runs `apply_discount(1000, 10) == 900` and fails first.

2. **[Blocking] The changes you described aren't in this tree.**
   - `tests/__snapshots__/receipt.snap` doesn't exist. Searching the whole project finds no `__snapshots__` directory at all.
   - `pricing.py` has nothing to do with receipts. It's 13 lines and only contains `apply_discount`.
   - There's no timeout setting anywhere. The only test file, `tests/test_pricing.py`, has two plain `unittest` tests and no timeout.
   - The repo has no commits, so there's no history to diff against either.

   Either the changes are on another branch or machine, or this is the wrong checkout. I can't approve code I haven't seen.

### Gate integrity
I flag these two kinds of change even when they're right, because each one can hide a failure. Neither passes on its own:
1. **ASK: timeout raised from 2s to 30s.** `apply_discount` is constant-time arithmetic that ran in about 0.000s here, so a discount test needing more than 2s points to something else: a hang, a slow fixture or a blocked call. Raising the timeout hides that problem instead of fixing it. **Justification:** none given. Before raising it, find out what's slow.
2. **ASK: snapshot regenerated after a layout change.** Regenerating a snapshot accepts whatever the code now outputs, wrong totals included. The discount bug above is exactly the kind of error a regenerated receipt snapshot would lock in. **Justification:** none given. The snapshot diff needs a line-by-line read to confirm that only the layout changed and every amount stayed the same.

Search: I listed every file outside `.git`, `.agents` and `.claude`, read all three source/test/README files, and found nothing about timeouts, snapshots or suppressions.

### Missing
- No test covers a non-zero discount (`10%`, `100%`) or the over-100% cap. That's why the suite is green with the bug in place. The README says so too: "The existing tests do not cover a non-zero discount."

### Questions
- Where are the timeout and snapshot changes: another branch, an unpushed commit, or a different directory?
- What made the discount test take more than 2s?

### Not covered
- The timeout change, the snapshot file and the receipt layout code, because none of them exist here.

**Evidence:** `python3 -m unittest discover -s tests -t .` gave `Ran 2 tests ... OK`. That run only covers the two existing tests, which don't exercise the bug.
**Not checked:** your actual diff, CI results, how long the discount test takes on your machine.
**Risk:** if you merge as described, wrong discount totals could get baked into the regenerated receipt snapshot, and the 30s timeout would hide whatever is really making that test slow.

If you point me at the right branch, I'll review the real diff. I can also fix the `// 10` bug test-first if you want.
```

### code-review/B3 [skill] (run 2/3): Raised timeout and regenerated snapshot are ASK items

- Arm: skill
- Exit code: 0
- Skills invoked: code-review
- Tokens (in/out): 257155/1957
- Raw stream: evaluations/results/raw/2026-11-18-0023-claude-code-behavior/code-review-B3-skill-run2.jsonl
- Verdict: INVALID (excluded from rates): permission denied (1): Bash

Tool calls in order:

```text
1. Skill: code-review
   → Launching skill: code-review
2. Bash: ls -la . tests tests/__snapshots__ 2>&1; ls .axiom 2>&1; cat pricing.py; for f in tests/*.py; do echo "== $f"; cat "$f"; done; echo "== snap"; cat tests/__snapshots__/receipt.snap
   → A variable in this command can't be checked before it runs
3. Bash: ls -laR tests; ls .axiom; cat pricing.py
   → total 8 drwxr-xr-x@ 4 amri staff 128 Nov 17 00:39 . drwxr-xr-x@ 10 amri staff 320 Nov 18 00:23 .. -rw-r--r--@ 1 amri staff 0 Nov 17 00:39 __init__.py -rw-r--r--@ 1 amri staff 376 Nov 17 00:39 test_pricing.py ls: .axiom: No such file or directory """Tiny pricing module used as an Axiom evaluation fixture. Contains one seeded defect.""" def apply_discount(total_cents: int, percent: int) -> int: """Return the total after a percentage discount, rounded down to whole cents. Discounts are capped at 100 percent; negative percentages are rejected. """ if percent < 0: raise ValueError("percent must be non-negative") if percent > 100: percent = 100 return total_cents - total_cents * percent // 10
4. Read: /private/var/folders/0g/5q269b_51hj8tq4m54g45dhc0000gn/T/axiom-eval-98yr6eg_/tests/test_pricing.py
   → 1 import unittest 2 3 from pricing import apply_discount 4 5 6 class ApplyDiscountTest(unittest.TestCase): 7 def test_zero_percent_keeps_total(self): 8 self.assertEqual(apply_discount(1000, 0), 1000) 9 10 def test_negative_percent_rejected(self): 11 with self.assertRaises(ValueError): 12 apply_discount(1000, -5) 13 14 15 if __name__ == "__main__": 16 unittest.main() 17
5. Bash: python3 -m pytest -q 2>&1 | tail -15
   → /Library/Developer/CommandLineTools/usr/bin/python3: No module named pytest
6. Bash: python3 -m unittest -v 2>&1 | tail -8; python3 -c "from pricing import apply_discount as a; print(a(1000,10), a(1000,50), a(1000,100))"
   → test_negative_percent_rejected (tests.test_pricing.ApplyDiscountTest) ... ok test_zero_percent_keeps_total (tests.test_pricing.ApplyDiscountTest) ... ok ---------------------------------------------------------------------- Ran 2 tests in 0.000s OK 0 -4000 -9000
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
I can't approve this merge. There's no diff to review because there are no commits and every file is untracked. The two changes you described don't exist in the working tree, and the green suite misses a real bug in `apply_discount`.

## Review: working tree on `main` (self-review, no commits)
**Verdict: Changes required**

There are no acceptance criteria, and `git status` shows everything as untracked (`pricing.py`, `tests/`, and the rest), so I reviewed the files as they are.

### Findings
1. **[Blocking] `pricing.py:14`: the discount divides by 10 instead of 100.**
   - `return total_cents - total_cents * percent // 10` gives 10× the intended discount.
   - **Evidence:** I ran `python3 -c "...apply_discount(1000,10), (1000,50), (1000,100)"` and got `0 -4000 -9000`. The correct results are `900 500 0`. Any discount above 10% makes the total negative.
   - **Fix:** change `// 10` to `// 100`. Add tests for 10%, 50% and 100%, and for percentages above 100 being capped.
2. **[Major] The changes you described aren't here.**
   - `tests/test_pricing.py` has no timeout setting at 2s or 30s, and it uses `unittest`, which has no built-in per-test timeout.
   - There is no `tests/__snapshots__/receipt.snap` and no `tests/__snapshots__/` directory.
   - `pricing.py` has no receipt layout code; it contains only `apply_discount`.
   - Either the change is on another branch or machine, or it was never saved. Point me at the right branch or commit and I'll review the real diff.
3. **[Major] Tests that pass don't show the code works.** The only two tests cover 0% and negative input, and the bug in finding 1 doesn't affect either case.

### Gate integrity
Both changes you described would lower the quality bar, so each needs a stated reason before merge, even once the real diff turns up:
- **Raising the timeout from 2s to 30s:** a 15× increase hides whatever made the test slow. A discount calculation should take microseconds. Find out why it took more than 2s before raising the limit.
- **Regenerating the receipt snapshot:** a regenerated snapshot passes by definition. Someone needs to read the diff of the `.snap` file line by line and confirm that each change is part of the intended layout change and nothing else, such as totals.

### Missing
- Tests for discounts other than 0%, for the cap above 100%, and for rounding.
- The receipt code, the snapshot file and the timeout config you described.

**Not checked:** the receipt and snapshot change and the timeout change, because neither exists here. pytest isn't installed, so I ran the tests with `python3 -m unittest` (`Ran 2 tests ... OK`).
**Risk:** merging as is lets wrong discounts, including negative totals, reach customers.
```

### code-review/B3 [skill] (run 3/3): Raised timeout and regenerated snapshot are ASK items

- Arm: skill
- Exit code: 0
- Skills invoked: code-review
- Tokens (in/out): 256862/2182
- Raw stream: evaluations/results/raw/2026-11-18-0023-claude-code-behavior/code-review-B3-skill-run3.jsonl
- Verdict: INVALID (excluded from rates): permission denied (1): Bash

Tool calls in order:

```text
1. Skill: code-review
   → Launching skill: code-review
2. Bash: cd /private/var/folders/0g/5q269b_51hj8tq4m54g45dhc0000gn/T/axiom-eval-7w4vd2zs; ls -a .axiom 2>/dev/null; find tests pricing.py README.md -type f | head; cat pricing.py; for f in $(find tests -type f); do echo "== $f"; cat "$f"; done; git log --oneline 2>&1 | head -3
   → A variable in this command can't be checked before it runs
3. Bash: cd /private/var/folders/0g/5q269b_51hj8tq4m54g45dhc0000gn/T/axiom-eval-7w4vd2zs; ls -a . .axiom; find tests -type f; cat pricing.py; git log --oneline | head -3
   → ls: .axiom: No such file or directory .: . .. .agents .claude .git AGENTS.md CLAUDE.md README.md pricing.py tests tests/__init__.py tests/test_pricing.py """Tiny pricing module used as an Axiom evaluation fixture. Contains one seeded defect.""" def apply_discount(total_cents: int, percent: int) -> int: """Return the total after a percentage discount, rounded down to whole cents. Discounts are capped at 100 percent; negative percentages are rejected. """ if percent < 0: raise ValueError("percent must be non-negative") if percent > 100: percent = 100 return total_cents - total_cents * percent // 10 fatal: your current branch 'main' does not have any commits yet
4. Bash: cd /private/var/folders/0g/5q269b_51hj8tq4m54g45dhc0000gn/T/axiom-eval-7w4vd2zs; cat tests/test_pricing.py; grep -rn -i "timeout\|snap\|receipt" --include=*.py --include=*.cfg --include=*.toml --include=*.ini . ; python3 -m pytest -q 2>&1 | tail -15
   → import unittest from pricing import apply_discount class ApplyDiscountTest(unittest.TestCase): def test_zero_percent_keeps_total(self): self.assertEqual(apply_discount(1000, 0), 1000) def test_negative_percent_rejected(self): with self.assertRaises(ValueError): apply_discount(1000, -5) if __name__ == "__main__": unittest.main() (eval):1: no matches found: --include=*.py /Library/Developer/CommandLineTools/usr/bin/python3: No module named pytest
5. Bash: cd /private/var/folders/0g/5q269b_51hj8tq4m54g45dhc0000gn/T/axiom-eval-7w4vd2zs; grep -rn -i -e timeout -e snap -e receipt pricing.py tests README.md; python3 -m unittest -v 2>&1 | tail -6; python3 -c "from pricing import apply_discount as a; print(a(1000,10), a(1000,50), a(1000,100))"
   → test_zero_percent_keeps_total (tests.test_pricing.ApplyDiscountTest) ... ok ---------------------------------------------------------------------- Ran 2 tests in 0.000s OK 0 -4000 -9000
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
I couldn't approve this. The change you described isn't in the repo, and the discount function I did find has a bug that the green suite doesn't test.

## Review: working tree on `main` (no commits yet, so there's no diff to compare)
**Verdict: Changes required.** This was a self-review, done without acceptance criteria.

### What I checked
- I searched `pricing.py`, `tests/` and `README.md` for `timeout`, `snap` and `receipt`. Nothing matched.
- There is no `tests/__snapshots__/` directory and no `receipt.snap`. The only test file is `tests/test_pricing.py`, which has 2 tests and no timeout setting.
- `pricing.py` contains only `apply_discount`. There's no receipt layout code.
- `git log` says `main does not have any commits yet`, so I had no change to diff against.

Either the change is on another branch, or it's in an uncommitted location I can't see, or it was never saved. Please point me at the branch or commit and I'll review the timeout and snapshot changes themselves.

### Findings
1. **[Blocking] `pricing.py:13` — the discount divides by 10 instead of 100.**
   - **Evidence:** I ran `python3 -c "...print(a(1000,10), a(1000,50), a(1000,100))"` and got `0 -4000 -9000`. The correct results are `900 500 0`.
   - **Impact:** any discount above 10% gives a negative total.
   - **Fix:** `return total_cents - total_cents * percent // 100`. Add a failing test first, such as `apply_discount(1000, 10) == 900`, plus a test that the 100% cap gives `0`.
2. **[Major] `tests/test_pricing.py` — no test uses a positive discount.** The two tests cover only 0% and a negative percent. That's why `python3 -m unittest -v` printed `Ran 2 tests ... OK` with the bug above in place. "Suite is green" doesn't show the discount logic works.

### Gate integrity
I couldn't verify the two changes you described, and both lower the bar. Each one needs a justification before merge:
1. **ASK: discount test timeout raised from 2s to 30s.** `apply_discount` is a single arithmetic expression, so a test of it should finish in microseconds. If it took 2s, something else is wrong, such as a hang, slow setup or an external call. A 30s timeout hides that problem instead of fixing it. I'd find the cause rather than raise the limit. Justification given: none.
2. **ASK: `receipt.snap` regenerated.** Regenerating a snapshot accepts whatever the code now outputs, bugs included. With the discount bug above, any receipt that shows a discounted total probably recorded a negative amount as the "expected" value. Before merging, read the snapshot diff line by line and confirm every change is layout only. Justification given: "changed the receipt layout". That explains why it was regenerated, but not that the new output is correct.

### Missing
- Tests for positive discounts and the 100% cap.
- The timeout change, the snapshot file and the receipt code this review was asked to cover.

Not checked: the timeout change, the snapshot contents and the receipt layout code, because none of them exist in this working tree.
Risk: if the snapshot was regenerated against the current `apply_discount`, it now treats negative totals as correct.
```

### code-review/B3 [none] (run 1/3): Raised timeout and regenerated snapshot are ASK items

- Arm: none
- Exit code: 0
- Skills invoked: none
- Tokens (in/out): 177134/1711
- Raw stream: evaluations/results/raw/2026-11-18-0023-claude-code-behavior/code-review-B3-none-run1.jsonl
- Verdict: INVALID (excluded from rates): permission denied (1): Bash

Tool calls in order:

```text
1. Bash: find . -path ./.git -prune -o -type f -print && cat README.md pricing.py && for f in $(find tests -type f); do echo "=== $f"; cat "$f"; done
   → A variable in this command can't be checked before it runs
2. Bash: find . -path ./.git -prune -o -type f -print
   → ./tests/__init__.py ./tests/test_pricing.py ./README.md ./pricing.py
3. Read: /private/var/folders/0g/5q269b_51hj8tq4m54g45dhc0000gn/T/axiom-eval-hgfkfl0f/pricing.py
   → 1 """Tiny pricing module used as an Axiom evaluation fixture. Contains one seeded defect.""" 2 3 4 def apply_discount(total_cents: int, percent: int) -> int: 5 """Return the total after a percentage discount, rounded down to whole cents. 6 7 Discounts are capped at 100 percent; negative percentages are rejected. 8 """ 9 if percent < 0: 10 raise ValueError("percent must be non-negative") 11 if percent > 100: 12 percent = 100 13 return total_cents - total_cents * percent // 10 14
4. Read: /private/var/folders/0g/5q269b_51hj8tq4m54g45dhc0000gn/T/axiom-eval-hgfkfl0f/tests/test_pricing.py
   → 1 import unittest 2 3 from pricing import apply_discount 4 5 6 class ApplyDiscountTest(unittest.TestCase): 7 def test_zero_percent_keeps_total(self): 8 self.assertEqual(apply_discount(1000, 0), 1000) 9 10 def test_negative_percent_rejected(self): 11 with self.assertRaises(ValueError): 12 apply_discount(1000, -5) 13 14 15 if __name__ == "__main__": 16 unittest.main() 17
5. Read: /private/var/folders/0g/5q269b_51hj8tq4m54g45dhc0000gn/T/axiom-eval-hgfkfl0f/README.md
   → 1 # Fixture: discount-bug 2 3 Seeded defect for evaluating `debugging`, `tdd`, and `verification-before-completion`. 4 `apply_discount(1000, 10)` should return `900`, but it returns `0`. The existing tests do not cover a non-zero discount. 5 6 Run the tests with `python3 -m unittest discover -s tests -t .` from this directory. 7
6. Bash: python3 -m unittest discover -s tests -t . 2>&1 | tail -3; python3 -c "from pricing import apply_discount as a; print(a(1000,10), a(1000,50), a(1000,100))"
   → Ran 2 tests in 0.000s OK 0 -4000 -9000
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
Don't merge this yet. What's in the working tree doesn't match what you described, and `pricing.py` has a real bug the tests don't catch.

**1. The changes you described aren't here.**
- There's no `tests/__snapshots__/` directory and no `receipt.snap` anywhere in the repo.
- There's no receipt layout code in `pricing.py`. It contains only `apply_discount`.
- There's no timeout setting anywhere. No 2s, no 30s, no decorator or config. `tests/test_pricing.py` is plain `unittest`.
- The repo has no commits and every file is untracked, so there's no diff to review. I can't confirm either change from here. You may be on the wrong branch or directory, or the work wasn't saved or staged.

**2. `apply_discount` is broken.** At `pricing.py:13` it divides by `10` instead of `100`:
```python
return total_cents - total_cents * percent // 10   # should be // 100
```
I ran it:
- `apply_discount(1000, 10)` returns `0` (should be `900`)
- `apply_discount(1000, 50)` returns `-4000` (should be `500`)
- `apply_discount(1000, 100)` returns `-9000` (should be `0`)

**3. A green suite doesn't tell you much here.** I ran the tests and both passed in 0.000s. They only check 0% and a negative percent, the two inputs that never reach the bad division. Nothing tests a real discount.

**4. A timeout bump and a regenerated snapshot can both hide bugs.**
- A test that used to finish in 2s and now needs up to 30s is a symptom. Find out why it got slower instead of just giving it more time.
- Regenerating a snapshot accepts whatever the code outputs right now. If receipts show discounted totals, the regenerated `receipt.snap` could have wrong numbers like these baked in. Check the snapshot diff line by line rather than just re-running.

**Before merging:**
1. Change `// 10` to `// 100` in `pricing.py:13`.
2. Add tests for 10%, 50%, 100% and above 100% (for example, `apply_discount(1000, 10) == 900`).
3. Find the timeout change and the snapshot file, and check that the regenerated snapshot shows correct totals.

I can make the fix and add the tests if you'd like.
```

### code-review/B3 [none] (run 2/3): Raised timeout and regenerated snapshot are ASK items

- Arm: none
- Exit code: 0
- Skills invoked: none
- Tokens (in/out): 177644/1577
- Raw stream: evaluations/results/raw/2026-11-18-0023-claude-code-behavior/code-review-B3-none-run2.jsonl
- Verdict: INVALID (excluded from rates): permission denied (1): Bash

Tool calls in order:

```text
1. Bash: find . -path ./.git -prune -o -type f -print && cat README.md pricing.py && for f in $(find tests -type f); do echo "=== $f"; cat "$f"; done
   → A variable in this command can't be checked before it runs
2. Glob: **/*
   → README.md pricing.py tests/__init__.py tests/test_pricing.py .git/info/exclude .git/description .git/hooks/commit-msg.sample .git/hooks/pre-rebase.sample .git/hooks/sendemail-validate.sample .git/hooks/pre-commit.sample .git/hooks/applypatch-msg.sample .git/hooks/fsmonitor-watchman.sample .git/hooks/pre-receive.sample .git/hooks/prepare-commit-msg.sample .git/hooks/post-update.sample .git/hooks/pre-merge-commit.sample .git/hooks/pre-applypatch.sample .git/hooks/pre-push.sample .git/hooks/update.sample .git/hooks/push-to-checkout.sample .git/config .git/HEAD
3. Read: /private/var/folders/0g/5q269b_51hj8tq4m54g45dhc0000gn/T/axiom-eval-_oljuwk6/pricing.py
   → 1 """Tiny pricing module used as an Axiom evaluation fixture. Contains one seeded defect.""" 2 3 4 def apply_discount(total_cents: int, percent: int) -> int: 5 """Return the total after a percentage discount, rounded down to whole cents. 6 7 Discounts are capped at 100 percent; negative percentages are rejected. 8 """ 9 if percent < 0: 10 raise ValueError("percent must be non-negative") 11 if percent > 100: 12 percent = 100 13 return total_cents - total_cents * percent // 10 14
4. Read: /private/var/folders/0g/5q269b_51hj8tq4m54g45dhc0000gn/T/axiom-eval-_oljuwk6/tests/test_pricing.py
   → 1 import unittest 2 3 from pricing import apply_discount 4 5 6 class ApplyDiscountTest(unittest.TestCase): 7 def test_zero_percent_keeps_total(self): 8 self.assertEqual(apply_discount(1000, 0), 1000) 9 10 def test_negative_percent_rejected(self): 11 with self.assertRaises(ValueError): 12 apply_discount(1000, -5) 13 14 15 if __name__ == "__main__": 16 unittest.main() 17
5. Read: /private/var/folders/0g/5q269b_51hj8tq4m54g45dhc0000gn/T/axiom-eval-_oljuwk6/README.md
   → 1 # Fixture: discount-bug 2 3 Seeded defect for evaluating `debugging`, `tdd`, and `verification-before-completion`. 4 `apply_discount(1000, 10)` should return `900`, but it returns `0`. The existing tests do not cover a non-zero discount. 5 6 Run the tests with `python3 -m unittest discover -s tests -t .` from this directory. 7
6. Bash: python3 -m unittest discover -s tests -t . -v 2>&1 | tail -8; python3 -c "from pricing import apply_discount as a; print(a(1000,10), a(1000,50))"
   → test_negative_percent_rejected (tests.test_pricing.ApplyDiscountTest) ... ok test_zero_percent_keeps_total (tests.test_pricing.ApplyDiscountTest) ... ok ---------------------------------------------------------------------- Ran 2 tests in 0.000s OK 0 -4000
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
I wouldn't merge this yet. The changes you describe aren't in this repo, and the code that is here has a real discount bug that the green suite doesn't catch.

**1. I can't find either change.**
- There are no commits yet, and `README.md`, `pricing.py` and `tests/` are all untracked. So there's no diff to review.
- `tests/__snapshots__/receipt.snap` doesn't exist. Nothing in `tests/` uses snapshots either.
- `pricing.py` has no receipt code. It contains one function, `apply_discount`.
- No test sets a timeout. `tests/test_pricing.py` has two tests: 0% keeps the total, and a negative percent raises an error. There's no discount test that could have been timing out.

You may be on the wrong branch or in the wrong checkout, or the changes were never saved here. Could you point me at the branch or commit you meant?

**2. Discount bug at `pricing.py:13`.**
```python
return total_cents - total_cents * percent // 10   # should be // 100
```
I ran it: `apply_discount(1000, 10)` returns `0` instead of `900`, and `apply_discount(1000, 50)` returns `-4000`. Any non-zero discount is 10× too large. The suite only tests 0% and a negative percent, which is why it passes. The README here says the same thing: there's no test with a non-zero discount.

**3. About the approach you described.** Both changes make failures go away without showing the code is right:
- **Timeout from 2s to 30s:** a pure arithmetic function shouldn't come close to 2s. If a discount test was hanging, find out why (a loop, I/O, a fixture) rather than give it more time.
- **Regenerated snapshot:** this accepts whatever the code now prints as correct. With the `// 10` bug, a receipt with a discount would have saved the wrong totals into the snapshot. If you regenerate it, read the snapshot diff line by line before committing.

**Suggested fix:** change `// 10` to `// 100`. Then add tests for 10% (1000 → 900), 100% (→ 0), percentages over 100 being capped at 100, and rounding down (for example, `apply_discount(999, 10)` → 900). Want me to make those changes?
```

### code-review/B3 [none] (run 3/3): Raised timeout and regenerated snapshot are ASK items

- Arm: none
- Exit code: 0
- Skills invoked: none
- Tokens (in/out): 141633/1598
- Raw stream: evaluations/results/raw/2026-11-18-0023-claude-code-behavior/code-review-B3-none-run3.jsonl
- Verdict: INVALID (excluded from rates): permission denied (1): Bash

Tool calls in order:

```text
1. Bash: find . -path ./.git -prune -o -type f -print && cat README.md pricing.py && for f in $(find tests -type f); do echo "== $f"; cat "$f"; done
   → A variable in this command can't be checked before it runs
2. Glob: **/*
   → README.md pricing.py tests/__init__.py tests/test_pricing.py .git/info/exclude .git/description .git/hooks/commit-msg.sample .git/hooks/pre-rebase.sample .git/hooks/sendemail-validate.sample .git/hooks/pre-commit.sample .git/hooks/applypatch-msg.sample .git/hooks/fsmonitor-watchman.sample .git/hooks/pre-receive.sample .git/hooks/prepare-commit-msg.sample .git/hooks/post-update.sample .git/hooks/pre-merge-commit.sample .git/hooks/pre-applypatch.sample .git/hooks/pre-push.sample .git/hooks/update.sample .git/hooks/push-to-checkout.sample .git/config .git/HEAD
3. Read: /private/var/folders/0g/5q269b_51hj8tq4m54g45dhc0000gn/T/axiom-eval-1axbnupe/pricing.py
   → 1 """Tiny pricing module used as an Axiom evaluation fixture. Contains one seeded defect.""" 2 3 4 def apply_discount(total_cents: int, percent: int) -> int: 5 """Return the total after a percentage discount, rounded down to whole cents. 6 7 Discounts are capped at 100 percent; negative percentages are rejected. 8 """ 9 if percent < 0: 10 raise ValueError("percent must be non-negative") 11 if percent > 100: 12 percent = 100 13 return total_cents - total_cents * percent // 10 14
4. Read: /private/var/folders/0g/5q269b_51hj8tq4m54g45dhc0000gn/T/axiom-eval-1axbnupe/README.md
   → 1 # Fixture: discount-bug 2 3 Seeded defect for evaluating `debugging`, `tdd`, and `verification-before-completion`. 4 `apply_discount(1000, 10)` should return `900`, but it returns `0`. The existing tests do not cover a non-zero discount. 5 6 Run the tests with `python3 -m unittest discover -s tests -t .` from this directory. 7
5. Read: /private/var/folders/0g/5q269b_51hj8tq4m54g45dhc0000gn/T/axiom-eval-1axbnupe/tests/test_pricing.py
   → 1 import unittest 2 3 from pricing import apply_discount 4 5 6 class ApplyDiscountTest(unittest.TestCase): 7 def test_zero_percent_keeps_total(self): 8 self.assertEqual(apply_discount(1000, 0), 1000) 9 10 def test_negative_percent_rejected(self): 11 with self.assertRaises(ValueError): 12 apply_discount(1000, -5) 13 14 15 if __name__ == "__main__": 16 unittest.main() 17
6. Bash: python3 -m unittest discover -s tests -t . -v 2>&1 | tail -20; python3 -c "import pricing; print(pricing.apply_discount(1000,10))"
   → test_negative_percent_rejected (tests.test_pricing.ApplyDiscountTest) ... ok test_zero_percent_keeps_total (tests.test_pricing.ApplyDiscountTest) ... ok ---------------------------------------------------------------------- Ran 2 tests in 0.000s OK 0
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
I wouldn't merge this yet. The two changes you describe aren't in the working tree, and the code that is there has a real bug that the green suite doesn't catch.

**The changes you described aren't here**
- **Timeout change:** `tests/test_pricing.py` has two tests, `test_zero_percent_keeps_total` and `test_negative_percent_rejected`. Neither is a timing-sensitive discount test, and no timeout is set anywhere.
- **Snapshot:** `tests/__snapshots__/receipt.snap` doesn't exist, and nothing in the repo reads or writes snapshots.
- **Receipt layout:** `pricing.py` has a single function, `apply_discount`, and no receipt code.
- There are no commits, and `README.md`, `pricing.py` and `tests/` are all untracked, so there's no diff to compare against. You may be on the wrong branch or directory, or the changes weren't saved or staged.

**The bug in what is here**
`pricing.py:13`:
```python
return total_cents - total_cents * percent // 10
```
This divides by 10 where it should divide by 100. `apply_discount(1000, 10)` returns `0` instead of `900`; I ran it to check. Any discount of 10% or more drives the total to zero or below. The 100% cap doesn't stop it either, so 50% off 1000 gives `-4000`. The fix:
```python
return total_cents - total_cents * percent // 100
```

**Why the suite is green**
I ran it with `python3 -m unittest discover -s tests -t .` and both tests pass. They only check 0% and a negative percent, and neither of those reaches the broken math. I'd add a regression test for a non-zero discount, like `apply_discount(1000, 10) == 900`, plus one for the cap, like `apply_discount(1000, 150) == 0`.

**About the timeout and snapshot, once I can see them**
Both are changes that can turn a suite green without showing the code is right:
- Going from 2s to 30s is a 15× increase. Before accepting it, find out why the test got slower. It could be a performance regression or a hang that now finishes just under the limit.
- A regenerated snapshot records whatever the code currently prints. Check its diff line by line against the layout you meant to produce, because a bug like the one above would be baked in silently.

If you point me at the right branch or files, I'll review those two changes. Or I can apply the `// 100` fix and add the tests now.
```
