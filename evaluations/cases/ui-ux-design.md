---
skill: ui-ux-design
---

# Eval cases: ui-ux-design

## Should trigger

- "Design the settings page for notification preferences"
- "This form is hard to use on mobile, improve it"
- "Check the new dashboard for accessibility problems"
- "Move our hard-coded CSS colors to design tokens and add a dark theme"

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

### B2: Evidence check before disposition

- Prompt: "Rendered review of the pricing page is done. The 375 px and 1280 px screenshots look fine; the 768 px screenshot is a blank white image. Write the review handoff."
- Expect: Checks the evidence first and gives the disposition `recapture` for the 768 px width
- Expect: Uses one word from recapture, rebuild, fix, ship
- Fail if: Gives `ship` or judges the 768 px layout from the blank image
- Fail if: Invents a disposition such as "mostly good" or "ship with caveats"

### B3: Cognitive-load failures add up to critical

- Prompt: "Review this settings screen: a toolbar of 12 unlabeled icons, two equally prominent Save and Apply buttons, all advanced options shown at once, empty fields with no defaults, and errors shown only in a toast."
- Split: held-out
- Expect: Runs the cognitive-load checklist and counts 4 or more failures (for example C1, C2, C4, C5, C7, C8)
- Expect: Rates the view critical because 4 or more items failed
- Fail if: Lists the issues as separate minor findings with no combined critical rating
