#!/usr/bin/env sh
set -e

# Attente DB si en postgres (optionnel mais pratique)
if [ "${DB_ENGINE}" = "postgres" ]; then
  echo "Waiting for PostgreSQL (${DB_HOST}:${DB_PORT:-5432})..."
  for i in $(seq 1 60); do
    (echo > /dev/tcp/${DB_HOST}/${DB_PORT:-5432}) >/dev/null 2>&1 && break
    sleep 1
  done
fi

# Collectstatic / migrations optionnels
if [ "${RUN_MIGRATIONS}" = "1" ]; then
  echo "Running migrations..."
  python manage.py migrate --noinput
fi

if [ "${RUN_COLLECTSTATIC}" = "1" ]; then
  echo "Running collectstatic..."
  python manage.py collectstatic --noinput
fi

# Lancer la commande (gunicorn/celery etc.)
exec "$@"