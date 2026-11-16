# Writing a Finding

A finding is useful when the author can act on it without asking a follow-up question. Use this before you write the report (procedure step 10).

## Anatomy

Every confirmed finding has six parts:

1. **Severity** from the table in SKILL.md.
2. **Location:** `path:line` (or a line range), on the changed side of the diff.
3. **Defect:** what is wrong, in one sentence, stated as fact.
4. **Trigger:** the input, state, or interleaving that makes it fail.
5. **Impact:** who or what breaks, and how badly.
6. **Fix:** the smallest change that resolves it. Name a structural remedy if the problem is structural.

Add **evidence** when you have it: a failing test, command output, a trace through callers, or a quoted line that refutes the author's assumption.

## Good vs bad

**Bad:**
> This might have some issues with concurrency. Consider looking into it.

No location, no trigger, no impact, no fix. The author cannot act.

**Good:**
> [Blocking] `src/coupons/redeem.py:31-35` — read-then-write on `coupon.remaining` without a lock. Trigger: two redemptions of the last coupon at the same time both read `remaining == 1`. Impact: the coupon is redeemed twice and `remaining` ends at 0, not -1, so the overuse is invisible. Fix: replace with a conditional `UPDATE ... WHERE remaining > 0` and check the affected row count.

---

**Bad:**
> Error handling is bad here.

**Good:**
> [Major] `api/orders.go:88` — `json.Unmarshal` error is discarded (`_ =`). Trigger: client sends `{"qty": "two"}`. Impact: the order is created with `qty = 0` and returns 201. Fix: return 400 when unmarshal fails; add a test for a non-numeric quantity.

---

**Bad (opinion as a defect):**
> [Blocking] I would use a factory here.

**Good:**
> [Note] `services/notify.ts:12-60` — three `if (channel === ...)` branches repeat the same retry wrapper. Consider a channel-to-sender map so the retry code exists once. Optional; not blocking.

---

**Bad (unverified claim):**
> [Blocking] This breaks the mobile app.

**Good (question, not defect):**
> Question: `GET /v1/profile` no longer returns `avatar_url` (`serializers/profile.py:20`). Does the iOS app still read it? I could not find the client code. If it does, this needs a deprecation period.

## Rules

- **State facts, not feelings.** "This returns null when the list is empty" beats "I'm not sure this handles empty lists."
- **Do not soften real defects.** Calling a production bug "a minor concern" misleads the author about the merge decision.
- **Do not inflate.** If you cannot name a concrete trigger and impact, downgrade the severity or turn it into a question.
- **Quantify when you can.** "Adds one query per line item; a 200-item order makes 201 queries" beats "could be slow."
- **One defect per finding.** Two defects in one finding means one gets lost.
- **Comment on code, not people.** "This function" not "you".
- **Separate pre-existing defects** from regressions this change introduces. Label pre-existing ones `[Pre-existing]` and do not block on them unless the change makes them worse.
- **Lead with leverage.** Order by severity, then by blast radius. A few high-confidence findings beat a long list where the one real bug is item 14.
- **Drop findings that callers, guards, or tests already rule out.** Cite the line that rules them out if the author might ask.
- **Zero findings is a valid result.** Say what you checked.
- **No style nits a formatter or linter would catch.**
- **Spec silence is not permission.** Where the spec says nothing, judge by what a reasonable user would expect, and grade by the effect on that user.
- **List what you set aside.** Behaviors you considered and judged out of scope go in one line each under "Not covered", with the reason, so the owner can rule on them. Nothing is dropped silently.

## Verdict wording

| Verdict | Use when |
|---|---|
| Changes required | Any Blocking finding, or Major findings without an approved exception |
| Approved with notes | Only Minor and Note findings, or Majors with a recorded exception |
| Approved | No findings, and the "Not covered" list does not hide a risk |

The approval bar is "this change improves the codebase and meets its acceptance criteria", not "this is how I would have written it". Do not block on preference.

## Structural remedies

When a finding is about structure, name the move:

- Replace a chain of conditionals with a typed model or a dispatch table.
- Collapse duplicated branches into one flow.
- Separate orchestration from business logic.
- Move feature-specific logic out of a shared module into the module that owns it.
- Reuse the existing helper instead of a near-duplicate.
- Make a type boundary explicit so downstream null checks disappear.
- Delete a pass-through wrapper that adds no meaning.

Prefer the remedy that removes moving parts over one that moves them around.

Sources: adapted from addyosmani/agent-skills (MIT) (`skills/code-review-and-quality`), obra/superpowers (MIT) (`skills/requesting-code-review/code-reviewer.md`) and general practice.
