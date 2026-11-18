# Attack-Surface Checklists

Load only the sections that match the surfaces found in reconnaissance. Each item is a question to trace in source, not a finding. A finding still needs all six elements from `SKILL.md`.

## Deep references by vulnerability class

Each section below is a short checklist. When a question applies, open the matching class reference for sinks by framework, vulnerable and safe code, harmless validation, false-positive traps, and severity guidance.

| Class | Reference | Typical surfaces |
|---|---|---|
| SQL, NoSQL, command, template, expression, LDAP, header injection | [injection](injection.md) | Query builders, ORMs' raw APIs, shell calls, template rendering, `eval` |
| Login, sessions, JWT, OAuth/OIDC, SAML, MFA, reset, API keys | [authn-and-session](authn-and-session.md) | Auth middleware, token verification, recovery flows |
| IDOR/BOLA, function-level authz, mass assignment, tenant isolation | [authz-and-tenancy](authz-and-tenancy.md) | Any handler that takes a resource ID; ORMs; multi-tenant stores |
| SSRF | [ssrf](ssrf.md) | Webhooks, URL import, previews, renderers, proxies |
| Path traversal, uploads, archives, XXE, deserialization | [files-and-deserialization](files-and-deserialization.md) | File APIs, upload handlers, XML parsers, pickle/YAML/Java serialization |
| XSS, CSRF, CORS, headers, open redirect, postMessage | [browser-and-web](browser-and-web.md) | Templates, SPAs, cookie-auth APIs, cross-origin config |
| Secrets, randomness, password hashing, crypto, webhook signatures, debug exposure | [secrets-and-crypto](secrets-and-crypto.md) | Config, env, key files, token generators, crypto calls |
| Vulnerable dependencies, dependency confusion, CI workflows, release | [supply-chain](supply-chain.md) | Manifests, lockfiles, `.github/workflows`, Dockerfiles |
| Races, state machines, numeric abuse, feature abuse, fail-open | [business-logic](business-logic.md) | Money, credits, quotas, approvals, export/import |
| Backup, restore, deletion, export, retention | [data-lifecycle](data-lifecycle.md) | Export jobs, dump scripts, soft delete, signed download links, purges |
| Prompt injection, model output in sinks, tool authorization, exfiltration through tools | [ai-llm](ai-llm.md) | Model calls, tool handlers, Markdown renderers, retrieval indexes |
| Hooks, MCP configs, permission allowlists, instruction files, skills and plugins, CI agents | [agent-config](agent-config.md) | Agent settings files, `AGENTS.md`/`CLAUDE.md`, `.mcp.json`, skill folders |

## Obvious-exposure sweep (do this literally, every full audit)

Cheap checks that every team assumes someone else did. Each hit still needs a traced impact before it becomes a finding.

- Committed secrets: `.env*`, `*.pem`, `*.key`, `credentials.json`, service-account JSON, tokens in config, fallback defaults such as `process.env.SECRET || 'dev'`. Is `.gitignore` covering them?
- Security TODOs: `rg -n -i 'TODO|FIXME|HACK|XXX' | rg -i 'auth|secur|valid|permission|csrf|xss|sanitiz|escape|bypass'`.
- Debug modes reachable in production config: `DEBUG = True`, `APP_DEBUG=true`, `app.run(debug=True)`, Spring Actuator `exposure.include=*`, `/debug/pprof`.
- Unprotected operational routes: `/admin`, `/debug`, `/metrics`, `/actuator`, `/env`, `/health` with details, `/graphql` introspection plus playground, `/swagger` on private APIs.
- Seed, demo, or test accounts with fixed passwords that production also loads.
- Dynamic code execution with input: `eval`, `exec`, `Function`, `vm.run*`, `child_process`, `shell=True`, `Runtime.exec`.
- Permissive CORS with credentials; cookies without `HttpOnly`, `Secure`, or `SameSite` on session cookies.
- Redirect parameters (`next`, `return`, `redirect`, `url`, `goto`, `continue`) passed to redirects.
- Error handlers returning stack traces, SQL errors, or internal paths.
- Lockfiles present and committed; obviously outdated security-critical packages.
- Agent configuration committed to the repository: hooks that run shell, MCP server definitions, broad permission allowlists, auto-approve settings, and secrets in instruction files (see [agent-config](agent-config.md)).

## Web, protocol, and authentication

- Is authentication enforced on every route, including alternate verbs, versioned or legacy paths, websockets, and GraphQL resolvers?
- Is authorization checked per resource at the last trusted decision point, not only in the UI or a parent route (IDOR, BOLA)?
- Session and token handling: fixation, expiry, revocation, refresh-token reuse, JWT algorithm or `kid` confusion, signature checks actually enforced.
- CSRF on state-changing requests with cookie auth; CORS with credentials and reflected origins.
- SSRF from user-controlled URLs, including redirects, DNS rebinding, and metadata addresses.
- Injection: SQL/NoSQL, command, template, LDAP, header, and path traversal at every sink.
- Mass assignment and over-posting; hidden fields that change authority (role, tenant, owner).
- Password reset, MFA, and account recovery flows that bypass the primary control.
- Host and forwarded headers (`Host`, `X-Forwarded-Host`, `X-Forwarded-For`, `Forwarded`) used for absolute URLs, reset links, tenant routing, or client-IP allowlists. Who can set them, and does trusted ingress strip client copies?
- Cache poisoning and deception: a request value that changes the response but is not in the cache key, or a private dynamic page cached because its path looks static (`/account/profile.css`). Needs both the cache and the app behavior; cache config outside the repo makes it `needs_validation`.
- Request smuggling: only relevant when the repo contains a proxy, gateway, or custom HTTP parser. Name both components and how each frames the same bytes.
- GraphQL: per-field authorization on nested types, introspection exposure, batching and alias abuse against rate limits, query depth and cost limits.

## Data isolation and lifecycle

Deep reference: [data-lifecycle](data-lifecycle.md).

- Is the tenant or owner scope applied to every query, cache key, search index, export, and background job?
- Are derived copies (caches, analytics, logs, backups, search) scoped and deleted with the source data?
- Do deletion and retention reach every copy? Can soft-deleted data still be reached?
- Do signed URLs and shared links expire and stay bound to their intended resource?
- Do cache keys, object-storage paths, search document IDs, temp files, and unique constraints include the tenant?
- Do bypass clients (`unscoped`, `withoutGlobalScope`, service-role keys, raw SQL, admin DB users) appear on request paths?
- Do import, restore, undo, and migration paths re-apply current ownership and validation?
- Do counts, filters, sort orders, and error differences reveal confidential state (existence or aggregate oracles)?

## Client side

- Is XSS prevented on every sink: `innerHTML`, `dangerouslySetInnerHTML`, `v-html`, markdown renderers, URL schemes (`javascript:`), and SVG uploads?
- Is postMessage origin validated? Can open redirects be chained with auth?
- Do secrets or privileged tokens reach client bundles or local storage?

## Cloud and deployment (source-visible only)

- IAM policies, bucket or object ACLs, and network policies defined in the repository: wildcard principals or actions, public buckets.
- Secrets in infrastructure code, CI variables echoed to logs, debug endpoints enabled by default.
- Anything that depends on a deployed setting not present in the repository is `needs_validation`, naming that setting.

## Supply chain and release

- CI workflows that run untrusted pull-request code with secrets (`pull_request_target`, self-hosted runners).
- Unpinned actions or images, lockfile drift, install scripts, dependency confusion (internal names resolvable publicly).
- Artifact signing and provenance; can release automation be triggered by lower-trust actors?

## Protocols, RPC, and messaging

- Is peer identity authenticated on every message or connection? Is replay prevented?
- Deserialization of untrusted data (pickle, Java serialization, YAML unsafe load, polymorphic JSON).
- Do message consumers trust producer-supplied tenant or role fields?

## Desktop, mobile, and local IPC

- Local sockets, named pipes, and localhost HTTP servers: who can connect, and is the caller authenticated?
- Deep links and intent handlers that perform privileged actions without confirmation.
- Webviews with JavaScript bridges exposed to remote content.

## AI and LLM features

Deep references: [ai-llm](ai-llm.md) for application features, [agent-config](agent-config.md) for agent harness configuration in the repository.

- Can untrusted content (documents, web pages, tool output) reach the model context and steer tool calls (indirect prompt injection)?
- Do model-chosen tool arguments cross authority boundaries (file paths, URLs, SQL, shell, other users' data)?
- Is model output rendered as HTML or Markdown that can exfiltrate data (image URLs with query data)?
- Are per-user data boundaries preserved in retrieval (RAG) indexes?
- Is authorization for tool calls enforced in code on the end user's identity, not in the system prompt? Instructions in a prompt are not a control.
- Can content written by one user (memory, shared documents, tickets) persist into another user's model context?
- Do destructive or irreversible tool actions require confirmation bound to the exact action and arguments?
- Do MCP or plugin servers authenticate the client and scope tokens per user, or share one powerful credential?
- Does model output reach `eval`, SQL, shell, file paths, or `innerHTML` without the same validation as user input?

## Resource exhaustion and availability

- Unbounded input sizes, decompression ratios, regular expressions (ReDoS), recursion depth, pagination limits.
- Expensive operations reachable unauthenticated; missing rate limits on authentication and costly endpoints.
- Validate only with a local, bounded fixture. Never test availability against a live or shared service.

## Memory safety and binaries

- In C, C++, and unsafe Rust or Go: bounds checks on parser input, integer overflow before allocation, use-after-free in error paths.
- Prefer existing sanitizer or fuzz harnesses, run inside the sandbox with limits.

Sources: adapted from cloudflare/security-audit-skill (MIT), addyosmani/agent-skills (MIT) and general practice.
