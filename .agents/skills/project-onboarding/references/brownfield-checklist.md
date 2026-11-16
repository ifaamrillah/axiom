# Brownfield Onboarding Checklist

Existing systems carry history: workarounds, half-finished migrations, docs that describe an older design. Document the system as it is, not as it should be. Record debt and drift as findings.

## Choose the depth

| Depth | When | Effort | Output |
|---|---|---|---|
| Quick | Small repo, or one well-scoped task coming | Manifests, entry points, CI, one traced flow | overview, tech-stack, development-guide |
| Focused | Large repo, known upcoming change area | Quick scan plus deep reading of the affected modules and their neighbors | Full set, module cards only for the change area |
| Deep | First adoption on a critical system, or audit | Every deployable, every module boundary, data model, integrations | Full set with module cards for all major modules |

Default to Focused when the user named a goal. Ask what is coming next if it is unclear; it decides where to go deep.

## Checklist

### Instructions and history
- [ ] Root and nested agent instructions (`AGENTS.md`, `CLAUDE.md`, `.cursor/rules`, `.github/copilot-instructions.md`), `CONTRIBUTING.md`
- [ ] `git log --oneline -n 30`, active branches, last release tag (`git describe --tags --abbrev=0`)
- [ ] Hot spots: most-changed files in the last 6 months
- [ ] Existing ADRs or design docs, with dates

### Stack and runtime
- [ ] Manifests and lockfiles; declared runtime versions
- [ ] Observed runtime versions on this machine
- [ ] Monorepo layout and package boundaries
- [ ] Mixed stacks (for example a legacy PHP app beside a new Node service)

### Architecture
- [ ] Deployables and how each starts (Dockerfile, Procfile, manifests)
- [ ] Module map and dependency direction; layering violations noted
- [ ] One traced request flow and one traced background flow with `path:line`
- [ ] Persistence: databases, schema source (`schema.rb`, migrations, ORM models), caches, file storage
- [ ] External integrations: payment, email, auth providers, queues, third-party APIs
- [ ] Auth and authorization boundary: where identity is established and checked

### Workflow
- [ ] Setup, run, test, lint, type check, build commands with evidence levels ([verifying commands](verifying-commands.md))
- [ ] Test layers and rough counts; known flaky or skipped tests
- [ ] CI stages and required checks
- [ ] Release and deploy process (who, how, where documented)
- [ ] Environments and config sources (`.env.example`, config directories); never copy values

### Reality checks
- [ ] Docs vs code drift (README commands, architecture diagrams, API docs)
- [ ] Workarounds and hacks: `rg -n 'HACK|FIXME|XXX|workaround|temporary' --glob '!vendor/**'`
- [ ] Dead or duplicate code paths; feature flags left on or off permanently
- [ ] Half-finished migrations: two ORMs, two HTTP clients, old and new module side by side
- [ ] Pinned or very old dependencies; known EOL runtimes
- [ ] Generated code and its generator (do not hand-edit generated files)

### Risk register
- [ ] Security-sensitive areas (auth, payments, PII, file upload, raw SQL, deserialization)
- [ ] Areas with no tests
- [ ] Single points of failure and operational constraints (cron on one host, manual steps)
- [ ] Unknowns you could not resolve, and what would resolve them

## Recording debt and drift

Use one line per finding with evidence and impact:

```markdown
| Finding | Evidence | Impact |
|---|---|---|
| Two HTTP clients (axios and got) | src/clients/*.ts | New code: use axios (12 of 14 call sites) |
| README says MySQL; code uses Postgres | README.md:22 vs config/database.yml:4 | README is wrong; drift recorded |
| Orders export runs only on host `worker-1` cron | deploy/crontab:3 | Fails silently if host is replaced |
```

Do not fix drift during onboarding unless asked. Record it and propose the correction.

## Exit criteria

- Each checklist item is done, marked not applicable, or listed as an unexamined area.
- The next agent can run tests and find where the upcoming change lives without searching again.

Sources: ideas from bmad-code-org/BMAD-METHOD document-project (brownfield scan levels), and general practice.
