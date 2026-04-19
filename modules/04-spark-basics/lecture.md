# 04 - Spark basics

## Goal
- освоить Spark DataFrame API как основной способ batch-обработки
- научиться читать данные из разных форматов, трансформировать их и писать обратно
- сформировать интуицию по lazy execution и trigger actions

## Technology focus

### Spark as a distributed processing engine
- Spark выполняет вычисления не на одной машине, а на наборе executors
- пользователь пишет high-level transformations, а Spark строит execution plan сам
- это позволяет писать лаконичный код, но требует понимания, когда реально стартует вычисление

### DataFrame API
- DataFrame - основной tabular abstraction в Spark
- он ближе к SQL и привычной аналитической модели, чем низкоуровневый RDD API
- почти все production batch pipelines в Spark сегодня строятся вокруг DataFrame и Spark SQL

### File formats
- CSV хорош для входного обмена, но неудобен для аналитики
- JSON хорош для semi-structured ingestion
- Parquet - columnar format, который сильно лучше для аналитических read-heavy сценариев

## Why this module matters
- это вход в мир Spark как processing engine
- дальше optimization, Iceberg и streaming будут опираться именно на DataFrame model
- здесь студент учится отделять transformation logic от format/storage concerns

## Key ideas
- transformations are lazy
- actions trigger jobs
- schema matters
- read and write options affect correctness and performance
- Spark code должен быть детерминированным и воспроизводимым

## Practice flow
1. Создать SparkSession.
2. Прочитать CSV и JSON.
3. Проверить schema и типы.
4. Сделать join, filter, aggregation.
5. Записать curated result в Parquet.
6. Перечитать результат и проверить его.

## Suggested implementation scope
- 160-220 строк кода в notebook
- обязательны helper-функции для чтения, валидации схемы и записи результата
- в итоговом решении должен быть хотя бы один join, один aggregate и одна post-write check

## Expected output
- студент уверенно выполняет сценарий `read -> transform -> write`
- понимает разницу между CSV, JSON и Parquet в инженерном контексте
- умеет объяснить, какая строка кода реально запускает job

## Questions for review
- почему Spark не считает сразу после transformation?
- зачем задавать схему явно, если есть `inferSchema`?
- почему columnar format важен для аналитических задач?

