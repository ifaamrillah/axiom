# Persuasion Principles for Discipline Skills

Language models respond to the same influence patterns found in the human text they learned from. Published research applying Cialdini's principles to language models reported that persuasion framing roughly doubled compliance with requests (Meincke et al., 2025). Use that knowledge to make important rules hold under pressure, and only for the user's genuine interest.

## The principles, applied

| Principle | Use in a skill | Example wording |
|---|---|---|
| Authority | Imperative, bright-line rules for non-negotiable steps | "Run the failing test before editing code. No exceptions." |
| Commitment | Make the agent state or record a choice, then hold it to it | "Before editing, write the baseline in the workflow state." |
| Scarcity (timing) | Tie a step to a moment so it cannot be deferred | "Immediately after the task passes, run the review. Before the next task." |
| Social proof | State the norm and the observed failure pattern | "Checklists without a tracked state get steps skipped. Every time." |
| Unity | Collaborative framing for honest feedback | "We both want this to work. Report the problem plainly." |
| Reciprocity | Rarely useful | Avoid |
| Liking | Breeds agreement and sycophancy | Never use for compliance |

## Which principles for which skill

| Skill type | Use | Avoid |
|---|---|---|
| Discipline (TDD, verification, approvals) | Authority, commitment, scarcity, social proof | Liking, reciprocity |
| Technique (how to design, how to search) | Moderate authority, unity | Absolute language everywhere |
| Collaborative (review, pairing) | Unity, commitment | Heavy authority, liking |
| Reference | Plain, clear statements | All persuasion |

## Bright lines beat judgment calls

"Consider writing tests first when feasible" invites the agent to decide it is not feasible. "Write the test first. If you edited code first, revert it." leaves nothing to argue with. Use absolute language only for the few rules that must not bend. If everything is MUST, nothing stands out.

Implementation intentions work: "When X happens, do Y" is followed more reliably than "generally do Y". Write triggers into the procedure:

```markdown
When a test fails that you did not expect: stop, read the full error, and record it before changing code.
```

## Close the "spirit vs letter" escape

Agents often argue that they honored the intent while skipping the step. State early in the skill that breaking the letter of the rule breaks its purpose. Then the rationalization table can stay short.

## Ethical limits

Legitimate: making critical practices hold, preventing predictable failures, keeping humans in control.

Not legitimate: false urgency, guilt, flattery, or pressure toward actions the user would not endorse.

Test: would the user agree with this wording if they read it and understood why it is there? If not, remove it.

## Checklist for a discipline skill

- [ ] The rule is one line, imperative, and appears near the top.
- [ ] Each step that can be skipped has a moment ("before", "immediately after").
- [ ] A rationalization table built from observed or labeled-predicted excuses.
- [ ] A red-flags list of thoughts that precede a violation.
- [ ] The "spirit vs letter" sentence.
- [ ] No liking or reciprocity framing; no false urgency.
- [ ] Pressure-test cases exist and pass ([pressure testing](pressure-testing.md)).

Sources: adapted from obra/superpowers (MIT) writing-skills persuasion-principles reference (citing Cialdini 2021 and Meincke et al. 2025), and general practice.
