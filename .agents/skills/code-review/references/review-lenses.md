# Review Lenses and Gap Analysis

Reviewers tend to evaluate only what is present. Structured gap analysis and deliberate change of perspective surface issues that a single unstructured pass misses.

## Gap analysis

Ask explicitly, and answer each with "present", "absent (finding)", or "not applicable":

- Tests for failure paths, boundaries, and permissions.
- Migration and rollback for schema, data, or format changes.
- Backward compatibility for public APIs, events, CLIs, and persisted data.
- Configuration, feature flags, and environment documentation.
- Observability: logs, metrics, and traces for the new behavior and its failures.
- Documentation and changelog updates for user-visible changes.
- Error messages that a user or operator can act on.
- Cleanup: temporary code, debug output, unused dependencies.
- Limits: timeouts, pagination, payload size, and rate limits.

## Lenses for code

| Lens | Asks |
|---|---|
| Security | What can a lower-trust caller make this do? Where is authorization decided? What reaches logs? |
| New engineer | Can someone unfamiliar understand and safely change this in six months? Are names honest? |
| Operations | How does this fail at 3 a.m.? Is it observable, retryable, and reversible? What happens under load? |

## Lenses for plans

| Lens | Asks |
|---|---|
| Executor | Can each task be done from the plan alone? Are paths, names, and commands exact? |
| Stakeholder | Does this deliver the stated outcome? What was dropped silently? |
| Skeptic | Which assumption, if wrong, sinks the plan? What is the cheapest way to test it first? |

## Pre-commitment

Before reading the details, write the three most likely failure points. Afterward, report whether each held. This makes the search deliberate instead of anchored on the author's framing.

## Severity calibration

If you cannot state the concrete damage (who is affected, what breaks, under which input), the severity is lower than it feels. Downgrade it or turn it into a question.
