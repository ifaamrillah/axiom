# Runnable Eval Cases

One file per skill, named `<skill>.md`. These cases can be run by [`scripts/run_evals.py`](../../scripts/run_evals.py). The scenario fixtures in `../skills/`, `../workflows/`, `../cross-agent/`, and `../efficiency/` stay as human-review scenarios.

## Format

```markdown
---
skill: <skill-name>
fixture: evaluations/fixtures/<name>   # optional; trigger runs start from this project
accept: <other-skill>                  # optional; comma-separated aliases that also count as a hit
---

# Eval cases: <skill-name>

## Should trigger

- "<prompt where the skill must be invoked>"

## Should not trigger

- "<prompt where it must not be invoked>" → `<owner-skill or none>`

## Behavior

### B1: <short title>

- Prompt: "<task prompt>"
- Fixture: `evaluations/fixtures/<name>` (optional)
- Safety: yes                      (optional; any failing run fails the case)
- Split: held-out                  (optional; confirmation only, see below)
- Seeded: <one planted defect>     (optional, repeatable; needs a Fixture)
- Expect: <observable signal in the transcript or final answer>
- Fail if: <observable failure signal>
```

Rules:

- At least 2 positive trigger prompts, 1 negative prompt with an owner, and 1 behavior case.
- Phrase prompts the way users actually write, including terse and indirect requests.
- Each expectation must be checkable by reading the transcript. Avoid "does a good job".
- Prompts that refer to code ("this bug", "this function") need a `fixture:`; in an empty workspace the correct response is a clarifying question, not a skill call.
- Workspaces receive the kernel block in `CLAUDE.md` and `AGENTS.md`, as a documented install does. Pass `--no-kernel` to measure skill descriptions alone.
- The negative owner names the skill that should handle the prompt instead, or `none`.
- Include at least one prompt that names the skill explicitly, one that pushes to skip the process ("just fix it"), and negatives that a sibling skill owns (near neighbours). Explicit names score low on `--routing`, which only compares words; the live trigger run is the evidence.

## Behavior case metadata

`--check` validates these keys.

- **`Safety: yes`** marks a case whose failure signal is harmful (unapproved install, destructive command, data loss). The case fails if any graded run fails; a pass rate such as 4/5 is still FAIL.
- **`Split: held-out`** marks a confirmation case. Do not change skills to make a held-out case pass, and do not read its transcripts while tuning. Its pass rate is reported apart from the tuning cases, so it shows whether a skill change generalizes. Cases without `Split` are tuning cases.
- **`Seeded: <defect>`** names one defect planted in the fixture. The grader judges each seeded defect as found or not found and counts extra findings it judges false. The report records recall (found/seeded) and the false-finding count next to the pass rate; they do not change pass or fail. Write one line per defect, specific enough that a grader can match it ("`create_note` builds SQL by string formatting", not "SQL injection").

Seeded cases suit any skill that finds problems: debugging, code review, security audit, performance. For a review or audit case, plant two to four defects in a tiny fixture, list each as `Seeded:`, and add one deliberately safe pattern that looks suspicious. Reporting the safe pattern is a false finding. Ask for findings only ("do not change files"), so the transcript shows what the agent believed, not what it happened to fix.

## Comparison arms and run validity

Behavior runs take `--arm` or `--arms`:

| Arm | Workspace |
|---|---|
| `skill` (default) | Fixture plus the Axiom skills in the host paths and the kernel in `CLAUDE.md` and `AGENTS.md` (`--no-kernel` drops the kernel) |
| `none` | Fixture only: no skills, no project instructions |
| `oneliner` | Fixture plus one generic instruction line (`ONELINER` in the runner) and no skills |

`--arms skill,none,oneliner` runs every case once per arm (times `--repeat`) and reports, per case, the pass count of each arm and the delta against the first arm. A case that every arm fails is marked UNCOVERED: the skill does not cover it yet, or the case is wrong. A skill earns its context cost only where it beats `none` and `oneliner`.

A run counts only when it is valid:

- The host stream must complete. A budget cap, usage limit, timeout, or crash makes the run invalid.
- A run with any permission denial is invalid, not failed: the harness decided the outcome, not the agent. Widen the allowed tools or change the case, then rerun.

Invalid runs are listed separately in the result and excluded from every pass rate. Their raw host output is saved under `evaluations/results/raw/`; `--keep-raw` saves the output of valid runs too.

## Running

```sh
python3 scripts/run_evals.py --check                         # structure and description collisions (CI)
python3 scripts/run_evals.py --routing                       # offline routing proxy; no host, no quota
python3 scripts/run_evals.py --host claude-code --kind trigger --dry-run
python3 scripts/run_evals.py --host claude-code --kind trigger --skill debugging
python3 scripts/run_evals.py --host claude-code --kind behavior --skill tdd
python3 scripts/run_evals.py --host claude-code --kind behavior --skill tdd --arms skill,none,oneliner --repeat 3 --grade
```

Trigger runs grade themselves by checking whether the host invoked the skill. Behavior runs write transcripts with unchecked expectation boxes. `--grade` asks a separate tool-less session to grade each valid run; without it, a human grades them, and an unchecked box is not a pass. Results go to [`../results/`](../results/README.md).
