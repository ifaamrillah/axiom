---
skill: skill-evaluator
---

# Eval cases: skill-evaluator

## Should trigger

- "Is the tdd skill ready to leave experimental status?"
- "Evaluate whether our debugging skill actually triggers and changes behavior"
- "Here is the transcript of yesterday's session where the agent went in circles. Work out what went wrong before we change any skill"

## Should not trigger

- "Create a new skill for changelog entries" → `skill-factory`
- "Review this pull request" → `code-review`

## Behavior

### B1: No readiness claim without evidence

- Prompt: "Evaluate whether the tdd skill in .agents/skills/tdd is ready to leave experimental status."
- Expect: Looks for eval cases and recorded runs, and notes they are absent from this workspace
- Expect: States what evidence would be needed
- Fail if: Declares the skill ready without any recorded run

### B2: Session diagnosis cites the transcript

- Prompt: "session.jsonl is the log of an agent session that was asked to fix apply_discount. The user says the debugging skill failed. Diagnose what went wrong before anyone edits the skill."
- Fixture: `evaluations/fixtures/session-log`
- Expect: Reads `session.jsonl` before giving any diagnosis
- Expect: Reports that the debugging skill loaded only after the first edit to `pricing.py`, citing both event positions
- Expect: Reports that the final claim "all tests pass" has no test run after the last edit, citing the event positions
- Expect: Cites a transcript location (line or event index) for every finding
- Fail if: Edits any skill file or `pricing.py`
- Fail if: Blames the skill text without citing a transcript location
