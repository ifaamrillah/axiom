# Eval run: behavior on claude-code

- Date: 2026-11-17T22:05
- Host version: 2.1.326 (Claude Code)
- Model: host default
- Skill filter: product-discovery
- Max turns: 25
- Repeats per behavior case: 1; grader: separate claude-code session, model host default
- Isolation: user settings excluded
- Arms: skill (skill: Axiom skills installed; none: no skills, no kernel; oneliner: no skills, one generic line)
- Kernel in project instructions (skill arm): yes
- Per-run budget cap (USD): 1.5
- Runner: scripts/run_evals.py

Graded by a separate headless session with no tools and no repository context.

| Case | Tags | skill pass | Skill invoked | Median tokens (in/out) | Seeded recall / false | Verdict |
|---|---|---|---|---|---|---|
| product-discovery/B2 | — | 1/1 | skill 1/1 | skill 79481/1356 | — | skill PASS |

- Tuning cases, graded runs passing: skill 1/1

Invalid runs (excluded from every rate above):

- none

### product-discovery/B2 [skill]: Premise challenge before deep elicitation, with a verdict that can kill

- Arm: skill
- Exit code: 0
- Skills invoked: product-discovery
- Tokens (in/out): 79481/1356
- Verdict: **PASS** (independent grader: The agent questioned the premise and noted the existing options (env/config flags, open-source libraries), though it did not explicitly cover the cost of doing nothing or adoption; it then gave S/M/L-sized alternatives with config flags as the smallest and a needs-clarification verdict, so the kill-recording expectation does not apply.)

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
I'd push back on building a service before we design one. At three developers, ten flags and one app, a separate flag service is probably more than you need. Here's my reasoning.

**What I checked:** this repo has only agent config (`CLAUDE.md`, `AGENTS.md`, `.claude/`, `.agents/`). There's no app code to see what flags you already use or how you deploy, so the rest is based on what you've told me.

**The premise:** a feature-flag service is a separate thing to run. It needs hosting, auth, uptime, a client SDK, and a decision about what the app does when the service is down. That overhead pays off with many teams, many apps, or non-engineers flipping flags. With ten flags, most of the value usually comes from one of these much smaller options:

| Option | What it is | Effort | Gives you | Gives up |
|---|---|---|---|---|
| **A. Flags in config or env vars** | A typed `flags.ts` (or similar) read from env or a config file | S (hours) | Code review on every change, zero infrastructure | Changing a flag needs a redeploy or restart |
| **B. Flags table in the app's existing database** | `flags(name, enabled, rules_json)`, cached for about 30s, plus a small admin page | S–M (a few days) | Changes at runtime with no redeploy, a simple audit log | You build a little UI and handle caching |
| **C. Self-hosted open source** (e.g. Unleash, Flagsmith, GrowthBook, or flagd via OpenFeature) | An off-the-shelf flag server | M (setup and running it) | Targeting, percentage rollouts and a UI already built | Another service to run and upgrade |
| **D. A custom flag service** (your proposal) | A new service you build yourselves | L | Exactly what you want | Everything C gives you, built and maintained by three people |

My starting recommendation is **B**, or **A** if a redeploy to change a flag is fine. D only makes sense if you need something none of the others can do, and I can't see what that would be yet.

**Verdict: `needs-clarification`.** The answer to this question decides between the options:

> **Do you need to change a flag without redeploying, and do you need per-user targeting or percentage rollouts?** My guess is "runtime on/off, plus enabling for a few named users, no percentages," which points to option B. Is that right?

- If redeploys are fine → **A**, and we're done in an afternoon.
- If you need runtime toggles, simple rules, or both → **B**.
- If you need percentage rollouts, experiments, or non-developers flipping flags → **C** before D.
- If you have a reason to build your own anyway, such as learning, compliance, or no new dependencies allowed, tell me. That changes the trade-offs.

After you answer I'll ask a question or two more (where the app runs, who flips flags), then write a short design summary for you to approve before any spec or code.
```
