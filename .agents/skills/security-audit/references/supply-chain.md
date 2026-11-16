# Dependencies, CI, and Supply Chain

Open this file when the audit covers dependency manifests and lockfiles, CI/CD workflows, build scripts, container images, release and signing, plugins, or auto-update channels.

## Core rule

A vulnerable or unpinned dependency is not a finding by itself. Show (a) who can influence what gets built or run, (b) which trusted job or runtime consumes it, and (c) what authority follows: code execution in a privileged context, a secret disclosed, or a release published. For a known CVE, show that the vulnerable code is **reachable** in this application.

Do not install packages, run `npm install`, refresh lockfiles, or call registries during an audit. Use only tools and databases already present locally.

## Known-vulnerable dependencies

### Commands (offline or already-installed tools only)

| Ecosystem | Read-only audit | Notes |
|---|---|---|
| npm | `npm audit --omit=dev --json` | Uses the registry advisory API (network). Run only if the user allows network for this |
| pnpm / Yarn | `pnpm audit --prod`, `yarn npm audit -A -R` (Yarn 2+), `yarn audit` (v1) | Network |
| Python | `pip-audit -r requirements.txt` | Network for the advisory DB unless a local cache exists |
| Ruby | `bundle-audit check` (uses a local advisory DB; `--update` fetches) | Offline after DB update |
| Java | OWASP Dependency-Check, `mvn dependency:tree`, `gradle dependencies` | Tree commands are local if dependencies are cached |
| PHP | `composer audit --locked` | Network |
| Go | `govulncheck ./...` | Reports only vulnerabilities in **called** functions; best reachability signal |
| Any | `osv-scanner` or `trivy fs` in their offline-database modes | Check the installed version's flag names; both need a previously downloaded DB |

If network is not authorized, list the lockfile versions of security-sensitive packages and compare them by hand with advisories you already know, marking each as `needs_validation` for an owner-run audit.

### Reachability triage

For each advisory:

1. Is the package in the runtime path, or dev/test only?
2. Is the vulnerable function or feature used? Search for the import and the specific API (for example, `lodash.template` with user input, `jsonwebtoken.verify` with the vulnerable option, `xml2js` with entity expansion).
3. Does lower-trust input reach it?
4. Is the vulnerable version actually installed (lockfile), not just allowed by the manifest range?

Report a reachable, exploitable advisory as a finding with the app's own trace. Report unreachable ones as hardening (upgrade on schedule).

## Dependency source confusion and integrity

| Red flag | Risk |
|---|---|
| No lockfile committed, or CI runs `npm install` / `pip install -r` without hashes instead of `npm ci` / `pip install --require-hashes` | Builds pick up new versions, including malicious ones |
| Internal package names (`@company/utils`, `company-auth`) with a resolver that falls back to the public registry (`--extra-index-url` in pip; npm without a scope registry mapping) | Dependency confusion: attacker publishes the same name publicly with a higher version |
| Git dependencies on a branch (`github:org/repo#main`), `curl \| sh` installers, unpinned tool downloads in Dockerfiles | Mutable inputs |
| Base images by tag (`node:20`) rather than digest | Mutable, but usually hardening unless a lower-trust party controls the tag |
| Postinstall scripts in new or obscure dependencies | Code runs at install time with developer and CI credentials |
| Typosquat-like names (`reqeusts`, `colourama`, `lodahs`) | Malicious package |

Pip `--extra-index-url` is the classic confusion vector: pip picks the highest version across all indexes. `--index-url` to a proxy that controls upstream resolution is safer.

## CI/CD workflows

CI configuration is authorization code. For each workflow, record the trigger, whose code runs, which secrets and token permissions exist, and what the job can publish.

### GitHub Actions red flags

| Pattern | Why it matters |
|---|---|
| `on: pull_request_target` or `workflow_run` **plus** checkout of the PR head (`ref: ${{ github.event.pull_request.head.sha }}`) and then building or running it | Fork code runs with repository secrets and a write token ("pwn request") |
| `${{ github.event.issue.title }}`, `...pull_request.title`, `...head_ref`, `...comment.body` interpolated directly inside `run:` | Script injection; branch names and titles are attacker-controlled |
| `permissions:` absent and repository default is write-all | Over-broad `GITHUB_TOKEN` (default depends on repo/org setting; a `needs_validation` fact if not in source) |
| Third-party actions by tag (`uses: some/action@v1`) rather than full commit SHA | Tag can be moved |
| Self-hosted runners on public repositories | Fork PRs can run code on your infrastructure |
| Caches or artifacts written by PR jobs and restored by release jobs | Cache poisoning across trust levels |
| Secrets echoed or passed as command-line arguments | Exposed in logs or process lists |

```yaml
# Vulnerable: attacker-controlled title runs as shell
- run: echo "Title: ${{ github.event.pull_request.title }}"
# Safe: pass through an environment variable; the shell sees data, not code
- env:
    TITLE: ${{ github.event.pull_request.title }}
  run: echo "Title: $TITLE"
```

Equivalent checks apply to GitLab CI (`rules` for merge requests from forks, protected variables), CircleCI (pass secrets to fork builds setting), Jenkins (`Jenkinsfile` from untrusted branches, script approval), and Buildkite.

Commands:

```bash
rg -n -e 'pull_request_target|workflow_run' .github/workflows
rg -n -e '\$\{\{\s*github\.event\.(issue|pull_request|comment|review|head_commit|commits)' -e 'github\.head_ref' .github/workflows
rg -n -e 'uses:\s*[^@]+@(v?[0-9]|main|master)' .github/workflows
rg -n -e 'permissions:' .github/workflows
```

If installed, `zizmor` and `actionlint` analyze workflows offline.

## Release, signing, and updates

- Artifacts promoted by mutable name or tag rather than the digest that was tested.
- Signatures checked but not bound to the expected signer identity, repository, or workflow.
- Auto-updaters that verify payload bytes but not version (rollback), channel, or platform; updaters fetching over HTTP or with TLS verification disabled.
- Plugin or extension systems that run install hooks before checking publisher identity.

## Validate without harm

- Workflow injection: show the trigger, the interpolation, and the secrets in scope from the YAML. Do not open pull requests or issues on the real repository to test it.
- Dependency confusion: show the resolver configuration and that the internal name is unregistered or resolvable publicly **from documentation or a lockfile**, not by publishing a package.
- Reachable CVE: a local unit test that drives the vulnerable API with the app's own call path and a harmless input.

## False-positive traps

| Looks bad | Check before reporting |
|---|---|
| Critical advisory in a dev dependency | Build-time only; exploitable only if lower-trust input reaches the build. Usually hardening |
| `pull_request_target` workflow | Safe if it never checks out or runs PR code (labeling, commenting) |
| Unpinned action from `actions/*` | First-party; still better pinned, but hardening |
| ReDoS advisory in a parser fed only trusted config | Not reachable |
| `latest` image tag | Hardening unless lower-trust actors control the registry tag |

## Severity guidance

| Result | Typical severity |
|---|---|
| Fork PR can run code with release or cloud secrets; dependency confusion on a name the build resolves publicly | Critical |
| Reachable, exploitable dependency RCE or auth bypass in production code; workflow script injection reachable by any GitHub user with write-scoped token | High |
| Reachable dependency bug with limited impact (DoS on an authenticated route); cache poisoning needing maintainer interaction | Medium |
| Unreachable advisories, tag-pinned actions, missing `permissions:` with no exploitable path | Low or hardening note |

Sources: adapted from cloudflare/security-audit-skill (MIT), addyosmani/agent-skills (MIT) and general practice.
