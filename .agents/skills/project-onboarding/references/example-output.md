# Worked Example: Onboarding Output

An illustrative onboarding of a fictional Laravel + Vue repository, `acme-clinic`. The paths, versions, and counts are examples of the expected shape, not real data. Compare the good and bad versions.

## Bad: generic and unverified

```markdown
# Overview
Acme Clinic is a modern, scalable web application built with best practices.

## Tech stack
Laravel, Vue, MySQL.

## Commands
- `npm run dev`
- `php artisan test`

## Conventions
Follows SOLID and clean architecture.
```

Problems: no versions or sources; "MySQL" not checked; commands not verified; conventions are generic claims; no metadata; no unknowns.

## Good: `.axiom/project/overview.md`

```markdown
---
status: active
sources: [composer.json, package.json, routes/, app/, docker-compose.yml]
verified_at_commit: 3f9c2e1
verified_on: 2026-11-16
---

# Overview

Appointment booking for small clinics. Patients book online; staff manage
schedules in an admin panel. One Laravel app serves both the API and the
Vue admin SPA; a queue worker sends reminders.

## Deployables
| Process | Start | Evidence |
|---|---|---|
| Web (PHP-FPM) | public/index.php | docker-compose.yml:8 |
| Queue worker | php artisan queue:work redis | docker-compose.yml:22 |
| Scheduler | php artisan schedule:run (cron) | deploy/crontab:1 |

## Layout
| Path | Holds |
|---|---|
| app/Domain/Booking | Booking rules, slot calculation |
| app/Http/Controllers/Api | JSON API for the SPA and mobile app |
| resources/js | Vue 3 admin SPA (Vite) |
| database/migrations | 84 migrations; schema source of truth |

Start reading at routes/api.php, then app/Domain/Booking/BookingService.php.
```

## Good: `.axiom/project/tech-stack.md` (excerpt)

```markdown
| Component | Version | Declared in | Observed |
|---|---|---|---|
| PHP | ^8.2 | composer.json:6 | 8.3.4 (php -v) |
| Laravel | 11.x | composer.lock | — |
| Node | 20 | .nvmrc:1 | 20.11.1 |
| Database | PostgreSQL 15 | docker-compose.yml:31 | — (README says MySQL: drift) |
| Queue | Redis 7 | docker-compose.yml:40, config/queue.php:12 | — |
```

## Good: `.axiom/project/conventions.md` (excerpt)

```markdown
- Controllers stay thin and call a Domain service.
  Example: app/Http/Controllers/Api/BookingController.php:30 → BookingService::book().
  Exception: app/Http/Controllers/Api/LegacyReportController.php queries the DB directly.
- Validation lives in FormRequest classes (app/Http/Requests/*). 31 of 33 endpoints follow this.
- Money stored as integer cents (`amount_cents` columns); see app/Support/Money.php.
- Tests: Pest; feature tests hit the API with RefreshDatabase (tests/Feature/*).
```

## Good: onboarding report (returned to the user)

```markdown
## Onboarding: acme-clinic @ 3f9c2e1 (Focused: booking module)

Created: .axiom/project/{overview,tech-stack,architecture,conventions,development-guide,glossary}.md
Linked, not duplicated: CONTRIBUTING.md (commit rules), docs/adr/ (6 ADRs)

Verified commands: composer install, php artisan test (212 passed, 2 failed: baseline),
npm ci, npm run build. CI-evidenced only: npm run test:e2e.

Drift: README says MySQL; docker-compose and config use PostgreSQL.
Risks: reminder job has no retry limit (app/Jobs/SendReminder.php:18);
payments module has no tests.
Not examined: app/Domain/Billing, resources/js/legacy.
Next: confirm DB with the team; then proceed with the booking change.
```

Sources: general practice.
