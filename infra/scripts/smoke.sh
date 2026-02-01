#!/usr/bin/env bash
set -euo pipefail

STACK="${1:-postgres}"

echo "[smoke] stack=${STACK}"

case "$STACK" in
  postgres|postgres_jupyter)
    docker exec -i bd-postgres psql -U "${POSTGRES_USER:-course}" -d "${POSTGRES_DB:-course}" -c "select 1;" >/dev/null
    echo "[smoke] postgres: OK"
    ;;
  *)
    echo "[smoke] Unknown stack: $STACK" >&2
    exit 1
    ;;
esac

if [[ "$STACK" == "postgres_jupyter" ]]; then
  running="$(docker inspect -f '{{.State.Running}}' bd-jupyter 2>/dev/null || true)"
  [[ "$running" == "true" ]] || (echo "[smoke] jupyter not running" >&2; exit 1)
  echo "[smoke] jupyter: OK (http://localhost:8888)"
fi

echo "[smoke] OK"