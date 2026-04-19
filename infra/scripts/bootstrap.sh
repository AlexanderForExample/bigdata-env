#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
# shellcheck source=infra/scripts/common.sh
source "${SCRIPT_DIR}/common.sh"

STACK="${1:-postgres}"

load_env

echo "[bootstrap] stack=${STACK}"

bootstrap_bigdata_core() {
  local driver_path="${ROOT_DIR}/${PG_JDBC_DRIVER_LOCAL_PATH:-spark-client/drivers/postgresql-42.7.2.jar}"
  local driver_name
  local driver_hdfs_path="${PG_JDBC_DRIVER_HDFS_PATH:-hdfs:///drivers/postgresql-42.7.2.jar}"

  driver_name="$(basename "${driver_path}")"

  retry 30 5 docker exec bd-namenode hdfs dfs -test -d / >/dev/null

  docker exec bd-namenode hdfs dfs -mkdir -p \
    /data/raw \
    /data/ods \
    /data/mart \
    /drivers \
    /user/hive/warehouse \
    /tmp/hive >/dev/null
  docker exec bd-namenode hdfs dfs -chmod -R 777 \
    /data \
    /drivers \
    /user/hive \
    /tmp/hive >/dev/null

  if [[ ! -f "${driver_path}" ]]; then
    echo "[bootstrap] Missing JDBC driver: ${driver_path}" >&2
    exit 1
  fi

  if docker exec bd-namenode hdfs dfs -test -e "${driver_hdfs_path}"; then
    echo "[bootstrap] JDBC driver already exists in HDFS"
  else
    docker cp "${driver_path}" "bd-namenode:/tmp/${driver_name}" >/dev/null
    docker exec bd-namenode hdfs dfs -put -f "/tmp/${driver_name}" "${driver_hdfs_path}" >/dev/null
    docker exec bd-namenode rm -f "/tmp/${driver_name}"
    echo "[bootstrap] Uploaded JDBC driver to ${driver_hdfs_path}"
  fi

  echo "[bootstrap] HDFS directories prepared"
}

bootstrap_airflow_bigdata() {
  bootstrap_bigdata_core

  retry 20 5 container_running bd-hive-metastore >/dev/null
  retry 20 5 container_running bd-hive-server >/dev/null
  retry 20 5 docker exec bd-postgres-tgt \
    pg_isready -U "${POSTGRES_TGT_USER:-postgres}" -d "${POSTGRES_TGT_DB:-postgres}" >/dev/null
  retry 12 10 docker exec bd-spark-client \
    bash -lc "spark-sql -e 'SHOW DATABASES;' >/dev/null 2>&1" >/dev/null

  docker exec bd-spark-client \
    bash -lc "spark-sql -e \"CREATE DATABASE IF NOT EXISTS ods; CREATE DATABASE IF NOT EXISTS dm;\" >/dev/null 2>&1"

  echo "[bootstrap] Hive databases ready: ods, dm"
}

case "${STACK}" in
  postgres|postgres_jupyter|airflow_postgres)
    echo "[bootstrap] No extra bootstrap required"
    ;;
  bigdata-core)
    bootstrap_bigdata_core
    ;;
  airflow_bigdata)
    bootstrap_airflow_bigdata
    ;;
  *)
    echo "[bootstrap] Unknown stack: ${STACK}" >&2
    exit 1
    ;;
esac

echo "[bootstrap] OK"
