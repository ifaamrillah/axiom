# Eval Results

Recorded runs of [eval cases](../cases/README.md). Each file is evidence of one run: date, host and version, model, filter, and per-case outcomes. Keep results separate from case definitions.

Rules:

- Do not edit a result after the run, except to fill in grading boxes for behavior runs. Record the grader and date when you do.
- Do not commit transcripts that contain secrets or private repository content.
- A result applies only to the recorded host version and model. It does not certify other hosts.
- Failed and errored cases stay in the record. They are the signal for improving skills.
- Invalid runs (stream did not complete, or any permission denial) are listed under "Invalid runs" and excluded from pass rates. They are not failures; fix the harness or the case and rerun.
- Raw host output for invalid runs (and for every run with `--keep-raw`) is kept in `raw/<run>/`, named in the result header. The runner never overwrites a result or raw file. Delete raw output that contains secrets before committing.
- Compare arms within one result file (`--arms`), or across two files only when host version, model, kernel setting, fixture, and grader match. Compare per case, not only the totals.

**Known limit of validity:** Claude Code refuses shell loops that expand a variable (`for f in …; do cat "$f"; done`), and no allowlist entry can permit them. Such runs are INVALID. Bare-host (`none`) runs hit this more often than skill runs, so compare arms only on cases with valid runs on both sides, and say how many runs were invalid.
