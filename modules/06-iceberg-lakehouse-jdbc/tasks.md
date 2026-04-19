# Tasks - 06 Iceberg lakehouse and JDBC integration

## Delivery format
- notebook или скрипт со Spark-кодом и проверками
- ориентир: 160-230 строк кода и пояснений

## Task A - JDBC ingestion
- настроить Spark read через JDBC
- прочитать минимум одну source table и проверить schema
- описать ограничения JDBC ingestion: parallel read, predicate pushdown, source load impact

## Task B - Curated layer design
- подготовить агрегированный или очищенный DataFrame
- описать бизнес-смысл curated table
- продумать partitioning strategy и future schema evolution risks

## Task C - Iceberg write and verification
- записать DataFrame в Iceberg table или подготовить полностью runnable код под будущий catalog
- выполнить проверки на counts, schema и повторное чтение
- описать, чем эта таблица отличается от набора обычных Parquet-файлов

## Expected result
- студент понимает JDBC как bridge в data platform
- умеет описать запись в Iceberg table на уровне кода и архитектуры
- умеет предложить базовые post-load checks

## Questions for review
- почему curated table лучше строить отдельно от OLTP source?
- что делает catalog в Iceberg-сценарии?
- какие риски появляются при schema evolution?

