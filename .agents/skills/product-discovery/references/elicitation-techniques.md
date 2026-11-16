# Elicitation Techniques

A library of question techniques for discovery. Pick one or two that fit the gap you are trying to close. Do not run them all. Each technique below names the gap it closes, when to use it, when to skip it, and example questions you can adapt.

Ask one question per message. Attach your recommended answer so that "yes" moves the conversation forward.

## Choose a technique

| Gap you notice | Start with | Then, if needed |
|---|---|---|
| The request names a solution, not a problem ("add a chatbot") | 5 whys | Jobs to be done |
| You do not know who the user is or what situation they are in | Jobs to be done | User journey |
| The idea sounds good but nobody has stress-tested it | Pre-mortem | Assumption mapping |
| The scope keeps growing | Constraint inversion | MoSCoW cut |
| Many beliefs, unclear which one matters | Assumption mapping | Smallest test |
| The flow is unclear (steps, handoffs, states) | User journey | Edge-case sweep |
| The team is anchored on one design | How might we | Analogues |
| Success is vague ("users will love it") | Success signal | Counterfactual |
| The change touches existing behavior | Current-state walkthrough | Edge-case sweep |
| A stakeholder conflict exists | Trade-off slider | Decision owner |

## 5 whys

**Closes:** solution-first requests that hide the real problem.
**Use when:** the request names a feature, a tool, or a screen.
**Skip when:** the user already gave the problem and the evidence for it.

Ask "why" about the request, then about each answer, until you reach a pain that a user or the business feels directly. You rarely need five rounds. Stop when the answer names a cost (time, money, risk, churn).

- "What happens today when a customer wants a refund?"
- "Why is that a problem for you: support cost, customer churn, or something else?"
- "If we did nothing for six months, what would get worse?"

**Red flag:** the chain ends at "because a competitor has it". That is a positioning reason, not a user problem. Record it as such.

## Jobs to be done

**Closes:** unclear users, unclear motivation.
**Use when:** you cannot say who hires this feature and for what.
**Skip when:** the actor and situation are already concrete.

Frame the job as: *When <situation>, I want to <motivation>, so I can <outcome>.* Look for the functional job (the task), the emotional job (how they want to feel), and the social job (how they want to look to others).

- "Describe the last time a customer asked for this. What had just happened?"
- "What do they use instead today? A support email, a phone call, a chargeback?"
- "What does 'done' look like for them: money back, or just a confirmation?"

The workaround they use today is your real competitor. A chargeback is a competitor to a refund form.

## User journey

**Closes:** missing steps, handoffs, and states.
**Use when:** the feature spans several screens, actors, or systems.
**Skip when:** the change is a single interaction.

Walk the journey step by step: trigger, steps, decision points, handoffs between actors, end states. For each step, ask what can go wrong.

- "What triggers the journey: an email, an order page, a support chat?"
- "Who acts after the customer submits: a person, a rule, or both?"
- "What states can the request be in? I propose: requested, approved, rejected, refunded. OK?"
- "Where does the customer see the outcome?"

Write the journey as a numbered list or a small table. It becomes the seed for user stories later.

## Pre-mortem

**Closes:** hidden risks in an idea that feels good.
**Use when:** stakes are high, or the user is enthusiastic and nobody has pushed back.
**Skip when:** the change is small and easy to reverse.

Ask the user to imagine the feature shipped and failed. List the causes. Sort them into "preventable now", "detectable early", and "accept the risk".

- "Imagine it is six months after launch and this feature is being rolled back. What is the most likely reason?"
- "Which failure would hurt most: fraud, support load, or nobody using it?"
- "What early signal would tell us we are heading there?"

Each serious failure cause becomes either a requirement, a non-goal, or a named risk in the brief.

## Assumption mapping

**Closes:** many beliefs, no idea which one could sink the work.
**Use when:** the idea rests on several "surely" statements.
**Skip when:** the facts are known or are in the repository.

List every assumption. Rate each on two axes: how important it is to success, and how much evidence exists. The riskiest assumption is important with little evidence. Test that one first, cheaply.

| Assumption | Importance | Evidence | Cheapest test |
|---|---|---|---|
| Most refund requests are for damaged items | High | Low | Tag last 100 support tickets |
| Payment provider supports partial refunds | High | Medium | Read provider API docs; run sandbox call |
| Customers will use self-service over email | Medium | Low | Count "how do I get a refund" searches |

- "What must be true for this to work that we have not checked?"
- "Which of these would you bet the least money on?"

## Constraint inversion

**Closes:** scope creep and over-designed first versions.
**Use when:** the idea keeps growing, or every option feels big.
**Skip when:** the scope is already one small slice.

Impose an artificial limit and see what survives. Or invert a constraint: ask what would happen if the obvious requirement did not apply.

- "If this had to ship in one week, what would it do?"
- "If there were no admin screen at all, how would approvals happen?" (Answer: an email with approve and reject links. That might be enough for version one.)
- "If only one kind of refund were supported, which one?"
- "What if the user had to do zero typing?"

## MoSCoW cut

**Closes:** a long feature list with no priorities.
**Use when:** you have more than five candidate capabilities.

Sort each capability into Must, Should, Could, Won't (this time). Must means the release has no value without it. Push hard: most first lists have too many Musts.

- "If we shipped only the Musts, would anyone use it? If yes, the Shoulds can wait."

## Success signal and counterfactual

**Closes:** vague outcomes.
**Use when:** the success criterion is a feeling ("better", "easier").

- "What number would you check one month after launch?"
- "What is that number today?" (No baseline means you cannot claim improvement later.)
- "What result would make you say this was not worth it?"

A good signal has a baseline, a target, and a time frame: "refund-related support tickets drop from about 120 a week to under 60 within 8 weeks."

## How might we and analogues

**Closes:** anchoring on one design.
**Use when:** the user arrived with a fixed solution.

Reframe as *How might we <outcome> for <user> without <constraint>?* Write two or three framings. Then ask where a similar problem is already solved.

- "How might we return money quickly without opening the door to fraud?"
- "Which product you use handles this well? What do you like about it?"

Look for structural similarity, not surface similarity.

## Current-state walkthrough

**Closes:** missing knowledge of existing behavior.
**Use when:** the change modifies an existing flow.

Read the code and docs first. Only ask what they do not answer.

- "The code sends refunds through `PaymentsClient.refund`. Is that the path support uses today, or do they refund in the provider dashboard?"
- "Orders have a `delivered_at` field. Is that the date the window should count from?"

## Edge-case sweep

**Closes:** happy-path-only thinking.
**Use when:** the flow is understood and you want to find its boundaries.

Walk these prompts quickly: zero, one, many; first time and repeat; concurrent actions; partial failure; permissions; time (expiry, time zones); money (rounding, currency); deleted or changed data.

- "Can a customer request a refund twice for the same item?"
- "What happens if the order was paid with a gift card?"

## Trade-off slider and decision owner

**Closes:** conflicting goals between stakeholders.

Name two goals that pull apart and ask where the slider sits.

- "Speed of refund versus fraud control: if they conflict, which wins for version one?"
- "Who makes the final call if support and finance disagree?"

Record the answer and the owner in the brief.

## Question quality rules

| Weak question | Better question |
|---|---|
| "What do you want?" | "I'd scope this to delivered orders only. OK?" |
| "Any other requirements?" | "Should agents be able to refund more than the item price, for goodwill?" |
| "How should it work?" | "Two options: auto-approve under $50, or always review. I recommend always review for version one. Which?" |
| Five questions in one message | One question, the one with the highest impact × uncertainty |
| A question the code answers | Read the code, then confirm: "I see refunds go through `PaymentsClient`. Keep that?" |

Sources: adapted from addyosmani/agent-skills (MIT) `skills/idea-refine/frameworks.md` and `skills/idea-refine/SKILL.md`, obra/superpowers (MIT) `skills/brainstorming/SKILL.md`, ideas from bmad-code-org/BMAD-METHOD (elicitation methods), and general practice.
