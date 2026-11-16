# Injection: SQL, NoSQL, Command, Template, and Interpreter Sinks

Open this file when untrusted data can reach a query language, a shell, a template engine, an expression evaluator, LDAP or XPath, a log line, or a response header. Each item below is a question to trace in source. A finding still needs the six elements from `SKILL.md`.

## Core rule

Injection exists when attacker-controlled bytes change the **structure** of an interpreted string (query, command, template, expression), not only its data. Find the point where code builds the string. Ask whether the input stays a bound value or becomes syntax.

Trace three kinds of path:

1. **Direct:** request field to sink in the same handler.
2. **Second-order:** data stored safely, then read back by different code and concatenated into a sink (a saved report filter, a username used in a later admin query, a filename used in a cron job).
3. **Structural input:** field **names**, sort keys, JSON keys, header names, and identifiers. Parameter binding protects values, never identifiers.

## Where to look

### SQL sinks by stack

| Stack | Unsafe sink (when built from input) | Safe form |
|---|---|---|
| Node (`pg`, `mysql2`) | `db.query("... " + x)`, template literal `` `... ${x}` `` | `db.query('... $1', [x])`, `?` placeholders |
| Node (Sequelize) | `sequelize.query(str)`, `Sequelize.literal(x)`, `where: sequelize.literal(...)` | `replacements` / `bind` options, model finders |
| Node (Prisma) | `$queryRawUnsafe(str)`, `$executeRawUnsafe(str)` | `` $queryRaw`... ${x}` `` (tagged template binds `x`) |
| Node (Knex) | `knex.raw("..." + x)`, `whereRaw("..." + x)` | `knex.raw('?? = ?', [col, val])` with `??` only for allowlisted identifiers |
| Node (TypeORM) | `query(str)`, `.where("x = " + v)` | `.where('x = :v', { v })` |
| Python (DB-API) | `cursor.execute("..." % x)`, `f"..."`, `.format()` | `cursor.execute("... %s", (x,))` |
| Django | `.raw(f"...")`, `.extra(where=[...])`, `RawSQL(str)`, `cursor.execute(str)` | ORM filters, `.raw(sql, params)` |
| SQLAlchemy | `text(f"...")`, `engine.execute(str)`, `order_by(text(x))` | `text("... :v").bindparams(v=x)`, column objects |
| Rails | `where("name = '#{x}'")`, `order(params[:sort])` (older Rails), `find_by_sql(str)`, `Arel.sql(x)`, `exists?(str)`, `group(str)`, `joins(str)` | `where(name: x)`, `where("name = ?", x)`, `sanitize_sql_*` |
| Spring / JPA | `createQuery("..." + x)`, `createNativeQuery(str)`, `JdbcTemplate.query("..." + x)`, `Statement.execute` | `PreparedStatement`, `:named` params, Criteria API |
| MyBatis | `${x}` in XML mappers | `#{x}` |
| Laravel | `DB::raw($x)`, `whereRaw($x)`, `orderByRaw($x)`, `selectRaw($x)`, `DB::select("..." . $x)` | Query builder, `whereRaw('a = ?', [$x])` |
| PHP (PDO / mysqli) | `$pdo->query("..." . $x)`, `mysqli_query($c, "..." . $x)` | `prepare` + `execute([$x])` |
| Go | `db.Query("..." + x)`, `fmt.Sprintf` into `db.Exec` | `db.Query("... $1", x)` / `?` |
| Go (GORM) | `db.Where(fmt.Sprintf(...))`, `db.Raw(str)`, `Order(userInput)` | `db.Where("name = ?", x)` |

### Identifier and clause injection (missed most often)

Binding does not cover table names, column names, `ORDER BY`, `LIMIT`, `ASC/DESC`, or JSON paths. Look for `sort`, `order`, `orderBy`, `dir`, `column`, `field`, `groupBy`, `filter[...]` parameters.

```ruby
# Vulnerable before Rails 6.1, or anywhere the value is wrapped in Arel.sql()
User.order(params[:sort])
# Safe: allowlist
SORTABLE = %w[name created_at].freeze
User.order(SORTABLE.include?(params[:sort]) ? params[:sort] : "created_at")
```

```go
// Vulnerable
db.Query(fmt.Sprintf("SELECT * FROM items ORDER BY %s", r.URL.Query().Get("sort")))
// Safe
cols := map[string]string{"name": "name", "date": "created_at"}
col, ok := cols[r.URL.Query().Get("sort")]
if !ok { col = "created_at" }
db.Query("SELECT * FROM items ORDER BY " + col)
```

### NoSQL and query-object injection

Untrusted JSON can turn a scalar comparison into an operator object.

```js
// Vulnerable: body {"username":"admin","password":{"$ne":null}} matches any password
const user = await Users.findOne({ username: req.body.username, password: req.body.password });

// Safe: force types before the query
const username = String(req.body.username);
const password = String(req.body.password);
const user = await Users.findOne({ username });
if (!user || !(await bcrypt.compare(password, user.passwordHash))) return deny();
```

Also check: `$where` and `$function` (server-side JS), `$regex` from input (ReDoS and match-all), `mapReduce`, aggregation `$lookup` stages built from input, Elasticsearch `query_string` and scripts, Redis `EVAL` with concatenated Lua, and GraphQL filters passed straight to the ORM. Mitigations to recognize: `mongo-sanitize`, `express-mongo-sanitize`, Mongoose `sanitizeFilter: true`, schema validation that rejects objects.

### OS command injection

| Stack | Unsafe | Safer |
|---|---|---|
| Node | `exec(str)`, `execSync(str)`, `spawn(cmd, { shell: true })` | `execFile(bin, [args])`, `spawn(bin, [args])` without `shell` |
| Python | `os.system`, `os.popen`, `subprocess.*(str, shell=True)`, `commands` | `subprocess.run([bin, arg], shell=False)` |
| Ruby | backticks, `%x()`, `system(str)`, `exec(str)`, `Open3.*(str)`, `Kernel#open("\|cmd")` | `system(bin, arg)` (array form) |
| Java | `Runtime.exec(String)` (tokenized, but `sh -c` wrappers are not), `ProcessBuilder("sh","-c",x)` | `ProcessBuilder(bin, arg)` |
| PHP | `exec`, `system`, `shell_exec`, `passthru`, `popen`, `proc_open`, backticks | `escapeshellarg` per argument, or avoid the shell |
| Go | `exec.Command("sh", "-c", x)` | `exec.Command(bin, arg)` |

Argument arrays stop shell metacharacters but not **argument injection**: a value starting with `-` becomes an option (`git` `--upload-pack=...`, `tar` `--checkpoint-action`, `curl -o`, `ssh -oProxyCommand`, `find -exec`). Check for a `--` separator before positional user values, or a leading-dash rejection.

```python
# Vulnerable: filename "-oProxyCommand=..." or "; rm" style input
subprocess.run(f"convert {name} out.png", shell=True)
# Safe
if name.startswith("-"): raise ValueError("bad name")
subprocess.run(["convert", "--", name, "out.png"], check=True)
```

### Server-side template injection (SSTI)

The bug is user input used **as the template source**, not as a template variable.

| Engine | Unsafe | Safe |
|---|---|---|
| Jinja2 / Flask | `render_template_string(user_text)`, `Template(user_text).render()`, `Environment(...).from_string(x)` | `render_template("x.html", name=user_text)`; `SandboxedEnvironment` for user templates |
| Django templates | `Template(user_text).render(ctx)` | Fixed templates; Django's language is limited but still leaks context objects |
| ERB / Rails | `ERB.new(user_text).result`, `render inline: params[:x]` | `render template:` with a fixed name |
| Twig / Blade | `$twig->createTemplate($x)`, `Blade::render($x)` | Fixed templates; sandbox extension |
| Freemarker / Velocity / Thymeleaf (Spring) | user-controlled template text; Thymeleaf view names built from input (`return "user/" + lang`) with `__${...}__` preprocessing | Fixed view names; allowlist |
| Handlebars / EJS / Pug (Node) | compiling user text; EJS `render(str, data)` where `data` carries user-controlled `settings` / options | Precompiled templates; never pass request objects as options |
| Go `text/template` | user text as template; `text/template` for HTML output | `html/template`, fixed templates |

### Code evaluation and expression languages

- JS: `eval`, `new Function`, `setTimeout(string)`, `vm.runInNewContext` (not a sandbox), `vm2` (deprecated, escapable).
- Python: `eval`, `exec`, `compile`, `pickle` (see the files and deserialization reference), `yaml.load` without `SafeLoader`.
- Ruby: `eval`, `instance_eval`, `send(params[:m])`, `public_send`, `constantize` on input.
- Java: SpEL `parser.parseExpression(x)` with `StandardEvaluationContext`, OGNL, MVEL, JEXL, `ScriptEngine.eval`.
- PHP: `eval`, `assert($str)` in old PHP, `preg_replace` with `/e`, `create_function`, `call_user_func($input)`, variable functions `$f()`.

### Other interpreters

- **LDAP:** filter built with `(uid=` + input + `)`. Safe: escape per RFC 4515 (`ldap.filter.escape_filter_chars`, Spring `LdapEncoder.filterEncode`).
- **XPath:** concatenated expressions. Safe: parameterized XPath variables.
- **Header / CRLF:** user data in `Location`, `Set-Cookie`, or custom headers. Most modern frameworks reject `\r\n` in header values; verify the version before reporting.
- **Log injection:** newline injection forging log lines matters only if a log consumer makes a security decision or renders logs as HTML (log viewer XSS).
- **CSV / formula injection:** cells starting with `=`, `+`, `-`, `@` in exports opened by staff. Usually a hardening note unless the product promises safe export to privileged users.
- **Email header injection:** user input in `To`, `Subject`, or raw SMTP headers.

## Search commands

```bash
# SQL built from strings
rg -n --hidden -g '!node_modules' -e 'query(Unsafe|Raw)?\s*\(\s*[`"'\''].*(\$\{|\+|%s|\.format|f")' -e 'execute\(\s*f"' -e '\.raw\(|whereRaw|orderByRaw|DB::raw|Sequelize\.literal|\$queryRawUnsafe'
rg -n -e 'createQuery\(.*\+' -e 'createNativeQuery' -e '\$\{' --glob '*Mapper.xml'
rg -n -e '\.order\(params' -e 'find_by_sql' -e 'where\(".*#\{'
# Commands
rg -n -e 'child_process' -e 'exec(Sync)?\(' -e 'shell\s*[:=]\s*true' -e 'shell=True' -e 'os\.system' -e 'Runtime\.getRuntime\(\)\.exec' -e 'shell_exec|passthru|proc_open' -e '"sh",\s*"-c"'
# Templates and eval
rg -n -e 'render_template_string' -e 'from_string\(' -e 'ERB\.new' -e 'render\s+inline:' -e 'createTemplate\(' -e 'parseExpression\(' -e '\beval\(' -e 'new Function\('
# NoSQL operators
rg -n -e '\$where' -e 'findOne\(\s*req\.(body|query)' -e 'find\(\s*req\.(body|query)'
```

A hit is a lead. Trace it backward to a lower-trust source before writing anything.

## Validate without harm

- Prefer a **unit-level harness**: call the query builder or repository function with a marker input and assert on the generated SQL string or the ORM's `toSQL()` / `to_sql` / `.query` output. No database needed.
- For SQL, a local SQLite or test container with dummy rows is enough. Use a boolean-difference input (`' OR '1'='1` against a dummy table) or a syntax-error marker. Never use `DROP`, `DELETE`, time-based payloads against shared databases, or stacked queries that write.
- For commands, inject a harmless marker that writes a file under the scratch directory (`; touch "$SCRATCH/marker"` in a sandbox) or echoes a unique string. Never `curl` out or open shells.
- For SSTI, render an arithmetic marker such as `{{7*191}}` and check for `1337`. Stop there. Do not walk object graphs to reach `os` or `Runtime`.
- For NoSQL, show the operator object passes validation and changes the match set on dummy documents.

## False-positive traps

| Looks bad | Check before reporting |
|---|---|
| Template literal inside `` sql`...` `` or Prisma `$queryRaw` tagged template | Tagged templates bind interpolations. Safe unless wrapped in `Prisma.raw` / `sql.raw` |
| String concatenation of a constant or enum | Trace the value. Hardcoded or server-derived identifiers are not injection |
| `exec` with a fixed command | No user input reaches it. Not a finding |
| `Runtime.exec(String)` with input | Java tokenizes on whitespace without a shell. Metacharacters do nothing unless the command is `sh -c` or the input injects arguments |
| Django `.extra()` / `RawSQL` with `params=` | Values bound. Check only the SQL string itself |
| Input validated as an integer upstream | Confirm the cast happens before the sink on **every** path, including batch and import |
| Jinja2 `render_template` with user data in context | Data is escaped variables, not template source |
| Rails `order(params[:x])` / `pluck(params[:x])` on Rails 6.1+ | Rails rejects non-attribute raw SQL there unless wrapped in `Arel.sql`. Check the Rails version and for `Arel.sql` wrappers |
| Admin-only endpoint | Still injection, but the principal is an admin. Severity drops if admins already have equal power (for example, they can run SQL by design) |

## Severity guidance

| Result | Typical severity |
|---|---|
| Unauthenticated SQL injection reading or writing the main store; unauthenticated command or template RCE | Critical |
| Authenticated SQLi crossing tenants or reading credentials; authenticated RCE | High |
| SQLi limited to the caller's own tenant data with no secrets, or blind SQLi needing many requests on a narrow table | Medium |
| Injection into a log, CSV export, or error message with no downstream decision | Low or hardening note |

Fix pattern: bind values, allowlist identifiers, use argument arrays plus `--`, never compile user text as a template, and add a regression test with the exact marker input.

Sources: adapted from cloudflare/security-audit-skill (MIT), addyosmani/agent-skills (MIT) and general practice.
