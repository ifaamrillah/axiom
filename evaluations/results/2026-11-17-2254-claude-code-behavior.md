# Eval run: behavior on claude-code

- Date: 2026-11-17T22:54
- Host version: 2.1.326 (Claude Code)
- Model: host default
- Skill filter: product-discovery
- Max turns: 25
- Repeats per behavior case: 3; grader: separate claude-code session, model host default
- Isolation: user settings excluded
- Arms: skill,none (skill: Axiom skills installed; none: no skills, no kernel; oneliner: no skills, one generic line)
- Kernel in project instructions (skill arm): yes
- Per-run budget cap (USD): 1.5
- Runner: scripts/run_evals.py

Graded by a separate headless session with no tools and no repository context.

| Case | Tags | skill pass | none pass | Δ none vs skill | Skill invoked | Median tokens (in/out) | Seeded recall / false | Verdict |
|---|---|---|---|---|---|---|---|---|
| product-discovery/B2 | — | 1/3 | 0/3 | -33 pp | skill 1/3, none 0/3 | skill 79738/1419, none 33089/1311 | — | UNCOVERED (skill FAIL, none FAIL) |

- Tuning cases, graded runs passing: skill 1/3, none 0/3

Invalid runs (excluded from every rate above):

- none

### product-discovery/B2 [skill] (run 1/3): Premise challenge before deep elicitation, with a verdict that can kill

- Arm: skill
- Exit code: 0
- Skills invoked: architecture-design
- Tokens (in/out): 79738/1480
- Verdict: **FAIL** (independent grader: The agent questioned necessity and offered four options (config flags, DB table, standalone service, buy/self-host) with rough effort, though not in S/M/L terms, but it never asked premise questions such as the cost of doing nothing or adoption before scoping, and it gave a recommendation rather than an explicit go/needs-clarification/kill verdict while key criteria remained assumed.)

Tool calls in order:

```text
1. Skill: architecture-design
   → Launching skill: architecture-design
```

Expectations:

- [ ] Before detailed scope questions, asks or answers the premise questions (right problem, cost of doing nothing, what already exists such as environment variables or an existing library, how users will adopt it)
- [x] Presents 2–3 alternatives with rough effort (S/M/L), including a smallest option such as config flags or an existing library
- [ ] Gives a verdict of go, needs-clarification, or kill, and does not give go while a must-have criterion is weak or unknown
- [ ] If the verdict is kill, records the decision, reason, date, and what would change it

Failure signals:

- [x] (must be false) Designs the full service without questioning whether it is needed

Final answer:

```text
With three developers and about ten flags, I'd build very little. Here is the decision, with my assumptions marked.

## Drivers

| Driver | Status |
|---|---|
| One internal app, 3 devs, ~10 flags | Given |
| Flags need to change without a deploy | **Assumed** |
| Per-user or per-group targeting, or percentage rollouts | **Assumed:** mostly on/off, maybe per-user allowlists |
| Non-developers need to toggle flags | **Assumed:** no |
| Audit trail of who changed what | **Assumed:** nice to have |
| Latency or availability target | **Assumed:** flag reads must not take the app down |

The repo has no application code yet, so I couldn't check your stack. I'm assuming a single app with an existing database.

## Options

| Option | What it is | Cost to build | Reversal cost |
|---|---|---|---|
| **A. Config or env flags** | Flags in a config file or env vars, read at startup. A change means a redeploy or restart. | Hours | Trivial |
| **B. Table in your existing DB (recommended)** | A `feature_flags` table (`key`, `enabled`, `allowed_users`, `updated_by`, `updated_at`) and a small helper with a short in-process cache (~30s). Changes happen through a SQL statement or a tiny admin page. | ~1–2 days | Low. It's one table and one function. |
| **C. Standalone flag service** | A separate service with its own API, SDK, and UI. | Weeks, plus ongoing ops | High |
| **D. Buy or self-host** (Unleash, Flagsmith, GrowthBook, LaunchDarkly) | A hosted or self-hosted product. | Days to integrate | Medium |

I'd rule out C. It adds a deployable, a datastore, and a failure mode for a problem that ten rows can solve. A separate service only pays off with multiple apps or teams, or with non-developers needing a UI. You have neither.

## Recommendation: B, with A as the starting point if you don't need runtime changes

- **Contract:** one function, `isEnabled(flag, { userId })`. It returns the default if the flag is missing or the lookup fails. A broken flag read should never take the app down, and the default should be the safe or off state.
- **Ownership:** the app owns the table. There is no second writer.
- **Caching:** a ~30s in-process cache, so a toggle takes effect within 30s and no request hits the DB per check.
- **Audit:** `updated_by` and `updated_at` columns, plus an optional history table if you want one.
- **Cleanup:** add an owner and a "remove by" date to each flag. The real cost of flags is the ones nobody deletes.
- **Tests:** unit tests for the missing-flag default, the DB-failure default, and cache expiry.

If the cost of building and maintaining B ever outweighs its value, option D (Unleash or GrowthBook, self-hosted) is the exit. Keeping `isEnabled()` as the only call site makes that swap a one-file change.

## Questions that would change the answer

1. Do you need to flip flags without a deploy? If not, use A.
2. Do you need percentage rollouts or targeting beyond a user allowlist? If so, D becomes more attractive than hand-rolling the bucketing logic.
3. Is there a database, and what stack is the app on? That determines the shape of the helper.

If this matches your needs, I can write a one-page ADR and a task breakdown. Once you tell me the stack, I can also start on the implementation.
```

### product-discovery/B2 [skill] (run 2/3): Premise challenge before deep elicitation, with a verdict that can kill

- Arm: skill
- Exit code: 0
- Skills invoked: architecture-design
- Tokens (in/out): 79756/1419
- Verdict: **FAIL** (independent grader: The agent questioned whether a service is needed and offered four options with a recommendation (start with A), but it gave no S/M/L effort estimates and no explicit go/needs-clarification/kill verdict, and the kill-record criterion does not apply since no kill was given.)

Tool calls in order:

```text
1. Skill: architecture-design
   → Launching skill: architecture-design
```

Expectations:

- [x] Before detailed scope questions, asks or answers the premise questions (right problem, cost of doing nothing, what already exists such as environment variables or an existing library, how users will adopt it)
- [ ] Presents 2–3 alternatives with rough effort (S/M/L), including a smallest option such as config flags or an existing library
- [ ] Gives a verdict of go, needs-clarification, or kill, and does not give go while a must-have criterion is weak or unknown
- [ ] If the verdict is kill, records the decision, reason, date, and what would change it

Failure signals:

- [x] (must be false) Designs the full service without questioning whether it is needed

Final answer:

```text
I'd build a small module inside the app, not a service. For three developers and about ten flags, a separate feature-flag service costs more than it returns.

I haven't read any app code. The repo has no commits and no application files, so these drivers come from your message or are my assumptions.

**Drivers**
- Given: one internal app, 3 developers, about 10 flags.
- Assumed: your own people are the only users, there's one datastore already, and a few minutes of delay on a flag change is fine.
- Assumed: you don't need percentage rollouts or A/B experiments.

**Options**

| Option | What it is | Flag change needs a deploy? | Cost to reverse |
|---|---|---|---|
| A. Config or env vars | A typed `flags` module that reads a config file or env vars | Yes (or a restart) | Trivial |
| B. DB table plus helper | A `feature_flags(key, enabled, updated_at, updated_by)` table. The app reads it through a small module with a short cache (30–60s), and a tiny admin page or CLI flips flags. | No | Low, because it sits behind the same `isEnabled(key, ctx)` function as A |
| C. Existing tool | Self-hosted Unleash or GrowthBook, or a hosted free tier | No | Medium, because you take on another system or vendor |
| D. Standalone service | Your own flag API, UI and SDK | No | High |

**Recommendation**
- Start with A, behind a single `isEnabled(key, ctx?)` function.
- Move to B only if you hit one of these: you need to flip flags without redeploying, you want an audit trail, or non-developers need to toggle flags.
- Skip C and D unless you need per-user targeting, percentage rollouts, or experiments. None of those fit your stated scale.
- Keeping everything behind one function means moving from A to B later touches one file.

**What to include if you build B**
- Typed, central flag definitions with a default for each, so a missing row or a DB outage falls back to the default and never breaks the app.
- A flag-removal habit: each flag gets an owner and a "remove by" date. Stale flags are the real cost at your scale.
- Audit via `updated_by` and `updated_at`, or an append-only history table if you need it.
- Tests that cover both flag states for each flag that is live.

**What I'd skip**
- SDKs, streaming updates, a rules engine, multi-environment hierarchies, and a standalone UI beyond one admin page.

**Questions that would change the answer**
1. Do you need to flip a flag in production without a deploy or restart? If yes, B. If no, A.
2. Does any flag need per-user or per-group targeting, like "on for the 3 of us first"? If yes, B needs a small rules field, or C becomes worth a look.
3. What's the stack and datastore? I can then sketch the module and schema.

If you answer 1 and 2, I can write a short ADR and a task list for the option you pick. I'd also look at the app code once it's in the repo.
```

### product-discovery/B2 [skill] (run 3/3): Premise challenge before deep elicitation, with a verdict that can kill

- Arm: skill
- Exit code: 0
- Skills invoked: product-discovery
- Tokens (in/out): 79639/1182
- Verdict: **PASS** (independent grader: The answer opens with a premise check (the existing repo, what a service really requires, the cost of building versus doing nothing), offers options A/B/C with S/S–M/L effort including a smallest config-file option, gives a needs-clarification verdict, and since the verdict is not kill the kill-recording requirement does not apply, and it never designs the full service.)

Tool calls in order:

```text
1. Skill: product-discovery
   → Launching skill: product-discovery
```

Expectations:

- [x] Before detailed scope questions, asks or answers the premise questions (right problem, cost of doing nothing, what already exists such as environment variables or an existing library, how users will adopt it)
- [x] Presents 2–3 alternatives with rough effort (S/M/L), including a smallest option such as config flags or an existing library
- [x] Gives a verdict of go, needs-clarification, or kill, and does not give go while a must-have criterion is weak or unknown
- [x] If the verdict is kill, records the decision, reason, date, and what would change it

Failure signals:

- [x] (must be false) Designs the full service without questioning whether it is needed

Final answer:

```text
I can't recommend building a service yet. At your scale, the premise needs checking first.

**What the repo shows:** it has no application code yet, only the Axiom config files. I don't know your stack or deploy process.

**Premise check:** a feature-flag service means a store, an API, an admin UI, auth, an audit trail and an SDK. Three developers and about ten flags probably don't need most of that. Here are the options, smallest first:

| Option | Effort | What you get | What you lack |
|---|---|---|---|
| A. Flags in a config file or env vars, read through one `isEnabled("x")` helper | S (about an hour) | Flags are versioned and reviewed in git. A flag change takes a deploy. | Runtime toggles, per-user targeting |
| B. A `flags` table in your existing database, the same helper, and a tiny admin page or SQL | S–M (about a day) | Runtime toggles with no deploy, and an easy path to per-user or percentage rollout later | Audit history unless you add it |
| C. A standalone service with an API, UI, SDK and audit log | L | Everything | A lot to maintain, and it is the one most likely to break while the other ten flags are fine |

Hosted or open-source options (Unleash, GrowthBook, or a free tier of a hosted service) are a fourth path, and they could replace C entirely. Whether they fit depends on whether you can send flag data to a third party.

I'd start with A, with the helper written so that moving to B later changes only the helper's internals. Doing nothing more than A is a valid result.

**Verdict so far: `needs-clarification`.** The question that decides between A, B and C:

**Do you need to flip a flag in production without a deploy, for example as a kill switch, or is "change it and redeploy" fast enough?**

- If a redeploy is fine, the answer is A, and we're nearly done.
- If you need runtime toggles, the answer is B.
- C only comes into play if you also need per-user targeting, percentage rollouts, or an audit trail for compliance.

I'd assume you need runtime toggles but not targeting, which points to B. Is that right? If you also tell me the stack, I can make B concrete.
```

### product-discovery/B2 [none] (run 1/3): Premise challenge before deep elicitation, with a verdict that can kill

- Arm: none
- Exit code: 0
- Skills invoked: none
- Tokens (in/out): 33089/1182
- Verdict: **FAIL** (independent grader: The answer questions necessity up front and offers three tiers with rough effort, but it gives no explicit go/needs-clarification/kill verdict (only a recommendation plus a request for stack info), and no kill record applies.)

Tool calls in order:

```text
(no tool calls)
```

Expectations:

- [x] Before detailed scope questions, asks or answers the premise questions (right problem, cost of doing nothing, what already exists such as environment variables or an existing library, how users will adopt it)
- [x] Presents 2–3 alternatives with rough effort (S/M/L), including a smallest option such as config flags or an existing library
- [ ] Gives a verdict of go, needs-clarification, or kill, and does not give go while a must-have criterion is weak or unknown
- [ ] If the verdict is kill, records the decision, reason, date, and what would change it

Failure signals:

- [x] (must be false) Designs the full service without questioning whether it is needed

Final answer:

```text
**My recommendation:** build very little, and possibly nothing. For 3 developers and about 10 flags, a flag service is mostly overhead. Start with the smallest thing that works and add pieces only when something forces you to.

## Questions that decide the design

1. **Do you need to change a flag without a deploy?** If not, a config file in the repo is enough, and it gives you review and history through git.
2. **Do non-developers need to flip flags?** If yes, you need a UI. If not, you don't.
3. **Do you need per-user or percentage rollouts?** Or is it just on/off per environment?
4. **Do you need an audit trail?** Who changed what, and when?

## Options, smallest first

| Tier | What it is | Build cost | Use when |
|---|---|---|---|
| 1. Config file | `flags.json` or env vars, read at startup | About an hour | Flag changes can ride a deploy |
| 2. DB table plus tiny admin | `flags(key, enabled, rules_json, updated_by, updated_at)`, cached in-process for about 30s, and a minimal admin page or CLI | 1–2 days | You need runtime toggles without a deploy |
| 3. Self-hosted OSS | Unleash or Flagsmith, with the OpenFeature SDK | Setup and ops work | You need segments, gradual rollouts, or a polished UI |

**Tier 2 is probably the right fit if you want your own service.** Here is what I'd put in it:

- **Evaluation:** a single `isEnabled(flagKey, context)` function. The context is the user ID and environment.
- **Rules:** keep them minimal. Support on/off, an optional user allowlist, and an optional percentage rollout. For the percentage, hash `flagKey + userId` so each user gets a stable result.
- **Caching:** poll or cache in the app with a short TTL. Never call the flag store on every request.
- **Failure behavior:** if the store is down, use the last known value, then a hardcoded default in code. A flag outage shouldn't take down the app.
- **Audit log:** an append-only table of changes. It's cheap and you'll want it the first time something breaks.
- **Admin:** a CLI or a single authenticated page. Skip RBAC, since three developers don't need it.
- **Wrapper:** call flags through your own thin interface, or OpenFeature. Then you can swap in Tier 3 later without touching call sites.

## What to leave out

- Multi-environment hierarchies, experiments and A/B statistics, and a separate service or deployment.
- SDKs for several languages. You have one app.
- Flag dependencies or scheduling.

## Process

Give every flag an owner and a removal date. At 10 flags, stale flags are a bigger risk than missing features. A comment or a `removeBy` field in the definition is enough.

## Next step

Tell me your stack and whether you need runtime toggles. The repo is empty right now, so I can't infer it. With that, I can sketch the Tier 2 schema and the `isEnabled` implementation, or scaffold Tier 1 with the wrapper interface so you can upgrade later.
```

### product-discovery/B2 [none] (run 2/3): Premise challenge before deep elicitation, with a verdict that can kill

- Arm: none
- Exit code: 0
- Skills invoked: none
- Tokens (in/out): 33091/1343
- Verdict: **FAIL** (independent grader: The answer questions the build premise and offers two options with rough effort (an hour vs. a day or two) including a smallest config option, but it doesn't explicitly cover cost of doing nothing or existing libraries up front, gives no formal go/needs-clarification/kill verdict (it recommends Option B while key criteria remain unknown), and no kill was issued so nothing was recorded.)

Tool calls in order:

```text
(no tool calls)
```

Expectations:

- [ ] Before detailed scope questions, asks or answers the premise questions (right problem, cost of doing nothing, what already exists such as environment variables or an existing library, how users will adopt it)
- [x] Presents 2–3 alternatives with rough effort (S/M/L), including a smallest option such as config flags or an existing library
- [ ] Gives a verdict of go, needs-clarification, or kill, and does not give go while a must-have criterion is weak or unknown
- [ ] If the verdict is kill, records the decision, reason, date, and what would change it

Failure signals:

- [x] (must be false) Designs the full service without questioning whether it is needed

Final answer:

```text
I'd build less than you probably expect. At 3 developers and about 10 flags, the hard parts of a flag service (targeting UIs, SDKs for many languages, analytics) don't apply. What's left is a few small decisions.

**The one question that decides the design:** do you need to flip a flag without a deploy?

**Option A: flags in code or config (start here if the answer is "rarely")**
- A single typed file in the repo, such as `flags.ts`, with `{ name, default, owner, description, removeBy }` per flag. Env vars can override it per environment.
- `isEnabled("new-checkout", { userId })` is a plain function.
- Your audit trail is git history and your review process is PRs.
- This takes about an hour to build and has no new infrastructure to run.

**Option B: flags in your existing database (if you need runtime flips)**
- One table: `key, enabled, rollout_percent, allowed_user_ids, updated_by, updated_at`.
- The app reads it with a 10–30 second in-memory cache, so flag checks never hit the DB on the hot path.
- Admin is either a small internal page (a table with toggles) or just SQL at first.
- Write an `audit_log` row on every change. It's a few lines and you'll want it the first time something breaks.
- This takes a day or two.

**What I'd include in either option**
- **Boolean flags plus two targeting rules:** a user allowlist and a stable percentage rollout. Hash `flagKey + userId` so a user stays in the same bucket. That covers nearly every real need at your size.
- **A safe default when evaluation fails:** if the DB or cache is down, return the flag's code-defined default rather than throwing.
- **An owner and a removal date on every flag.** Stale flags are the real long-term cost, so make the removal date visible and add a lint or CI warning when one is past due.
- **One evaluation path.** If you have both a frontend and a backend, evaluate server-side and send the frontend the resolved values. That avoids two implementations drifting apart.

**What I'd skip:** multi-environment promotion workflows, complex rule engines, experiments and analytics, and SDKs for other languages.

**On build vs. adopt:** since this is for one app, it's reasonable to build. If it grows toward targeting rules or non-developers toggling flags, look at OpenFeature with a provider, Unleash, or GrowthBook. If you wrap your own evaluation behind an `isEnabled()` function from day one, switching later is cheap.

**My recommendation:** build Option B with the DB table, cache, percentage rollout, allowlist and audit log, and skip the admin UI until someone asks for it. If you never need to flip a flag live, Option A is enough.

To pick between them, I need to know:
1. What's your stack, and do you already have a database?
2. Do non-developers need to flip flags?
3. Do you need per-user targeting, or is on/off per environment enough?

If you tell me the stack, I can sketch the schema and the evaluation function. The repo is empty right now, so I'd start from scratch.
```

### product-discovery/B2 [none] (run 3/3): Premise challenge before deep elicitation, with a verdict that can kill

- Arm: none
- Exit code: 0
- Skills invoked: none
- Tokens (in/out): 33087/1311
- Verdict: **FAIL** (independent grader: The answer questions whether a service is needed first and offers config-file, DB-table and hosted/self-hosted alternatives with rough effort for only the build option, but it never gives an explicit go/needs-clarification/kill verdict (it hedges with 'build a very small one, or don't build one at all'), and no kill record applies.)

Tool calls in order:

```text
(no tool calls)
```

Expectations:

- [x] Before detailed scope questions, asks or answers the premise questions (right problem, cost of doing nothing, what already exists such as environment variables or an existing library, how users will adopt it)
- [x] Presents 2–3 alternatives with rough effort (S/M/L), including a smallest option such as config flags or an existing library
- [ ] Gives a verdict of go, needs-clarification, or kill, and does not give go while a must-have criterion is weak or unknown
- [ ] If the verdict is kill, records the decision, reason, date, and what would change it

Failure signals:

- [x] (must be false) Designs the full service without questioning whether it is needed

Final answer:

```text
**Recommendation: build a very small one, or don't build one at all.** At 3 developers and about 10 flags, the work is mostly deciding what you need. The code is small.

## First, check whether you need a service
Before building, check which of these you actually need:

| Need | Smallest thing that works |
|---|---|
| Flip a flag per environment on deploy | Env vars or a checked-in JSON/YAML file |
| Flip a flag at runtime without a deploy | A DB table, plus a small cache |
| Per-user or percentage rollout | A DB table, plus a deterministic hash |
| Non-developers toggling flags | An admin page, which is where the cost starts |
| Audit trail and history | An `audit` table, or git history if flags live in a file |

If all you need is deploy-time flags, a config file in the repo is enough. You get review, history and rollback from git, and there's nothing to operate.

If you need runtime toggles, build the DB-backed version below. Self-hosting Unleash or GrowthBook, or using a hosted free tier such as Flagsmith or PostHog, is also reasonable. That's worth a short look first, but a custom build at this scale is defensible.

## What I'd build (runtime toggles)
**Data model.** One `flags` table with these columns:
- `key` (unique)
- `enabled`
- `rollout_percent` (0–100)
- `allow_users` (list of user IDs)
- `description`
- `owner`
- `updated_at` and `updated_by`

Add an `audit_log` table that records who changed what and when.

**Evaluation.** This is a single function, `isEnabled(key, {userId})`:
1. If the flag is missing, return the code-defined default. Every flag has a default in code, so an outage or a missing row fails safe.
2. If the user is in `allow_users`, return true.
3. If `enabled` is false, return false.
4. Otherwise return `hash(key + userId) % 100 < rollout_percent`. The hash makes the result stable per user.

**Delivery.** The flags live inside your one app, so there's no separate service and no SDK.
- Load all flags into memory.
- Refresh every 15–30 seconds, or on a change notification (Postgres `LISTEN/NOTIFY`).
- Evaluation then never hits the network or DB per request.

**Admin.** Start with a CLI or a protected endpoint that lists and toggles flags. Build a UI only once someone asks for one.

**Hygiene.** This matters more than the tooling. Give each flag an owner and an expiry date, and log a warning when a flag is past its date. Most flag systems fail because dead flags pile up.

## What to skip
- Multi-environment projects and complex targeting rules
- Multivariate flags (stick to booleans)
- Experiment and analytics integration
- Your own SDKs
- A separate deployable service

Total effort is roughly 1–3 days for the table, evaluator, cache and CLI. Wrapping the evaluator behind the [OpenFeature](https://openfeature.dev) interface is optional. It makes a later move to a vendor a config change.

## Questions that would change this
1. Do flags need to change without a deploy? If not, use the config file.
2. Does anyone non-technical need to flip flags?
3. What's the stack, and is there already a database? I can look at the repo if you point me at the app. This directory is empty.

If you can answer the first and third, I can sketch the schema and evaluator for your stack.
```
