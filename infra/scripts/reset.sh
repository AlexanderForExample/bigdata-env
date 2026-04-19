#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
# shellcheck source=infra/scripts/common.sh
source "${SCRIPT_DIR}/common.sh"

STACK="${1:-postgres}"

echo "[reset] stack=${STACK}"

compose_cmd_for_stack "$STACK"
"${COMPOSE_CMD[@]}" down -v --remove-orphans

echo "[reset] stack volumes removed"
