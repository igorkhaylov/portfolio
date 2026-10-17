#!/bin/bash
set -e

echo ">>> Compiling translation .mo files..."
python manage.py compilemessages

echo ">>> Applying database migrations..."
python manage.py migrate --no-input

echo ">>> Collecting static files..."
# Into the static volume shared with nginx (docker-compose*.yml). No --clear.
python manage.py collectstatic --no-input

echo ">>> Ensuring superuser..."
python manage.py createsuperuserauto

echo ">>> Starting Gunicorn..."
exec gunicorn config.wsgi:application \
    --name "${DJANGO_APP_NAME}" \
    --workers "${GUNICORN_WORKERS:-4}" \
    --timeout "${GUNICORN_TIMEOUT:-60}" \
    --graceful-timeout "${GUNICORN_GRACEFUL_TIMEOUT:-30}" \
    --worker-tmp-dir /dev/shm \
    --bind 0.0.0.0:8000 \
    --access-logfile - \
    --error-logfile -
