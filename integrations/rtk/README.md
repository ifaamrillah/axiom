# Token-Efficient Command Output (optional)

Output compressors such as [RTK](https://github.com/rtk-ai/rtk) shorten shell command output before the agent reads it. RTK is a binary the user installs; a host hook rewrites commands (`git status` becomes `rtk git status`) and passes the exit code through. Axiom does not install it or depend on it.

## Detect

- A hook is active when command output carries the tool's markers (for example, lines saying how many lines were hidden and how to recover them), or the project or user instructions say so.
- Without a hook, `command -v rtk` shows whether it is installed. Do not prefix commands with it unless the user's setup asks for that.

## Trust condensed output, with three exceptions

Treat condensed output as complete for orientation and progress. Rerun the command uncondensed (`rtk bypass <cmd>`, or the tool's documented equivalent) when:

1. the result is empty but output was clearly expected;
2. the result contradicts the exit code (exit 1 with no visible failure, or exit 0 with errors shown);
3. the result is garbled or cut mid-line.

## Verification evidence

A completion claim needs the decisive line from the real output (for example `FAILED (failures=1)` or `Ran 25 tests … OK`). If compression hid that line, rerun the proving command uncondensed, or save its full output to a file and search it, before you claim anything. A summary written by the compressor is not evidence.

## Limits

- Only shell commands are compressed; file reads and searches through the host's own tools are not.
- Compression is lossy by design; recovery depends on noticing what is missing.
- Reported savings count shell output only and are estimated by the tool itself, not total session cost.

Without a compressor, keep output small by hand: quiet or summary flags (`git status -sb`, `git diff --stat` before the full diff, `pytest -q`), narrow paths, and full logs saved to a file and searched rather than printed.
