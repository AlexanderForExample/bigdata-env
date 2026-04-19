#!/usr/bin/env bash

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)"
ENV_FILE="${ROOT_DIR}/infra/env/.env"

require_env_file() {
  if [[ ! -f "${ENV_FILE}" ]]; then
    echo "Missing ${ENV_FILE}. Create it: cp infra/env/.env.example infra/env/.env" >&2
    return 1
  fi
}

load_env() {
  require_env_file || return 1
  set -a
  # shellcheck disable=SC1090
  . "${ENV_FILE}"
  set +a
}

compose_args_for_stack() {
  local stack="${1:-postgres}"

  COMPOSE_ARGS=(-f "${ROOT_DIR}/infra/compose/base.yml")

  case "${stack}" in
    postgres)
      COMPOSE_ARGS+=(-f "${ROOT_DIR}/infra/compose/postgres.yml")
      ;;
    postgres_jupyter)
      COMPOSE_ARGS+=(
        -f "${ROOT_DIR}/infra/compose/postgres.yml"
        -f "${ROOT_DIR}/infra/compose/jupyter.yml"
      )
      ;;
    bigdata-core)
      COMPOSE_ARGS+=(-f "${ROOT_DIR}/infra/compose/bigdata-core.yml")
      ;;
    airflow_postgres)
      COMPOSE_ARGS+=(-f "${ROOT_DIR}/infra/compose/airflow-postgres.yml")
      ;;
    airflow_bigdata)
      COMPOSE_ARGS+=(
        -f "${ROOT_DIR}/infra/compose/airflow-postgres.yml"
        -f "${ROOT_DIR}/infra/compose/bigdata-core.yml"
        -f "${ROOT_DIR}/infra/compose/hive.yml"
        -f "${ROOT_DIR}/infra/compose/postgres-tgt.yml"
      )
      ;;
    *)
      echo "Unknown stack: ${stack}" >&2
      return 1
      ;;
  esac
}

compose_cmd_for_stack() {
  local stack="${1:-postgres}"

  require_env_file || return 1
  compose_args_for_stack "${stack}" || return 1

  COMPOSE_CMD=(docker compose --env-file "${ENV_FILE}")
  COMPOSE_CMD+=("${COMPOSE_ARGS[@]}")
}

retry() {
  local attempts="$1"
  local delay_seconds="$2"
  local attempt=1
  shift 2

  until "$@"; do
    if (( attempt >= attempts )); then
      return 1
    fi
    sleep "${delay_seconds}"
    attempt=$((attempt + 1))
  done
}

container_running() {
  [[ "$(docker inspect -f '{{.State.Running}}' "$1" 2>/dev/null || true)" == "true" ]]
}

container_healthy() {
  local status
  status="$(docker inspect -f '{{if .State.Health}}{{.State.Health.Status}}{{else}}{{.State.Status}}{{end}}' "$1" 2>/dev/null || true)"
  [[ "${status}" == "healthy" || "${status}" == "running" ]]
}
