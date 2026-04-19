# 07 - Airflow with Spark batch pipelines

## Goal
- объединить orchestration и distributed processing в одном end-to-end pipeline
- научиться декомпозировать batch pipeline на слои raw, ods, dm и final load
- показать, как Airflow и Spark вместе образуют production-like batch architecture

## Technology focus

### Airflow as control plane
- Airflow отвечает за schedule, зависимости, retries и операционное наблюдение
- самих тяжелых трансформаций в DAG быть не должно: они должны жить в отдельных Spark scripts

### Spark as processing engine
- Spark выполняет вычисления, читает и пишет данные в storage layer
- через Spark удобно реализовывать многошаговый ETL/ELT pipeline

### Layered batch design
- raw - минимально обработанные данные из источника
- ods - очищенные и таблично представленные данные
- dm/mart - агрегированный слой для конечного потребителя
- final load - выгрузка в BI-friendly или application-friendly target

## Why this module matters
- это первый модуль, где pieces курса складываются в реальную pipeline story
- здесь студенты учатся думать не отдельными скриптами, а системой стадий, зависимостей и проверок
- такой модуль ближе всего к ежедневной работе data engineer

## Practice flow
1. Разобрать существующие Spark jobs.
2. Зафиксировать contract каждой стадии.
3. Сопоставить стадии с задачами DAG.
4. Добавить post-load validation.
5. Разобрать, как искать проблему в случае падения одной из стадий.

## Suggested implementation scope
- 150-220 строк DAG и notebook-кода
- обязательны mapping pipeline stages, review текущего DAG и дополнительные validation checks
- в решении должна быть объяснена ответственность каждой стадии и точка контроля качества

## Expected output
- студент понимает, как устроен layered batch pipeline
- умеет объяснить, зачем stages разделены на отдельные job'ы
- умеет предложить post-load checks и operational improvements

## Questions for review
- почему heavy transformation лучше держать вне DAG-кода?
- что именно проверять после `load_to_pg`?
- как локализовать ошибку, если raw успешен, а dm пустой?

