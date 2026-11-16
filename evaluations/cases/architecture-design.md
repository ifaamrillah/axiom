---
skill: architecture-design
fixture: evaluations/fixtures/discount-bug
---

# Eval cases: architecture-design

## Should trigger

- "Should we put a Redis cache in front of apply_discount, or is that overkill? Weigh the options."
- "Design how discounts, coupons, and loyalty points should fit together before we build them"
- "Pick an approach for storing discount rules: config file, database table, or code"

## Should not trigger

- "apply_discount returns 0 for 10%, fix it" → `debugging`
- "Review my PR" → `code-review`

## Behavior

### B1: Evidence before adding infrastructure

- Prompt: "Should we add a Redis cache in front of apply_discount? Recommend an approach."
- Fixture: `evaluations/fixtures/discount-bug`
- Expect: Compares at least two options, including not adding a cache, with trade-offs
- Expect: Notes that there is no measurement showing apply_discount is slow, or asks for one
- Expect: Recommends against adding Redis without evidence of a performance problem
- Fail if: Writes code or adds a dependency
