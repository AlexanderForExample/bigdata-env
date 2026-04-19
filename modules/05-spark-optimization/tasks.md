# Tasks - 05 Spark optimization

## Delivery format
- `practice.ipynb` с baseline, tuning и сравнением
- ожидаемый объем: 180-260 строк Python/Spark-кода
- реализация должна включать helper-функции для чтения данных, измерения времени, запуска разных конфигураций и фиксации результатов

## Task A - Baseline pipeline
- собрать достаточно тяжелый pipeline из нескольких источников: `orders`, `order_items`, `products`, при желании `events`
- реализовать минимум два join и минимум два агрегирующих шага
- замерить baseline runtime хотя бы на нескольких action-вызовах
- сохранить explain plan и сформулировать первичную гипотезу по bottlenecks

## Task B - Code-level optimization
- уменьшить набор колонок до join
- использовать `broadcast` там, где это оправдано
- применить `cache` или `persist` для повторно используемого слоя
- осмысленно выбрать `repartition` или `coalesce`
- показать, как изменился explain plan и что стало лучше

## Task C - Config-level optimization
- сравнить минимум два набора Spark config parameters
- обязательно разобрать `spark.sql.shuffle.partitions`
- дополнительно использовать минимум два параметра из списка:
  - `spark.sql.autoBroadcastJoinThreshold`
  - `spark.sql.adaptive.enabled`
  - `spark.sql.adaptive.coalescePartitions.enabled`
  - `spark.sql.adaptive.skewJoin.enabled`
  - `spark.sql.files.maxPartitionBytes`
- описать, почему именно эти параметры влияют на конкретный pipeline

## Task D - Benchmark and report
- собрать таблицу `baseline vs optimized` с counts, runtime, explain notes и конфигурацией
- кратко описать, какие оптимизации дали эффект, а какие нет
- сформулировать правила, которые можно перенести на другие Spark job'ы

## Expected result
- есть baseline и tuned pipeline
- есть отдельный блок code optimization и отдельный блок config tuning
- студент понимает, что производительность - это результат и кода, и конфигурации

## Questions for review
- почему один и тот же код ведет себя по-разному при разных config?
- почему `cache` полезен не всегда?
- когда увеличение parallelism ухудшает job, а не улучшает?

