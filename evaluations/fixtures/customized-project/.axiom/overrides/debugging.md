# Override: debugging

## Facts
- Tests run with `python3 -m unittest discover -s tests -t .` from the project root.

## Extra steps
- before the final report: run `python3 -m unittest discover -s tests -t . -v` and quote its `Ran N tests` line.

## Stricter rules
- State the root cause on one line that starts with `Root cause:`.
