# Search Recipes by Question Type

Pick the recipe for the question you are answering. Run several searches from different angles in one round, then narrow. Stop after two rounds that add nothing new and report what you have.

Commands use `rg` (ripgrep). Substitute `git grep -n` or `grep -rn` when `rg` is missing. Always exclude vendored and generated trees: `rg -n --glob '!{node_modules,vendor,dist,build,.venv,target,coverage}/**' ...`.

## Naming variants

One spelling is never enough. For a concept like "user id", search:

```sh
rg -n -i 'user_?id|userId|UserId|USER_ID|user-id'
```

Also try plural forms, abbreviations (`usr`, `acct`), and the domain synonym the team uses (check the glossary or README).

## 1. Where is X defined?

| Language | Pattern |
|---|---|
| TypeScript/JS | `rg -n '(function\|class\|interface\|type\|const\|let)\s+X\b'` and `rg -n 'export (default )?(function\|class\|const) X'` |
| Python | `rg -n '^\s*(def\|class\|async def)\s+X\b'` and `rg -n '^X\s*='` |
| Go | `rg -n 'func (\([^)]*\) )?X\('` and `rg -n 'type X (struct\|interface)'` |
| Java/Kotlin | `rg -n '(class\|interface\|enum\|record)\s+X\b'` and `rg -n '\s X\('` |
| PHP | `rg -n '(class\|interface\|trait\|function)\s+X\b'` |
| Ruby | `rg -n '^\s*(def\|class\|module)\s+(self\.)?X\b'` |
| Any | Language server "go to definition" when the host offers it beats text search |

Then confirm: open the hit and check it is the definition in use, not a test double, a shadowing local, or a dead copy. Check for re-exports (`export { X } from`, `__init__.py` imports, barrel `index.ts`).

## 2. Who calls X? (impact, blast radius)

```sh
rg -n '\bX\s*\('                 # direct calls
rg -n '\.X\b'                    # method calls and property access
rg -n "['\"]X['\"]"              # string references: routes, DI keys, reflection, event names
rg -n 'import.*\bX\b|from .* import .*\bX\b|require\(.*X'
```

Text search misses dynamic dispatch. Also check:

- Dependency injection registrations and container config (Spring beans, Laravel service providers, NestJS modules).
- Event or message names (`emit('X'`, `@EventListener`, queue topics).
- Templates and views that call helpers by name.
- Reflection and string-built names (`getattr(obj, name)`, `$this->{$method}()`, `send(:x)`).
- Interface implementations: callers of the interface method reach every implementation.

Report callers as a list with `path:line`, grouped by module, and say which kinds of dynamic dispatch you checked.

## 3. How does data flow from A to B?

Trace one concrete path end to end. Do not summarize the architecture.

1. Find the entry: route, CLI command, job, or event handler that receives A ([entry points](entry-points.md)).
2. Follow each hop: handler, validation, service, repository or client, storage. At each hop note the function and `path:line`.
3. Note transformations: renamed fields, type conversions, defaults filled in, serialization.
4. Find the exit: database write, HTTP response, queue publish, file write.
5. Confirm with a test or log line that exercises the path, if one exists (`rg -n 'X' tests/ spec/ __tests__/`).

Output as a numbered hop list:

```text
1. POST /api/orders → src/routes/orders.ts:14 createOrder()
2. validate body (zod OrderInput) → src/schemas/order.ts:8
3. OrderService.create() → src/services/order.ts:41 (adds status='pending')
4. OrderRepo.insert() → src/repos/order.ts:22 (INSERT orders)
5. publishes 'order.created' → src/events/bus.ts:30
```

## 4. Where does this config value come from?

Values usually pass through layers. Find every layer and the precedence.

```sh
rg -n 'MAX_RETRIES'                                   # code reads and defaults
rg -n 'MAX_RETRIES' -g '*.{env,env.*,yml,yaml,toml,json,ini,properties,conf}'
rg -n 'MAX_RETRIES' -g '{Dockerfile*,docker-compose*,*.tf,*.tfvars}' .github/ helm/ k8s/ deploy/ 2>/dev/null
```

Typical precedence (highest first): command-line flag, process environment, `.env.local`/`.env`, environment-specific file (`application-prod.yml`, `config/production.rb`), base config file, code default. Confirm the real order from the loader code (`dotenv`, `pydantic-settings`, Spring profiles, Laravel `config/*.php` with `env()`, Viper). Never print secret values in your report; name the key and file only.

## 5. Why does it behave this way? (history)

```sh
git log --oneline -n 20 -- path/to/file
git log -S 'X' --oneline          # commits that added or removed the string
git blame -L 40,60 path/to/file
git log --format='%h %ad %s' --date=short --follow -- path/to/file
```

Link the commit or PR that introduced the behavior. Commit messages are evidence of intent, not of current behavior.

## 6. Where are the tests for X?

```sh
rg -l '\bX\b' -g '*{test,spec}*'  # files mentioning X in test-named files
rg -n 'describe\(.X|def test_.*x|func Test.*X|it\(.*X' -i
```

Check co-located tests (`foo.test.ts`), mirrored trees (`tests/unit/...`), and fixtures. If none exist, say so: "no tests reference X".

## 7. Is X still used? (dead code)

Combine the "who calls" recipe with build entry points. Zero text hits plus no dynamic reference plus not exported from a public package means probably dead. Exported from a library: callers may live in other repositories, so mark it "unused in this repo" only.

A negative claim ("no callers", "unused", "not configured anywhere") needs a search record: list the patterns and naming variants searched and the paths covered, for example `rg -n "applyDiscount|apply_discount|'applyDiscount'" src/ tests/ scripts/`. Without the record, report the claim as unverified.

## Red flags

| Red flag | Do instead |
|---|---|
| One grep, first hit, done | Run 3+ searches with name variants; open the hits |
| Reporting a test double as the definition | Check the path is under source, not tests or mocks |
| "No callers" based on text search alone | Check DI, events, reflection, templates, and interfaces first |
| Reading the whole module to answer "where" | Search first, then read the range around the hit |
| Quoting `.env` values | Name the key and file; never copy secret values |

Sources: adapted from yeachan-heo/oh-my-claudecode (MIT) explore and tracer agents, and general practice.
