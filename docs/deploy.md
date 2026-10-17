# Deploy runbook

**The model:** CI builds the backend image and pushes it to **GHCR**; the server **only
pulls** — it never builds. The server holds a git checkout of this repo (for
`docker-compose.prod.yml`, `nginx/nginx.conf`, `Makefile`), its own `./.env`, the data
directory (`DATA_DIR`) and a Docker login to the registry.

Current production: `hetzner-server`, checkout `/webapps/igorkhaylov.uz/portfolio`, data
`/webapps/igorkhaylov.uz/data`, in-stack nginx on `127.0.0.1:8490`. The edge nginx on the
host terminates TLS for `igorkhaylov.uz` and proxies to that port.

## Everyday deploy

```bash
cd /webapps/igorkhaylov.uz/portfolio
git pull
make prod deploy            # = docker compose -f docker-compose.prod.yml pull && up -d --remove-orphans
make prod seed              # only when seed_portfolio.py changed: refresh the site content
```

`make prod seed` rewrites every entry it knows (matched by natural key) — edits made in the
admin to those same entries are overwritten, everything added in the admin is kept.

## First deploy on a new server

1. **Registry login** — a GitHub *classic* token with only `read:packages`:
   `echo "$GHCR_PAT" | docker login ghcr.io -u <github-user> --password-stdin`
   (the pull then works whether the GHCR package is public or private).
2. **Checkout + data + env:**

   ```bash
   git clone https://github.com/igorkhaylov/portfolio.git /webapps/igorkhaylov.uz/portfolio
   mkdir -p /webapps/igorkhaylov.uz/data/media
   cd /webapps/igorkhaylov.uz/portfolio
   ./scripts/init_env.sh && chmod 600 .env    # .env from .env.example with generated secrets
   ```

   Then set in `.env`:

   | Variable | Value in prod |
   |---|---|
   | `ENVIRONMENT` | `prod` |
   | `APP_PORT` | `8490` |
   | `DATA_DIR` | `../data` |
   | `DJANGO_ALLOWED_HOSTS` | `igorkhaylov.uz,www.igorkhaylov.uz` |
   | `DJANGO_CSRF_TRUSTED_ORIGINS` / `DJANGO_CORS_ALLOWED_ORIGINS` | `https://igorkhaylov.uz,https://www.igorkhaylov.uz` |
   | `GUNICORN_WORKERS` | `2` |

   `init_env.sh` already generated `DJANGO_SECRET_KEY`, `DJANGO_SUPERUSER_PASSWORD` and
   `POSTGRES_PASSWORD` — the admin password is in this file.
3. **Start and fill:**

   ```bash
   make prod deploy
   docker compose -f docker-compose.prod.yml ps     # backend "healthy"
   make prod seed
   ```

4. **Edge nginx** (host, from `/etc/nginx/sites-available/vhost.template.conf`):
   `proxy_pass http://127.0.0.1:8490;`, `include proxy_params` (sets `X-Forwarded-Proto`
   — without it Django redirects to https forever), `client_max_body_size 50M` for admin
   uploads, then `certbot --nginx -d igorkhaylov.uz -d www.igorkhaylov.uz`.

If `backend` never becomes healthy, `nginx` never starts (it waits on `service_healthy`) —
read `docker compose -f docker-compose.prod.yml logs backend`: usually a placeholder
`DJANGO_SUPERUSER_PASSWORD`, a short `DJANGO_SECRET_KEY` or a missing `DATA_DIR/media`.

## Deploy from CI (optional)

`.github/workflows/deploy.yml` SSHes into the server and does the same `git reset` +
`make prod deploy`. It runs on `workflow_dispatch`, and after every build only when the
repository variable `AUTO_DEPLOY=true`. It needs the Environment `prod` with the secrets
`SSH_HOST`, `SSH_PORT`, `SSH_USER`, `SSH_KEY`, `SSH_FINGERPRINT`, `DEPLOY_PATH`,
`GHCR_USER`, `GHCR_PAT`. Without them the deploy job is simply skipped.

## Rollback

Images stay in the registry by `sha-` tag:

```bash
BACKEND_IMAGE=ghcr.io/igorkhaylov/portfolio:sha-<previous-sha> make prod deploy
```

Only the image rolls back — an applied migration does not. `make prod dump media` before
risky releases ([backup.md](backup.md)).
