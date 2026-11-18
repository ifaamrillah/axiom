# Premise Challenge and Verdict

Open this before elicitation goes deep on a new capability, and again when you write the verdict. The goal is to find out early whether the work should happen at all, and to make "do not build it" an ordinary, recorded result.

## When to run it

| Request | Premise check | Scorecard |
|---|---|---|
| New capability, vague idea, or costly work | Yes, all four questions | Yes |
| Medium feature with a known problem | Yes, briefly | Yes, with short notes |
| Clearly scoped small request (outcome, user, and acceptance already stated) | One line: "premise accepted because …" | Skip; record verdict `go` with the reason |

Skipping the scorecard is allowed only when the request is small and clear. Write down that you skipped it. A skipped check is not a passed check.

## The premise questions

Ask these before detailed questions about scope or behavior. Answer from the repository first; ask the user only what the code and docs cannot answer. Ask one at a time, with your recommended answer.

1. **Right problem?** Is the stated request the real problem, or a guess at a solution? ("You asked for a refund form. Is the pain support time, slow refunds, or chargebacks?")
2. **Cost of doing nothing?** What happens if this is never built? If the honest answer is "very little", say so.
3. **What already exists?** Which code, product feature, library, or manual process already solves part of it? Name files and features you found.
4. **How do users get it?** How will the intended users find, adopt, or switch to it? A feature nobody reaches delivers no value.

Also check the project's out-of-scope records (see [glossary and out-of-scope records](../../requirements-analysis/references/glossary-and-out-of-scope.md)). If the concept was rejected before, show that record and ask what has changed.

## Alternatives with rough effort

Present 2–3 real alternatives. One of them must be the smallest option that could still help, such as a doc change, a config change, reuse of existing code, or a manual process. "Do nothing" counts when the cost of doing nothing is low.

| Option | What it is | Effort | Value | Main risk |
|---|---|---|---|---|
| Smallest | Reuse `PaymentsClient.refund` from the internal tool; no customer form | S | Cuts dashboard work only | Emails stay |
| Recommended | Customer form plus agent approval | M | Removes most emails | New table and UI |
| Larger | Form plus auto-approval under a limit | L | Fastest refunds | Fraud with no data |

Effort sizes are rough: **S** about a day or less, **M** a few days to two weeks, **L** more than two weeks or several teams. They are for comparison, not estimates to commit to.

## Assessment scorecard

Rate each criterion as **strong**, **adequate**, **weak**, or **unknown**. Give one line of evidence for each rating. Mark which criteria are must-have for this request; by default the first three are.

| Criterion | Must-have | Strong when |
|---|---|---|
| Problem evidence | Yes | Data, support tickets, user reports, or code show the pain |
| User value | Yes | A named user gains something observable |
| Feasibility | Yes | Known approach fits the stack, constraints, and time |
| Reuse | No | Existing code or product covers part of the work |
| Risk | No | The riskiest assumption is named and cheap to test |
| Adoption | No | There is a clear path for users to reach it |

Add a criterion when the request needs one (legal approval, cost, data access). Do not drop a must-have criterion to reach a verdict.

## Verdict

| Verdict | Use when |
|---|---|
| **go** | Every must-have criterion is strong or adequate, and the user approves the brief |
| **needs-clarification** | A must-have criterion is weak or unknown, but a question, a spike, or data could fix it |
| **kill** | The problem is not real, the cost of doing nothing is low, an existing solution is enough, or the work is infeasible |

Rules:

- **go** is not allowed while any must-have criterion is weak or unknown.
- **needs-clarification** names the exact question or experiment and who can answer it.
- **kill** is a valid result, not a failure. Record it as an out-of-scope record with the decision, reason, date, and what would change the decision. Then stop; do not continue to requirements.
- The user can overrule a verdict. Record the override and the reason in the brief.

## Example verdict

```markdown
## Assessment
| Criterion | Rating | Evidence |
|---|---|---|
| Problem evidence (must) | strong | ~120 refund emails/week (support lead) |
| User value (must) | strong | Customers get refunds without email back-and-forth |
| Feasibility (must) | adequate | `PaymentsClient.refund` exists; needs a table and form |
| Reuse | strong | Internal tool in `src/admin/` hosts the approval list |
| Risk | adequate | Over-refund risk; covered by hard rules |
| Adoption | unknown | Link placement on the order page not decided |

Verdict: go. Adoption is not a must-have here; it becomes an open decision.
```

Sources: ideas from garrytan/gstack (premise challenge; MIT) and github/spec-kit (assessment verdicts; MIT), rewritten.
