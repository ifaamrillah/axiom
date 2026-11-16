# Entry-Point Maps by Ecosystem

Start from the manifest, find the process entry, then the routing or command layer. Confirm each entry in the files; do not assume a framework's default layout. Monorepos repeat this per package or service (look for `pnpm-workspace.yaml`, `turbo.json`, `nx.json`, `lerna.json`, Go workspaces `go.work`, Maven modules, Gradle `settings.gradle*`, Cargo workspaces).

## Node / TypeScript

| Look at | What it tells you |
|---|---|
| `package.json` `main`, `module`, `exports`, `bin` | Library and CLI entries |
| `package.json` `scripts` (`dev`, `start`, `build`, `test`) | Real commands and the entry file they run |
| `.nvmrc`, `engines`, `packageManager`, lockfile type | Runtime and package manager (`package-lock.json` npm, `pnpm-lock.yaml` pnpm, `yarn.lock` yarn, `bun.lockb` bun) |
| `tsconfig.json` `paths`, `baseUrl` | Import aliases like `@/` |
| Express/Fastify/Koa: `app.listen`, `server.ts`, `routes/` | `rg -n '\.(get\|post\|put\|patch\|delete)\(' src/` |
| NestJS: `main.ts` `NestFactory.create`, `*.module.ts`, `@Controller` | Controllers and DI modules |
| Next.js: `app/` (`page.tsx`, `route.ts`, `layout.tsx`), `pages/`, `pages/api/`, `middleware.ts` | File-system routes |
| Vite/React SPA: `index.html` → `src/main.tsx`, router config | Client entry and routes |
| Workers/queues: `bullmq`, `agenda`, `node-cron` usage | Background entries |

## Python

| Look at | What it tells you |
|---|---|
| `pyproject.toml` (`[project]`, `[tool.poetry]`, `[project.scripts]`), `setup.cfg`, `requirements*.txt`, `uv.lock`, `poetry.lock` | Dependencies, console scripts, tooling |
| `__main__.py`, `if __name__ == "__main__":` | Script entries |
| Django: `manage.py`, `settings.py` (`INSTALLED_APPS`, `ROOT_URLCONF`), `urls.py`, `views.py`, `models.py`, `migrations/` | Apps, routes, data model |
| Flask: `create_app()`, `Blueprint`, `@app.route` | App factory and routes |
| FastAPI: `FastAPI()`, `APIRouter`, `@router.get` | Routes; `Depends()` for DI |
| Celery/RQ: `celery.py`, `@shared_task`, `@app.task` | Background jobs |
| Tests: `pytest.ini`, `conftest.py`, `tox.ini`, `noxfile.py` | Fixtures and test config |

## Go

| Look at | What it tells you |
|---|---|
| `go.mod` (module path, Go version), `go.work` | Module identity |
| `cmd/<name>/main.go`, any `package main` | Binaries: `rg -l '^package main' --glob '*.go'` |
| `internal/` vs `pkg/` | Private vs importable packages |
| `http.HandleFunc`, `chi`/`gin`/`echo`/`gorilla/mux` router setup | Routes: `rg -n '\.(GET\|POST\|Handle\|HandleFunc)\('` |
| `wire.go`, `fx.Provide` | DI wiring |
| `Makefile`, `magefile.go`, `.goreleaser.yml` | Build and release commands |

## Java / Kotlin (Spring)

| Look at | What it tells you |
|---|---|
| `pom.xml` / `build.gradle(.kts)`, `mvnw` / `gradlew` | Build tool, modules, Java version |
| `@SpringBootApplication` class with `main` | Process entry |
| `@RestController`, `@Controller`, `@RequestMapping`, `@GetMapping` | HTTP routes |
| `@Service`, `@Repository`, `@Component`, `@Configuration` + `@Bean` | DI graph |
| `src/main/resources/application*.yml\|properties` | Config and profiles |
| `@Scheduled`, `@KafkaListener`, `@RabbitListener`, `@EventListener` | Non-HTTP entries |
| `db/migration/` (Flyway), `db/changelog/` (Liquibase) | Schema history |

## PHP / Laravel

| Look at | What it tells you |
|---|---|
| `composer.json` (`require`, `autoload.psr-4`, `scripts`), `composer.lock` | Dependencies and namespaces |
| `public/index.php`, `bootstrap/app.php` | HTTP entry |
| `routes/web.php`, `routes/api.php`, `routes/console.php` | Routes; `php artisan route:list` if runnable |
| `app/Http/Controllers`, `app/Http/Middleware`, `app/Http/Kernel.php` or `bootstrap/app.php` middleware | Request handling |
| `app/Providers/*ServiceProvider.php` | DI bindings and boot logic |
| `app/Console/Kernel.php` or `routes/console.php` schedule, `app/Jobs`, `app/Listeners` | Scheduled and queued work |
| `config/*.php` with `env()`, `.env.example` | Config sources |
| `database/migrations`, `app/Models` | Data model |

## Ruby / Rails

| Look at | What it tells you |
|---|---|
| `Gemfile`, `Gemfile.lock`, `.ruby-version` | Dependencies and runtime |
| `config/routes.rb` | Routes; `bin/rails routes` if runnable |
| `app/controllers`, `app/models`, `app/jobs`, `app/mailers` | Request, data, async |
| `config/application.rb`, `config/environments/*.rb`, `config/initializers/` | Config and boot |
| `db/schema.rb` or `db/structure.sql`, `db/migrate/` | Current schema and history |
| `Procfile`, `config/sidekiq.yml` | Process types |

## Mobile

| Platform | Look at |
|---|---|
| Android | `settings.gradle*` (modules), `app/build.gradle*` (`applicationId`, `minSdk`, flavors), `AndroidManifest.xml` (launcher `Activity`, services, receivers, permissions), `Application` subclass, navigation graphs `res/navigation/` |
| iOS | `*.xcodeproj`/`*.xcworkspace`, `Package.swift`, `Podfile`; `@main` App struct or `AppDelegate`/`SceneDelegate`; `Info.plist` (URL schemes, permissions) |
| React Native | `package.json`, `index.js` → `AppRegistry.registerComponent`, `App.tsx`, navigation setup, `android/` and `ios/` native shells, `app.json`/`app.config.ts` (Expo) |
| Flutter | `pubspec.yaml`, `lib/main.dart` (`runApp`), router (`go_router`, `auto_route`), `android/` and `ios/` shells |

## Cross-cutting (any stack)

| Look at | What it tells you |
|---|---|
| `Dockerfile` `CMD`/`ENTRYPOINT`, `docker-compose.yml` services | What actually runs in production and which services exist |
| `Procfile`, `k8s/`, `helm/`, `*.tf`, `serverless.yml` | Deployed process types and infrastructure |
| `.github/workflows/`, `.gitlab-ci.yml`, `Jenkinsfile`, `.circleci/` | The commands CI trusts: test, lint, build, release |
| `Makefile`, `justfile`, `Taskfile.yml`, `scripts/` | Developer commands |
| `.env.example`, `config/` | Required configuration keys |

Sources: general practice.
