# XSS, CSRF, CORS, Security Headers, and Browser Trust

Open this file when the target renders content into HTML, sets cookies for browser sessions, answers cross-origin requests, redirects based on input, uses `postMessage`, WebSockets, service workers, or browser storage. Server-side session logic is in the authentication reference.

## Core rule

A browser finding needs a **controllable source**, an **executing or disclosing sink**, and a **victim** other than the attacker (another user's session, another origin, or shared storage). Self-XSS and reading your own data are not findings. Framework escaping, CSP, `SameSite`, and same-origin policy are real controls; check them before assigning impact.

## Cross-site scripting

### Sinks by framework

| Framework | Escapes by default | Escape hatches to hunt |
|---|---|---|
| React / Next.js | JSX text and attributes | `dangerouslySetInnerHTML`, `href={userUrl}` (`javascript:` URLs; React warns but still renders in 18), `ref.current.innerHTML`, `<script>` in `next/head` with interpolation, server-rendered JSON in `<script>` without escaping `</script>` |
| Vue | `{{ }}` | `v-html`, `:href` with user URL, render functions with `innerHTML`, compiling user templates (`Vue.compile`, `template:` from data) |
| Angular | Interpolation and property binding with sanitizer | `bypassSecurityTrustHtml/Url/Script/ResourceUrl`, `[innerHTML]` (sanitized, but check custom sanitizer bypasses), `ElementRef.nativeElement.innerHTML` |
| Svelte | `{}` | `{@html ...}` |
| jQuery | none | `.html()`, `.append(str)`, `$(userString)`, `.attr('href', user)` |
| Vanilla DOM | none | `innerHTML`, `outerHTML`, `insertAdjacentHTML`, `document.write`, `eval`, `setTimeout(str)`, `location = user`, `srcdoc` |
| Django templates | Yes | `\|safe`, `{% autoescape off %}`, `mark_safe()`, `format_html` misuse (passing pre-joined strings) |
| Jinja2 (Flask) | Yes for `.html` templates via `render_template` | `\|safe`, `Markup(user)`, `autoescape false`, templates with non-HTML extensions (autoescape off by default) |
| ERB (Rails) | Yes | `raw()`, `.html_safe`, `<%==`, `content_tag` with `html_safe` input, `link_to user_text, user_url` (URL scheme) |
| Blade (Laravel) | `{{ }}` | `{!! !!}`, `@php echo $x @endphp` |
| Thymeleaf (Spring) | `th:text` | `th:utext`, inline `[(${x})]` |
| JSP | No | `<%= %>`, `${x}` without `fn:escapeXml` / `<c:out>` |
| Go | `html/template` yes; `text/template` no | `template.HTML(user)`, `template.JS`, `template.URL`, writing with `fmt.Fprintf(w, ...)` into HTML |

Also check: Markdown renderers with raw HTML enabled (`marked` without sanitizer, `markdown-it` with `html: true`, `react-markdown` with `rehype-raw`), rich-text editors whose stored HTML is rendered elsewhere, SVG uploads served inline, PDF/HTML email previews, and error pages that echo the request.

### Context matters

Escaping for HTML text does not protect other contexts.

| Context | Example | Required handling |
|---|---|---|
| HTML text | `<p>{x}</p>` | HTML entity encoding |
| Attribute (quoted) | `<a title="{x}">` | Attribute encoding; quotes required |
| URL attribute | `<a href="{x}">` | Scheme allowlist (`http`, `https`, `mailto`); encoding alone does not stop `javascript:` |
| Inline script | `<script>var d = {x}</script>` | JSON encode **and** escape `<`, `>`, `&`, U+2028/2029 (`JSON.stringify` alone allows `</script>`) |
| CSS | `style="{x}"` | Avoid; allowlist values |
| Event handler | `onclick="f('{x}')"` | Avoid entirely |

```jsx
// Vulnerable: javascript: URL in a user profile link
<a href={profile.website}>Website</a>
// Safe
const safe = /^https?:\/\//i.test(profile.website) ? profile.website : undefined;
<a href={safe} rel="noopener noreferrer">Website</a>
```

```html
<!-- Vulnerable: server-rendered state breaks out of the script tag -->
<script>window.__STATE__ = <%- JSON.stringify(state) %></script>
<!-- Safe: serialize-javascript or escape <, >, & -->
<script>window.__STATE__ = <%- serialize(state, { isJSON: true }) %></script>
```

Sanitizers: DOMPurify (client and with jsdom on server), `bleach` (deprecated; prefer `nh3`), `sanitize-html`, Rails `sanitize`, OWASP Java HTML Sanitizer, `bluemonday` (Go), HTML Purifier (PHP). Sanitizing then modifying the string (string replace, re-parsing in a different parser) can reintroduce XSS (mutation XSS).

### DOM XSS

Attacker-controlled inputs: `location.hash`, `location.search`, `document.referrer`, `window.name`, `postMessage` data, `localStorage`, URL fragments that never reach the server. Trace these to the sinks above.

### Prototype pollution (client and Node)

A key like `__proto__` or `constructor.prototype` reaching a recursive merge (`lodash.merge` < 4.17.12, `$.extend(true, ...)`, custom deep-merge, `set(obj, userPath, v)`) changes every object. It is a finding only with a **gadget**: a later read of a polluted property that changes authorization (`if (user.isAdmin)`), template options, or child-process options. Pollution alone is a hardening note.

## CSRF

Cookie-authenticated, state-changing requests need one effective control: a synchronizer token, a double-submit token bound to the session, strict `Origin`/`Referer` validation, or `SameSite=Lax`/`Strict` cookies with no state-changing `GET`.

| Framework | Default protection | How it gets disabled |
|---|---|---|
| Django | `CsrfViewMiddleware` on | `@csrf_exempt`, middleware removed, DRF `SessionAuthentication` enforces CSRF but custom auth classes may not |
| Rails | `protect_from_forgery with: :exception` in `ApplicationController` (default in new apps) | `skip_forgery_protection`, `protect_from_forgery with: :null_session` on cookie-auth controllers |
| Spring Security | CSRF on for session auth | `http.csrf().disable()` / `csrf(c -> c.disable())`; `ignoringRequestMatchers` |
| Laravel | `VerifyCsrfToken` middleware on `web` group | `$except` array, routes in `api` group using session cookies (Sanctum SPA mode needs `EnsureFrontendRequestsAreStateful`) |
| Express | None | Need `csrf-csrf`, `csrf-sync`, or `SameSite` cookies plus Origin checks (`csurf` is deprecated) |
| Go | None | `gorilla/csrf`, Go 1.25 `http.CrossOriginProtection` |
| Next.js | Server Actions compare `Origin` and `Host` | Custom API routes need their own control |

Not CSRF: endpoints authenticated by a bearer token in an `Authorization` header (browsers do not attach it cross-site), read-only `GET` routes, and JSON endpoints that require `Content-Type: application/json` **and** reject simple content types (a cross-site form cannot set that type without a CORS preflight). Check that the server actually rejects `text/plain` bodies parsed as JSON.

Also check: state-changing `GET` routes (`/logout` is low; `/account/delete?confirm=1` is not), method override (`_method=DELETE` in a form POST), login CSRF (logging the victim into the attacker's account, relevant when the account then captures victim data).

## CORS

```js
// Vulnerable: reflects any origin with credentials
res.setHeader('Access-Control-Allow-Origin', req.headers.origin);
res.setHeader('Access-Control-Allow-Credentials', 'true');
// Vulnerable: weak matching
if (origin.endsWith('example.com')) allow(origin);      // evil-example.com
if (/https:\/\/.*\.example\.com/.test(origin)) allow(origin); // unanchored
// Safe
const ALLOWED = new Set(['https://app.example.com']);
if (ALLOWED.has(origin)) { res.setHeader('Access-Control-Allow-Origin', origin); res.setHeader('Vary', 'Origin'); }
```

Notes:
- `Access-Control-Allow-Origin: *` with credentials is rejected by browsers. A bare `*` without credentials is fine for public data.
- `null` origin allowed with credentials is exploitable from sandboxed iframes.
- CORS misconfiguration matters only when responses carry **cookie-authenticated** sensitive data. APIs using bearer tokens from JS are not exposed by CORS alone.
- Framework configs: Express `cors({ origin: true, credentials: true })` reflects everything; Spring `@CrossOrigin(origins = "*", allowCredentials = "true")` is rejected by Spring 5.3+, but `allowedOriginPatterns("*")` with credentials does not; Django `CORS_ALLOW_ALL_ORIGINS = True` with `CORS_ALLOW_CREDENTIALS = True`; Laravel `config/cors.php` `supports_credentials` with `allowed_origins => ['*']` can reflect the request origin (check the CORS package version).

## Open redirect

Parameters named `next`, `return`, `returnTo`, `redirect`, `url`, `continue`, `callback`, `goto`. Fix by allowing only relative paths that start with a single `/` (reject `//evil` and `/\evil`) or an exact host allowlist. An open redirect alone is low; it is higher when chained with OAuth (stealing codes via `redirect_uri` that permits an open-redirect path) or used to bypass an SSRF allowlist.

## Security headers

| Header | Good value | When missing is a finding |
|---|---|---|
| `Content-Security-Policy` | `default-src 'self'; script-src 'self'; object-src 'none'; base-uri 'none'; frame-ancestors 'none'` (or nonce/hash-based `script-src`) | Never alone. It raises the severity of a real XSS when absent and can lower it when strict |
| `Strict-Transport-Security` | `max-age=31536000; includeSubDomains` | Hardening, unless a cookie without `Secure` is sent over HTTP on the same host |
| `X-Frame-Options` / `frame-ancestors` | `DENY` or `'none'` / `'self'` | Clickjacking finding only if a framed page has a one-click sensitive action |
| `X-Content-Type-Options` | `nosniff` | Relevant with user uploads served from the app origin |
| `Referrer-Policy` | `strict-origin-when-cross-origin` | Relevant when URLs carry tokens |
| `Permissions-Policy` | Disable unused features | Hardening |

Missing headers are hardening notes in nearly every case. Report them in the hardening section, not as findings.

## postMessage, WebSockets, and storage

- `window.addEventListener('message', e => ...)` must check `e.origin` against an exact allowlist before acting. `indexOf`, `startsWith`, `includes`, and unanchored regex checks are bypassable. Senders must not use `postMessage(secret, '*')`.
- WebSocket upgrades authenticated by cookies must check `Origin` (cross-site WebSocket hijacking).
- Tokens in `localStorage` are readable by any XSS. That is a design trade-off, not a finding by itself; it raises XSS impact.
- Service workers that cache personalized responses must clear caches on logout and key by user.

## Search commands

```bash
rg -n -e 'dangerouslySetInnerHTML|v-html|\{@html|bypassSecurityTrust|innerHTML\s*=|outerHTML|insertAdjacentHTML|document\.write|\.html\(' 
rg -n -e '\|\s*safe\b|mark_safe|Markup\(|\.html_safe|raw\(|<%==|\{!!|th:utext|template\.HTML\('
rg -n -e 'csrf_exempt|skip_forgery_protection|null_session|csrf\(\)\.disable|csrf\(c\s*->\s*c\.disable|VerifyCsrfToken|\$except'
rg -n -e 'Access-Control-Allow-Origin|cors\(|CORS_ALLOW|allowedOriginPatterns|supports_credentials|@CrossOrigin'
rg -n -e "addEventListener\(\s*['\"]message" -e 'postMessage\('
rg -n -e 'redirect\(\s*req\.(query|body)|res\.redirect\(\s*req|redirect_to\s+params|HttpResponseRedirect\(request\.(GET|POST)|return redirect\(\$request' 
```

## Validate without harm

- Render the template or component in a unit test (React Testing Library, Django test client, Rails view spec) with a marker payload such as `<img src=x onerror=window.__xss=1>` and assert on the output HTML or the flag in a local headless browser. Do not use payloads that exfiltrate.
- Stored XSS: two dummy users in a local instance. User A stores the marker; load the page as user B and observe execution.
- CSRF: a local HTML file on a second local origin that auto-submits a form to the local app with a dummy session. Observe the state change in the dummy account.
- CORS: send a request with a crafted `Origin` header to a local instance and read the response headers.

## False-positive traps

| Looks bad | Check before reporting |
|---|---|
| `dangerouslySetInnerHTML` | Input may be sanitized (DOMPurify) or come from a trusted CMS editor role. Who writes it? |
| `v-html` on admin-only content | If only admins write and admins are trusted with HTML by design, it is not a boundary crossing |
| Reflected input in an error page | Check the response content type. JSON responses with `application/json` do not execute |
| No CSRF token on an API | Bearer-token auth is not CSRF-able |
| Missing CSP | Hardening note, not a finding |
| `Access-Control-Allow-Origin: *` | Without credentials and on public data, intended |

## Severity guidance

| Result | Typical severity |
|---|---|
| Stored XSS that runs for other users including admins, with session-cookie or token access | High (Critical if it reaches admin takeover with no interaction on a high-value system) |
| Reflected or DOM XSS needing a victim click; CSRF on a sensitive action (email change, payout settings) | Medium to High |
| CORS reflection exposing cookie-authenticated sensitive data | High |
| Clickjacking on a one-click sensitive action; open redirect chained into OAuth token theft | Medium |
| Open redirect alone; CSRF on low-impact actions; missing headers | Low or hardening note |

Sources: adapted from cloudflare/security-audit-skill (MIT), addyosmani/agent-skills (MIT) and general practice.
