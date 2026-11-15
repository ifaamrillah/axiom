# Runnable Eval Cases

One file per skill, named `<skill>.md`. These cases can be run by [`scripts/run_evals.py`](../../scripts/run_evals.py). The scenario fixtures in `../skills/`, `../workflows/`, `../cross-agent/`, and `../efficiency/` stay as human-review scenarios.

## Format

```markdown
---
skill: <skill-name>
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
- Expect: <observable signal in the transcript or final answer>
- Fail if: <observable failure signal>
```

Rules:

- At least 2 positive trigger prompts, 1 negative prompt with an owner, and 1 behavior case.
- Phrase prompts the way users actually write, including terse and indirect requests.
- Each expectation must be checkable by reading the transcript. Avoid "does a good job".
- The negative owner names the skill that should handle the prompt instead, or `none`.

## Running

```sh
python3 scripts/run_evals.py --check                         # structure only (CI)
python3 scripts/run_evals.py --host claude-code --kind trigger --dry-run
python3 scripts/run_evals.py --host claude-code --kind trigger --skill debugging
python3 scripts/run_evals.py --host claude-code --kind behavior --skill tdd
```

Trigger runs grade themselves by checking whether the host invoked the skill. Behavior runs write transcripts with unchecked expectation boxes. A human (or a separately recorded judge) grades them, and an unchecked box is not a pass. Results go to [`../results/`](../results/README.md).
