# Secrets Exposure and Cryptography Misuse

Open this file when the repository contains credentials or key material, generates tokens or IDs that guard access, hashes passwords, encrypts or signs data, verifies webhooks, or logs request data.

## Core rule

A secret matters by the **authority** it grants. For each candidate, name what the secret unlocks, who can read it today, and whether production uses it. For crypto, name the security property the code relies on (confidentiality, integrity, unpredictability, authenticity) and show the primitive or usage that fails to provide it.

Never copy a discovered secret value into notes, findings, or reports. Record file, line, secret type, and a short redacted prefix (for example `AKIA****`).

## Secrets in source and history

### Where to look

- Committed env and config: `.env*`, `config/*.yml`, `settings.py`, `application.properties` / `application.yml`, `appsettings*.json`, `config/database.php`, `docker-compose*.yml`, Helm `values*.yaml`, Terraform `*.tfvars`, CI files.
- Key files: `*.pem`, `*.key`, `*.p12`, `*.pfx`, `id_rsa*`, `*.jks`, `credentials.json`, service-account JSON (`"type": "service_account"`), `.npmrc` / `.pypirc` with tokens, `kubeconfig`.
- Defaults in code: `process.env.JWT_SECRET || 'dev-secret'`, `os.getenv("SECRET_KEY", "changeme")`, `@Value("${jwt.secret:default}")`. A fallback default used when the variable is unset in production is as bad as a committed secret.
- Client bundles: anything under `NEXT_PUBLIC_*`, `VITE_*`, `REACT_APP_*`, `EXPO_PUBLIC_*` is shipped to browsers. Server keys there are exposed.
- Mobile apps: keys in `Info.plist`, `strings.xml`, `google-services.json` (Firebase web keys are public by design; service-account keys are not).
- Git history: secrets removed in a later commit are still in history and in every clone.
- Logs and errors: request bodies, `Authorization` headers, tokens in URLs, full exception dumps returned to clients.

### Commands

Use read-only, local tooling if present. Print file names and rule IDs, not values.

```bash
# Pattern sweep (names only)
rg -l -i -e 'api[_-]?key|secret|passw(or)?d|token|bearer|private[_-]?key|-----BEGIN' --hidden -g '!node_modules' -g '!*.lock'
rg -n -e 'AKIA[0-9A-Z]{16}' -e 'ghp_[A-Za-z0-9]{36}' -e 'xox[baprs]-' -e 'sk_live_' -e 'AIza[0-9A-Za-z_-]{35}' -e '-----BEGIN (RSA|EC|OPENSSH|PRIVATE) KEY' --hidden -o | cut -d: -f1,2
# Fallback defaults
rg -n -e "env\.[A-Z_]*(SECRET|KEY|TOKEN)[A-Z_]*\s*(\|\||\?\?)\s*['\"]" -e "getenv\(\s*['\"][A-Z_]*(SECRET|KEY)['\"],\s*['\"]"
# Scanners (only if already installed; do not install during an audit)
gitleaks detect --no-banner --redact -v --source .          # includes history
trufflehog git file://. --no-verification --no-update     # live verification calls providers; keep it off
```

Live verification of a secret (calling the provider to see if it works) is an external action. Do not do it. Report the secret as `confirmed` exposure when the file is readable by the lower-trust principal; mark whether it is still valid as `needs_validation` for the owner.

### Who can read it

| Location | Lower-trust reader | Usual verdict |
|---|---|---|
| Public repository or published package | Anyone | Confirmed exposure |
| Private repository | Everyone with repo read access, CI logs, forks | Real but narrower; severity depends on what the key unlocks vs what repo readers already have |
| Client bundle or mobile app | Every user | Confirmed exposure |
| Server-only config file in a private repo, test fixture key, example placeholder | Repo readers only / nobody | Often hardening; check if production uses the value |

## Randomness

Security values must come from a CSPRNG.

| Stack | Insecure for tokens | Secure |
|---|---|---|
| Node | `Math.random()`, `Date.now()`, `uuid` v1 | `crypto.randomBytes(32)`, `crypto.randomUUID()` (v4), `crypto.getRandomValues` |
| Python | `random.*`, `uuid.uuid1()` | `secrets.token_urlsafe(32)`, `secrets.token_hex`, `uuid.uuid4()` |
| Ruby | `rand`, `Random.new` | `SecureRandom.hex(32)`, `SecureRandom.urlsafe_base64` |
| Java | `java.util.Random`, `Math.random()` | `SecureRandom` |
| PHP | `rand`, `mt_rand`, `uniqid`, `lcg_value` | `random_bytes`, `random_int`, `bin2hex(random_bytes(32))` |
| Go | `math/rand` (and `math/rand/v2` non-crypto sources) | `crypto/rand.Read`, `crypto/rand.Text` (Go 1.24+) |

Token length: at least 128 bits of entropy for session IDs, reset tokens, API keys, and invite codes. Short numeric codes (6 digits) are acceptable only with strict attempt limits and short expiry.

## Password hashing

Good: argon2id, scrypt, bcrypt (cost ≥ 10; 12 typical), PBKDF2-HMAC-SHA256 with ≥ 600,000 iterations. Framework defaults (Django PBKDF2/argon2, Devise bcrypt, Laravel bcrypt/argon, Spring `DelegatingPasswordEncoder`) are fine.

Bad: MD5, SHA-1, SHA-256 (even salted, single round), reversible encryption, plain text. Note bcrypt truncates input at 72 bytes; pre-hashing with an unkeyed fast hash then encoding as hex is a common workaround; raw binary pre-hash can introduce null-byte issues.

## Encryption and signing misuse

| Red flag | Problem | Do instead |
|---|---|---|
| AES-ECB (`AES/ECB/...`, Java `Cipher.getInstance("AES")` defaults to ECB) | Leaks patterns | AES-GCM or ChaCha20-Poly1305 |
| CBC or CTR without a MAC | Malleable; padding-oracle risk with CBC | AEAD, or encrypt-then-MAC |
| Static or reused IV / nonce, especially with GCM | Nonce reuse breaks GCM confidentiality and integrity | Random 96-bit nonce per message, or a counter with a unique key |
| Hardcoded key or key derived from a password with one SHA round | Key is effectively public or brute-forceable | KMS or secret store; scrypt/argon2/HKDF as appropriate |
| `createCipher` (Node, deprecated) | Weak MD5-based key derivation, no IV | `createCipheriv` with a real key and IV |
| RSA PKCS#1 v1.5 encryption, RSA without padding, keys < 2048 bits | Known attacks | RSA-OAEP, ≥ 2048 bits, or prefer ECDH/X25519 |
| Custom "encryption" (XOR, base64, rot13) | None | Library AEAD |
| Decryption failure falls back to plaintext or skips verification | Fail-open | Fail closed |
| TLS verification disabled: `verify=False`, `rejectUnauthorized: false`, `NODE_TLS_REJECT_UNAUTHORIZED=0`, `InsecureSkipVerify: true`, `CURLOPT_SSL_VERIFYPEER => false`, trust-all `X509TrustManager` | MITM on that connection | Remove, or pin a private CA |
| `==` comparison of HMACs, tokens, or API keys | Timing leak (usually hard to exploit remotely) | Constant-time compare |

## Webhook and signature verification

```js
// Vulnerable: computes the HMAC but compares with == and over a re-serialized body
const sig = crypto.createHmac('sha256', secret).update(JSON.stringify(req.body)).digest('hex');
if (sig == req.headers['x-signature']) handle(req.body);
// Safe: raw body, constant-time compare, timestamp tolerance against replay
const expected = crypto.createHmac('sha256', secret).update(rawBody).digest();
const given = Buffer.from(String(req.headers['x-signature'] || ''), 'hex');
if (given.length !== expected.length || !crypto.timingSafeEqual(given, expected)) return res.sendStatus(401);
```

Check that: verification happens before any side effect; a missing signature header is rejected (not skipped); the signing secret is per-tenant where tenants configure webhooks; timestamps or delivery IDs prevent replay where the provider supplies them. Prefer the provider SDK's verifier (Stripe `constructEvent`, GitHub `X-Hub-Signature-256`, Slack signing secret helper).

## Sensitive data in logs and responses

- Request logging middleware that logs bodies or headers (`morgan('combined')` does not log bodies; custom loggers often do).
- Exceptions returned to clients: Django `DEBUG = True`, Flask `app.run(debug=True)` (Werkzeug debugger is an RCE console), Rails `config.consider_all_requests_local = true` in production, Spring Boot `server.error.include-stacktrace=always`, Laravel `APP_DEBUG=true` (Ignition has had RCE CVEs).
- Exposed management endpoints: Spring Actuator `management.endpoints.web.exposure.include=*` (`/actuator/env`, `/heapdump`), Django debug toolbar, `phpinfo()`, `/debug/pprof` in Go, Laravel Telescope or Horizon without a gate.
- Serializers returning `passwordHash`, `resetToken`, `apiKey`, `mfaSecret` fields.

## Validate without harm

- Exposure: show the file and line and the access path (public repo, client bundle). Inspect a locally built bundle (`rg` over `dist/` or `.next/`) rather than the deployed site.
- Weak randomness: show the generator in source. Do not predict real tokens.
- Crypto misuse: a unit test that encrypts two equal blocks with ECB and shows equal ciphertext, or flips a CBC byte and shows decryption succeeds without integrity failure.
- Webhook bypass: call the handler locally with no signature or a wrong signature and show it processes the dummy event.
- Debug mode: show the setting and the condition that enables it in production config. Do not trigger the debugger on a deployment.

## False-positive traps

| Looks bad | Check before reporting |
|---|---|
| Secret-like string in tests or examples | Placeholder (`sk_test_`, `xxxx`, `changeme` in `.env.example`) and not used in production |
| Firebase `apiKey`, Stripe `pk_live_`, Google Maps browser key, Sentry DSN | Public by design. Report only if restrictions are missing and abuse costs money, as hardening |
| `md5` / `sha1` in code | Used for cache keys, ETags, or non-security checksums. Not a crypto finding |
| `Math.random` | Used for UI jitter or sampling, not tokens |
| `verify=False` in a script under `scripts/` that runs only against localhost | Low or hardening |
| Secret in a private repo's history, already rotated | Ask the owner; mark `needs_validation` for current validity |

## Severity guidance

| Result | Typical severity |
|---|---|
| Production cloud admin keys, database credentials, or signing secrets readable by the public (public repo, client bundle) | Critical |
| Same secrets readable by a broad lower-trust group; webhook signature not verified on a payment or permission-changing event; Werkzeug/Ignition debug console reachable in production config | High to Critical |
| Predictable reset or invite tokens; ECB or unauthenticated encryption of sensitive fields with a realistic ciphertext reader; TLS verification disabled on a production outbound call carrying credentials | Medium to High |
| Weak password hash with no known disclosure path; timing-unsafe comparison; stack traces in errors | Low or hardening note |

Sources: adapted from cloudflare/security-audit-skill (MIT), addyosmani/agent-skills (MIT) and general practice.
