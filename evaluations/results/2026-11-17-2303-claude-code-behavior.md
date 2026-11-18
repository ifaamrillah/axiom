# Eval run: behavior on claude-code

- Date: 2026-11-17T23:03
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
| product-discovery/B2 | — | 1/3 | 0/3 | -33 pp | skill 3/3, none 0/3 | skill 121832/1196, none 33094/983 | — | UNCOVERED (skill FAIL, none FAIL) |

- Tuning cases, graded runs passing: skill 1/3, none 0/3

Invalid runs (excluded from every rate above):

- none

### product-discovery/B2 [skill] (run 1/3): Premise challenge before deep elicitation, with a verdict that can kill

- Arm: skill
- Exit code: 0
- Skills invoked: product-discovery
- Tokens (in/out): 79570/1102
- Verdict: **FAIL** (independent grader: The answer covers the premise questions (problem, do-nothing cost, existing tools) before the options, offers four options with S/M/L effort including a config-file smallest option, and gives needs-clarification rather than go, while the kill-record expectation does not apply since the verdict is not kill (though the grader marks it false as nothing was recorded).)

Tool calls in order:

```text
1. Skill: product-discovery
   → Launching skill: product-discovery
```

Expectations:

- [x] Before detailed scope questions, asks or answers the premise questions (right problem, cost of doing nothing, what already exists such as environment variables or an existing library, how users will adopt it)
- [x] Presents 2–3 alternatives with rough effort (S/M/L), including a smallest option such as config flags or an existing library
- [x] Gives a verdict of go, needs-clarification, or kill, and does not give go while a must-have criterion is weak or unknown
- [ ] If the verdict is kill, records the decision, reason, date, and what would change it

Failure signals:

- [x] (must be false) Designs the full service without questioning whether it is needed

Final answer:

```text
I haven't read the repo for this. Git status shows no app code in this working directory, only the Axiom config files, so I'm going on what you've told me.

**Request vs. problem**
- **Request:** build a feature-flag service.
- **Problem (my assumption):** 3 developers want to change ~10 behaviors in one internal app without redeploying, or ship code dark.
- **Success signal:** not stated yet.

**Premise challenge**
- **If you do nothing:** flags stay as code constants or env vars, and changing one means a redeploy. For a 3-person team on one internal app, that may be fine.
- **What already exists:** hosted and open-source flag tools like Unleash, Flagsmith, GrowthBook and OpenFeature with a file provider. LaunchDarkly's free tier is another option. A config file or env var covers 10 flags.
- **"Our own service" means a server, a datastore, an API, an SDK, auth, a UI and uptime.** That's the bulk of the work, and with 10 flags and 3 users almost none of it is needed.

**Approaches**

| Option | Effort | What you get | Risk |
|---|---|---|---|
| A. Flags in a config file or env vars, behind a small `isEnabled("x")` wrapper | S (hours) | Edit and redeploy, or restart, to flip a flag | You can't flip a flag at runtime |
| B. A `flags` table in the app's existing database, read with a short cache, plus a bare admin page | S–M (days) | Runtime toggles, no new service | You own a small bit of code |
| C. A standalone flag service with its own API, SDK and UI | L (weeks) | Nothing the team needs at this size | Ongoing maintenance for 10 flags |
| D. A hosted or self-hosted tool such as Unleash or Flagsmith | S to adopt | Full-featured, with audit trail and targeting | A new dependency, and possibly a vendor |

**My recommendation:** A, with the wrapper written so you can move to B or D later without touching call sites. C isn't justified at this scale. The wrapper is the one piece worth building now.

**Verdict: `needs-clarification`.** It becomes `go` for A or B, and `kill` for C, as soon as I know the answer to this:

**Do you need to flip a flag at runtime without a redeploy, for example in production while something is on fire? I'd assume no, and go with A. OK?**

If you do need runtime flips, I'd move to B. Other things that would change the answer are percentage rollouts, per-user targeting, or an audit trail. If any of those apply, tell me, and D starts to beat building anything yourselves.
```

### product-discovery/B2 [skill] (run 2/3): Premise challenge before deep elicitation, with a verdict that can kill

- Arm: skill
- Exit code: 0
- Skills invoked: product-discovery
- Tokens (in/out): 121832/1278
- Verdict: **FAIL** (independent grader: The agent challenged the premise first (scale, do-nothing, existing options, cost), offered a smallest option with S effort plus hosted tools, and gave a needs-clarification verdict; however it did not present 2–3 alternatives each with S/M/L effort, only one effort estimate, though the kill-record expectation is not applicable since verdict wasn't kill (marked false as not demonstrated).)

Tool calls in order:

```text
1. Skill: product-discovery
   → Launching skill: product-discovery
2. Bash: git ls-files | head -20; ls -a | head -30; grep -rIil "feature.flag\|featureflag\|unleash\|launchdarkly\|growthbook" --e
   → . .. .agents .claude .git AGENTS.md CLAUDE.md
```

Expectations:

- [x] Before detailed scope questions, asks or answers the premise questions (right problem, cost of doing nothing, what already exists such as environment variables or an existing library, how users will adopt it)
- [x] Presents 2–3 alternatives with rough effort (S/M/L), including a smallest option such as config flags or an existing library
- [x] Gives a verdict of go, needs-clarification, or kill, and does not give go while a must-have criterion is weak or unknown
- [ ] If the verdict is kill, records the decision, reason, date, and what would change it

Failure signals:

- [x] (must be false) Designs the full service without questioning whether it is needed

Final answer:

```text
I checked the repo first. It has no app code, no commits and no existing flag usage, so it tells me nothing about your stack or how you use flags today. The premise question comes first, since building the service only makes sense if it holds.

**Request:** build your own feature-flag service.
**Problem I'm assuming:** you want to turn behavior on or off without a deploy, for one internal app, with three developers and about ten flags.

**Premise challenge, from what you've told me:**
- **Scale:** ten flags and three developers is far below the point where a service pays for itself. Nothing needs targeting rules, percentage rollouts, audit trails or SDKs for many languages.
- **Do nothing:** a typed config file or environment variables already gives you flags. A change needs a redeploy or restart.
- **Existing options:** a database table (or one JSON file) plus a small cached lookup function covers most of this. Hosted and self-hosted tools such as Unleash, GrowthBook and Flagsmith, or a free tier, cover the rest without maintenance on your side.
- **Cost of building:** a service means an admin UI, auth, storage, caching and uptime, and someone has to own it. For a team of three, that likely costs more than the flags are worth.

**Smallest option that could help:**
- Flags live in one table (`key`, `enabled`, `updated_at`).
- The app reads them through one `isEnabled(key)` function with a short cache, around 30 seconds.
- Developers toggle them with a small admin page or a SQL or CLI command.
- That's roughly S effort, and you could swap in a hosted tool later by changing only that one function.

**Current verdict: `needs-clarification`.** I can't call it `go` for a full service yet, and the evidence points toward a much smaller build. One answer would change that.

**Question 1 (highest impact):** what do you need flags to do that a config file or env var can't?

- **(a)** Flip a flag at runtime with no redeploy. This is my guess, and it points to the table-plus-function option above.
- **(b)** Let non-developers toggle flags, which means a UI with auth.
- **(c)** Roll out to some users but not others (per-user or percentage targeting). This is the case where a real tool starts to earn its place.
- **(d)** Something else, such as audit history or per-environment values.

If it's (a), I'd recommend the small table-and-function approach and drop the service idea. Is that right?
```

### product-discovery/B2 [skill] (run 3/3): Premise challenge before deep elicitation, with a verdict that can kill

- Arm: skill
- Exit code: 0
- Skills invoked: product-discovery
- Tokens (in/out): 124637/1196
- Verdict: **PASS** (independent grader: The agent challenged the premise (problem, do-nothing cost, existing options), offered three alternatives with rough effort (config ~1 hour, table ~1 day, hosted tool), and gave a needs-clarification verdict rather than go; expectation 4 applies only to a kill verdict, so it is vacuously satisfied, and the agent did not design a full service.)

Tool calls in order:

```text
1. Skill: product-discovery
   → Launching skill: product-discovery
2. Grep: feature.?flag|flags?\.|toggle|unleash|launchdarkly|growthbook
   → Found 20 files limit: 20 .agents/skills/quality-constraints/assets/definition-of-done.md .claude/skills/quality-constraints/assets/definition-of-done.md .agents/skills/quality-constraints/assets/constitution.md .claude/skills/quality-constr
3. Glob: *
   → .agents/skills/architecture-design/references/data-and-api.md .claude/skills/architecture-design/references/data-and-api.md .agents/skills/architecture-design/references/decisions-and-adrs.md .claude/skills/architecture-design/references/de
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
The repo has no application code, only the Axiom skill files, so it can't tell me anything about your app. Here is the premise challenge before any design work.

**Request:** build your own feature-flag service.
**Underlying problem (my assumption):** you need to ship code dark and turn behavior on or off without a deploy.

**Why I'm doubtful about a "service" for this team:**
- **Size:** three developers and about ten flags is the scale where a service costs more than it saves. A service means a datastore, an API, an admin UI, auth, an audit trail, caching and its own uptime. That is a bigger project than the ten flags it would manage.
- **Cheaper options that already exist:**
  1. **Config or env flags.** A typed `flags` module, with values from env vars or a JSON file. A change needs a redeploy or restart.
  2. **A DB table plus a tiny admin page or SQL.** Flags can change at runtime, and you get no per-user targeting.
  3. **A hosted or open-source tool** (GrowthBook, Unleash, a free tier of a hosted service). You get a UI, targeting and an audit trail, and you don't write or run anything.
- **If you do nothing,** you presumably keep using hardcoded constants or redeploys. I don't know whether that is actually hurting you.

**Verdict now: `needs-clarification`.** Right now "build a service" is a solution looking for a problem. The answer to the question below decides whether this is a config file (about an hour), a table (about a day), or a real service.

**Question 1 (highest impact):** What do you need to do with a flag that a redeploy can't do? My guess is that you only need to flip a flag at runtime without a deploy, for everyone at once. If so, I'd recommend a DB table or config file and not a service. Is that right, or do you also need any of these?
- (a) Per-user or percentage rollouts
- (b) Non-developers toggling flags
- (c) An audit trail of who changed what
- (d) Something else

Two more things I'll ask later, once I know this: what the app's stack and datastore are, and why building beats buying (for example a data-residency rule, a cost limit, or a wish to avoid vendors).
```

### product-discovery/B2 [none] (run 1/3): Premise challenge before deep elicitation, with a verdict that can kill

- Arm: none
- Exit code: 0
- Skills invoked: none
- Tokens (in/out): 33098/959
- Verdict: **FAIL** (independent grader: The answer questions whether a service is needed and offers config-file, DB-table, and buy options with some effort hints (not S/M/L), but it gives no explicit go/needs-clarification/kill verdict, and no kill decision is recorded.)

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
For three developers and about ten flags, build the smallest thing that works. I'd also check first whether you need a service at all.

**Start with a config file, not a service**

A `flags.json` or a `flags` table, read through one small `isEnabled(flag, context)` function, covers most needs at this scale. A service only pays off if you need one of these:

- Toggling flags at runtime without a deploy
- Per-user or percentage rollouts
- Non-developers flipping flags
- An audit trail of who changed what

If none apply, use env vars or a checked-in file. Changing a flag is then a PR, which gives you review and history for free.

**If you do need runtime toggling, build this**

1. **Storage:** one `flags` table in your existing database, with `key`, `enabled`, `description`, `owner`, `updated_by`, `updated_at`, and an optional `rules` JSON column. Don't add new infrastructure.
2. **Evaluation:** an in-process `isEnabled(key, {userId, ...})` function. Cache the flags in memory and refresh every 10–30 seconds. Failing to reach the database should never break the app, so fall back to a default declared in code.
3. **Targeting:** only what you need now, probably on/off, a user allowlist, and a percentage rollout. For percentages, hash `flagKey + userId` so each user gets a stable answer.
4. **Admin:** a protected page or a CLI command to toggle flags. Log every change to an audit table.
5. **Hygiene:** every flag gets an owner and a removal date. Stale flags are the real cost of flag systems, and with ten flags you can review them in a five-minute monthly check.

**What to skip**

- Multi-environment hierarchies
- A client SDK
- An experimentation or metrics layer
- Streaming updates
- A separate deployable service

You can add any of these later if a real need shows up.

**Buy instead if you want the extras**

Self-hosted Unleash or Flagsmith, or the free tiers of LaunchDarkly or Statsig, give you the UI, audit log, and targeting for little cost. For one app, the main reasons to build are avoiding a vendor or keeping the system as simple as possible. Building should take a day or two. Maintaining it is what costs you over time.

**Questions that would change my advice**

- Do you need to change flags without a deploy?
- Do you need per-user or percentage rollouts?
- What's the stack and database?
- Will anyone besides the three of you toggle flags?

If you tell me the stack, I can sketch the schema and the `isEnabled` function, or scaffold it in this repo.
```

### product-discovery/B2 [none] (run 2/3): Premise challenge before deep elicitation, with a verdict that can kill

- Arm: none
- Exit code: 0
- Skills invoked: none
- Tokens (in/out): 33094/983
- Verdict: **FAIL** (independent grader: The answer questions whether a service is needed, covers what already exists and the cost of building, and offers tiered alternatives including a smallest config-only option, but it gives no explicit go/needs-clarification/kill verdict (only a conditional recommendation), and no kill is recorded.)

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
For three developers and about ten flags in one app, I'd build much less than a "service". The question that decides it is whether you need to flip a flag without redeploying.

**Tier 0: flags in code or config (an hour of work)**
- A `flags.ts` (or YAML/JSON) file with typed defaults, plus env-var overrides per environment.
- Changing a flag means a PR and a deploy. You get review history and nothing new to operate.
- This is enough if "toggle without deploy" isn't a real need.

**Tier 1: one DB table plus a small module (about a day)**
- Use your existing database with a `flags(key, enabled, updated_at, updated_by)` table.
- The app reads it through an in-process cache with a TTL of 10–30 seconds, and falls back to the code defaults if the DB is unreachable.
- A tiny admin surface is enough: a CLI command or a single internal page with toggles. An audit log is one extra table or column.
- This covers runtime toggling and kill switches.

**Tier 2: a separate service**
- Only worth it if you have several apps or services sharing flags, or non-developers need a UI with permissions. You have neither.

**Build later, only if you actually hit it**
- Percentage rollouts or per-user targeting. A deterministic hash of `userId + flagKey` is about 10 lines, so it can wait.
- Flag-evaluation analytics, experiments, SDKs, or a streaming/push layer.

**Whichever tier you choose**
- Give every flag an owner and a removal date. Stale flags are the real long-term cost at this scale.
- Make flag reads synchronous and cheap, so they never add a network call to the request path.
- Default to the safe value when a flag is missing or the store is down.
- Before building anything, check whether a hosted free tier (Unleash self-hosted, GrowthBook, PostHog or LaunchDarkly's free plan) covers you. At ten flags it probably does. It's worth ruling out, though your reasons to build in-house are fair too.

**What would change my recommendation**
1. Do you need to toggle flags in production without a deploy?
2. Do you need per-user or percentage targeting, or only global on/off?
3. Will non-developers (PMs, support) flip flags?
4. What's the stack, and is there already a database?

If the answers are "yes, global only, no, and there's a DB", build Tier 1. I can scaffold it in this repo once you tell me the stack.
```

### product-discovery/B2 [none] (run 3/3): Premise challenge before deep elicitation, with a verdict that can kill

- Arm: none
- Exit code: 0
- Skills invoked: none
- Tokens (in/out): 33089/1093
- Verdict: **FAIL** (independent grader: The answer questions the need by recommending a config-file-first approach and offers build-vs-buy options, but it does not explicitly cover premise questions (cost of doing nothing, adoption) before scope, lacks S/M/L effort sizing for alternatives, and gives no explicit go/needs-clarification/kill verdict (kill-record expectation is not applicable/unmet).)

Tool calls in order:

```text
(no tool calls)
```

Expectations:

- [ ] Before detailed scope questions, asks or answers the premise questions (right problem, cost of doing nothing, what already exists such as environment variables or an existing library, how users will adopt it)
- [ ] Presents 2–3 alternatives with rough effort (S/M/L), including a smallest option such as config flags or an existing library
- [ ] Gives a verdict of go, needs-clarification, or kill, and does not give go while a must-have criterion is weak or unknown
- [ ] If the verdict is kill, records the decision, reason, date, and what would change it

Failure signals:

- [x] (must be false) Designs the full service without questioning whether it is needed

Final answer:

```text
With three developers and about ten flags, build very little. I'd start with a config file and add pieces only when something forces you to.

## Recommended build

**Phase 1: flags as typed config, no service**
- Keep one `flags.ts` (or YAML/JSON) file in the repo. Each flag has a name, a default, an owner and a created date.
- A small `isEnabled(flag, context)` helper reads it.
- Flags change through PR and deploy. You get review, history and rollback from git for free.
- This covers most teams at your scale.

**Phase 2: runtime toggles, only if you need them**
Add this if you need to flip a flag without a deploy, for example as a kill switch during an incident.
- Add one table: `flags(key, enabled, rollout_pct, updated_by, updated_at)`. Put it in the app's existing database.
- Add a tiny admin endpoint or page behind your existing auth.
- Cache flag values in-process for 10–30 seconds. Don't add Redis or a separate service.
- Write an audit row on every change.

**Evaluation features, in priority order**
1. On/off.
2. Per-user or per-group allowlist, such as internal testers.
3. Percentage rollout, using a stable hash of `flagKey + userId`.
4. Skip targeting rules, experiments and multi-environment hierarchies until there's a real need.

## Things that matter more than the service
- **Flag hygiene:** give every flag an owner and an expiry date, and have CI warn on stale flags. Flag debt is the real long-term cost.
- **Safe defaults:** if the lookup fails, return the hardcoded default and never throw.
- **Tests:** make it easy to force a flag in tests.
- **Logging:** log which flag value each request used, so you can debug later.

## Build vs. buy
Since this is for one internal app, check these options before you commit:
- **Self-hosted Unleash or Flagsmith:** a real UI and SDKs, but you have to operate them.
- **OpenFeature with a simple provider:** your code uses a standard API, so you can swap to a vendor later without rewriting call sites. Even if you hand-roll the backend, I'd write the call sites against this interface.
- **Hosted free tiers** (LaunchDarkly, PostHog, GrowthBook): often free at your scale.

Building makes sense if you want zero new infrastructure and about a day or two of work. It stops making sense once you want a polished UI, targeting rules or experiments.

## Questions that would change the plan
1. Do you need to flip flags without a deploy? If not, stay on Phase 1.
2. Who flips flags: only developers, or also non-technical people who'd need a UI?
3. What's the stack, and is there an existing database?
4. What are the flags for: kill switches, gradual rollouts, or per-customer features?

Tell me the stack and the answer to question 1, and I can scaffold Phase 1 in this repo. It's currently empty.
```
