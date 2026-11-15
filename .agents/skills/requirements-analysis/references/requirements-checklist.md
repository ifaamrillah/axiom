# Requirements-Quality Checklist

These checks test the quality of the **written requirements**: completeness, clarity, consistency, measurability, and coverage. They do not test whether an implementation works.

| Wrong (tests implementation) | Right (tests requirements) |
|---|---|
| "Verify the button submits the form" | "Is the behavior after a failed submit specified?" |
| "Confirm the API returns 200" | "Are error responses defined for every failure the spec names?" |
| "Test that the page loads fast" | "Is 'fast' quantified with a measurable target?" |

## Checklist

### Completeness

- [ ] Every user story has acceptance scenarios, including at least one failure path.
- [ ] Error, empty, and loading states are specified for each user-facing flow.
- [ ] Permissions are defined: who can do what, and what happens when they cannot.
- [ ] Data lifecycle is defined: creation, update, deletion, retention.

### Clarity

- [ ] No unquantified adjectives remain ("fast", "large", "secure", "prominent").
- [ ] Each requirement has one interpretation; terms match the glossary.
- [ ] No `[NEEDS CLARIFICATION]` marker remains on a must-have requirement.

### Consistency

- [ ] Requirements do not contradict each other, the constitution, or existing behavior.
- [ ] The same concept uses the same name everywhere.

### Measurability

- [ ] Every must-have requirement can be verified by a test or an observation.
- [ ] Non-functional requirements have numbers and measurement conditions.

### Coverage

- [ ] Edge cases are listed for boundaries, concurrency, and partial failure.
- [ ] Security and privacy considerations are stated for sensitive data and external input.
- [ ] Accessibility expectations are stated for user-facing changes.

## Ownership

Check items only when a reviewer has evaluated them against the spec text. A checked item means the requirement is well-written. It does not mean the feature is implemented.
