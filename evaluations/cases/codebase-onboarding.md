---
skill: codebase-onboarding
accept: project-onboarding
fixture: evaluations/fixtures/discount-bug
---

# Eval cases: codebase-onboarding

`codebase-onboarding` is an alias of `project-onboarding`; invoking either counts as a hit.

## Should trigger

- "I'm new to this repo. Onboard me: what is it, how do I run the tests, where do I start?"
- "Get familiar with this codebase and write down what a new contributor needs to know"

## Should not trigger

- "Fix the failing pricing test" → `debugging`
- "Is it safe to accept percent above 100?" → `security-audit`

## Behavior

### B1: Verified commands, no code changes

- Prompt: "Onboard me to this repository. How do I run the tests?"
- Fixture: `evaluations/fixtures/discount-bug`
- Expect: Gives the test command (python3 -m unittest or equivalent) and either runs it or says it was not run
- Expect: Describes what the code does from reading it, not from guessing
- Fail if: Edits pricing.py or the tests
