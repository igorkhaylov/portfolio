# igorkhaylov.uz — personal site

Bilingual (ru/en) portfolio of Igor Khaylov: profile, what I do, the infrastructure I run,
projects, experience and stack. Every word on the page is a database row, editable in the
Django admin and seeded from git. Built on
[django-template](https://github.com/igorkhaylov/django-template) — Django 5.2, PostgreSQL,
Nginx, Docker Compose, **uv** — trimmed for a one-page site: files on local disk instead
of S3, no Redis/Celery, a hand-written front-end instead of a theme.

- **What goes where on the page, and how to edit it:** [docs/content.md](docs/content.md)
- **Server runbook:** [docs/deploy.md](docs/deploy.md) · **Backups:** [docs/backup.md](docs/backup.md)

## Tech stack

- **Python 3.13** / **Django 5.2** · **PostgreSQL 17** · **Nginx** · **Gunicorn**
- **django-modeltranslation** + **Rosetta** — ru/en content and UI strings
- **django-stdimage** (maintained fork) — image variants for avatar, covers, screenshots
- Front-end: one stylesheet and one small script, no framework or CDN; light/dark theme
  follows the OS, with a toggle; an inline SVG icon sprite
- **uv**, **Ruff**, **pre-commit**, **pytest**, **structlog**
- CI: GitHub Actions (tests → image → GHCR), GitLab CI mirror

## Project structure

```
├── backend/
│   ├── apps/
│   │   ├── common/          # Shared abstract models, utils, validators
│   │   ├── users/           # Custom User
│   │   └── portfolio/       # The site: models, admin, views, seed_portfolio
│   ├── config/settings/     # base.py, third_party.py, dev.py, test.py (ENVIRONMENT selects)
│   ├── templates/           # base.html, includes/ (header, footer, icon sprite), portfolio/
│   ├── static_src/          # css/site.css, js/site.js, img/
│   ├── locale/              # ru / en UI strings
│   ├── scripts/entrypoint.sh# compilemessages → migrate → collectstatic → superuser → gunicorn
│   └── tests/               # pytest, no external services
├── docs/                    # content.md · deploy.md · backup.md · stdimage.md · uv.md
├── nginx/                   # nginx.conf (prod: serves /static/ and /media/) · nginx.dev.conf
├── scripts/                 # init_env.sh · dump_all.sh · restore_all.sh
├── docker-compose.yml       # local production-like (builds from source)
├── docker-compose.dev.yml   # development (repo bind-mounted, backend idles)
├── docker-compose.prod.yml  # production (pulls the GHCR image)
├── docker-compose.test.yml  # test runner, what CI runs
└── Makefile                 # `make help`
```

### The `portfolio` app

```
apps/portfolio/
├── models/          # profile · showcase (Stat, FocusArea) · resume · skills · projects
├── admin/           # one module per model group
├── views/pages.py   # index (single page) and project detail
├── management/commands/seed_portfolio.py   # the site content, ru + en
├── templatetags/portfolio_tags.py          # language switch URL, text helpers
├── translation.py   # translated fields (modeltranslation)
└── sitemaps.py · context_processors.py
```

Pages: `/` (single page) and `/projects/<slug>/`, both under `i18n_patterns` (`/ru/…`,
`/en/…`). `/sitemap.xml`, `/robots.txt` and `/healthcheck/` sit outside the language prefix.

## Quick start

Needs Docker with the Compose plugin, `make`, `openssl`.

```bash
make init                   # .env with generated secrets, dev stack, migrate, seed content
make dev createsuperuser    # your admin account
make dev run                # dev server (autoreload) → http://localhost:8050/ru/
```

The admin is at `/ru/admin/`. After editing `seed_portfolio.py`: `make dev seed`.

### Everyday commands

```bash
make help                   # the full list
make dev up / down / down-v # start / stop / stop and DROP volumes (database!)
make dev bash / shell       # shell in the backend container / Django shell
make dev test / lint / format
make dev makemigrations / migrate / seed
make dev makemessages / compilemessages
make dev logs backend
make dump [media] / make restore dumps/<ts>
```

`make dev <target>` runs against `docker-compose.dev.yml`; without a prefix the target
uses `docker-compose.yml` (local production-like); `make prod <target>` the pull-only
production compose.

## Deployment topology

```
browser ──https──▶ edge nginx (host, certbot) ──▶ 127.0.0.1:8490 nginx (stack)
                                                   ├─ /static/, /media/  (volumes)
                                                   └─ everything else ──▶ backend:8000 (gunicorn)
```

The edge terminates TLS and sets `X-Forwarded-Proto`; Django trusts it via
`SECURE_PROXY_SSL_HEADER`. The in-stack nginx must **not** re-set that header. Static files
are collected with `ManifestStaticFilesStorage` (content-hashed names, cached for 30 days);
media sits in `DATA_DIR/media` on the host.

Production never builds on the server:

```bash
git pull && make prod deploy    # pull the image CI built, restart
make prod seed                  # when the content in seed_portfolio.py changed
```

Full runbook: [docs/deploy.md](docs/deploy.md).

## Environment variables

See [`.env.example`](.env.example) — every variable is documented there. The ones that
matter in prod: `ENVIRONMENT=prod` (HTTPS redirect, secure cookies, HSTS, JSON logs),
`DJANGO_SECRET_KEY` (≥ 50 chars), `DJANGO_ALLOWED_HOSTS` / `_CSRF_TRUSTED_ORIGINS`,
`DJANGO_SUPERUSER_PASSWORD` (a placeholder fails the boot), `APP_PORT`, `DATA_DIR`,
`BACKEND_IMAGE`.

## Testing

```bash
make dev test                          # inside the dev container
cd backend && uv run pytest            # on the host
docker compose -f docker-compose.test.yml up --build --exit-code-from backend   # what CI runs
```

The suite runs in a minimal configuration (`config.settings.test`): in-memory SQLite,
locmem cache and email, in-memory storage. It seeds the real content and renders every
page in both languages, so a broken seed or template fails CI.

## Internationalization

Content fields are translated with modeltranslation (`_ru` / `_en` columns, language tabs in
the admin, Russian is the fallback). UI strings in templates use `{% translate %}`:

```bash
make dev makemessages       # extract strings
make dev compilemessages    # the container entrypoint also compiles them on boot
```

or edit them in the Rosetta UI at `/ru/rosetta/`.

## Code quality

Ruff (`E, F, I, UP, B, C4, SIM, DJ, RUF`, line length 120) runs from pre-commit on every
commit — `uv tool install pre-commit && pre-commit install`.

## CI/CD

- `.github/workflows/build-push.yml` — on push to `main` and `v*` tags: runs
  `docker-compose.test.yml`, then builds and pushes `ghcr.io/igorkhaylov/portfolio`
  (`latest`, `sha-<full-sha>`, semver tags).
- `.github/workflows/deploy.yml` — SSH deploy of a given tag; manual, or after every build
  when the repository variable `AUTO_DEPLOY=true`. See [docs/deploy.md](docs/deploy.md).
