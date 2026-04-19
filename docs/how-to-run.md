# How to run

## Minimal stacks

### Postgres
```bash
cp infra/env/.env.example infra/env/.env
make up STACK=postgres
make smoke STACK=postgres
make down STACK=postgres
```

### Postgres + Jupyter
```bash
cp infra/env/.env.example infra/env/.env
make up STACK=postgres_jupyter
make smoke STACK=postgres_jupyter
make down STACK=postgres_jupyter
```

## Big data stacks

### bigdata-core
```bash
cp infra/env/.env.example infra/env/.env
make up STACK=bigdata-core
make bootstrap STACK=bigdata-core
make smoke STACK=bigdata-core
make down STACK=bigdata-core
```

Main endpoints:
- NameNode UI: `http://localhost:9870`
- ResourceManager UI: `http://localhost:8088`
- HistoryServer UI: `http://localhost:8188`
- Spark notebook: `http://localhost:8889`

### airflow_postgres
```bash
cp infra/env/.env.example infra/env/.env
make up STACK=airflow_postgres
make smoke STACK=airflow_postgres
make down STACK=airflow_postgres
```

Main endpoint:
- Airflow UI: `http://localhost:8083`

### airflow_bigdata
```bash
cp infra/env/.env.example infra/env/.env
make up STACK=airflow_bigdata
make bootstrap STACK=airflow_bigdata
make smoke STACK=airflow_bigdata
make down STACK=airflow_bigdata
```

Bootstrap creates HDFS base paths, uploads the PostgreSQL JDBC driver to HDFS and creates Hive databases `ods` and `dm`.

## Course mapping

- Полная матрица модулей и рекомендуемых стеков: `docs/stacks/stacks-matrix.md`
- Для `00-api-to-postgres` рекомендован стек `postgres_jupyter`
- Для модулей `01`, `04`, `05` нужен `bigdata-core`
- Для модуля `03` нужен `airflow_postgres`
- Для модуля `07` нужен `airflow_bigdata`
- Для модулей `06` и `08` нужен lakehouse/streaming stack

## Notes

- Поддерживаемые compose-стеки оформлены через `Makefile` и `infra/compose/`.
- Для стеков с HDFS/Hive используйте `make bootstrap` после `make up`.
- `docker-compose.yml` в корне репозитория остается как legacy reference и не считается основным способом запуска.
