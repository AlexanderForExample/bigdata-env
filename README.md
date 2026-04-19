# BigData Env

Локальная инфраструктура для учебных модулей по Postgres, Airflow, Hadoop/YARN, Spark и Hive. Основной способ запуска теперь проходит через `Makefile` и модульные overlay-файлы в `infra/compose/`.

## Supported stacks

| Stack | Purpose | Main services |
|-------|---------|---------------|
| `postgres` | SQL и ingestion practice | `postgres` |
| `postgres_jupyter` | notebooks + Postgres | `postgres`, `jupyter` |
| `bigdata-core` | HDFS, YARN, Spark client | `namenode`, `datanode`, `resourcemanager`, `nodemanager`, `historyserver`, `spark-client` |
| `airflow_postgres` | Airflow basics | `airflow-webserver`, `airflow-scheduler`, `airflow-triggerer`, `airflow-db` |
| `airflow_bigdata` | Airflow + Spark batch + Hive + target DB | `airflow_*`, `bigdata-core`, `hive-*`, `postgres-tgt` |

## Quick start

```bash
cp infra/env/.env.example infra/env/.env
make up STACK=postgres_jupyter
make smoke STACK=postgres_jupyter
make down STACK=postgres_jupyter
```

Для стеков с HDFS и Hive после `up` нужен bootstrap:

```bash
cp infra/env/.env.example infra/env/.env
make up STACK=airflow_bigdata
make bootstrap STACK=airflow_bigdata
make smoke STACK=airflow_bigdata
make down STACK=airflow_bigdata
```

## Main commands

```bash
make up STACK=<stack>
make ps STACK=<stack>
make logs STACK=<stack>
make bootstrap STACK=<stack>
make smoke STACK=<stack>
make down STACK=<stack>
make reset STACK=<stack>
```

## Notes

- `docker-compose.yml` в корне пока остается как legacy reference, но поддерживаемый путь запуска - через `Makefile`.
- Подробные команды по каждому стеку лежат в `docs/how-to-run.md`.
- Матрица модулей и стеков лежит в `docs/stacks/stacks-matrix.md`.
