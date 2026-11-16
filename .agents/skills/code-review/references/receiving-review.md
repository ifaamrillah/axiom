# Receiving Review Feedback

Use this when you are the author and review findings arrive, from a human, another agent, or a tool. The goal is correct code, not a pleasant exchange. Agreeing with a wrong finding is as much a failure as ignoring a right one.

## Sequence

1. **Read all of it** before changing anything. Items can depend on each other.
2. **Restate** each item as a technical requirement in your own words. If you cannot, the item is unclear.
3. **Stop on anything unclear.** Ask about every unclear item before implementing any item. Partial understanding produces partial, inconsistent fixes.
4. **Verify against the code.** Read the cited lines, the callers, and the tests. Run the code or a test if the claim is about behavior.
5. **Decide** per item: correct (fix), incorrect (push back with evidence), or unverifiable (say what you need).
6. **Fix one item at a time.** Order: blocking defects and security first, then simple fixes, then larger refactors. Run the related tests after each.
7. **Re-run the full checks** at the end and report the real output.

## Verifying a finding

Before you implement a suggestion, check:

- Is the claim true in **this** codebase, version, and platform? Reviewers often reason from a general rule.
- Does the suggested fix break an existing caller, test, or compatibility promise?
- Is there a reason for the current code (a comment, a commit message, a linked issue, an ADR)?
- Is the suggested feature actually used? If a reviewer asks to "do it properly" for code nobody calls, search for callers first. If none exist, propose removal instead (YAGNI).
- Does the suggestion conflict with a decision the user or project owner already made? If so, stop and raise it with them; do not decide it between author and reviewer.

## Responding

| Situation | Response |
|---|---|
| Finding is correct | Fix it and state what changed: "Fixed: `redeem.py:31` now uses a conditional UPDATE; added `test_concurrent_redeem`." |
| Finding is wrong | Push back with evidence: the line, the test, or the output that refutes it. |
| You cannot verify | Say what is missing: "I can't confirm the iOS client reads `avatar_url` without its source. Should I keep the field until someone checks?" |
| Finding is partly right | Fix the right part; explain the rest. |
| You pushed back and were wrong | "Checked again: `parse()` does return null for empty input. Fixing." No long apology, no defense. |

## Performative agreement

Do not open with praise or agreement. Phrases like "Great catch!", "You're absolutely right!", or "Thanks for the thorough review!" add nothing and signal that the item was accepted without checking. The fix itself is the acknowledgment.

**Bad:**
> You're absolutely right! Let me remove that legacy branch right away.

**Good:**
> Checked: the legacy branch handles API v1 clients, and `access.log` shows 3% of traffic still on v1. Removing it would break them. Options: keep it until v1 sunset (2027-01), or remove it now and accept the breakage. Which do you want?

**Bad:**
> Good point, I'll add caching, metrics, and CSV export.

**Good:**
> `/reports/export` has no callers in the web or mobile clients. I suggest deleting it rather than extending it. Keep or delete?

## When to push back

- The suggestion breaks existing behavior or a test.
- The reviewer lacked context (a constraint, a platform limit, a prior decision).
- The suggestion adds unused capability.
- The suggestion is technically wrong for this stack or version.
- The suggestion conflicts with the project's constitution or constraints.

Push back with reasoning and evidence, not tone. Ask a specific question when you need the reviewer's input. Escalate to the user when it is an architectural or product decision.

## Red flags in your own response

| Red flag | Do instead |
|---|---|
| Implementing every item without reading the code | Verify each claim first |
| Fixing items 1-3 while asking about 4-5 | Clarify all unclear items first |
| Batch fix, one test run at the end | Test after each fix |
| "Done" with no evidence | Show the diff location and the test output |
| Silently skipping an item you disagree with | State the disagreement and the evidence |
| Lowering a check to make a finding go away | Fix the cause; see [quality constraints](../../quality-constraints/SKILL.md) |

Sources: adapted from obra/superpowers (MIT) (`skills/receiving-code-review/SKILL.md`) and general practice.
