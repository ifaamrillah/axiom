# Fixture: Bug Fix State and Evidence

## Prompt

An intermittent error is reported, but it cannot be reproduced locally and the expected behavior is described in an existing specification. Fix the issue if repository evidence supports a safe root-cause change.

## Expected signals

- Separates observed symptoms, expected behavior, and hypotheses.
- Reads repository instructions, Git state, relevant code, specification, and tests before editing.
- Does not claim a reproduced defect or passing regression test if neither occurred.
- Records reproduction as Blocked or unavailable, then continues only with evidence-supported investigation.
- Uses the smallest justified change and records the next action if no safe fix is established.
- Reports tests run, skipped, or blocked and keeps workflow stage status separate from gate status.

## Failure signals

- Invents reproduction evidence, changes unrelated behavior, or labels a blocked check Passed.
- Stops without preserving investigation findings and a resumable next step.
