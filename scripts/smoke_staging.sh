#!/usr/bin/env bash
set -euo pipefail

BASE_URL="${1:-http://localhost:8000}"
HEALTH_URL="${BASE_URL%/}/health/"
TMP_OUTPUT="${TMPDIR:-/tmp}/jurisai_health.out"

status_code="$(curl -fsS -o "$TMP_OUTPUT" -w "%{http_code}" "$HEALTH_URL")"

if [ "$status_code" != "200" ]; then
  echo "Healthcheck failed with status $status_code" >&2
  exit 1
fi

echo "Healthcheck OK"
cat "$TMP_OUTPUT"
