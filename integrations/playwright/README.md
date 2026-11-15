# Browser Automation

Optional. Browser automation verifies user journeys and rendered UI. It can reach live data, so use only a local or test environment, test-owned accounts, and bounded journeys. Without it, use integration tests or a manual checklist and label the reduced coverage.

*Status: guidance checked against upstream documentation on 2026-11-16. Axiom has not run these tools in a live session here.*

## Choosing a tool

| Option | Best for | Notes |
|---|---|---|
| Project's own suite (`@playwright/test`, Cypress, …) | Durable regression coverage | Use first when it exists; run it with the project's scripts |
| Playwright CLI (`@playwright/cli`, `playwright-cli`) | Agent-driven exploration and evidence | Concise commands and element refs keep page data out of the context; ships a skill installable via `playwright-cli install --skills` |
| Playwright MCP server | Long, stateful, exploratory loops | Richer introspection with a higher token cost per step |
| Host built-in browser | Quick visual checks | Capabilities and permissions vary by host |

## Agent workflow with a CLI (example)

```sh
playwright-cli open http://localhost:3000/settings   # local or test environment only
playwright-cli snapshot                              # accessibility snapshot with element refs
playwright-cli fill e7 "New name" --submit           # act by ref
playwright-cli screenshot --filename=settings-after.png
playwright-cli close
```

Patterns:

- **Snapshot before acting.** Use refs from the latest snapshot. Take a new snapshot after navigation.
- **Test accounts:** save storage state once for a test-owned account, then reuse it. Never store real credentials in the repository.
- **Determinism:** mock unstable third-party requests at the network layer. Seed data through fixtures.
- **Failures:** capture a trace or video, and link it in the report.
- **Promote to tests:** convert valuable exploratory journeys into specs in the project's suite.

## Evidence in pull requests

Recent GitHub CLI versions can attach local images and videos to PRs and issues (`gh pr create --attach <file>`, `gh pr comment --attach <file>`). Check `gh --version` and `gh pr create --help` before relying on it. Otherwise, upload through the web UI or link CI artifacts. Attach evidence for user-visible changes only.

## Safety

Do not automate production accounts, payments, or messages to real people. Do not enter real credentials on behalf of the user. Clean up only test-owned data.

## References

- [Playwright CLI](https://github.com/microsoft/playwright-cli)
- [Playwright test docs](https://playwright.dev/docs/intro)
