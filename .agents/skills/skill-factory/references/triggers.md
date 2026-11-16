# Writing Triggers That Fire

The host decides whether to load a skill from its `name` and `description` alone. The body is invisible until then. A skill that never loads teaches nothing, and a skill that loads on the wrong prompts wastes context and steals work from the right skill.

## Description anatomy

```yaml
description: <What it does, in one sentence with the domain nouns>. Use when <situations, symptoms, and the words users type>.
```

| Part | Purpose | Example |
|---|---|---|
| Capability sentence | Tells the router the domain | "Diagnose failing behavior by reproducing it, isolating the cause, and proving the fix." |
| "Use when" clause | Concrete situations | "Use when a test fails, an error or stack trace appears, or behavior differs from expected." |
| User vocabulary | Words people actually type | "flaky", "regression", "500 error", "it broke after upgrading" |
| Boundary hint (optional) | Steers away from a sibling | "Not for writing new features." |

Axiom's validator requires the trigger clause. Keep the whole description under ~500 characters when possible; hard limit 1024.

## Do not summarize the procedure

If the description lists the workflow steps, an agent may follow the description and skip the body. One reported case: a description that said "review between tasks" produced one review, while the body required two (spec, then quality). Name the domain and the situations; leave the steps to the body.

```yaml
# Bad: the steps are in the description; agents shortcut them
description: Run tests, write a failing test, make it pass, refactor. Use for TDD.

# Good: domain plus situations
description: Drive implementation with a failing test first. Use when adding behavior or fixing a bug where a test can express the expected result, including "test-first" or "TDD" requests.
```

## Vocabulary sources

Collect trigger words before writing:

1. How users phrase the task tersely: "fix this", "why is X slow", "ship it".
2. Indirect phrasings: "can you make sure this is safe before I merge?" (security review).
3. Symptoms and error text: "ENOENT", "timeout", "N+1", "hydration mismatch".
4. Synonyms: test/spec/check; bug/defect/regression; docs/README/runbook.
5. Artifact names: "ADR", "OpenAPI", "migration", "Dockerfile".

Write the eval case prompts from this list, then make sure the description covers each one.

## Avoid collisions

List the sibling skills whose domains are near yours. For each, write one negative eval prompt with that sibling as owner. If two descriptions both match a prompt, sharpen the one that should lose: narrow its nouns or add a boundary hint.

| Collision | Fix |
|---|---|
| `debugging` and `tdd` both match "fix this bug with a test" | Pick the owner; add the other as a step inside the owner's procedure |
| `code-review` and `security-audit` both match "review for vulnerabilities" | Security nouns ("vulnerability", "OWASP", "auth") in `security-audit`; review nouns ("diff", "PR") in `code-review` |
| Alias skills | One canonical skill with the full description; the alias says "compatibility alias" so routing prefers the canonical |

## Bad vs good

| Bad | Problem | Good |
|---|---|---|
| "Helps with tests." | No situations, no vocabulary | "Design and write automated tests... Use when adding coverage, choosing test levels, or fixing flaky tests." |
| "I can review your code." | First person; vague | "Review a diff for correctness, security, and maintainability. Use when asked to review a PR, a diff, or changes before merge." |
| "Use when using setTimeout in tests." | Too narrow; ties a general problem to one API | "Use when tests are flaky, time-dependent, or pass and fail without code changes." |
| A 900-character list of every keyword | Matches everything, routes poorly | 2 sentences; the eval cases prove coverage |

## Iterating on triggers

1. Run the trigger cases (`python3 scripts/run_evals.py --host <host> --kind trigger --skill <name>` in the Axiom repository).
2. Missed positive: add the missing situation or word to the description. Do not add the exact prompt text; generalize it.
3. False positive: narrow the nouns or add a boundary hint; check the owner's description covers the prompt.
4. Rerun the whole trigger set for this skill and its siblings. A fix for one prompt can break another.
5. Record the run. Description changes are measured changes; do not tweak without rerunning.

Sources: adapted from obra/superpowers (MIT) writing-skills discovery reference, and general practice.
