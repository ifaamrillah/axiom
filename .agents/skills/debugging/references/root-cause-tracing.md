# Root-Cause Tracing

Bugs usually show up far from where they start. Tracing walks backward from the symptom to the first place the state was wrong.

## Procedure

1. **Name the bad observation exactly.** For example: "`order.total` is `NaN` in `render_invoice()` at `invoice.py:88`."
2. **Find the immediate source.** Ask which line produced that value or state. Read it.
3. **Ask what called it, and with what.** Move one frame up the stack or one step back in the data flow. Inspect the inputs at that point.
4. **Repeat** until you reach a frame where the inputs are valid but the output is wrong. That frame contains the defect.
5. **Confirm** with a check: give that frame valid inputs in isolation and observe the wrong output.
6. **Fix at the origin.** Optionally add a guard at the symptom site if the system benefits from [defense in depth](defense-in-depth.md). The guard is not the fix.

## A traced example

Symptom: a test run creates a `.git` directory inside `packages/core/`, the source tree.

| Step | Question | Finding |
|---|---|---|
| 1 | What runs `git init`? | `WorktreeManager.create(dir)` calls `execFile("git", ["init"], { cwd: dir })` |
| 2 | With what value? | `dir` is `""`; an empty `cwd` means "current directory", which is the package root |
| 3 | Who passed `""`? | `Session.create()` passed `project.dir` through unchanged |
| 4 | Where did `project.dir` come from? | `Project.create(name, ctx.tempDir)` in a test file |
| 5 | Why was `ctx.tempDir` empty? | The test read it at module load, before `beforeEach` created the temp dir |

Root cause: the test helper exposed `tempDir` as a plain field that is `""` until setup runs. Fix: make it a getter that throws when read before setup. Guards added afterward: `Project.create` rejects an empty dir, and `git init` refuses non-temp paths under `NODE_ENV=test`.

Note how fixing at step 1 or 2 (for example "skip `git init` when `dir` is empty") would have left every other consumer of `tempDir` broken.

## Techniques when reading is not enough

- **Stack capture at the symptom:** log a stack trace where the bad value is detected to learn who produced it. Log *before* the dangerous operation, and to stderr in tests:
  ```ts
  console.error("DBG git init", { dir, cwd: process.cwd(), stack: new Error().stack });
  ```
  Then `npm test 2>&1 | grep -A20 "DBG git init"` and look for test file names in the stacks.
- **Boundary logging:** at each component boundary (HTTP handler, queue consumer, service call, DB layer), log the inputs and outputs once. The first boundary with bad output narrows the search. See [instrumentation](instrumentation.md).
- **Binary search in time:** `git bisect run <check>` when a known-good revision exists. See [bisection](bisection.md).
- **Binary search in data:** halve the input until the minimal failing input remains.
- **Watch the value:** debugger watchpoints (`watch` in gdb/Delve, field watchpoints in IntelliJ, `Object.defineProperty` setter traps in JS), or temporary assertions where the value must hold an invariant.
- **Find all writers:** search for every assignment to the field or key (`grep -rn "\.total\s*=" src/`). When one writer is suspicious, assert there.

## Where to stop tracing

Stop at the first frame that:

- received valid inputs and produced invalid output (a logic defect), or
- read state from outside the call chain (global, cache, database, environment) that was already wrong; then trace who wrote that state, or
- crosses into code you do not own (library, service); then confirm the contract with a minimal call and decide whether your usage or their behavior is wrong.

## Anti-patterns

- Patching the symptom site because that is where the error surfaced.
- Adding `null` or `NaN` checks everywhere instead of finding the producer.
- Concluding from one log line without confirming the frame in isolation.
- Stopping at a library frame and blaming the library without a minimal reproduction.

Remove temporary logs and assertions before completion unless they become intended observability.

Sources: adapted from obra/superpowers (MIT) `skills/systematic-debugging/root-cause-tracing.md` and general practice.
