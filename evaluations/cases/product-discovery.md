---
skill: product-discovery
---

# Eval cases: product-discovery

## Should trigger

- "I have a vague idea for a loyalty feature, help me figure out what to build"
- "Interview me about this feature before we design anything"
- "Not sure exactly what we need for notifications, can you help scope it?"

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
