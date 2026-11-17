---
name: code-review
description: Independently review a diff, branch, or plan for correctness, regressions, security, missing tests, weakened quality bars, and what is absent rather than only what is present. Use when asked to review or do a quality pass on a PR, diff, or another agent's changes, to check a plan before implementing it, before integrating substantial or security-sensitive changes, and after a delegated task completes.
---

# Code Review

## Purpose

Catch defects before they land. The reviewer protects the codebase, not the author's feelings. A false approval costs far more than a false rejection, but invented findings waste everyone's time. Both are failures.

## Inputs

The task or specification and its acceptance criteria, the complete diff (or plan), relevant surrounding code, and the project's constraints (`.axiom/CONSTRAINTS.md`, constitution) when present. A review without the acceptance criteria can only check code health, not correctness. Say so if they are missing.

## Posture

- **Read-only.** The reviewer reports. The owner fixes. When the host supports it, run the review as a read-only role, such as the reviewer role in the Axiom repository (`agents/roles/reviewer.md`).
- **Fresh context when possible.** A reviewer who did not write the change sees what the author cannot. Prefer a separate subagent with a constructed brief ([task reviewer prompt](../axiom-orchestrator/assets/prompts/task-reviewer.md)) for substantial or risky changes. For a small diff, a self-review is acceptable if it still predicts first and says it was a self-review.
- **Predict first.** Before reading details, write down the 3 places this change is most likely to be wrong. Then check them deliberately.
- **More scrutiny for AI-written code.** When an agent wrote the diff (including you, earlier), also run the [AI-generated code checklist](references/ai-generated-code.md): invented APIs, scope creep, tests that cannot fail, and claims without evidence.

## Procedure

1. **Spec compliance first.** For each acceptance criterion, decide met, partially met, not met, or not verifiable, and cite the evidence. Scope creep (unrequested behavior) is a finding.
2. **Trace changed behavior** through callers, data flows, and persisted formats. Use [blast radius](references/blast-radius.md) when signatures, schemas, or shared behavior change.
3. **Correctness and edge cases:** boundaries, empty and null values, concurrency, ordering, error paths, retries, and time zones. See [edge-case hunter](references/edge-case-hunter.md). For each area the diff touches (shared state, I/O, money, time, queries, user input), open the matching section of the [defect pattern catalog](references/defect-patterns.md). For each language in the diff, run its [per-language checklist](references/language-checklists.md), which also covers SQL and migrations.
4. **Security boundaries:** authorization at the last trusted decision point, input validation, output encoding, secrets, injection, and sensitive data in logs. Escalate to [security-audit](../security-audit/SKILL.md) for material attack-surface changes.
5. **Tests and evidence:** do the tests fail without the change? Do they cover failure paths? Did the claimed checks actually run? See [verification gap](references/verification-gap.md) and the [test review checklist](references/api-and-test-review.md#test-review), including its quick mutation check.
   When the diff changes an endpoint, event, CLI, library export, or config key, also apply the [API and interface checklist](references/api-and-test-review.md#api-and-interface-review).
6. **Bar-lowering detection:** new `@ts-ignore`, `eslint-disable`, `# type: ignore`, `noqa`, skipped or deleted tests, removed assertions, loosened thresholds, broadened catch-all error handling, TODO stubs presented as done. Each one is a finding unless it is justified and approved. See [quality-constraints](../quality-constraints/SKILL.md); run the per-language grep patterns in [bar-lowering detection](../quality-constraints/references/bar-lowering-detection.md).
7. **What is missing:** run the [gap analysis](references/review-lenses.md#gap-analysis). Look for migrations, docs, config, feature flags, rollback, observability, and tests that should exist and do not.
8. **Lenses:** for code, apply the security, new-engineer, and operations lenses. For plans, apply the executor, stakeholder, and skeptic lenses. See [review lenses](references/review-lenses.md).
9. **Maintainability and performance** where they matter: duplication, needless abstraction, hot-path complexity, N+1 queries.
10. **Report**, then re-review fixes until blocking findings are resolved or explicitly escalated. Write each finding with location, trigger, impact, and fix; see [writing a finding](references/writing-findings.md) for good and bad examples and verdict wording.

## Severity

| Severity | Meaning | Merge |
|---|---|---|
| Blocking | Incorrect behavior, data loss, security boundary violation, failed acceptance criterion, broken build or test | Must fix |
| Major | Likely defect under realistic conditions, missing required test, weakened quality bar | Fix or record an owner-approved exception |
| Minor | Real but low-impact issue | Fix when cheap |
| Note | Suggestion or question | Optional |

Separate **confirmed** findings (with file:line and a reproduction or reasoning chain) from **questions** (where the reviewer lacks context). Do not present a question as a defect.

## Output format

```markdown
## Review: <scope> (<commit or diff range>)
Verdict: Changes required | Approved with notes | Approved
Acceptance: AC1 met (test_x), AC2 not met (no handling for empty cart), …

### Findings
1. [Blocking] path/file.ts:42 — <defect>. Impact: <who/what breaks>. Evidence: <repro or trace>. Fix: <smallest change>.
2. …

### Missing
- <expected artifact or test that is absent>

### Questions
- …

### Not covered
- <files, behaviors, or checks this review did not inspect>
```

## Plan review mode

When reviewing a plan before execution: check that every file path referenced exists or is marked new, that tasks are ordered by dependency, that each task has a verification step, that acceptance criteria are testable, and that no placeholders or TBDs remain. Simulate the first two tasks mentally as the implementer would. Use the [Ready for Development standard](../task-planning/SKILL.md#ready-for-development-standard).

## Receiving review

When you are the author and findings arrive, verify each one against the code before changing anything. Ask about every unclear item before fixing any. Fix correct findings one at a time with a test run after each. Push back on wrong ones with evidence. Do not open with praise or agreement; the fix is the acknowledgment. See [receiving review feedback](references/receiving-review.md).

## High-stakes claims

For irreversible or security-critical decisions, add an adversarial pass: a fresh reviewer that tries to disprove the specific claim. See [adversarial review](references/adversarial-review.md).

## Rules

Do not approve work that was not inspected. Do not invent findings to look thorough: no concrete trigger, no finding (turn it into a question). A `shortcut:` comment that states its limit and upgrade trigger is a recorded decision; flag it only when the limit is wrong for the stated scope, and flag unmarked shortcuts or markers with no trigger. State the reviewed scope and what was not covered. Style nits that a formatter or linter would catch are not findings.

## References

- [Defect pattern catalog](references/defect-patterns.md): bad and good snippets for concurrency, errors, leaks, N+1, off-by-one, time, money, null, injection
- [Per-language checklists](references/language-checklists.md): Python, TypeScript/JavaScript, Go, Java/Kotlin, PHP/Laravel, SQL and migrations
- [API, interface, and test review](references/api-and-test-review.md)
- [Writing a finding](references/writing-findings.md)
- [Receiving review feedback](references/receiving-review.md)
- [Reviewing AI-generated code](references/ai-generated-code.md)
- [Review lenses and gap analysis](references/review-lenses.md)
- [Edge-case hunter](references/edge-case-hunter.md)
- [Verification gap](references/verification-gap.md)
- [Blast radius](references/blast-radius.md)
- [Adversarial review](references/adversarial-review.md)
- Independent review delegation (`agents/delegation/review.md` in the Axiom repository)
