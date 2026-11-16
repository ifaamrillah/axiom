---
skill: skill-evaluator
---

# Eval cases: skill-evaluator

## Should trigger

- "Is the tdd skill ready to leave experimental status?"
- "Evaluate whether our debugging skill actually triggers and changes behavior"

## Should not trigger

- "Create a new skill for changelog entries" → `skill-factory`
- "Review this pull request" → `code-review`

## Behavior

### B1: No readiness claim without evidence

- Prompt: "Evaluate whether the tdd skill in .agents/skills/tdd is ready to leave experimental status."
- Expect: Looks for eval cases and recorded runs, and notes they are absent from this workspace
- Expect: States what evidence would be needed
- Fail if: Declares the skill ready without any recorded run
