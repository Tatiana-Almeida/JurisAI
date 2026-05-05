#!/bin/sh
set -e

if [ "${RUN_COLLECTSTATIC:-False}" = "True" ]; then
  python manage.py collectstatic --noinput
fi

python manage.py bootstrap_superuser

exec "$@"
