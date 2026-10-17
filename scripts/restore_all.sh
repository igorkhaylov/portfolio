#!/usr/bin/env bash
#
# Restore a backup made by scripts/dump_all.sh into the running stack:
#   database.sql.gz       → PostgreSQL (the dump drops/recreates objects itself)
#   media.tar.gz          → media/ (extracted over the existing files), if present
#
# Usage:
#   make restore dumps/<ts>
#   make prod restore dumps/<ts>
#
set -euo pipefail
cd "$(dirname "$0")/.."

COMPOSE="${COMPOSE:-docker compose}"
EXEC="${EXEC:-}"

DIR="${1:-}"
if [ -z "$DIR" ] || [ ! -f "$DIR/database.sql.gz" ]; then
  echo "Usage: make restore dumps/<ts>   (directory with database.sql.gz)" >&2
  exit 1
fi

set -a
. ./.env
set +a
: "${POSTGRES_USER:?POSTGRES_USER is not set in .env}"
: "${POSTGRES_DB:?POSTGRES_DB is not set in .env}"

echo "This OVERWRITES the database and media of the running stack with $DIR."
read -r -p "Type 'yes' to continue: " answer
[ "$answer" = "yes" ] || { echo "Aborted."; exit 1; }

echo "  • database…"
gunzip -c "$DIR/database.sql.gz" | $COMPOSE exec -T db psql -q -v ON_ERROR_STOP=1 -U "$POSTGRES_USER" -d "$POSTGRES_DB"

if [ -f "$DIR/media.tar.gz" ]; then
  echo "  • media…"
  $COMPOSE exec -T $EXEC backend sh -c \
    'tar -C "$(python manage.py shell -c "from django.conf import settings; print(settings.MEDIA_ROOT)")" -xzf -' \
    <"$DIR/media.tar.gz"
fi

echo "✓ Restored from $DIR."
