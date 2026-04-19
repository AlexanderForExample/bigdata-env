#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
# shellcheck source=infra/scripts/common.sh
source "${SCRIPT_DIR}/common.sh"

STACK="${1:-postgres}"

load_env

echo "[smoke] stack=${STACK}"

smoke_postgres() {
  retry 20 3 docker exec bd-postgres \
    pg_isready -U "${POSTGRES_USER:-course}" -d "${POSTGRES_DB:-course}" >/dev/null
  echo "[smoke] postgres: OK"
}

smoke_jupyter() {
  retry 20 3 container_running bd-jupyter >/dev/null
  echo "[smoke] jupyter: OK (http://localhost:${JUPYTER_PORT:-8888})"
}

spark_submit_smoke() {
  local container_name="$1"
  local label="$2"

  retry 6 15 docker exec "${container_name}" bash -lc '
    cat > /tmp/spark_smoke.py <<'"'"'PY'"'"'
from pyspark.sql import SparkSession

spark = (
    SparkSession.builder
    .master("yarn")
    .appName("spark_smoke")
    .config("spark.submit.deployMode", "client")
    .config("spark.pyspark.python", "/opt/conda/bin/python")
    .config("spark.executorEnv.PYSPARK_PYTHON", "/opt/conda/bin/python")
    .config("spark.yarn.appMasterEnv.PYSPARK_PYTHON", "/opt/conda/bin/python")
    .getOrCreate()
)

assert spark.range(1).count() == 1
spark.stop()
PY
    "${SPARK_HOME}/bin/spark-submit" --master yarn --deploy-mode client /tmp/spark_smoke.py >/tmp/spark-smoke.log 2>&1
    rm -f /tmp/spark_smoke.py /tmp/spark-smoke.log
  ' >/dev/null

  echo "[smoke] ${label}: OK"
}

smoke_bigdata_core() {
  retry 30 5 container_running bd-namenode >/dev/null
  retry 30 5 docker exec bd-namenode hdfs dfs -test -d / >/dev/null
  echo "[smoke] hdfs: OK"

  retry 30 5 docker exec bd-resourcemanager bash -lc 'yarn node -list >/dev/null 2>&1' >/dev/null
  echo "[smoke] yarn: OK"

  retry 20 3 container_running bd-spark-client >/dev/null
  spark_submit_smoke bd-spark-client "spark-submit (spark-client)"
  echo "[smoke] spark-client: OK (http://localhost:${SPARK_NOTEBOOK_PORT:-8889})"
}

smoke_airflow_postgres() {
  retry 20 3 docker exec bd-airflow-db \
    pg_isready -U airflow -d airflow >/dev/null
  echo "[smoke] airflow-db: OK"

  retry 30 5 docker exec bd-airflow-webserver \
    curl -fsS http://localhost:8080/health >/dev/null
  retry 20 3 container_healthy bd-airflow-scheduler >/dev/null
  retry 20 3 container_healthy bd-airflow-triggerer >/dev/null
  echo "[smoke] airflow: OK (http://localhost:${AIRFLOW_PORT:-8083})"
}

smoke_airflow_bigdata() {
  smoke_airflow_postgres
  smoke_bigdata_core

  retry 20 3 container_running bd-hive-metastore >/dev/null
  retry 20 3 container_running bd-hive-server >/dev/null
  echo "[smoke] hive: OK"

  retry 20 3 docker exec bd-postgres-tgt \
    pg_isready -U "${POSTGRES_TGT_USER:-postgres}" -d "${POSTGRES_TGT_DB:-postgres}" >/dev/null
  echo "[smoke] postgres-tgt: OK"

  spark_submit_smoke bd-airflow-webserver "spark-submit (airflow)"

  retry 10 10 docker exec bd-spark-client \
    bash -lc "spark-sql -e 'SHOW DATABASES;' >/dev/null 2>&1" >/dev/null
  echo "[smoke] metastore: OK"
}

case "$STACK" in
  postgres)
    smoke_postgres
    ;;
  postgres_jupyter)
    smoke_postgres
    smoke_jupyter
    ;;
  bigdata-core)
    smoke_bigdata_core
    ;;
  airflow_postgres)
    smoke_airflow_postgres
    ;;
  airflow_bigdata)
    smoke_airflow_bigdata
    ;;
  *)
    echo "[smoke] Unknown stack: $STACK" >&2
    exit 1
    ;;
esac

echo "[smoke] OK"
