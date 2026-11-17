---
skill: product-discovery
---

# Eval cases: product-discovery

## Should trigger

- "I have a vague idea for a loyalty feature, help me figure out what to build"
- "Interview me about this feature before we design anything"
- "Not sure exactly what we need for notifications, can you help scope it?"
- "Before we build a referral program, is it even worth doing? Push back if not."

## Should not trigger

- "Rename getUser to fetchUser everywhere" → `none`
- "Fix the null pointer in OrderService" → `debugging`

## Behavior

### B1: One question at a time with a recommendation

- Prompt: "I want some kind of discount feature for repeat customers. Help me shape it."
- Expect: Asks one question per turn rather than a long questionnaire
- Expect: Offers a recommended answer so the user can accept with yes
- Expect: Separates the stated request from the underlying problem
- Fail if: Starts writing code or files before outcomes are clarified

### B2: Premise challenge before deep elicitation, with a verdict that can kill

- Prompt: "We should build our own feature-flag service for our one internal app. Three developers, about ten flags. Help me work out what to build."
- Expect: Before detailed scope questions, asks or answers the premise questions (right problem, cost of doing nothing, what already exists such as environment variables or an existing library, how users will adopt it)
- Expect: Presents 2–3 alternatives with rough effort (S/M/L), including a smallest option such as config flags or an existing library
- Expect: Gives a verdict of go, needs-clarification, or kill, and does not give go while a must-have criterion is weak or unknown
- Expect: When, and only when, the verdict is kill, records the decision, reason, date, and what would change it (this expectation is met when the verdict is not kill)
- Fail if: Designs the full service without questioning whether it is needed

### B3: Small, clearly scoped request skips the scorecard

- Prompt: "Help me scope this: add a 'copy order number' button next to the order number on the order page, for support agents. Done when one click copies it."
- Split: held-out
- Expect: States in one line why the premise holds, and says the scorecard is skipped for a small, scoped request
- Fail if: Runs a full criterion-by-criterion scorecard or asks more than two questions
