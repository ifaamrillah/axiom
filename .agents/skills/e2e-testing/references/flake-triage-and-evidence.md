# E2E Flake Triage and Evidence

Open this when an end-to-end test fails intermittently, when a CI run fails and you need to know why, or when you must attach proof that a UI change works.

## Triage a failing E2E test

1. **Get the artifacts first.** Download the HTML report, `trace.zip`, screenshot, and video for the failing attempt. Do not rerun before looking; a rerun that passes destroys nothing but also explains nothing.
2. **Open the trace.** `npx playwright show-trace path/to/trace.zip` (or drag it into trace.playwright.dev, which runs locally in the browser). Read, in order:
   - The failing action and its error (timeout, strict-mode violation, detached element, assertion mismatch).
   - The DOM snapshot before and after the failing action. Was the target there? Covered by an overlay? Disabled?
   - The network tab around that time: a 4xx/5xx, a slow request, a request that never fired.
   - The console tab: uncaught exceptions, hydration errors, failed asset loads.
3. **Reproduce the rate locally.**
   ```sh
   npx playwright test -g "renames a project" --repeat-each=30 --workers=1
   npx playwright test -g "renames a project" --repeat-each=30 --workers=4   # parallel-only?
   ```
4. **Classify** with the table below and fix the cause.
5. **Prove the fix** with the same repeat command. Report before and after (for example, "4/30 to 0/30 at 4 workers").

## Flake causes and fixes

| Symptom in trace or error | Cause | Fix |
|---|---|---|
| `Timeout ... waiting for locator` while element is visible in the after-snapshot | Assertion read once (`isVisible()`, `textContent()`) | Use a web-first assertion (`toBeVisible`, `toHaveText`) |
| `strict mode violation: resolved to 2 elements` | Ambiguous locator | Scope it (`within row`, `filter({ hasText })`) or use `exact: true` |
| Click lands on wrong element or "intercepts pointer events" | Overlay, toast, cookie banner, or animation | Wait for overlay to hide; dismiss banner in a fixture; disable animations in test config |
| Element detached from DOM | Re-render between locate and act | Use locators (lazy), not stored element handles |
| Passes alone, fails in parallel | Shared account or data across workers | Unique data per test; per-worker accounts |
| Fails only on first test after deploy | Cold start, lazy compilation | `webServer` health check URL; warm-up in global setup |
| Date or count differs | Real clock, data from other tests | `page.clock`; isolated data |
| Request to third party fails or slows | Real external dependency | `page.route` stub |
| Hydration error in console, then click ignored | Clicking before the SPA is interactive | Assert an interactive-ready signal (enabled button, app-ready marker) before acting |
| Fails only in WebKit or Firefox | Real browser difference or unsupported API | Investigate as a product bug first |

Do not "fix" with `waitForTimeout`, higher global timeouts, `force: true` clicks, or more retries. Each hides a real cause; `force: true` also skips the actionability checks that model a real user.

## Evidence capture

| Evidence | When | How |
|---|---|---|
| Assertion per checkpoint | Always | Web-first `expect` in the spec |
| Screenshot of final state | Every UI change | `await page.screenshot({ path: 'evidence/settings-after.png', fullPage: true })` or `playwright-cli screenshot --filename=...` |
| Before screenshot | UI fixes (show the bug) | Same, captured on the base branch or before the fix |
| Trace | Failures, new flows, flake triage | `trace: 'on-first-retry'` in config; `--trace on` for one run; `playwright-cli tracing-start` / `tracing-stop` |
| Video | Flows hard to judge from stills (animations, multi-step) | `video: 'retain-on-failure'`; `playwright-cli video-start` / `video-stop` |
| Accessibility snapshot | Structure checks; cheap text evidence | `await expect(locator).toMatchAriaSnapshot(...)`; `playwright-cli snapshot --filename=...` |
| Visual regression | Pixel-stable components only | `await expect(page).toHaveScreenshot()`; mask dynamic regions; generate baselines in the CI image |

Rules:

- Name evidence by journey and state (`checkout-before.png`, `checkout-after.png`), and list the paths in the report.
- Check screenshots for secrets, personal data, and tokens before attaching them anywhere.
- Traces include network bodies and storage. Treat them as sensitive; do not publish traces from accounts with real data.
- Visual baselines differ across OS and fonts. Generate and compare them in the same container image.
- A screenshot is evidence of a state, not of behavior. Pair it with the assertion that checked the state.

## Reporting template

```
Journey: member renames project from settings
Command: PLAYWRIGHT_HTML_OPEN=never npx playwright test tests/settings.spec.ts --project=chromium
Result: 3 passed, 0 flaky, 0 failed (14.2s)
Flake check: --repeat-each=20 --workers=4 -> 20/20 passed
Evidence: evidence/settings-before.png, evidence/settings-after.png, test-results/.../trace.zip
Not covered: Firefox and WebKit projects not run locally; CI runs them
```

Sources: adapted from microsoft/playwright-cli (Apache-2.0) skills/playwright-cli/references/tracing.md and references/video-recording.md, addyosmani/agent-skills (MIT) skills/browser-testing-with-devtools/SKILL.md, and general practice.
