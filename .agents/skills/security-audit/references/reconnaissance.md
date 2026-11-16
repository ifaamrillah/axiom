# Reconnaissance

Map the target before hunting. Reconnaissance reads source and local configuration only. It sends no inputs and contacts no deployed or shared service.

## Facts to collect (with file:line)

1. **Product and principals.** What the product does; who uses and operates it; each lower-trust principal and the actions it has **by design**.
2. **Stack and local operation.** Languages, frameworks, and build system; offline build and test commands; which inputs those commands process; missing toolchains.
3. **Identity and authority.** Where authentication happens on each surface; per-resource authorization and tenant or owner scoping; privilege changes, revocation, and recovery paths; which controls are visible in source and which depend on deployment facts.
4. **Entry surfaces.** HTTP and browser, RPC, messages and queues, files and archives, CLI, environment and config, plugins, dependencies and CI, cloud events, model context and tool arguments, mobile deep links and webviews, local IPC.
5. **Paths to sinks.** For each surface, the major transformations, stored or derived copies, and security-relevant sinks (queries, shell, filesystem, templates, deserializers, outbound requests, privilege changes).
6. **Execution limits.** Small offline tests or fixtures usable for validation; commands that would fetch, publish, or touch shared state (prohibited); whether the sandbox controls in `SKILL.md` can be enforced locally.
7. **Comparable baseline** (optional). Similar software visible in docs or dependencies, used to calibrate effort and severity, never to dismiss a finding.

When delegation is available, split this into parallel read-only researchers: (a) product and stack, (b) principals and controls, (c) entry surfaces and sinks, (d) local execution and deployment visibility. Each returns facts only.

## Finding entry points and controls fast

Fingerprint the stack from manifests (`package.json`, `requirements*.txt`, `pyproject.toml`, `Gemfile`, `pom.xml`, `build.gradle*`, `composer.json`, `go.mod`), then use the table to locate routes, auth, and config.

| Stack | Routes and handlers | Auth and authorization | Security config |
|---|---|---|---|
| Express / Fastify / NestJS | `rg -n "\.(get\|post\|put\|patch\|delete\|all\|use)\(\s*['\"]/"`; Nest `@(Get\|Post\|Put\|Patch\|Delete)\(` | `passport`, custom middleware, Nest `@UseGuards`, `@Public` | `helmet`, `cors(`, `express-session`, `.env*` |
| Next.js | `app/**/route.ts`, `pages/api/**`, Server Actions (`'use server'`), `middleware.ts` matcher | Auth.js callbacks, `middleware.ts`, per-route checks | `next.config.*` headers, `NEXT_PUBLIC_*` vars |
| Django / DRF | `urls.py` (`path(`, `re_path(`, routers) | `permission_classes`, `@login_required`, `get_queryset` | `settings*.py`: `DEBUG`, `ALLOWED_HOSTS`, `SECRET_KEY`, `MIDDLEWARE`, `CSRF_*`, `SESSION_*`, `CORS_*` |
| Flask / FastAPI | `@app.route`, `@bp.route`, `@router.(get\|post)` | `login_required`, `Depends(get_current_user)` | `app.config`, `SECRET_KEY`, `debug=` |
| Rails | `config/routes.rb`, `bin/rails routes` (local, no network) | `before_action`, Devise, Pundit/CanCanCan, `skip_before_action` | `config/environments/production.rb`, `credentials.yml.enc`, `config/initializers/*` |
| Spring | `@(Get\|Post\|Put\|Delete\|Request)Mapping`, `RouterFunction` | `SecurityFilterChain`, `@PreAuthorize`, `permitAll` | `application*.yml/properties`, actuator exposure |
| Laravel | `routes/web.php`, `routes/api.php`, `php artisan route:list` (local) | middleware groups, policies, gates, `authorize()` | `config/*.php`, `.env.example`, `VerifyCsrfToken::$except` |
| Go | `http.HandleFunc`, `mux.Handle`, chi `r.Get`, gin `r.GET`, echo `e.GET` | middleware chains, group-level `Use` | flags, env loading, `tls.Config` |
| GraphQL | schema files, resolvers, `@auth` directives | resolver-level checks, context builders | introspection, depth or cost limits |

Also enumerate non-HTTP entries: queue consumers (`@KafkaListener`, `@RabbitListener`, Celery `@task`, Sidekiq `perform`, BullMQ `Worker`), cron and scheduled jobs, CLI commands, webhooks, file watchers, websocket handlers, and serverless function handlers (`handler(event, context)`).

For each entry, record: path or name, method, authentication requirement, authorization check, input parser, and the first sink it reaches. A spreadsheet-like table in the architecture summary is the fastest shared context.

## Trust-boundary questions

Answer these with file:line. Unknowns become `needs_validation` facts, not assumptions.

1. Where is the tenant or owner of the current request derived, and can the request override it?
2. Which routes are public by design? Is that list explicit (allowlist) or implicit (whatever lacks a decorator)?
3. Which components trust headers set by a proxy (`X-Forwarded-*`, `X-User-Id`, `X-Tenant`)? Is the proxy in the repo?
4. Which data stores have bypass clients or admin connections on request paths?
5. Which outbound calls take URLs from users or tenants?
6. Which code runs with elevated authority (background jobs, admin tools, CI) and reads data that lower-trust users wrote?
7. Which secrets does each process hold, and which of them reach logs, clients, or build artifacts?

## Prioritization

Rank ledger units in this order when the budget cannot cover everything, and record the reason:

1. Unauthenticated and lowest-trust entry surfaces.
2. Boundaries protecting the most valuable assets: credentials, cross-tenant data, code execution, money movement, release authority.
3. Changed source since the last run, prior `needs_validation`, prior gaps.
4. Classes that historically yield findings for this kind of target (authorization for business SaaS, injection for legacy PHP, SSRF for integration-heavy products, deserialization for Java and Python services handling blobs).

Break ties by unit ID so runs are repeatable.

## Architecture summary

Write about 1,000 words or fewer: principals, protected resources, the stack, entry surfaces, key source-to-sink paths, controls, and deployment facts that are not visible in source. This summary is the shared context for hunters and verifiers.

Suggested skeleton:

```markdown
# Architecture: <target> @ <commit>
## Product and principals      (who, what they may do by design, protected assets)
## Stack and local execution   (languages, frameworks, offline test command, sandbox status)
## Entry surfaces              (table: entry, auth, authz, parser, first sink, file:line)
## Trust boundaries and controls (one line each, strongest control with file:line)
## Not visible in source       (proxy, IdP, WAF, IAM, cache facts that decide outcomes)
## Class references selected   (which class references apply and why; which were excluded and why)
```

Select a class reference because reconnaissance found its boundary, not because a library name appears. Record excluded classes with the source fact that excludes them (for example, "no outbound HTTP with user-controlled URLs: SSRF excluded").

## Coverage ledger

Seed **units** deterministically from the map. A unit is one **surface × boundary × attack class** (for example `api/orders × tenant-isolation × IDOR`). Unit IDs stay stable across runs so that coverage can be compared over time.

Unit states:

| State | Meaning |
|---|---|
| `planned` | Seeded, not yet assigned |
| `assigned` | Given to a hunter |
| `candidate` | Produced at least one candidate (linked by fingerprint) |
| `covered` | Hunted with no surviving candidate; record what was checked |
| `deferred` | Not done this run; give the reason |
| `blocked` | Cannot proceed; give the exact blocker |
| `out_of_scope` | Excluded by scope; never counts as covered |

## Prior runs

If prior ledgers and findings exist, read them before planning:

- A prior `confirmed` record whose relevant source is unchanged is carried into the current candidate set and re-verified. Hunters skip only that root cause.
- If the relevant source changed, create a revalidation unit. The prior verdict does not carry over.
- Prior `needs_validation`, `deferred`, `blocked`, and `out_of_scope` units are current work, not suppression keys.
- A prior `rejected` record suppresses only the identical unchanged claim, never coverage of its unit.
- A prior `quick` or scoped run contributes only its recorded evidence and gaps, never an implied "the rest is fine".

Sources: adapted from cloudflare/security-audit-skill (MIT) and general practice.
