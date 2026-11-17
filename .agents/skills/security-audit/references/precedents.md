# Precedents: What Is Normally Not Reported

Open this file before reporting a candidate, and in every candidate verifier pass. Each precedent names a class of claim that is usually noise, why, and the condition that makes it reportable again.

## How to apply a precedent

- Precedents reduce noise. They never override a concrete exploit with evidence. A traced path from a lower-trust principal to a real result is reported, whatever the precedent says.
- Check the "becomes reportable when" condition in source before you apply a precedent. If source settles the condition, decide: report the finding, or reject it.
- If the condition depends on a fact outside source (deployed config, how a file ships, who sets a variable), the candidate is `needs_validation`. Name that fact. When in doubt, use `needs_validation`.
- Never drop a candidate silently. A candidate excluded by a precedent becomes a `rejected` record (full audit) or a "rejected concern" line (guidance mode). Cite the precedent and the condition you checked.
- A precedent can lower a finding to a hardening note. A hardening note has no severity.

## General precedents

| Claim | Why it is normally not reported | Becomes reportable when |
|---|---|---|
| Injection through environment variables or command-line arguments | The operator who sets them already controls the process. No trust boundary is crossed | A lower-trust party sets the value: a web handler passes request data into a child process's environment or arguments, CI reads PR titles, branch names, or commit messages (`github.event.*`), tenants configure env on a shared platform, or the program is setuid or runs as a privileged service |
| Guessing a UUIDv4 or another identifier with at least 122 bits of randomness | Guessing it is not a practical attack path | IDs are sequential, time-based (UUIDv1, ULID prefixes, timestamps), or made with a weak generator (`Math.random`, `rand()`), or they leak through URLs, emails, logs, list endpoints, or referrers. A missing ownership check is still a finding; the ID type only changes likelihood (see [authorization and tenancy](authz-and-tenancy.md)) |
| XSS where the framework escapes output (React and Vue text, Angular interpolation, Jinja2 with autoescape, Django templates, ERB, Blade `{{ }}`) | Auto-escaping encodes the value for its HTML context | Input reaches a raw sink: `dangerouslySetInnerHTML`, `v-html`, `\|safe`, `Markup()`, `mark_safe`, `{% autoescape off %}`, `raw()`, `.html_safe`, Blade `{!! !!}`, `bypassSecurityTrust*`, direct `innerHTML`, a user-controlled URL in `href` or `src` (`javascript:`), or a template with autoescape off (Flask non-`.html` templates). See the framework table in [browser and web](browser-and-web.md) |
| Authorization check missing in client-side code only (hidden button, route guard, disabled field) | The server is the control. The client is attacker-controlled anyway | The server endpoint behind it also lacks the check. Report the server-side gap, at file:line of the server handler, not the client code |
| Issue found only in tests, fixtures, docs, examples, or sample code | No lower-trust principal reaches it in production | The file ships or loads in production (imported by app code, registered as a route, copied into the build or image, used as a scaffolding template for user projects), or it holds a secret that is valid for a real system (then report the secret) |
| Generic denial of service: no rate limit, large input, slow endpoint, resource exhaustion | Volume attacks are an operations concern, and source rarely shows the edge controls | A cheap, concrete amplification exists: one small request causes large work or a crash of a shared process. Examples: catastrophic regex on unauthenticated input, decompression or XML entity expansion, unbounded GraphQL depth or batch size, a fan-out loop sized by user input. No visible limit is needed in front of it. An unauthenticated remote stop of a shared service is High (see the anchors in `SKILL.md`) |
| Outdated dependency or a CVE in the lockfile | Dependency scanners own this. A version number alone does not show a vulnerable path | The application calls the vulnerable function with input a lower-trust principal controls. Trace that path and validate it as in [supply chain](supply-chain.md) |
| Memory-safety classes (buffer overflow, use-after-free, out-of-bounds read) in memory-safe code | The language runtime prevents them | The code is C or C++, `unsafe` Rust, Go with `unsafe` or cgo, or crosses FFI (ctypes, cffi, JNI, N-API, native extensions), or it parses input with a native library the app wraps |
| SSRF in static HTML or client-side `fetch` | The visitor's browser makes the request, not the server. No server-side position is gained | A server-side renderer loads the content: a headless browser, a PDF or image generator, a link unfurler, or server-side rendering that fetches URLs from the content. See [SSRF](ssrf.md) |
| Log spoofing or log injection (forged lines via CR/LF) | Forged log lines alone change no security decision | The log is rendered as HTML (log-viewer XSS), parsed to drive a security action (blocklists, alerting, audit evidence used for disputes), or processed by a logger that evaluates content (message lookups in old Log4j 2 releases) |
| Missing hardening headers alone (CSP, HSTS, X-Frame-Options, X-Content-Type-Options, Referrer-Policy) | Absence is a defense-in-depth gap, not a crossed boundary | The absence enables a concrete attack you can trace: a one-click sensitive state change that can be framed (clickjacking), a secret in a URL sent to third parties through `Referer`, or user uploads served inline with sniffable content types. A missing CSP next to a confirmed XSS changes that finding's severity; it is not a separate finding |

The common false-positive patterns in [hunting and validation](hunting-and-validation.md) (self-impact, admin powers by design, theoretical chains) also apply. They are not repeated here.

## Exclusions by language and file type

Apply these rules to a file before you hunt in it. Each rule ends with its exception.

- **Python, JavaScript, TypeScript, Java, Kotlin, C#, Go, Ruby, PHP, safe Rust:** skip memory-safety classes. Exception: `unsafe` blocks, cgo, FFI calls, and native extensions.
- **C, C++, unsafe Rust:** memory-safety classes apply in full. Prefer existing sanitizer or fuzz harnesses (see [attack-surface checklists](attack-surfaces.md)).
- **`*.test.*`, `*_test.go`, `*_spec.rb`, `test_*.py`, `tests/`, `__tests__/`, `spec/`, `fixtures/`, `testdata/`:** skip dangerous-API and weak-crypto findings. Exception: the file is imported by production code, or it holds a secret valid for a real system.
- **`docs/`, `examples/`, `samples/`, `*.md`, `*.ipynb`:** skip. Exception: the content is served by the application, installed into user projects, or contains a real secret.
- **Static `*.html`, `*.css`, client-only bundles:** skip SSRF and server-side injection. Exception: a server-side renderer processes the file. XSS still applies when the page puts URL or user data into a raw sink.
- **React JSX and TSX, Vue templates, Angular templates:** skip XSS for text interpolation. Exception: the raw sinks listed above, and user URLs in `href` or `src`.
- **Jinja2, Django, ERB, Blade templates:** skip XSS for escaped output. Exception: the raw filters and directives listed above. Server-side template injection is a separate class (see [injection](injection.md)).
- **Shell scripts, Makefiles, and operator CLIs:** treat arguments and environment as trusted. Exception: a lower-trust party supplies them (CI event data, a web handler, a multi-tenant job runner).
- **CI workflow files:** trusted inputs are secrets and repository variables. `github.event.*` text fields (titles, bodies, branch names, commit messages) are attacker-controlled on public repositories (see [supply chain](supply-chain.md)).
- **Lockfiles and manifests:** do not report version numbers as findings. Report only a traced, reachable vulnerable call.
- **Agent configuration (hooks, MCP configs, allowlists, instruction files):** see [agent configuration](agent-config.md). Text in an instruction file is not a control and is not a finding by itself.

Sources: idea from anthropics/claude-code-security-review (precedents and exclusions; MIT), rewritten; general practice.
