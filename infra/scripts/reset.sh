#!/usr/bin/env bash
set -euo pipefail

STACK="${1:-postgres}"

echo "[reset] stack=${STACK}"

case "$STACK" in
  postgres)
    docker compose --env-file infra/env/.env -f infra/compose/base.yml -f infra/compose/postgres.yml down -v --remove-orphans
    echo "[reset] postgres volumes removed"
    ;;
  *)
    echo "[reset] Unknown stack: $STACK" >&2
    exit 1
    ;;
esac
