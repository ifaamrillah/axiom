# Root-Cause Tracing

Bugs usually show up far from where they start. Tracing walks backward from the symptom to the first place the state was wrong.

## Procedure

1. **Name the bad observation exactly.** For example: "`order.total` is `NaN` in `render_invoice()` at `invoice.py:88`."
2. **Find the immediate source.** Ask which line produced that value or state. Read it.
3. **Ask what called it, and with what.** Move one frame up the stack or one step back in the data flow. Inspect the inputs at that point.
4. **Repeat** until you reach a frame where the inputs are valid but the output is wrong. That frame contains the defect.
5. **Confirm** with a check: give that frame valid inputs in isolation and observe the wrong output.
6. **Fix at the origin.** Optionally add a guard at the symptom site if the system benefits from defense in depth. The guard is not the fix.

## Techniques when reading is not enough

- **Stack capture at the symptom:** log a stack trace where the bad value is detected to learn who produced it.
- **Boundary logging:** at each component boundary (HTTP handler, queue consumer, service call, DB layer), log the inputs and outputs once. The first boundary with bad output narrows the search.
- **Binary search in time:** `git bisect run <check>` when a known-good revision exists.
- **Binary search in data:** halve the input until the minimal failing input remains.
- **Watch the value:** debugger watchpoints, or temporary assertions, where the value must hold an invariant.

## Anti-patterns

- Patching the symptom site because that is where the error surfaced.
- Adding `null` or `NaN` checks everywhere instead of finding the producer.
- Concluding from one log line without confirming the frame in isolation.

Remove temporary logs and assertions before completion unless they become intended observability.
