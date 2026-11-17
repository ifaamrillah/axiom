---
skill: skill-factory
---

# Eval cases: skill-factory

## Should trigger

- "Create a skill that makes agents write changelog entries"
- "Turn our deploy checklist into an agent skill"
- "Agents ignore the wording in our review skill; rewrite it so they follow it"

## Should not trigger

- "Is the tdd skill ready to ship?" → `skill-evaluator`
- "Write the changelog for 2.3.0" → `release-management`

## Behavior

### B1: Test-first skill authoring

- Prompt: "Create a skill that makes agents write a changelog entry for every user-facing change."
- Expect: Writes eval cases (trigger and behavior) or a baseline observation before or alongside the skill
- Expect: The SKILL.md has name and description frontmatter with a "Use when" clause
- Fail if: Writes SKILL.md with no eval cases at all

### B2: Composition prohibition becomes a recipe

- Prompt: "Our code-review skill has the line 'Don't be verbose or over-explain findings.' Reviews still ramble. Fix the skill wording."
- Expect: Replaces the line with a positive recipe (for example "one line per finding: location, problem, fix") instead of a stronger prohibition
- Expect: Edits the failing line rather than appending a new paragraph next to it
- Expect: The new recipe has no "unless" or "except when" clause
- Fail if: Keeps the "don't be verbose" line and adds more prohibitions ("Never write long reviews")
