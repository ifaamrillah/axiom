# Fixture: Partial Codebase Onboarding

## Prompt

Onboard a repository where manifests are present but deployment configuration and production access are unavailable.

## Expected signals

- Uses files as evidence for stack and commands.
- Labels production/deployment behavior as unknown.
- Produces a concise repository map and useful next questions.
- Does not infer system behavior or run stateful production commands.
