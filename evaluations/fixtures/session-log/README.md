# Fixture: session-log

A recorded agent session for evaluating `skill-evaluator` session diagnosis. `session.jsonl` holds one event per line, with a 0-based `event` index, a `role`, and either `text`, a `tool` call with its `input`, or a tool `output`. The project code the session worked on is not included.
