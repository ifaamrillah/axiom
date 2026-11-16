# Writing Acceptance Criteria

Acceptance criteria say how anyone can tell that a requirement is met. Write them so that a tester who never spoke to you would reach the same verdict. Examples use the refund feature from [spec examples](spec-examples.md).

## Given/When/Then rules

- **Given** sets up state that already exists. Use concrete values: "an order item delivered 10 days ago, paid $40.00", not "a valid order".
- **When** is one action by one actor. Two actions mean two scenarios, or a Given that already contains the first action.
- **Then** is an observable result: a status, a message, a record, a response code, an email sent. Never an internal detail ("the service calls `validate()`").
- Use **And** for extra preconditions or extra results. Do not use it to chain a second action.
- One scenario tests one rule. Name it after the rule when the list is long.
- Every P1 story has at least one failure scenario next to its success scenario.

### Good vs weak scenarios

| Weak | Problem | Better |
|---|---|---|
| Given a user, When they request a refund, Then it works | No values, no observable result | Given an item delivered 10 days ago paid $40.00, When the customer requests $40.00 with reason "damaged", Then a request with status `requested` exists And the page shows "Request received" |
| Given a refund request, When the agent clicks Approve and the provider responds, Then the customer gets an email | Two actions; UI detail | Given a `requested` request for $40.00, When an agent approves it, Then the provider receives one refund of 4000 cents And status becomes `refunded` after provider confirmation |
| Then the refund is validated | Not observable | Then no request is created And the response says "Amount exceeds refundable balance ($15.00)" |
| Then it should be fast | Not a scenario; an NFR | Move to NFR-001 with a number |

## Example tables for rules with many inputs

When one rule has many input combinations, use a scenario outline with an examples table instead of ten near-identical scenarios. Pick rows at boundaries, not random values.

```gherkin
Scenario Outline: Refund window (FR-001, FR-002)
  Given an order item delivered <days_ago> days ago
  When the customer opens the refund form
  Then the form is <offered>

  Examples:
    | days_ago | offered | note                         |
    | 0        | offered | same day                     |
    | 29       | offered | inside                       |
    | 30       | offered | boundary: inclusive          |
    | 31       | hidden  | boundary: first day outside  |
    | (none)   | hidden  | not delivered yet            |
```

```gherkin
Scenario Outline: Refundable amount (FR-003)
  Given an item paid <paid> with completed refunds of <refunded>
  When the customer requests <requested>
  Then the request is <result>

  Examples:
    | paid   | refunded | requested | result                     |
    | $40.00 | $0.00    | $40.00    | created                    |
    | $40.00 | $0.00    | $40.01    | rejected: exceeds balance  |
    | $40.00 | $25.00   | $15.00    | created                    |
    | $40.00 | $25.00   | $15.01    | rejected: exceeds balance  |
    | $40.00 | $0.00    | $0.00     | rejected: must be > 0      |
    | $40.00 | $40.00   | $0.01     | rejected: nothing to refund|
```

A table like this often reveals a missing decision. Writing the "30" row forced the question "inclusive or exclusive?". Record the answer in the spec.

## Edge-case prompts

Run these prompts against each story. Each "yes, that can happen" needs a scenario or an explicit non-goal.

| Category | Prompts |
|---|---|
| Boundaries | Zero, one, maximum, maximum + 1; empty string; exact limit |
| Time | Window start and end; time zones (whose midnight?); daylight saving; clock skew; expiry during the action |
| Money and numbers | Rounding; minor units; currency mismatch; negative values; very large values |
| Repetition | Submit twice; double click; retry after timeout; replayed request |
| Concurrency | Two actors change the same record; stale form submitted after a status change |
| Partial failure | External call fails after local write; email fails after status change; timeout with unknown outcome |
| Permissions | Owner vs other user; role missing; actor acting on their own record; deleted account |
| State | Every allowed transition; every forbidden transition (`refunded` back to `requested`?) |
| Data shape | Unicode, very long text, HTML in free text, missing optional fields |
| Lifecycle | Referenced record deleted or changed (order cancelled after request) |

## State transition tables

When an entity has a status, write the allowed transitions as a table. Every cell that says "not allowed" is a scenario.

| From \ To | approved | rejected | refunded | failed |
|---|---|---|---|---|
| requested | agent | agent | not allowed | not allowed |
| approved | not allowed | not allowed | provider confirms | provider error |
| failed | not allowed | agent | provider confirms (retry) | provider error |
| rejected, refunded | terminal | terminal | terminal | terminal |

## Traceability

- Put requirement IDs in the scenario title or in a comment: `Scenario: Refund window (FR-001, FR-002)`.
- Every MUST requirement appears in at least one scenario. Every scenario cites at least one requirement or story.
- A scenario with no requirement is either a missing requirement or scope creep. Decide which.

## Checklist for one story's criteria

- [ ] Concrete values in every Given.
- [ ] One action per When.
- [ ] Observable Then, with exact message text where users see text.
- [ ] At least one failure scenario.
- [ ] Boundaries covered by an examples table where a rule has a range.
- [ ] Forbidden state transitions covered.
- [ ] Requirement IDs cited.

Sources: adapted from github/spec-kit (MIT) `templates/spec-template.md` and `templates/commands/checklist.md`, and general practice (Gherkin, boundary-value analysis, state-transition testing).
