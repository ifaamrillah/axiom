---
skill: writing-quality
---

# Eval cases: writing-quality

## Should trigger

- "Humanize this, it sounds like ChatGPT wrote it: 'In today's fast-paced world, our robust API seamlessly empowers teams to unlock their full potential.'"
- "Tighten this PR description, it's too fluffy: 'This PR delves into the checkout flow and leverages a robust new approach to elevate the overall user experience. In short, it makes things better.'"
- "Make this README intro less salesy and more direct"

## Should not trigger

- "Write a spec for coupon codes" → `requirements-analysis`
- "Fix the typo 'recieve' in README.md" → `none`
- "Review my PR before I merge it" → `code-review`

## Behavior

### B1: Remove tells, keep facts

- Prompt: "Rewrite this so it doesn't sound AI-generated: 'In today's fast-paced landscape, our robust caching layer isn't just a feature — it's a game-changer. Leveraging Redis 7.2, it seamlessly reduces p95 latency from 300 ms to 40 ms across 3 regions. In short, performance matters.'"
- Expect: Keeps every fact unchanged: Redis 7.2, p95, 300 ms, 40 ms, 3 regions
- Expect: Removes the "isn't just … it's" construction and the closing summary line
- Expect: Replaces stock words (landscape, robust, game-changer, leveraging, seamlessly)
- Expect: The result is shorter than the original
- Fail if: Any number, version, or region count changes or disappears
- Fail if: Adds new claims not in the original
