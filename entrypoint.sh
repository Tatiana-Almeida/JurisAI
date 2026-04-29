#!/bin/sh
set -e

if [ "${RUN_COLLECTSTATIC:-False}" = "True" ]; then
  python manage.py collectstatic --noinput
fi

exec "$@"
