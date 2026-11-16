---
skill: skill-factory
---

# Eval cases: skill-factory

## Should trigger

- "Create a skill that makes agents write changelog entries"
- "Turn our deploy checklist into an agent skill"

## Should not trigger

- "Is the tdd skill ready to ship?" → `skill-evaluator`
- "Write the changelog for 2.3.0" → `release-management`

## Behavior

### B1: Test-first skill authoring

- Prompt: "Create a skill that makes agents write a changelog entry for every user-facing change."
- Expect: Writes eval cases (trigger and behavior) or a baseline observation before or alongside the skill
- Expect: The SKILL.md has name and description frontmatter with a "Use when" clause
- Fail if: Writes SKILL.md with no eval cases at all
