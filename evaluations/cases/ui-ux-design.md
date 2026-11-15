---
skill: ui-ux-design
---

# Eval cases: ui-ux-design

## Should trigger

- "Design the settings page for notification preferences"
- "This form is hard to use on mobile, improve it"
- "Check the new dashboard for accessibility problems"

## Should not trigger

- "Optimize this SQL query" → `none`
- "Add an index to the orders table" → `none`

## Behavior

### B1: States and accessibility before visuals

- Prompt: "Spec out the UI for a discount code input on the checkout page."
- Expect: Lists loading, empty, error, and success states
- Expect: Includes accessibility requirements such as a visible label, an error message near the field, and keyboard use
- Expect: Detects or asks about the stack instead of assuming a framework
- Fail if: Picks a UI framework without checking the project
