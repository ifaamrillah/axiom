# Reconnaissance

Map the target before hunting. Reconnaissance reads source and local configuration only. It sends no inputs and contacts no deployed or shared service.

## Facts to collect (with file:line)

1. **Product and principals.** What the product does; who uses and operates it; each lower-trust principal and the actions it has **by design**.
2. **Stack and local operation.** Languages, frameworks, and build system; offline build and test commands; which inputs those commands process; missing toolchains.
3. **Identity and authority.** Where authentication happens on each surface; per-resource authorization and tenant or owner scoping; privilege changes, revocation, and recovery paths; which controls are visible in source and which depend on deployment facts.
4. **Entry surfaces.** HTTP and browser, RPC, messages and queues, files and archives, CLI, environment and config, plugins, dependencies and CI, cloud events, model context and tool arguments, mobile deep links and webviews, local IPC.
5. **Paths to sinks.** For each surface, the major transformations, stored or derived copies, and security-relevant sinks (queries, shell, filesystem, templates, deserializers, outbound requests, privilege changes).
6. **Execution limits.** Small offline tests or fixtures usable for validation; commands that would fetch, publish, or touch shared state (prohibited); whether the sandbox controls in `SKILL.md` can be enforced locally.
7. **Comparable baseline** (optional). Similar software visible in docs or dependencies, used to calibrate effort and severity, never to dismiss a finding.

When delegation is available, split this into parallel read-only researchers: (a) product and stack, (b) principals and controls, (c) entry surfaces and sinks, (d) local execution and deployment visibility. Each returns facts only.

## Architecture summary

Write about 1,000 words or fewer: principals, protected resources, the stack, entry surfaces, key source-to-sink paths, controls, and deployment facts that are not visible in source. This summary is the shared context for hunters and verifiers.

## Coverage ledger

Seed **units** deterministically from the map. A unit is one **surface × boundary × attack class** (for example `api/orders × tenant-isolation × IDOR`). Unit IDs stay stable across runs so that coverage can be compared over time.

Unit states:

| State | Meaning |
|---|---|
| `planned` | Seeded, not yet assigned |
| `assigned` | Given to a hunter |
| `candidate` | Produced at least one candidate (linked by fingerprint) |
| `covered` | Hunted with no surviving candidate; record what was checked |
| `deferred` | Not done this run; give the reason |
| `blocked` | Cannot proceed; give the exact blocker |
| `out_of_scope` | Excluded by scope; never counts as covered |

## Prior runs

If prior ledgers and findings exist, read them before planning:

- A prior `confirmed` record whose relevant source is unchanged is carried into the current candidate set and re-verified. Hunters skip only that root cause.
- If the relevant source changed, create a revalidation unit. The prior verdict does not carry over.
- Prior `needs_validation`, `deferred`, `blocked`, and `out_of_scope` units are current work, not suppression keys.
- A prior `rejected` record suppresses only the identical unchanged claim, never coverage of its unit.
- A prior `quick` or scoped run contributes only its recorded evidence and gaps, never an implied "the rest is fine".
