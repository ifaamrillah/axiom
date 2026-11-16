# Server-Side Request Forgery (SSRF)

Open this file when the server makes an outbound request whose URL, host, port, path, or redirect target a lower-trust principal can influence: webhooks, "import from URL", link previews and unfurling, image or PDF renderers, avatar fetchers, OAuth/OIDC discovery URLs, XML/SVG processors that fetch entities, proxies, and integrations where tenants configure endpoints.

## Core rule

SSRF lets an outside principal use the server's network position. The impact depends on what the server can reach: cloud metadata credentials, internal admin APIs, databases with no auth on the private network, or `localhost` services. A finding needs (a) attacker influence over the destination and (b) a reachable internal target or a response channel that matters.

Variants:

- **Full-read SSRF:** the response body comes back to the attacker (preview, import). Highest impact.
- **Blind SSRF:** the request is sent but the response is not returned (webhooks). Impact depends on whether a state-changing internal endpoint exists, or on timing/error oracles.
- **Partial control:** only the path or query is controlled on a fixed host. Look for path traversal into other internal endpoints (`/api/v1/../../admin`).

## Where to look

| Stack | Outbound sinks |
|---|---|
| Node | `fetch`, `axios`, `got`, `node-fetch`, `request`, `http.get`, `undici`, Puppeteer/Playwright `page.goto`, `sharp`/`jimp` with URLs |
| Python | `requests`, `httpx`, `urllib.request.urlopen` (also handles `file://`), `aiohttp`, `pycurl`, `PIL.Image.open(urlopen(...))`, WeasyPrint, `pdfkit`/wkhtmltopdf |
| Ruby | `Net::HTTP`, `open-uri` (`URI.open` / `Kernel#open` with a URL), `HTTParty`, `Faraday`, `RestClient` |
| Java / Spring | `RestTemplate`, `WebClient`, `HttpURLConnection`, `URL.openStream`, Apache `HttpClient`, `OkHttp`, `ImageIO.read(URL)` |
| PHP / Laravel | `file_get_contents($url)`, `curl_exec`, `fopen`, Guzzle, `Http::get`, `getimagesize($url)`, `simplexml_load_file` |
| Go | `http.Get`, `http.Client.Do`, `net.Dial`, `httputil.ReverseProxy` with dynamic `Director` |
| Anywhere | Headless browsers and HTML-to-PDF converters rendering user HTML (they follow `<img>`, `<iframe>`, `<link>`, CSS `url()`), XML parsers with external entities, SVG rasterizers, FFmpeg/ImageMagick with URL inputs |

```bash
rg -n -e 'fetch\(|axios\.|got\(|http\.get\(|requests\.(get|post)|httpx\.|urlopen\(|URI\.open|Net::HTTP|RestTemplate|WebClient|file_get_contents\(\$|curl_exec|http\.(Get|Post)\(|NewRequest\(' 
rg -n -i -e 'webhook|callback_?url|preview|unfurl|import.?url|avatar_?url|image_?url|proxy|redirect_uri|jwks_uri|discovery'
```

## Vulnerable vs safe

```python
# Vulnerable: any URL, follows redirects, returns body
r = requests.get(request.json["url"], timeout=10)
return r.text

# Safer: scheme + host policy, resolve once, check every address, pin the connection, no redirects
import ipaddress, socket
from urllib.parse import urlsplit

def resolve_public(url):
    u = urlsplit(url)
    if u.scheme not in ("https",) or not u.hostname:
        raise ValueError("scheme")
    infos = socket.getaddrinfo(u.hostname, u.port or 443, proto=socket.IPPROTO_TCP)
    addrs = {ipaddress.ip_address(i[4][0]) for i in infos}
    if any(not a.is_global for a in addrs):   # rejects private, loopback, link-local, reserved
        raise ValueError("non-public address")
    return u, addrs
# Then connect to the checked IP (pin it) and send Host: u.hostname, with allow_redirects=False.
```

```js
// Node: use an agent that checks the address at connect time (handles DNS rebinding)
import { RequestFilteringHttpsAgent } from 'request-filtering-agent';
await fetch(url, { agent: new RequestFilteringHttpsAgent(), redirect: 'error' }); // node-fetch style
```

Go: set `net.Dialer.Control` to reject non-public IPs at dial time, and set `CheckRedirect` on the client to return `http.ErrUseLastResponse` or re-check the target.

The strongest design is an **allowlist** of destination hosts. Denylists of private ranges are second best and easy to get wrong.

## Bypasses to check the defense against

A validator that string-matches the URL usually fails one of these. Check the defense in source; you do not need to send them anywhere.

| Bypass | What it defeats |
|---|---|
| Redirects: allowed host returns `302 Location: http://169.254.169.254/` | Checks on the first URL only, with redirects followed |
| DNS rebinding: hostname resolves public at check time, private at fetch time | Check-then-fetch with two resolutions |
| Alternate IP encodings: `http://2130706433/`, `http://0x7f.1/`, `http://0177.0.0.1/`, `http://127.1/`, `http://0.0.0.0/` | Regex or prefix checks on the host string |
| IPv6 forms: `[::1]`, `[::ffff:127.0.0.1]`, `[fd00::1]`, `[fe80::...]` | IPv4-only denylists |
| Parser differentials: `http://allowed.com@evil/`, `http://evil#@allowed.com`, `http://allowed.com.evil/`, backslashes | Validator and fetcher parse differently |
| Non-HTTP schemes: `file://`, `gopher://`, `dict://`, `ftp://`, `jar:`, `netdoc:` | Missing scheme allowlist (libcurl and `urllib` support several) |
| Hostnames that resolve to private IPs (`localtest.me`, wildcard DNS services) | Checks on the literal host, not the resolved IP |
| `startsWith("https://allowed.com")` | `https://allowed.com.evil.net` |

## High-value internal targets (for impact reasoning only)

- Cloud metadata: `169.254.169.254` (AWS, GCP, Azure, OpenStack), `fd00:ec2::254` (AWS IPv6), `metadata.google.internal`. AWS IMDSv2 requires a `PUT` for a session token, which blocks most GET-only SSRF; GCP requires the `Metadata-Flavor: Google` header; Azure requires `Metadata: true`. Whether IMDSv2 is enforced is a deployment fact → `needs_validation` unless infrastructure code in the repo sets it.
- Kubernetes API, kubelet (`:10250`), Docker socket over TCP (`:2375`), Consul, etcd, Redis, Elasticsearch, internal admin panels.
- `localhost` services: debug ports, actuator endpoints (`/actuator/env`), Prometheus, admin APIs bound to loopback.

## Validate without harm

- Prove attacker control of the destination by unit-testing the validator: call it with the bypass list above and show which pass. No network needed.
- If execution is allowed, start a **local loopback listener** inside the sandbox (for example `python3 -m http.server` on 127.0.0.1 with a canary path) and show the target fetches it when it should not. Network isolation must stay on.
- Never point the target at real metadata endpoints, internal services of a deployed environment, or any external host you do not control.
- For blind SSRF, the local listener's access log is the evidence.

## False-positive traps

| Looks bad | Check before reporting |
|---|---|
| User sets a webhook URL and the server calls it | That is the feature. The finding is only that internal destinations are not blocked, and that needs a reachable internal target |
| Fetch to a URL built from a fixed base plus a user ID | Check whether the user value can contain `/`, `..`, `@`, `#`, or `?` to change host or path |
| Outbound proxy configured | An egress proxy with an allowlist may block everything. Mark `needs_validation` naming the proxy policy |
| Admin-configured integration URL | Admins may be trusted to point the server anywhere. Check whether lower-privilege tenants can set it |
| Response not returned and no internal state-changing endpoint known | Blind SSRF with no demonstrated effect is low or `needs_validation` |

## Severity guidance

| Result | Typical severity |
|---|---|
| Unauthenticated full-read SSRF reaching cloud credentials or an unauthenticated internal admin API | Critical |
| Authenticated full-read SSRF to internal services or metadata | High |
| Blind SSRF that can trigger a known state-changing internal endpoint; full-read SSRF limited to `file://` of non-secret files | Medium |
| Blind SSRF with only port-scan style timing signals | Low |

Fix pattern: allowlist destinations where the product allows it; otherwise check the resolved IP at connect time, disable redirects or re-check each hop, restrict schemes to `https`, and route outbound traffic through an egress proxy. Add a regression test with the bypass list.

Sources: adapted from cloudflare/security-audit-skill (MIT), addyosmani/agent-skills (MIT) and general practice.
