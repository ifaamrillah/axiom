# Browser Automation

Browser automation can verify a user journey or rendered UI when the project and host provide it. It is optional and may have access to live data. Use a safe local/test environment, test-owned accounts, and bounded journeys.

## Choose an interface

For repeatable, bounded browser checks, prefer a concise CLI already available in the project or host when its commands cover the required interaction and evidence. For example, Microsoft's [playwright-cli](https://github.com/microsoft/playwright-cli) offers agent-oriented browser commands and named sessions. Use native browser tools when they provide needed visual inspection or richer page-state exploration. Do not install a new dependency solely because this guide names an option.

Keep each session and target environment explicit. Capture relevant screenshots or other observations, verify the expected user-visible result, and close or clean up test sessions when appropriate. Never use a real user's authenticated session or production data unless specifically authorized.

If browser automation is unavailable, use integration tests or a manual checklist and label reduced coverage.
