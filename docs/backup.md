# Backup & restore

The state lives in two places:

| What | Where | Covered by |
|---|---|---|
| PostgreSQL: all the site content, admin users | `postgres-data` volume | `make dump`, optional `db-backup` sidecar |
| Media: avatar, CV, project covers and screenshots | `DATA_DIR/media/` | `make dump media` |

Most of the content is also in git: `seed_portfolio` rebuilds it on an empty database.

## Manual backup

```bash
make prod dump             # on the server: database.sql.gz
make prod dump media       # + media.tar.gz
make dev dump media        # dev stack
```

Each run creates `dumps/<timestamp>/` (git-ignored). Copy it off the server — a backup
on the same disk is not a backup.

## Restore

```bash
make prod restore dumps/<timestamp>
```

It asks for confirmation, then loads the PostgreSQL dump (it drops and recreates objects
itself) and extracts `media.tar.gz` over `media/` if present.

## Automated database backups (optional)

`docker-compose.prod.yml` has a `db-backup` service (tiredofit/db-backup), off by default.
Enable it with `COMPOSE_PROFILES=backup` in the server's `.env`, then `make prod deploy`.
It backs up **PostgreSQL only** (every 24 h, 7 days retention by default, into
`DB_BACKUP_FS_PATH`); media still needs `make prod dump media`, e.g. from cron:

```cron
30 3 * * * cd /webapps/igorkhaylov.uz/portfolio && make prod dump media >/dev/null 2>&1
```
