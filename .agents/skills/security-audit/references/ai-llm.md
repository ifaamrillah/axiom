# AI and LLM Features

Open this file when the application calls a language model and does something with the output: renders it, stores it, passes it to tools, or retrieves data for it. The questions to ask live in the "AI and LLM features" section of the [attack-surface checklists](attack-surfaces.md). This file gives the trust model, sinks, harmless validation, traps, and severity. For agent harness configuration (hooks, MCP configs, allowlists), use [agent configuration](agent-config.md).

## Trust model

Treat model output as **controlled by the least-trusted content in its context**. If a document, web page, email, ticket, tool result, or another user's message can reach the prompt, its author can steer the output. The system prompt is not a control. The model is not a security boundary.

So the boundary that matters sits in code: between the model's output and every sink, and between the end user's identity and every tool call.

## Sinks

| Model output reaches | Class | Safe pattern |
|---|---|---|
| HTML or Markdown rendered to a user | XSS; data exfiltration through image or link URLs that carry context data in the query string | Render as text, or sanitize; allowlist image and link hosts; no auto-loading of remote images in rendered output |
| SQL, shell, `eval`, a code interpreter | Injection or code execution (see [injection](injection.md)) | Parameterized queries with model values as data; a sandbox with no network and no secrets for generated code |
| File paths | Path traversal (see [files and deserialization](files-and-deserialization.md)) | Resolve and check containment, as for user input |
| URLs the server fetches | SSRF (see [SSRF](ssrf.md)) | The same egress controls as for user URLs |
| Tool arguments that select a resource (user ID, tenant ID, document ID, recipient) | Authorization bypass, cross-tenant access | The tool checks the **end user's** identity and scope in code; it never trusts an ID the model chose |
| Tools that send data out (email, HTTP fetch, webhooks, link unfurling, file share) | Data exfiltration | Allowlisted destinations; confirmation bound to the exact recipient and content |
| Destructive or irreversible tools | Unauthorized action | Confirmation bound to the exact action and arguments, shown to the user before it runs |
| Memory, shared documents, or a retrieval index another user's session reads | Stored prompt injection, cross-user leakage | Per-user or per-tenant memory and indexes; retrieval filtered by the requester's permissions before ranking |

## Search commands

```bash
rg -n -e 'openai|anthropic|ChatCompletion|messages\.create|generateText|streamText|invoke\(|LLMChain|ChatModel' -l
rg -n -e 'tools\s*[:=]|tool_choice|function_call|@tool|registerTool|tool\(' -l
rg -n -e 'dangerouslySetInnerHTML|v-html|innerHTML|marked\(|markdown-it|remark|ReactMarkdown' -l
rg -n -e 'similarity_search|vector|embedding|retriever|index\.query' -l
```

## Harmless validation

- You rarely need the model. Treat its output as attacker-chosen and call the sink or tool handler directly in a unit test with the argument an attacker would pick. Example: call the "read document" tool as user A with user B's document ID on a local instance; if it returns B's dummy document, the authorization gap is shown without any model call.
- Rendering: feed the renderer a Markdown image whose URL points to a local canary and check that the output would load it.
- Retrieval: index dummy documents for two tenants locally and query as tenant A.
- A live model run spends quota and needs the user's approval. Use a benign marker instruction, dummy data, no network, and no real credentials.

## False-positive traps

| Looks bad | Check before reporting |
|---|---|
| The model can be talked into saying something harmful | Content safety, not a crossed trust boundary, unless the output reaches a sink or another user |
| The system prompt can be extracted | Not a finding unless the prompt contains secrets or authorization logic that should have been in code |
| Prompt injection is possible | Needs an authority path: a tool, a sink, or another user who sees the result. Injection that only affects the injecting user's own session is self-impact |
| The model hallucinates wrong answers | Quality, not security, unless code acts on the answer as an authorization decision |
| A tool has broad power | Check whether the handler enforces the end user's scope in code. If it does, the breadth is a hardening note |

## Severity guidance

| Result | Typical severity |
|---|---|
| Content from an outsider makes the agent run code, or read and send another tenant's data, without confirmation | High to Critical |
| Model-chosen IDs read another user's records through a tool with no scope check | High (the same as the IDOR it is) |
| Stored injection in shared memory or documents that steers other users' sessions toward a sink | Medium to High, by the sink |
| Markdown image exfiltration of the current user's own context, needing injected content in that context | Medium |
| System prompt disclosure with no secrets | Hardening note |

Fix pattern: enforce authorization in tool code on the end user's identity, treat model output as untrusted input at every sink, scope memory and retrieval per user or tenant, and bind confirmation to the exact action and arguments.

Sources: class from cloudflare/security-audit-skill (MIT), rewritten; general practice.
