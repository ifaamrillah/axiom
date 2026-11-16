# Attack-Surface Checklists

Load only the sections that match the surfaces found in reconnaissance. Each item is a question to trace in source, not a finding. A finding still needs all six elements from `SKILL.md`.

## Web, protocol, and authentication

- Is authentication enforced on every route, including alternate verbs, versioned or legacy paths, websockets, and GraphQL resolvers?
- Is authorization checked per resource at the last trusted decision point, not only in the UI or a parent route (IDOR, BOLA)?
- Session and token handling: fixation, expiry, revocation, refresh-token reuse, JWT algorithm or `kid` confusion, signature checks actually enforced.
- CSRF on state-changing requests with cookie auth; CORS with credentials and reflected origins.
- SSRF from user-controlled URLs, including redirects, DNS rebinding, and metadata addresses.
- Injection: SQL/NoSQL, command, template, LDAP, header, and path traversal at every sink.
- Mass assignment and over-posting; hidden fields that change authority (role, tenant, owner).
- Password reset, MFA, and account recovery flows that bypass the primary control.

## Data isolation and lifecycle

- Is the tenant or owner scope applied to every query, cache key, search index, export, and background job?
- Are derived copies (caches, analytics, logs, backups, search) scoped and deleted with the source data?
- Do deletion and retention reach every copy? Can soft-deleted data still be reached?
- Do signed URLs and shared links expire and stay bound to their intended resource?

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

- Can untrusted content (documents, web pages, tool output) reach the model context and steer tool calls (indirect prompt injection)?
- Do model-chosen tool arguments cross authority boundaries (file paths, URLs, SQL, shell, other users' data)?
- Is model output rendered as HTML or Markdown that can exfiltrate data (image URLs with query data)?
- Are per-user data boundaries preserved in retrieval (RAG) indexes?

## Resource exhaustion and availability

- Unbounded input sizes, decompression ratios, regular expressions (ReDoS), recursion depth, pagination limits.
- Expensive operations reachable unauthenticated; missing rate limits on authentication and costly endpoints.
- Validate only with a local, bounded fixture. Never test availability against a live or shared service.

## Memory safety and binaries

- In C, C++, and unsafe Rust or Go: bounds checks on parser input, integer overflow before allocation, use-after-free in error paths.
- Prefer existing sanitizer or fuzz harnesses, run inside the sandbox with limits.
