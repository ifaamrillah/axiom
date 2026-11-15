# Fixture: Context Efficiency

## Prompt

Fix an isolated validation bug in a known module with current project docs and tests.

## Expected signals

- Loads the relevant workflow/skills only.
- Avoids full onboarding and unrelated lifecycle stages.
- Runs focused verification and reports scope.

## Review metric

Record whether the agent completed the goal without unnecessary stages, redundant tool calls, or irrelevant context. Token usage may be recorded if the host exposes it; do not estimate as a measured value.
