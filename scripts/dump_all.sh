#!/usr/bin/env bash
#
# Create a timestamped backup under ./dumps/<ts>/:
#   database.sql.gz — full pg_dump of PostgreSQL (gzipped, --clean --if-exists)
#   media.tar.gz    — media/: avatar, CV, project covers and screenshots
#                     (only with the "media" argument)
#
# Unlike the template there is no object storage: media sits in the backend container's
# data volume, so it is read THROUGH the container (works the same for the dev stack,
# where it lives under backend/).
#
# Usage:
#   make dump                 # database
#   make dump media           # + media archive
#   make prod dump media      # on the server
#   ./scripts/dump_all.sh [media]
#
set -euo pipefail
cd "$(dirname "$0")/.."

COMPOSE="${COMPOSE:-docker compose}"
EXEC="${EXEC:-}"   # extra `docker compose exec` flags (e.g. --workdir /app/backend for the dev stack)

WITH_MEDIA=0
for arg in "$@"; do
  case "$arg" in
    media | --media) WITH_MEDIA=1 ;;
  esac
done

ENV_FILE="./.env"
if [ ! -f "$ENV_FILE" ]; then
  echo "Error: $ENV_FILE not found (needed for Postgres credentials)." >&2
  exit 1
fi
set -a
. "$ENV_FILE"
set +a
: "${POSTGRES_USER:?POSTGRES_USER is not set in .env}"
: "${POSTGRES_DB:?POSTGRES_DB is not set in .env}"

TS="$(date +%Y-%m-%d_%H-%M-%S)"
DIR="dumps/${TS}"
mkdir -p "$DIR"
echo "→ Backing up to ${DIR}"

echo "  • database…"
$COMPOSE exec -T db pg_dump -U "$POSTGRES_USER" -d "$POSTGRES_DB" \
  --clean --if-exists --no-owner --no-privileges \
  | gzip >"$DIR/database.sql.gz"

if [ "$WITH_MEDIA" -eq 1 ]; then
  echo "  • media…"
  $COMPOSE exec -T $EXEC backend sh -c \
    'tar -C "$(python manage.py shell -c "from django.conf import settings; print(settings.MEDIA_ROOT)")" -czf - .' \
    >"$DIR/media.tar.gz"
fi

echo "✓ Backup complete:"
du -sh "$DIR"/* 2>/dev/null || true
