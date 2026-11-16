# Adversarial Review

A confident answer is not a correct one. Long sessions quietly turn assumptions into "facts". For a non-trivial claim, have a fresh-context reviewer try to disprove it while correction is still cheap.

## When a claim is non-trivial

At least one is true:

- It introduces or changes branching logic or crosses a module or service boundary.
- It asserts a property the compiler cannot check: thread safety, idempotence, ordering, an invariant, or "this is safe".
- Its correctness depends on context a future reader cannot see.
- Its blast radius is irreversible: production deploy, data migration, public API change, or security control.

Skip it for mechanical edits, clear user instructions, read-only summaries, and one-line changes with obvious correctness. Skip it when the user explicitly prefers speed.

## Cycle

1. **Claim.** Write the claim and why it matters in 2–3 lines.
2. **Extract.** Isolate the artifact (code, plan section, or decision) and the contract it must satisfy. Remove your reasoning, so the reviewer is not anchored by it.
3. **Doubt.** Give the artifact and contract to a fresh reviewer with this brief:

   ```text
   You did not write this. Your job is to disprove the claim, not approve it.
   Claim: <claim>. Contract: <contract>. Artifact: <artifact>.
   Find concrete counterexamples: inputs, interleavings, states, or environments
   where the claim fails. For each one, give the scenario, the failing step, and the evidence.
   If you cannot break it, list what you checked and what you could not check.
   ```

4. **Reconcile.** Check each counterexample against the artifact text. Classify it as valid (fix it), invalid (cite the line that refutes it), or unresolvable (record it as a risk or question).
5. **Stop** when the findings are trivial, after 3 cycles, or when the user overrides.

## Host limits

This cycle needs a subagent with fresh context. If you are already a subagent and the host cannot nest delegation, return the claim to the coordinator rather than running a degraded self-review. If no delegation exists at all, do a self-review against the extracted artifact only, and label the result **degraded: not independent**.
