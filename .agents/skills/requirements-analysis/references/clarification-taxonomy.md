# Clarification Taxonomy

Scan the spec against each category. Rate each one **Clear**, **Partial**, or **Missing**. Ask about the categories where an answer would change the architecture, data model, task breakdown, tests, UX, operations, or compliance. Skip categories that would not change any of these.

| Category | Look for |
|---|---|
| Functional scope | Core goals, success criteria, explicit out-of-scope, roles and personas |
| Domain and data | Entities, attributes, relationships, identity and uniqueness, lifecycle and state transitions, volume and scale |
| Interaction and UX | Critical journeys, error, empty, and loading states, accessibility, localization |
| Non-functional | Performance targets, scalability, reliability and availability, observability, security and privacy, compliance |
| Integrations | External services and their failure modes, data import and export formats, protocol and version assumptions |
| Edge cases | Negative paths, rate limits, conflicts (concurrent edits), partial failure, retries |
| Constraints and trade-offs | Technical constraints, rejected alternatives, budget and time |
| Terminology | Canonical terms, ambiguous adjectives ("fast", "secure", "intuitive") that need numbers |
| Completion signals | Testable acceptance criteria, definition of done for this feature |

## Question rules

- At most 5 questions per round. Order them by impact × uncertainty.
- Ask one at a time when interactive. Phrase each so that "yes" accepts the recommended answer.
- Prefer multiple choice (2–5 options) or a short answer of 5 words or fewer.
- Never ask what the repository, the existing spec, or prior clarifications already answer.
- Record each answer under **Clarifications** with the date and the affected requirement IDs, then edit those requirements.

## Stop

Stop when all high-impact categories are Clear, when the user says to proceed, or when the question budget is spent. Report categories left Partial or Missing as deferred, with the risk of each.
