# Hunting and Validation

## Hunter brief (one ledger unit or a small group of units)

```text
You are auditing <unit IDs> in <target> at <source ref>. Read-only source review.
Do not contact deployed or external services. Run target code only inside the approved
sandbox (no network, empty allowlisted environment, read-only target, scratch-only writes,
explicit limits). If the sandbox is unavailable, do not execute anything.
Context: <architecture summary>; checklist sections: <attack-surface sections>.
Exclude these unchanged prior root causes: <fingerprints>.
For each candidate, return a structured record (no prose-only results):
- fingerprint: stable, source-derived, e.g. <file>:<function>:<sink>:<class>
- proposed verdict: confirmed | needs_validation
- the six elements: principal, input, intended control, boundary, affected resource, result
- trace: entrypoint → propagation → sink, each step with file:line
- evidence: commands and fixtures used, with their output, or "static only"
- proposed likelihood, impact, and smallest fix
For units with no candidate, return what you checked, so the unit can be marked covered.
```

## Coverage critic (after each wave)

A fresh agent reviews the ledger and hunter returns:

- surfaces from reconnaissance with no unit, and new surfaces discovered during hunting;
- units marked covered with shallow evidence (no trace, no controls checked);
- attack classes that never applied to an important surface.

The parent adds or reassigns units. A **clean pass** means the critic found nothing material. The `standard` and `deep` profiles continue waves until a clean pass or until the budget forces deferral.

## Candidate verifier brief

```text
You did not write this candidate. Try to refute it from repository source and bounded
local evidence. Same sandbox rules apply; if a control is unavailable, do not execute,
and record the missing capability as a needs_validation blocker.
1. Check every trace step: does each cited file:line exist and do what is claimed?
   Is the first step a real lower-trust entrypoint, and the last the claimed effect?
2. Reconstruct the strongest controls on the path: validation, identity, authorization,
   normalization, framework defaults, containment. Does any of them stop it?
3. For a proposed confirmed candidate, reproduce the minimum result independently with
   dummy principals. Do not infer a stronger result than you observe.
4. Check that likelihood, impact, and the fix match only what the evidence shows.
5. For needs_validation: is the blocker genuinely outside source? Name the exact
   missing fact and a safe owner-run check. If source settles it, decide it.
Return: verdict (confirmed | needs_validation | rejected), corrected record fields,
and the refuting control (file:line) for a rejection.
```

The verifier receives only the candidate, its unit, the architecture facts it needs, the relevant checklist sections, and prior records with the same fingerprint. It never receives another verifier's conclusion.

## Consolidation

Merge candidates that share a root cause (the same missing control at the same decision point) under one fingerprint. List all affected entry points in that record.
