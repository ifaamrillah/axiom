# Agent Configuration as Attack Surface

Open this file when the target contains configuration for coding agents or agent harnesses: hook definitions, MCP server configs, permission allowlists, instruction files, installed skills or plugins, or CI jobs that run an agent. These files are executable or steer an executor. Treat a change to them like a change to a build script.

## Principals and boundaries

| Lower-trust principal | What it controls | Boundary at risk |
|---|---|---|
| Pull-request author or outside contributor | Committed agent config, instruction files, any file an agent reads | Code execution on a maintainer's machine or CI runner |
| Author of a third-party skill, plugin, or MCP server | Scripts, hooks, and tool code that run with the user's authority | The user's files, credentials, and network |
| Author of content an agent reads (issue, web page, document, dependency README, tool output) | Text in the model context | Tool calls the agent makes with someone else's authority |
| The agent itself, after it reads injected text | Tool arguments | Every permission the harness grants without confirmation |

## Where to look

Find these by name, then read the effective configuration in precedence order (organization, user, project, local). Host-specific file names and precedence rules belong to each host's documentation; record which host and version you assumed.

- Project-level agent settings and local overrides (for example `.claude/settings.json`, `.codex/config.toml`, `opencode.json`), and whether version control ignores the local ones.
- MCP server definitions (for example `.mcp.json` or an `mcpServers` block).
- Instruction files: `AGENTS.md`, `CLAUDE.md`, `GEMINI.md`, rules directories, Copilot instructions.
- Skill and plugin folders (`SKILL.md` plus `scripts/`), plugin manifests, and marketplace sources.
- CI workflows that start an agent, and the events that trigger them.

## Surfaces and when each becomes a finding

| Surface | Inspect | Finding when | Not a finding |
|---|---|---|---|
| Hooks that run shell commands | The command string, which event fires it, and what data it interpolates | The hook puts untrusted data (tool input, file names, branch names, model text) into a shell string; or a committed hook runs for every contributor without a trust prompt from the host | A hook the developer wrote for themselves in an ignored local file (same principal) |
| MCP server configs | `command`, `args`, `env`, URL, transport, and auth | Unpinned packages fetched at start (`npx pkg@latest`, `uvx` without a version) from a name an outsider could take; tokens inline in a committed file; a remote server over plain HTTP or without client auth; one shared high-privilege credential used for all users | A pinned, locally built server with read-only scope |
| Permission allowlists and deny lists | Wildcards, network rules, write scope outside the workspace | A committed allowlist lets the agent run any shell command, fetch any domain, or write outside the workspace without confirmation; a deny list that alternate commands bypass is relied on as a control | An allowlist of read-only commands |
| Auto-approve and bypass modes | Settings or CLI flags that skip confirmations, in committed config and CI | Confirmations are off where the agent also reads lower-trust content and holds write tokens or secrets | Bypass mode inside a disposable sandbox with no secrets and no network |
| Secrets in instruction files | Tokens, passwords, internal URLs with credentials in `AGENTS.md`, `CLAUDE.md`, rules, or skills | Any real secret. These files go to model providers and into transcripts. Handle as in [secrets and crypto](secrets-and-crypto.md) | Placeholder values and variable names |
| Skills and plugins from untrusted sources | Provenance, pinning (commit SHA, not a branch), bundled scripts, hooks the plugin installs | Code from an unpinned or unreviewed source runs on invocation or at session start with the user's authority | Instruction-only skills from a pinned, reviewed source |
| Prompt injection through repository files | Hidden instructions in READMEs, code comments, HTML comments, issue templates, fixtures, zero-width or bidirectional characters | An agent with tool authority reads that content in an automated or low-attention flow (CI review bot, auto-triage, scheduled agent) and can act on it without a human confirming the exact action | Injected text that only reaches an agent with no tools, whose output goes back to the same user |
| CI agents | Trigger events, token permissions, secrets in the job, write-back steps | A lower-trust event (issue comment, PR from a fork, `pull_request_target`) starts an agent that holds repository write access or secrets. See [supply chain](supply-chain.md) | Agents on trusted events with read-only tokens |

Instructions in a prompt or instruction file are not a control. "Never run destructive commands" in `AGENTS.md` does not stop an agent; the permission system does. Report the missing technical control, not the wording.

## Harmless validation

- Static first. Read the files and state the effective configuration with file:line for each setting.
- Never execute the target's hooks, start its MCP servers, or install its skills or plugins on your own machine. Never use a token you found.
- If execution is needed, use the sandbox from `SKILL.md`. Replace the hook or server command with a canary (`touch $SCRATCH/marker`) and show that the event fires it.
- For an injection path, show the chain in source: where the content enters, which agent reads it, which tool it can call, and that no confirmation is bound to that call. Running a live model to prove the injection spends quota and needs the user's approval. Use a benign marker instruction, a sandboxed agent with no network, and dummy credentials.
- Whether a host asks for trust before it runs project hooks or MCP servers is host behavior. If source and the host's documentation do not settle it, the candidate is `needs_validation`, naming the host and version.

## Severity guidance

| Result | Typical severity |
|---|---|
| A lower-trust CI event drives an agent that holds repository write tokens or release secrets | High to Critical |
| A committed hook or MCP server runs attacker code on a contributor's machine with no trust prompt | High |
| A real secret in an instruction file | By the secret's power (see secrets and crypto) |
| Unpinned MCP package or skill source, no evidence of takeover | Hardening note, or Medium if the name is unclaimed and anyone could register it |
| A broad committed allowlist with no lower-trust content path | Hardening note |

Fix pattern: pin every executable source, keep secrets in the host's secret store, scope tokens per user and per task, require confirmation bound to the exact action and arguments for writes and network calls, and run agents on lower-trust input with no secrets and read-only tokens.

Sources: idea from affaan-m/ECC (agent configuration as attack surface; MIT), rewritten; general practice.
