---
skill: spec-analysis
---

# Eval cases: spec-analysis

## Should trigger

- "Check whether spec.md, plan.md, and tasks.md are consistent"
- "What's left to implement compared to the spec?"
- "Analyze the spec and tasks for gaps before we start coding"

## Should not trigger

- "Write the spec for a referral program" → `requirements-analysis`
- "Fix the failing unit test" → `debugging`

## Behavior

### B1: Read-only analysis

- Prompt: "Analyze consistency: spec says 'discount capped at 100%, 10% of 1000 is 900'; tasks.md has only 'T1 reject negative percent'. Report gaps."
- Expect: Reports a coverage gap: no task covers the 10%-of-1000 requirement
- Expect: Does not edit spec, plan, or tasks during analysis
- Expect: Assigns a severity to each finding
- Fail if: Rewrites or renumbers existing tasks
