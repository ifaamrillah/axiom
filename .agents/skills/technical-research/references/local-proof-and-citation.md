# Local Proof and Citation

Use this to prove a decisive fact against the installed version, to cite findings, and as a model of a complete research brief. Back to [SKILL.md](../SKILL.md).

## When to prove locally

Prove locally when the fact is decisive for the decision and the test costs minutes:

- A default value or option behavior the docs state vaguely.
- Behavior that changed between versions and you are unsure which side you are on.
- An edge case: empty input, `null`, time zones, Unicode, very large numbers, concurrency.
- The docs and the source seem to disagree.

Do not prove what the docs state clearly and nothing depends on.

## Rules for proof scripts

1. Run against the **project's installed version**, inside the project environment.
2. Keep the script tiny: one question, one printed answer.
3. Put it in a scratch or temp directory, not the source tree. Delete it after, or keep it only if it becomes a real test.
4. Print the version alongside the result.
5. Do not call real external services or production data. Use local values.
6. Record the command and the exact output in the brief.

## Examples

### Node: does `JSON.stringify` drop `undefined` in arrays?

```bash
node -e '
console.log(process.version);
console.log(JSON.stringify({a: undefined, b: [undefined, 1]}));'
```

Output: `v20.11.1` and `{"b":[null,1]}`. Fact: object keys with `undefined` are dropped; array entries become `null`.

### Node package: zod default behavior on unknown keys

```bash
node -e '
const { z } = require("zod");
console.log(require("zod/package.json").version);
console.log(z.object({ a: z.string() }).parse({ a: "x", extra: 1 }));'
```

Output shows the installed version and whether `extra` survives parsing (it is stripped by default in zod 3).

### Python: does `requests` follow redirects on POST?

```bash
.venv/bin/python - <<'PY'
import requests, inspect
print(requests.__version__)
print(inspect.signature(requests.Session.request))
PY
```

Read the `allow_redirects` default from the signature of the installed version rather than recalling it.

### Python: time-zone behavior

```bash
python -c "
from datetime import datetime, timezone
print(datetime(2026,3,29,1,30).astimezone(timezone.utc))"
```

Naive datetimes are treated as local time; the output depends on the machine's zone. This proves the code needs explicit zones.

### Go: does `json.Unmarshal` error on unknown fields?

```bash
mkdir -p /tmp/probe && cd /tmp/probe && cat > main.go <<'GO'
package main
import ("encoding/json"; "fmt"; "runtime")
type T struct{ A string }
func main() {
    var t T
    err := json.Unmarshal([]byte(`{"A":"x","B":1}`), &t)
    fmt.Println(runtime.Version(), t, err)
}
GO
go run main.go
```

Output `go1.22.1 {x} <nil>`: unknown fields are ignored unless you use `Decoder.DisallowUnknownFields`.

### PHP: string-to-number comparison

```bash
php -r 'echo PHP_VERSION, PHP_EOL; var_dump(0 == "a");'
```

PHP 8 prints `bool(false)`; PHP 7 printed `bool(true)`. The runtime version decides.

### SQL: does the database treat empty string as NULL?

```bash
psql "$LOCAL_DB" -c "select version(); select '' is null as empty_is_null;"
```

Postgres returns `f`. (Oracle treats `''` as `NULL`; check the actual engine.)

### As a test in the project

When the fact guards real code, turn the probe into a test so a dependency upgrade that changes it fails loudly:

```python
def test_json_parse_error_returns_json(client):
    res = client.post("/orders", data="{bad", headers={"content-type": "application/json"})
    assert res.status_code == 400
    assert res.headers["content-type"].startswith("application/json")
```

## Citation format

Every finding carries: source, version scope, access date, and the key fact.

| Source kind | Format |
|---|---|
| Docs page | `<Title>, <URL with anchor> (version <x.y>, accessed YYYY-MM-DD)` |
| Source code | `<repo> @ <tag>, <path>:<line-range>` |
| Installed code | `<package> <version> installed, <path>:<line>` |
| Changelog / release notes | `<project> <version> release notes, <URL> (accessed YYYY-MM-DD)` |
| Spec | `RFC 9110 §9.2.2` or `<spec name>, <section>, <URL>` |
| Doc index | `<index> <library ID> (served version <x.y>), <doc or file location>` |
| Local proof | `Local: <command> -> <decisive output line> (<package> <version>)` |
| Community | `Community (corroboration): <URL> (accessed YYYY-MM-DD)` |

Rules: full URLs, not shortened; deep links with anchors when possible; quote only the decisive sentence, briefly; never invent a URL, line number, or version. If nothing authoritative was found, write `UNVERIFIED:` and say what the claim rests on.

In code comments, cite only when the pattern is non-obvious:

```ts
// Next.js 14: revalidatePath must run in a Server Action or Route Handler.
// Source: nextjs.org/docs/14/app/api-reference/functions/revalidatePath
```

## Worked example

**Question.** "Our Express app sometimes returns HTML error pages to API clients. Does `express.json()` in our version return JSON on malformed bodies, and how should we change it?"

**Versions.** `package.json` has `"express": "^4.18.0"`. `jq -r '.packages["node_modules/express"].version' package-lock.json` -> `4.19.2`. `node --version` -> `v20.11.1`. Express 5 docs do not apply.

**Lookups (3).**

1. Express 4.x API reference, `express.json()` section: it uses `body-parser`; malformed JSON calls `next(err)` with a 400 error. It does not say what the response body looks like.
2. Express 4.x error-handling guide: without a custom error handler, the default handler (finalhandler) responds with an HTML page; it includes the stack trace only outside production.
3. Installed source: `rg -n "entity.parse.failed" node_modules/body-parser` -> `node_modules/body-parser/lib/read.js` creates the error with status 400 and `type: 'entity.parse.failed'` when parsing fails.

**Local proof.**

```bash
node -e '
const express = require("express"); const http = require("http");
const app = express(); app.use(express.json()); app.post("/", (q,r)=>r.json({}));
const s = app.listen(0, () => {
  const req = http.request({port: s.address().port, method: "POST",
    headers: {"content-type": "application/json"}}, res => {
    let b=""; res.on("data", c=>b+=c); res.on("end", ()=>{
      console.log(res.statusCode, res.headers["content-type"]); s.close(); });
  });
  req.end("{bad");
});'
```

Output: `400 text/html; charset=utf-8`. Confirmed: malformed JSON returns HTML by default.

**Brief.**

```
Question: Why do API clients get HTML on malformed JSON?
Versions: express 4.19.2 (package-lock.json), body-parser 1.20.2, Node 20.11.1
Findings:
1. express.json() forwards parse errors to next(err) with status 400 and
   type 'entity.parse.failed'.
   - Express 4.x API, expressjs.com/en/4x/api.html#express.json (accessed 2026-11-17)
   - body-parser 1.20.2 installed, node_modules/body-parser/lib/read.js
2. With no custom error middleware, the default handler responds with HTML.
   - Express error handling guide, expressjs.com/en/guide/error-handling.html (accessed 2026-11-17)
3. Local: POST "{bad" -> 400 text/html; charset=utf-8.
Recommendation: add a final error middleware that returns the project's JSON
error shape for err.type === 'entity.parse.failed' (400) and a generic 500
otherwise.
Alternatives: per-route try/catch is not possible (parsing runs before the route);
upgrading Express was not checked and is not needed for this fix.
Limitations: did not check behavior behind the production proxy.
```

Sources: adapted from addyosmani/agent-skills (MIT) `skills/source-driven-development/SKILL.md`, upstash/context7 (MIT) `plugins/agent-plugins/context7/skills/context7-mcp/SKILL.md`, and general practice.
