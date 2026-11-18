# Eval run: behavior on claude-code

- Date: 2026-11-17T22:02
- Host version: 2.1.326 (Claude Code)
- Model: host default
- Skill filter: product-discovery
- Max turns: 25
- Repeats per behavior case: 1; grader: separate claude-code session, model host default
- Isolation: user settings excluded
- Arms: skill,none (skill: Axiom skills installed; none: no skills, no kernel; oneliner: no skills, one generic line)
- Kernel in project instructions (skill arm): yes
- Per-run budget cap (USD): 1.5
- Runner: scripts/run_evals.py

Graded by a separate headless session with no tools and no repository context.

| Case | Tags | skill pass | none pass | Δ none vs skill | Skill invoked | Median tokens (in/out) | Seeded recall / false | Verdict |
|---|---|---|---|---|---|---|---|---|
| product-discovery/B2 | — | 0/1 | 0/1 | +0 pp | skill 1/1, none 0/1 | skill 79180/967, none 33153/1056 | — | UNCOVERED (skill FAIL, none FAIL) |

- Tuning cases, graded runs passing: skill 0/1, none 0/1

Invalid runs (excluded from every rate above):

- none

### product-discovery/B2 [skill]: Premise challenge before deep elicitation, with a verdict that can kill

- Arm: skill
- Exit code: 0
- Skills invoked: product-discovery
- Tokens (in/out): 79180/967
- Verdict: **FAIL** (independent grader: The agent questions the premise and offers four options with S/M/L effort, starting with config flags, but it never states an explicit go, needs-clarification or kill verdict; the kill-record expectation passes because no kill was given.)

Tool calls in order:

```text
1. Skill: product-discovery
   → Launching skill: product-discovery
```

Expectations:

- [x] Before detailed scope questions, asks or answers the premise questions (right problem, cost of doing nothing, what already exists such as environment variables or an existing library, how users will adopt it)
- [x] Presents 2–3 alternatives with rough effort (S/M/L), including a smallest option such as config flags or an existing library
- [ ] Gives a verdict of go, needs-clarification, or kill, and does not give go while a must-have criterion is weak or unknown
- [x] If the verdict is kill, records the decision, reason, date, and what would change it

Failure signals:

- [x] (must be false) Designs the full service without questioning whether it is needed

Final answer:

```text
Before we design anything, I want to push on the premise. At three developers and about ten flags, a separate feature-flag *service* (its own server, database and UI) is probably more than you need. Most teams your size do fine with one of these:

| Option | What it is | Effort | When it fits |
|---|---|---|---|
| **A. Flags in config** | A `flags.json` file or env vars, read by a small `isEnabled("x")` helper | S (an afternoon) | Changing a flag through a deploy or restart is acceptable |
| **B. Flags in your app's existing database** | A `flags` table plus a small admin page or SQL toggle, cached for about 30s | S–M (1–2 days) | You need to flip flags at runtime without deploying, maybe with simple per-user rules |
| **C. Off-the-shelf, self-hosted** | flagd (an OpenFeature project), Unleash OSS or GrowthBook | M (setup plus running it) | You need percentage rollouts, targeting, audit history or a UI for non-developers |
| D. A separate service you build yourself | Its own deployable, API, storage and UI | L, and you maintain it forever | Rarely right at this size. C gives you this without the upkeep. |

My starting recommendation is **A**, and **B** if you have to flip flags at runtime. Whichever you pick, put a thin interface in front of it so you can move to C later without touching every call site.

Your answer to this question decides most of the choice:

**Do you need to turn a flag on or off without redeploying or restarting the app?**
- (a) No. A deploy or restart is fine, so go with **A**.
- (b) Yes, and flags are simply on or off for everyone, so go with **B**.
- (c) Yes, and also per user, per group or by percentage rollout, so it's between **B** with simple rules and **C**.

I'd guess (a) or (b). Does that match, or is there a reason behind "build our own service" that I'm missing, like a past problem with config flags or an off-the-shelf tool you've ruled out?
```

### product-discovery/B2 [none]: Premise challenge before deep elicitation, with a verdict that can kill

- Arm: none
- Exit code: 0
- Skills invoked: none
- Tokens (in/out): 33153/1056
- Verdict: **FAIL** (independent grader: The agent questioned whether a separate service was needed and offered tiered options with rough effort (env-var config flags in half a day, a DB table in 1–2 days, or buying an existing tool), but it never gave an explicit go, needs-clarification or kill verdict, and it did not address the cost of doing nothing or how users would adopt it.)

Tool calls in order:

```text
(no tool calls)
```

Expectations:

- [x] Before detailed scope questions, asks or answers the premise questions (right problem, cost of doing nothing, what already exists such as environment variables or an existing library, how users will adopt it)
- [x] Presents 2–3 alternatives with rough effort (S/M/L), including a smallest option such as config flags or an existing library
- [ ] Gives a verdict of go, needs-clarification, or kill, and does not give go while a must-have criterion is weak or unknown
- [x] If the verdict is kill, records the decision, reason, date, and what would change it

Failure signals:

- [x] (must be false) Designs the full service without questioning whether it is needed

Final answer:

```text
For three developers and about ten flags, I'd skip building a *service*. Build a small flag module inside the app instead. A separate service brings deployment, uptime, auth, a client SDK and network failure modes, and none of that pays off at this size.

## What to build

**Step 1: flags in code (half a day)**
- One file, such as `flags.ts` or `flags.py`, lists every flag with its name, default value, owner, description and the date it should be removed.
- Each flag can be overridden by an environment variable (`FLAG_NEW_CHECKOUT=true`).
- One accessor, `isEnabled("new_checkout", user?)`, is the only way code reads a flag.
- Changing a flag means a redeploy or an env change. That's often enough when you have three people.

**Step 2: runtime toggles, only if you need to flip flags without a deploy (1–2 days)**
- Add a `feature_flags` table to the database the app already uses, with `name, enabled, rules (json), updated_by, updated_at`.
- The accessor reads the table, caches it in memory for 30–60 seconds, and falls back to the code default if the database is unreachable.
- Add an admin page behind your existing auth: a list of flags with toggles.
- Add an audit row for each change (who, when, old value, new value). It's cheap and helps when debugging.

**Targeting: keep it minimal**
- Most internal apps need three things: on/off, an allowlist of user IDs or emails, and maybe a percentage rollout using `hash(flag + user_id) % 100`.
- Leave out segments, rule engines, A/B analytics and multi-environment promotion until someone asks for them.

## Things that matter more than features
- **Removal discipline.** Ten flags turns into forty stale ones. The removal date plus a CI check or test that fails on expired flags fixes this.
- **Safe defaults.** If the store is down, every flag returns its code default.
- **Testability.** Tests should be able to force a flag on or off, for example `withFlag("x", true)`.

## When to buy instead
Use a hosted or open-source tool (Unleash, Flagsmith, GrowthBook, or a free tier of LaunchDarkly or PostHog) if you'll need any of these: several apps or services sharing flags, non-engineers managing rollouts, experiment analytics, or compliance-grade audit. At your size, self-hosting one of those is also more ops work than the database table.

## Questions that settle the design
1. Do you need to flip flags without a deploy, or are env vars and a redeploy fine?
2. Do flags depend on the user (allowlists or percentages), or are they global on/off?
3. What's the stack: language, framework, database?
4. Who flips flags: only you three, or others too?

If you answer those, I can write the flag module, the migration and the admin page for your stack. The repo here is currently empty, so tell me where the app lives or what it's built with.
```
