# Authentication, Sessions, and Tokens

Open this file when the target logs users in, issues or verifies sessions, JWTs, API keys, OAuth/OIDC or SAML artifacts, runs MFA or passkeys, or offers password reset, email change, or account linking. Authorization of an already-identified principal is in the authorization and tenancy reference.

## Core rule

For every credential, walk **issue → store → transmit → verify → refresh → revoke**. At verification, list every binding the credential needs for its role: signature or secret, issuer, audience, expiry, principal, session, tenant, assurance level, and one-time state. A missing binding that the server **accepts** is the finding. A missing header or flag alone is not.

The effective authentication policy is the **weakest parallel door** to the same identity: legacy login, mobile API, SSO callback, magic link, API key, password reset, support impersonation, websocket upgrade.

## Where to look

| Stack | Login, session, and token code |
|---|---|
| Express / Node | `passport.use(...)` strategies, `express-session` config, `jsonwebtoken.verify` / `jose.jwtVerify`, `cookie-session`, NextAuth/Auth.js `callbacks`, custom `authenticate` middleware and the routes registered **before** it |
| Django | `AUTHENTICATION_BACKENDS`, `django.contrib.auth` views, `SESSION_*` and `CSRF_*` settings, DRF `DEFAULT_AUTHENTICATION_CLASSES`, `simplejwt` settings, `allauth` adapters |
| Flask | `flask_login.login_user`, `SECRET_KEY`, `SESSION_COOKIE_*`, `itsdangerous` serializers, `flask_jwt_extended` config |
| Rails | Devise config (`config/initializers/devise.rb`), `has_secure_password`, `session_store`, `protect_from_forgery`, `skip_before_action :authenticate_user!` |
| Spring | `SecurityFilterChain` beans, `permitAll()` matchers, `oauth2ResourceServer().jwt()`, `JwtDecoder` beans, `UserDetailsService`, `PasswordEncoder` |
| Laravel | `config/auth.php` guards, `Auth::attempt`, Sanctum/Passport config, `routes/*.php` middleware groups, `withoutMiddleware('auth')` |
| Go | middleware wrapping `http.Handler`, `golang-jwt/jwt` `Parse` with keyfunc, `gorilla/sessions` store keys, chi/gin groups that skip middleware |

Grep for the doors:

```bash
rg -n -e 'permitAll|anonymous\(\)|AllowAny|skip_before_action\s+:authenticate|withoutMiddleware|@PermitAll|login_exempt|csrf_exempt'
rg -n -e 'jwt\.(decode|verify|Parse)|jwtVerify|JwtDecoder|algorithms\s*=|verify_signature|ignoreExpiration|ParseUnverified'
rg -n -e 'reset_password|password_reset|forgot|magic.?link|verify_email|change_email|impersonat|sudo|act_as'
rg -n -e 'Math\.random|random\.random\(|rand\(|mt_rand|uniqid|new Random\(' -- '*token*' '*reset*' '*session*'
```

## Classes and examples

### Unauthenticated route

Middleware order or allowlists leave a sensitive route open. Look for routes registered before `app.use(auth)`, broad `permitAll()` patterns such as `/api/**/public/**` that also match private paths, alternate verbs (`HEAD`, `OPTIONS`, method override), trailing slash and case variants, and versioned or legacy prefixes (`/v1/` vs `/v2/`).

```js
// Vulnerable: export route registered before the auth middleware
app.get('/api/reports/export', exportHandler);
app.use('/api', requireAuth);
// Safe: mount auth first, or attach it to the route
app.get('/api/reports/export', requireAuth, exportHandler);
```

```java
// Vulnerable: pattern ordering; first match wins in Spring Security
http.authorizeHttpRequests(a -> a
    .requestMatchers("/api/**").permitAll()
    .requestMatchers("/api/admin/**").hasRole("ADMIN"));
// Safe: most specific first, deny by default
http.authorizeHttpRequests(a -> a
    .requestMatchers("/api/admin/**").hasRole("ADMIN")
    .requestMatchers("/api/public/**").permitAll()
    .anyRequest().authenticated());
```

### JWT verification

| Red flag | Why | Do instead |
|---|---|---|
| `jwt.decode(token)` used for identity (Node `jsonwebtoken.decode`, PyJWT `options={"verify_signature": False}`, Go `ParseUnverified`) | No signature check | `verify` with a pinned key |
| Algorithm taken from the token header, or `algorithms` list missing | `none` or HS/RS confusion (HMAC with the public key) | Pin `algorithms: ['RS256']` server-side |
| `kid`, `jku`, `x5u` used to fetch or select keys without an allowlist | Attacker supplies their own key | Map `kid` to a fixed key set (JWKS from configured issuer only) |
| No `aud` / `iss` check | Token for another service accepted | Verify both |
| `ignoreExpiration: true`, no `exp` | Tokens live forever | Short expiry plus refresh |
| HS256 secret is short, default, or committed (`secret`, `changeme`) | Forgeable tokens | Long random secret from a secret store |
| Go keyfunc returns the key without checking `token.Method` | Algorithm confusion | `if _, ok := t.Method.(*jwt.SigningMethodRSA); !ok { return nil, err }` |

```python
# Vulnerable
claims = jwt.decode(token, options={"verify_signature": False})
# Safe
claims = jwt.decode(token, PUBLIC_KEY, algorithms=["RS256"], audience="api://orders", issuer=ISSUER)
```

### Sessions and cookies

- **Fixation:** session ID not rotated at login, MFA completion, privilege change, or impersonation. Look for `req.session.regenerate` (Express), `cycle_key` (Django does this in `login()`), `reset_session` (Rails Devise does it), `session.invalidate()` / `changeSessionId()` (Spring default `migrateSession`).
- **Revocation:** logout, password change, account disable, and role removal must kill server sessions **and** refresh tokens. Stateless JWTs with long expiry and no denylist survive logout; that matters only if the product promises revocation.
- **Signed client-side sessions** (Flask default, `cookie-session`, Rails cookie store): the secret key is the whole security model. A committed or default `SECRET_KEY` lets anyone forge a session. Check `SECRET_KEY`, `secret_key_base`, `APP_KEY`, `SESSION_SECRET` in committed config and defaults in code.
- **Cookie flags:** missing `HttpOnly`, `Secure`, or `SameSite` on a session cookie is a hardening note unless you can name a realistic path (XSS that reads it, a plain-HTTP route on the same host, a sibling subdomain controlled by another party with `Domain=` set wide).

### Passwords and login

- Storage: bcrypt (cost ≥ 10, 12 typical), scrypt, argon2id, or PBKDF2 with a high iteration count. MD5, SHA-1, or unsalted SHA-256 for passwords is a real weakness, but a **finding** needs a reachable disclosure of the hashes. Otherwise report it as hardening with high priority.
- Comparison: `==` on secrets or tokens leaks timing; use `crypto.timingSafeEqual`, `hmac.compare_digest`, `MessageDigest.isEqual`, `hash_equals`, `subtle.ConstantTimeCompare`. Remote timing attacks on modern stacks are hard; treat as hardening unless a local fixture shows a usable signal.
- Brute force: no rate limit or lockout on login, OTP, or reset-code endpoints. A 6-digit code with unlimited attempts is a real finding (10^6 guesses). An unthrottled password login is usually medium at most and depends on deployment (WAF, gateway) you cannot see, so mark it `needs_validation` unless the limit is clearly absent in source and no edge control exists.
- Enumeration: different responses for "no such user" vs "wrong password". Low severity on its own; many products expose account existence through signup anyway.

### Password reset, email change, magic links

Checklist for every recovery token:

1. Generated with a CSPRNG (`crypto.randomBytes`, `secrets.token_urlsafe`, `SecureRandom`, `random_bytes`, `crypto/rand`). Not `Math.random`, `uuid v1`, timestamps, or user ID hashes.
2. Stored hashed or at least bound to one user and one purpose.
3. Expires (≤ 1 hour is common) and is single-use; issuing a new token invalidates older ones.
4. Reset link host is **not** built from the request `Host` or `X-Forwarded-Host` header (host-header poisoning sends the token to the attacker's domain).
5. Successful reset invalidates other sessions.
6. Email change requires the current password or fresh auth, and confirms the **new** address before it becomes a login identifier.

```python
# Vulnerable: reset URL built from the attacker-controlled Host header
link = f"https://{request.get_host()}/reset/{token}"
# Safe: configured canonical origin
link = f"{settings.PUBLIC_BASE_URL}/reset/{token}"
```

Note: Django's `get_host()` checks `ALLOWED_HOSTS`; with a strict list this is not exploitable. `ALLOWED_HOSTS = ['*']` makes it exploitable.

### OAuth / OIDC

As a **client (relying party):** session-bound `state` checked on callback; PKCE for public clients; ID token signature, `iss`, `aud`, `nonce`, and expiry checked; account matched on the provider's stable `sub`, not on an unverified `email` claim. Account linking by email from a provider that does not verify email lets an attacker take over existing accounts.

As an **authorization server:** exact `redirect_uri` match (not prefix or substring), codes single-use and bound to client and redirect URI, refresh tokens rotated or bound.

### SAML

The signed element must be the element the code reads identity from (signature wrapping). Check that unsigned assertions are rejected, the XML parser disables external entities, and `Audience`, `Recipient`, `NotOnOrAfter`, and `InResponseTo` are verified. Prefer a maintained library and check its version for known bypasses.

### MFA and step-up

- A first-factor session must not reach MFA-protected APIs before the second factor completes. Check every API route, not only the UI flow.
- Enrolling, replacing, or disabling a factor requires fresh authentication.
- Recovery codes are single-use and hashed.
- "Remember this device" tokens are bound to the user and revocable.

### API keys and service credentials

- Key lookup must bind tenant and scope from the server-side key record, not from a request header or body.
- Publishable keys (Stripe `pk_`, Firebase web config, Google Maps browser keys) are public by design. Not a finding.
- Keys in URLs end up in logs and `Referer` headers.

## Validate without harm

- Use dummy users created in a local test database or test fixtures. Never test against real accounts.
- JWT: sign a token locally with `alg: none` or with a wrong key, call the verify function in a unit test, and show it is accepted.
- Missing auth: start the app locally with test config and request the route without a cookie, or call the router's matcher in a test.
- Reset token predictability: show the generator in source; do not attempt to predict real tokens.
- Brute-force limits: show the absence in source and, at most, send a small fixed number of requests (for example 20) to a **local** instance. Never run guessing against a deployment.

## False-positive traps

| Looks bad | Check before reporting |
|---|---|
| Route has no auth decorator | Global middleware, a router-level guard, a gateway policy, or `DEFAULT_PERMISSION_CLASSES` may cover it |
| `jwt.decode` without verify | Often used only to read `exp` for client-side refresh timing, after a separate server verify |
| Long-lived JWT | Matters only if revocation is promised or the token leaks somewhere |
| Missing rate limit in app code | An API gateway, WAF, or IdP may enforce it. Mark `needs_validation` naming that control |
| `SECRET_KEY` in repo | Check whether it is a dev-only default that production overrides via environment. If prod reads the committed value, it is critical |
| Username enumeration | Low impact; often already public via signup. Report as low or hardening |

## Severity guidance

| Result | Typical severity |
|---|---|
| Forge any user's session or JWT (committed signing secret used in production, `alg` confusion, signature not verified); unauthenticated admin route | Critical |
| Account takeover of a targeted user via reset poisoning, OAuth email linking, or MFA bypass | High |
| Session fixation needing a victim action; OTP brute force with partial throttling | Medium |
| Account enumeration; missing cookie flags with a speculative path | Low or hardening note |

Sources: adapted from cloudflare/security-audit-skill (MIT), addyosmani/agent-skills (MIT) and general practice.
