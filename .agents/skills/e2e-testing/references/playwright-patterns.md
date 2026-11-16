# Playwright Test Patterns (with Cypress Notes)

Open this when writing or fixing specs in `@playwright/test` or Cypress: choosing locators, waiting, reusing login, isolating test data, and configuring CI.

## Locator strategy

Pick the first row that works. Locators that match what a user perceives survive redesigns; locators tied to DOM structure do not.

| Priority | Playwright | Cypress (with Testing Library) | Use for | Breaks when |
|---|---|---|---|---|
| 1 | `getByRole('button', { name: 'Save' })` | `cy.findByRole('button', { name: 'Save' })` | Buttons, links, inputs, headings, dialogs | Accessible name changes (usually a real change) |
| 2 | `getByLabel('Email')` | `cy.findByLabelText('Email')` | Form fields | Label text changes |
| 3 | `getByPlaceholder('Search')` | `cy.findByPlaceholderText(...)` | Fields with no label (fix the label too) | Placeholder copy changes |
| 4 | `getByText('Order placed')` | `cy.contains('Order placed')` | Static text, messages | Copy changes, translations |
| 5 | `getByTestId('cart-total')` | `cy.get('[data-testid="cart-total"]')` (or `data-cy`) | No accessible handle; dynamic values | Rarely; IDs are contracts |
| Avoid | `locator('div > ul li:nth-child(3) .btn')` | `cy.get('.css-1x2y3z')` | Never in durable tests | Any layout or styling change |
| Avoid | XPath by position | `cy.get('button').eq(2)` | Never | Any reorder |

Rules:

- Scope before you match: `page.getByRole('row').filter({ hasText: 'Invoice #42' }).getByRole('button', { name: 'Pay' })`.
- If no good locator exists, the element is probably inaccessible. Add a label or role in the app; that fixes a real accessibility bug.
- Use `exact: true` or a regex anchored with `^...$` when names overlap (`Save` and `Save draft`).
- Configure the test ID attribute once if the project uses another name: `use: { testIdAttribute: 'data-cy' }`.
- With playwright-cli, `generate-locator <ref>` prints the locator Playwright would use for a snapshot ref.

## Waiting strategy

Playwright actions auto-wait for the element to be attached, visible, stable, enabled, and receiving events. Web-first assertions retry until a timeout. Use them; do not add your own sleeps.

| Need | Do | Do not |
|---|---|---|
| Element appears | `await expect(locator).toBeVisible()` | `await page.waitForTimeout(2000)` |
| Text updates | `await expect(locator).toHaveText('3 items')` | `expect(await locator.textContent()).toBe(...)` (no retry) |
| Navigation done | `await expect(page).toHaveURL(/\/orders\/\d+/)` | `waitForNavigation` around a click (deprecated pattern) |
| Network call finished | `const resp = page.waitForResponse('**/api/orders'); await click; await resp;` | Waiting for `networkidle` (unreliable with polling or websockets) |
| Spinner gone | `await expect(page.getByRole('progressbar')).toBeHidden()` | Checking `count() === 0` once |
| Element count | `await expect(rows).toHaveCount(5)` | `expect(await rows.count()).toBe(5)` |
| Polled non-DOM value | `await expect.poll(() => api.getStatus(id)).toBe('done')` | Loop with sleep |

Cypress equivalents: commands and `.should()` retry automatically. Use `cy.intercept('GET', '/api/orders').as('orders'); cy.wait('@orders')` for network. Never use `cy.wait(2000)`.

Anti-pattern: reading a value with `textContent()`, `isVisible()`, or `count()` and then asserting it with a plain `expect`. These read once and do not retry.

## Authentication and session reuse

Log in through the UI once per role, save the browser storage state, and reuse it. Test the login form itself in one dedicated spec.

```ts
// playwright.config.ts
export default defineConfig({
  projects: [
    { name: 'setup', testMatch: /auth\.setup\.ts/ },
    {
      name: 'chromium',
      use: { ...devices['Desktop Chrome'], storageState: 'playwright/.auth/user.json' },
      dependencies: ['setup'],
    },
  ],
});

// tests/auth.setup.ts
import { test as setup, expect } from '@playwright/test';
setup('authenticate as member', async ({ page }) => {
  await page.goto('/login');
  await page.getByLabel('Email').fill(process.env.E2E_USER_EMAIL!);
  await page.getByLabel('Password').fill(process.env.E2E_USER_PASSWORD!);
  await page.getByRole('button', { name: 'Sign in' }).click();
  await expect(page.getByRole('navigation', { name: 'Main' })).toBeVisible();
  await page.context().storageState({ path: 'playwright/.auth/user.json' });
});
```

- Add `playwright/.auth/` to `.gitignore`. Storage state contains session cookies.
- Credentials come from environment variables or CI secrets for test-owned accounts. Never hard-code them; never use a real person's account.
- Faster option: authenticate through the API (`request.post('/api/login')`) and save `request.storageState()`.
- Multiple roles: one storage file per role (`admin.json`, `member.json`); use `test.use({ storageState: ... })` per file or describe block.
- Tests that change account state (password, MFA, deletion) need their own throwaway account, not the shared one.
- Cypress: `cy.session(['member'], () => { /* login */ }, { validate() { cy.getCookie('sid').should('exist') } })`.

## Test data and isolation

Each test must pass alone, in any order, and in parallel.

- **Create data through the API or a seed endpoint, not the UI**, in a fixture. Drive the UI only for the behavior under test.
- **Use unique values** per test: `const name = \`proj-${test.info().workerIndex}-${Date.now()}\``.
- **Clean up what you create** in fixture teardown, by ID. Never truncate shared tables in a shared environment.
- **Do not depend on data another test created.** No "test 2 edits the project test 1 made."
- **Stub unstable third parties** at the network layer: `await page.route('**/api.stripe.com/**', r => r.fulfill({ json: fixture }))`. Keep your own backend real.
- **Freeze time** when the UI shows dates: `await page.clock.setFixedTime(new Date('2024-02-01T10:00:00Z'))`.

```ts
// tests/fixtures.ts
import { test as base } from '@playwright/test';
export const test = base.extend<{ project: { id: string; name: string } }>({
  project: async ({ request }, use, testInfo) => {
    const name = `proj-${testInfo.workerIndex}-${Date.now()}`;
    const res = await request.post('/api/projects', { data: { name } });
    const project = await res.json();
    await use(project);
    await request.delete(`/api/projects/${project.id}`);
  },
});
export { expect } from '@playwright/test';
```

## A well-formed spec

```ts
import { test, expect } from './fixtures';

test('member renames a project from settings', async ({ page, project }) => {
  await page.goto(`/projects/${project.id}/settings`);
  await page.getByLabel('Project name').fill('Renamed');
  await page.getByRole('button', { name: 'Save' }).click();
  await expect(page.getByRole('status')).toHaveText('Saved');
  await page.reload();                                         // proves persistence
  await expect(page.getByLabel('Project name')).toHaveValue('Renamed');
});
```

One journey per test, named for the user outcome. Assert the outcome a user would see, and persistence where it matters.

## CI configuration

```ts
// playwright.config.ts (relevant parts)
export default defineConfig({
  forbidOnly: !!process.env.CI,                  // fail if .only is committed
  retries: process.env.CI ? 2 : 0,               // retries surface flakes; they are not a fix
  workers: process.env.CI ? 2 : undefined,
  reporter: process.env.CI ? [['html', { open: 'never' }], ['github']] : 'list',
  use: {
    baseURL: process.env.BASE_URL ?? 'http://localhost:3000',
    trace: 'on-first-retry',
    screenshot: 'only-on-failure',
    video: 'retain-on-failure',
  },
  webServer: {
    command: 'npm run start:test',
    url: 'http://localhost:3000/health',
    reuseExistingServer: !process.env.CI,
    timeout: 120_000,
  },
});
```

```yaml
# .github/workflows/e2e.yml (job steps)
- run: npm ci
- run: npx playwright install --with-deps chromium
- run: npx playwright test
  env: { CI: 'true', E2E_USER_EMAIL: '${{ secrets.E2E_USER_EMAIL }}', E2E_USER_PASSWORD: '${{ secrets.E2E_USER_PASSWORD }}' }
- uses: actions/upload-artifact@v4
  if: ${{ !cancelled() }}
  with: { name: playwright-report, path: playwright-report/, retention-days: 14 }
```

- Treat a test that passed only on retry as flaky (Playwright marks it "flaky" in the report). Triage it; see [flake triage and evidence](flake-triage-and-evidence.md).
- Shard large suites: `npx playwright test --shard=1/4`, then merge blob reports with `npx playwright merge-reports`.
- Pin the Playwright version in `package.json` and install matching browsers in CI.
- Run locally without opening the HTML report: `PLAYWRIGHT_HTML_OPEN=never npx playwright test`.

## Useful commands

```sh
npx playwright test tests/settings.spec.ts             # one file
npx playwright test -g "renames a project"             # by title
npx playwright test --project=chromium --headed        # watch it run
npx playwright test --repeat-each=20 --workers=1 -g "renames"   # flake check
npx playwright test --last-failed
npx playwright show-trace test-results/<test>/trace.zip
npx playwright codegen http://localhost:3000            # record locators
npx cypress run --spec cypress/e2e/settings.cy.ts --browser chrome
```

Sources: adapted from microsoft/playwright-cli (Apache-2.0) skills/playwright-cli/SKILL.md, references/storage-state.md, references/test-generation.md, references/playwright-tests.md, addyosmani/agent-skills (MIT) references/testing-patterns.md, and general practice.
