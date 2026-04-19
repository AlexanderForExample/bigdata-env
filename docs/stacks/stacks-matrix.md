# Stacks Matrix

| Module | Topic | Recommended stack | Notes |
|-------:|-------|-------------------|-------|
| 00 | API -> Postgres ingestion | `postgres_jupyter` | Jupyter нужен для практики с notebook и SQL/API загрузкой |
| 01 | HDFS and YARN fundamentals | `bigdata-core` | Нужны HDFS, YARN и Spark client |
| 02 | SQL in Postgres for analytics | `postgres_jupyter` | Достаточно Postgres и Jupyter |
| 03 | Airflow basic | `airflow_postgres` | Нужны Airflow и Postgres для простого DAG |
| 04 | Spark basics | `bigdata-core` | Нужны Spark, HDFS и Jupyter/Spark client |
| 05 | Spark optimization | `bigdata-core` | Нужны Spark и YARN для сравнения поведения job |
| 06 | Iceberg lakehouse and JDBC integration | `lakehouse` | Нужны Spark, Hive Metastore, Iceberg и JDBC-источник |
| 07 | Airflow with Spark batch pipelines | `airflow_bigdata` | Нужны Airflow, Spark, HDFS, Hive и целевая БД |
| 08 | Kafka streaming to Iceberg | `streaming_lakehouse` | Нужны Kafka, Spark Structured Streaming и Iceberg |
| 09 | Data quality, metrics and visualization | `observability` | Нужны источники данных, Airflow metadata и dashboard tool |

## Suggested stack groups

### `postgres_jupyter`
- `postgres`
- `jupyter`

### `bigdata-core`
- `namenode`
- `datanode`
- `resourcemanager`
- `nodemanager`
- `historyserver`
- `spark-master` или `spark-client`

### `airflow_postgres`
- `airflow-webserver`
- `airflow-scheduler`
- `airflow-triggerer`
- `airflow-init`
- `postgres`

### `lakehouse`
- сервисы из `bigdata-core`
- `hive-metastore`
- `hive-server`
- JDBC-источник, например `postgres-tgt`

### `airflow_bigdata`
- сервисы из `airflow_postgres`
- сервисы из `bigdata-core`
- `hive-metastore`
- `hive-server`
- целевая БД, например `postgres-tgt`

### `streaming_lakehouse`
- сервисы из `lakehouse`
- `kafka`
- producer/consumer или streaming job

### `observability`
- данные из предыдущих модулей
- Airflow metadata или job logs
- dashboard tool: `Grafana`, `Metabase` или `Superset`

## Notes
- Сейчас часть этих стеков уже реализована в проекте полностью, часть пока существует как целевой дизайн курса.
- Матрица нужна как ориентир для развития `docker-compose`, `infra/compose` и smoke-проверок по модулям.
