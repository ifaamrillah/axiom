# Blast Radius

The diff shows what changed, not what breaks. Map the dependents of a change and prove what you can by running checks.

## When to use

- A signature, return shape, data format, event schema, or shared behavior changed.
- A dependency upgrade, configuration default flip, or migration.
- A refactor that claims behavior preservation.
- Someone asks "what could this break?"

## Procedure

1. **Name the change surface.** List exported symbols, persisted formats, CLI flags, API contracts, environment variables, and timing or ordering assumptions.
2. **Map dependents.** Search for each symbol and string. Use structural (AST) or code-graph search when available to catch uses that text search misses. Follow re-exports and dynamic dispatch one hop further than feels necessary. Include tests, scripts, infrastructure, and documentation.
3. **Classify each dependent:**
   - **Certain:** calls or reads the changed surface directly.
   - **Likely:** consumes a type, format, or side effect that the change touches.
   - **Unlikely:** shares a module but not the surface.
4. **Prove what you can.** For every certain and likely dependent, run the check that would catch a break: its test, type check, build, or a one-off command. Report the real output.
5. **Name the remainder.** A dependent you could not check is **unverified**, not safe.

## Report

```markdown
Surface: <symbols/formats>
Dependents: certain N, likely N, unlikely N
| Dependent | Class | Check run | Result |
|---|---|---|---|
| src/api/orders.ts:120 | certain | `npm test -- orders` | pass (34/34) |
| jobs/export.py | likely | none possible (needs prod data) | unverified |
```

## Rules

- "It should be fine" is not a classification. Every dependent is certain, likely, unlikely, or unverified, with the reason in the same row.
- Reasoning narrows the search. Execution settles the verdict.
- This analysis does not edit code. Fixes go through implementation.
