# 06 - Iceberg lakehouse and JDBC integration

## Goal
- познакомить студентов с lakehouse-подходом и table format слоем
- показать, как JDBC-источник связывается со Spark и curated tables
- подготовить основу для batch и streaming сценариев поверх Iceberg

## Technology focus

### Why plain Parquet is not always enough
- набор Parquet-файлов сам по себе не дает полноценной табличной семантики
- сложно безопасно делать evolve schema, управлять snapshots и поддерживать таблицу как логическую сущность
- table format решает эти проблемы metadata layer'ом поверх файлов

### Apache Iceberg
- Iceberg хранит данные в файлах, но управляет ими как таблицей через manifest, metadata и snapshot model
- это дает versioning-like семантику, эволюцию схемы и более управляемую работу с большими таблицами
- Iceberg особенно полезен там, где один и тот же слой читается batch, streaming и SQL-движками

### JDBC integration
- JDBC нужен как bridge между операционной БД и аналитическим compute layer
- через JDBC Spark может читать source tables и писать curated result обратно
- это важный паттерн для миграции данных из OLTP мира в data platform

## Why this module matters
- модуль соединяет классический SQL-источник и modern table format
- после него понятнее, зачем нужны Hive Metastore, catalog и managed table semantics
- это мост между ранними Postgres/Spark-модулями и более production-like data architecture

## Core ideas
- source tables are not always analytical tables
- curated layer должен быть устойчивым, воспроизводимым и пригодным для повторного чтения
- schema evolution и snapshots важны даже на учебных данных, потому что они отражают реальные проблемы платформы

## Practice flow
1. Прочитать источник через JDBC.
2. Построить curated DataFrame.
3. Записать его в Iceberg table.
4. Прочитать результат обратно через catalog.
5. Сравнить counts и схему между source и target.

## Suggested implementation scope
- 160-230 строк кода в notebook
- обязательны JDBC read/write helpers, трансформация и post-load checks
- если real Iceberg catalog пока не поднят, notebook должен быть максимально близок к будущей runnable реализации

## Expected output
- студент понимает отличие file layer и table format layer
- умеет описать сценарий `JDBC -> Spark -> Iceberg`
- понимает, зачем нужен catalog и metadata management

## Questions for review
- что дает Iceberg сверх набора Parquet-файлов?
- почему JDBC-источник хорошо подходит для initial ingestion?
- какие проверки важны после записи curated table?

