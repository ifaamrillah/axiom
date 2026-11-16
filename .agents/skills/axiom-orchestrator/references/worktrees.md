# Worktree Isolation

Use a separate working tree when two writers would otherwise share one checkout, or when risky work must not disturb the user's current branch. Isolation removes file collisions. It does not remove logical conflicts: two branches can still disagree at merge time.

## When to isolate

| Situation | Isolate? |
|---|---|
| Parallel writers with disjoint files, host offers native worktrees | Yes. One worktree per writer |
| Parallel writers, no worktree support | Only if write sets are strictly disjoint and no worker runs a formatter or codegen over the whole tree. Otherwise go sequential |
| A long or risky change while the user keeps working on their branch | Yes, with the user's consent |
| Read-only explorers or reviewers | No |
| A small sequential change on a feature branch | No |
| User is on `main`/`master` and asked for implementation | Ask before editing in place. Offer a branch or worktree |

## Procedure

1. **Detect existing isolation first.** You may already be in a linked worktree.

   ```sh
   git rev-parse --git-dir          # differs from the next line inside a linked worktree
   git rev-parse --git-common-dir
   git rev-parse --show-superproject-working-tree   # non-empty means submodule, not worktree
   git branch --show-current        # empty means detached HEAD
   ```

   If already isolated, do not nest another worktree. Report the path and branch.

2. **Prefer the host's native worktree feature.** A manual `git worktree add` behind the host's back creates state the host cannot see or clean up. Host specifics belong in the adapters.

3. **Manual fallback.** Pick a location in this order: the user's declared preference, an existing `.worktrees/` or `worktrees/` directory, then `.worktrees/` by default. A project-local directory must be ignored by Git before use:

   ```sh
   git check-ignore -q .worktrees || echo "NOT IGNORED: add .worktrees/ to .gitignore first"
   git worktree add .worktrees/<task-id> -b axiom/<task-id> <base-commit>
   ```

   Adding a `.gitignore` entry is a repository change: say so in the report. If a sandbox denies `git worktree add`, report it and fall back to sequential work in place.

4. **Set up and baseline each worktree.** Dependencies and build output are per tree.

   | Ecosystem | Setup | Baseline check |
   |---|---|---|
   | Node | `npm ci` / `pnpm install --frozen-lockfile` / `yarn install --immutable` | `npm test` |
   | Python | `uv sync` / `poetry install` / `pip install -r requirements.txt` | `pytest -q` |
   | Go | `go mod download` | `go test ./...` |
   | Rust | `cargo fetch` | `cargo test` |
   | Java | `./mvnw -q -DskipTests install` / `./gradlew assemble` | `./mvnw test` / `./gradlew test` |
   | PHP | `composer install` | `vendor/bin/phpunit` |
   | Ruby | `bundle install` | `bundle exec rspec` |

   Use the project's documented commands when they exist. Record failures as that tree's baseline.

5. **Separate runtime state.** Worktrees share the machine. Give each worker its own port, database name, cache directory, or container name when tests start services.

6. **Integrate in dependency order.** Merge or rebase one worktree at a time into the integration branch, rerun checks after each, and resolve conflicts in the coordinator. Never let two workers resolve the same conflict.

7. **Clean up** only what you created, after the work is integrated or abandoned on purpose:

   ```sh
   git worktree list
   git worktree remove .worktrees/<task-id>
   git branch -d axiom/<task-id>      # -d, not -D: refuses to drop unmerged work
   ```

   Removing a worktree with uncommitted changes or deleting an unmerged branch is destructive. Ask first.

## Red flags

| Red flag | Do instead |
|---|---|
| Creating a worktree inside an existing linked worktree | Detect first; reuse the current one |
| `.worktrees/` not ignored | Ignore it before creating; otherwise its contents can be committed |
| Two worktrees running the same dev server port | Assign ports per worker |
| Running a repo-wide formatter in one worker | It rewrites files other workers own. Format only owned files |
| `git worktree remove --force` to "clean up" | Check for uncommitted work and ask |
| Assuming lockfile changes merge cleanly | Give the lockfile one owner; regenerate after merge |

Sources: adapted from obra/superpowers (MIT) using-git-worktrees, yeachan-heo/oh-my-claudecode (MIT) team worktree mode docs, and general practice.
