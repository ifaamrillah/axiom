# Parallel Execution Policy

Parallelize only when work is independent, dependencies are satisfied, context is sufficient, and write scopes do not conflict.

Before delegation, specify task ID, objective, inputs, deliverables, acceptance criteria, verification, dependencies, and allowed/restricted/shared files.

Prefer one owner for shared files. If tasks overlap, split the scope or execute sequentially. Integrate and verify delegated outputs before marking the parent task complete.

Use host-native subagents only when available and beneficial. Otherwise execute sequentially or provide a handoff for another operator. Never claim unsupported parallelism.
