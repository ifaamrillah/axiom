# Designing Eval Cases

An eval case is a prompt plus observable expectations. It is only useful if a skill-less agent would plausibly fail it and a grader can decide pass or fail from the transcript alone. Case format: `evaluations/cases/README.md` in the Axiom repository.

## Trigger cases

| Kind | How many | Good prompts |
|---|---|---|
| Positive | 2-4 | Terse ("fix the flaky test"), indirect ("why does this pass locally and fail in CI?"), and one with domain jargon |
| Negative | 1-3 | Near-misses that a sibling skill owns, each with its owner named; one unrelated prompt with owner `none` |

Rules:

- Write prompts the way users type, not the way the description reads. A prompt copied from the description proves nothing.
- Prompts that point at code ("this function") need a fixture. In an empty workspace the right answer is a question, not a skill call.
- Run negatives against siblings too. A description fix can steal another skill's prompts.
- Report precision and recall separately. 3/3 positives with 2/3 negatives is a routing problem, not a pass.

## Behavior cases

Each behavior case targets one failure the skill exists to prevent.

| Part | Rule | Example |
|---|---|---|
| Prompt | A real task, not a quiz about the skill | "Make apply_discount(1000, 10) return 900, using TDD." |
| Fixture | Minimal repository where the behavior can happen | `evaluations/fixtures/discount-bug` |
| Expect | Observable actions or output, in order when order matters | "Runs the new test and reports it failing, with the assertion" |
| Fail if | The specific shortcut the baseline took | "Edits `pricing.py` before a failing test was run" |

### Observable vs unobservable

| Unobservable (rewrite it) | Observable |
|---|---|
| "Understands the codebase" | "Cites at least 3 `path:line` references in the answer" |
| "Does a good job on tests" | "Adds a test that fails before the change and passes after" |
| "Follows TDD" | "First edit is to a test file; test run shows a failure before any edit to src/" |
| "Is careful with data" | "Asks before running `migrate:fresh`; does not run it" |
| "Writes good docs" | "Doc has `verified_at_commit` and every command is marked verified or unverified" |

### Discipline cases under pressure

For discipline skills, include at least one pressure case (time, authority, sunk cost combined). See the skill factory's [pressure testing reference](../../skill-factory/references/pressure-testing.md). Without pressure, a case only shows the agent can recite the rule.

### Coverage map

List the skill's critical rules and check each has a case:

```markdown
| Rule in SKILL.md | Case |
|---|---|
| Failing test before code | B1 |
| Do not weaken existing tests | B1 (Fail if) |
| Minimal change | B2 |
| Report evidence | B1 Expect 3 |
| Refactor only on green | none: gap |
```

A rule with no case is untested. A case with no rule is either a missing rule or a case to delete.

## Baselines

- Run each behavior case without the skill (or with the previous version) and record the result. A case the baseline already passes does not measure the skill; harden it or drop it.
- Repeat runs. Agents are stochastic: use at least 3 runs per case before calling a rate (the runner's `--repeat`). Report "4/5", not "pass".
- Keep the host, model, kernel setting, and fixture constant between baseline and skill runs. Otherwise the comparison is invalid.
- Use `--no-kernel` when you need to measure the skill description alone, because the kernel can change routing.

## Arms, validity, and case metadata

These ideas hold for any eval harness; the Axiom runner's flags and case keys are in the case format.

- **Arms.** Run each behavior case in at least two arms: with the skill installed, and without it. A third arm with one short generic instruction ("reproduce first, cite evidence, keep changes small") shows whether the skill beats cheap advice. Compare pass counts per case, side by side; a total can hide a case where the skill made things worse.
- **Uncovered cases.** A case that every arm fails is uncovered: no configuration handles it yet. Either the skill needs a rule for it, or the case asks for something unobservable. Fix one before tuning more.
- **Valid runs only.** A run counts only if it finished. A run stopped by a budget cap, usage limit, or timeout, or one where the harness denied a tool the agent asked for, is invalid, not failed. List invalid runs apart, exclude them from rates, and keep their raw output to see what happened.
- **Safety cases.** Mark a case as safety when its failure signal causes harm (unapproved install, destructive command, data loss). One failing run fails the case; 4 of 5 is not a pass.
- **Held-out cases.** Keep some cases for confirmation only. Do not tune the skill against them or read their transcripts while editing. Report their pass rate apart from the tuning cases; a gain on tuning cases that does not show on held-out cases is overfitting.
- **Seeded defects.** For skills that find problems (debugging, review, audit, performance), plant known defects in a small fixture and list each one. Grade recall (seeded defects found out of planted) and count extra findings that are false. A skill that finds every planted defect while inventing three others is not precise.

## Variant evals: does a section earn its place?

Every line of a skill costs context each time it loads. Test whether a section, reference, or rule changes outcomes before keeping it.

1. **Pick one variable:** one section, one reference, or one rule. Two changes at once cannot be told apart.
2. **Build the variant** in a separate git worktree with only that change (removed, or added). The other side stays the current version.
3. **Use a case that needs it.** If a strong model passes the case without the content, the case cannot show its value. Write a case whose answer depends on what the section says.
4. **Run both sides** with the same host, model, kernel setting, fixture, and grader, at least 10 runs per side. Record the graded pass rate and the median tokens from the run summary.
5. **Decide:**

| Result | Action |
|---|---|
| Pass rate higher with the content, beyond run-to-run spread | Keep it |
| Same pass rate, more tokens | Cut it, or move it to a reference opened only when needed |
| Same pass rate, same tokens | Keep only if it covers a case the evals do not yet test; add that case |
| Lower pass rate with the content | Cut or rewrite it |

Fewer than 10 runs per side is a hint, not a result. Record both sides in `evaluations/results/` with the variant named in the file name.

Offline first: `python3 scripts/run_evals.py --routing` ranks skills for every case prompt by text similarity and fails on near-duplicate descriptions. It costs nothing, so run it after any description change. It is a proxy only; a live trigger run is still the evidence.

## Common design mistakes

| Mistake | Effect | Fix |
|---|---|---|
| Expectations restate the skill text | Grader passes recitation | Expect actions and artifacts |
| One giant case with 8 expectations | One failure hides the rest | Split by failure mode |
| Fixture too big | Slow, noisy runs | Smallest repo that shows the behavior |
| Expectation depends on hidden files | Grader cannot see them | Ask the agent to report the content, or grade a tool call |
| Only happy-path prompts | Misses the shortcut | Add the pressure the baseline gave in to |
| Changing cases after seeing results to make them pass | Measures nothing | Change cases only when they are wrong, and record why |

Sources: adapted from obra/superpowers (MIT) writing-skills testing-skills-with-subagents, and general practice.
