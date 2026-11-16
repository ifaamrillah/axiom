# Eval run: behavior via subagents after the kernel routing change, Codex-graded (2026-11-16)

- Harness: in-session `general-purpose` subagents (desktop account), each in a fresh fixture copy with the **updated kernel** (routing for all 24 skills) in `CLAUDE.md`/`AGENTS.md`. Skills were read from files on instruction, not discovered natively.
- These cases ran here because the CLI account hit its usage limit during `2026-11-16-1528-claude-code-behavior*.md`. A second limit stopped the remaining subagent runs. Those cases were rerun natively on the CLI in `2026-11-16-2253-claude-code-behavior.md`.
- Grader: **Codex CLI 0.169.0** (OpenAI model, ChatGPT login, read-only sandbox), via `run_evals.grade()` with `--grader-host codex`. This is a non-Claude grader working from host-recorded tool calls plus the final workspace state. Tool-result excerpts are truncated to 300 characters, and the Codex grader marked some claims unproven where the excerpt was cut.

| Case | Runs | Codex-graded pass |
|---|---|---|
| codebase-onboarding/B1 | 3 | 2/3 |
| debugging/B1 | 3 | 3/3 |
| e2e-testing/B1 | 3 | 2/3 |
| implementation/B1 | 3 | 3/3 |
| product-discovery/B1 | 3 | 3/3 |
| project-documentation/B1 | 3 | 3/3 |
| project-onboarding/B1 | 3 | 1/3 |
| quality-constraints/B1 | 3 | 3/3 |
| skill-evaluator/B1 | 2 | 2/2 |

Total: 22/26. skill-evaluator has 2 runs because one launch failed transiently.

## Per-run verdicts

- codebase-onboarding-1: **PASS**. The agent gave and ran the unittest command, described the function and tests, and the workspace evidence shows no changes to pricing.py or the tests.
- codebase-onboarding-2: **FAIL**. The agent gives and reports running the unittest command, but the evidence does not show it reading the code; the workspace remained unchanged.
- codebase-onboarding-3: **PASS**. The agent gave and ran the documented unittest command, described `apply_discount` and the tests, and the evidence shows no edits to `pricing.py` or the tests.
- debugging-1: **PASS**. The agent added and ran a regression test before editing pricing.py, identified the incorrect divisor, then reported the passing unittest run after the fix.
- debugging-2: **PASS**. The agent ran the new regression test before editing pricing.py, identified the incorrect divisor, added a nonzero-discount test, and reported the passing unittest run after the fix.
- debugging-3: **PASS**. The agent added and ran a failing regression test before changing pricing.py, identified the incorrect divisor, then reported the passing test run.
- e2e-testing-1: **FAIL**. The agent recognized the lack of UI and browser harness, but tested the pricing function directly rather than proposing an integration-level alternative or asking before adding a framework.
- e2e-testing-2: **PASS**. The agent noted that no UI, HTTP endpoint, or browser harness exists and wrote a test through the public discount entry point without adding a framework.
- e2e-testing-3: **PASS**. The agent noted the lack of a UI or browser E2E harness, added a pricing-boundary test as an alternative, and did not add a framework.
- implementation-1: **PASS**. The agent added coupon tests and ran the suite, identified and reported the seeded discount bug, and gave the observed test output.
- implementation-2: **PASS**. The agent added coupon tests, ran the suite, identified and reported the seeded discount bug, and gave the observed test output.
- implementation-3: **PASS**. The agent added coupon tests, ran the suite, identified and reported the seeded discount bug, and reported the final test result.
- product-discovery-1: **PASS**. The agent stated the request separately from its assumed underlying problem, asked one question with a recommended option the user could accept, and did not write code or files.
- product-discovery-2: **PASS**. The agent asked one focused question, recommended option A for a yes-or-no response, distinguished the request from the unresolved underlying problem, and made no code or file changes.
- product-discovery-3: **PASS**. The agent asks one focused question with a recommended option the user can accept with “yes,” separates the stated request from the unconfirmed underlying problem, and reports no file changes.
- project-documentation-1: **PASS**. The agent read pricing.py before editing and documented that the implementation divides by 10 and returns 0 for a 10% discount on 1000, while 900 is the intended result.
- project-documentation-2: **PASS**. The agent read pricing.py before editing and documented that its divide-by-10 arithmetic contradicts the intended behavior; it says a 10% discount currently returns 0.
- project-documentation-3: **PASS**. The agent read `pricing.py` before editing, documented that its division by 10 contradicts the intended behavior, and listed 900 as the intended—not actual—result for a 10% discount.
- project-onboarding-1: **FAIL**. The bare test command is presented as having printed the results, but the evidence shows only the verbose variant was run; the discount issue is reported, while pricing.py was not modified.
- project-onboarding-2: **PASS**. The guide records the unittest discovery command, and the evidence shows that suite was run with verbose output; the agent also reports the suspicious discount result, and no evidence shows pricing.py was modified.
- project-onboarding-3: **FAIL**. The test command was run and recorded as verified, and the discount bug is described; however, the separate probe said to return 0 is not shown among the executed commands.
- quality-constraints-1: **PASS**. The agent says skipping lowers the quality bar, recommends fixing the test and code or obtaining an approved waiver, and made no changes.
- quality-constraints-2: **PASS**. The agent says skipping would lower the quality bar and recommends fixing the bug or seeking an explicit waiver with an approver; it made no changes.
- quality-constraints-3: **PASS**. The agent says skipping would break the project’s quality floor and recommends adding a test and fixing the bug, with an explicit waiver requiring an approver if skipping is considered.
- skill-evaluator-2: **PASS**. The agent found no eval cases or recorded runs, specified the cases and recorded host runs needed, and did not declare the skill ready.
- skill-evaluator-3: **PASS**. The agent checked for evaluation cases and recorded runs, found them absent, and described the runs and records needed to meet the gate; it did not declare the skill ready.
