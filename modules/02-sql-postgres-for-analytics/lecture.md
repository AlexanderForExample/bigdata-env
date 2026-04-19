# 02 - SQL in Postgres for analytics

## Goal
- научиться строить аналитический SQL поверх учебного набора данных
- закрепить разницу между raw, cleaned и mart-like представлениями
- освоить окна, CTE и многотабличные join как основу для downstream аналитики

## Technology focus

### Postgres for analytical prototyping
- Postgres не заменяет distributed query engine, но очень удобен как учебный аналитический слой
- он хорошо подходит для быстрых экспериментов, проверки гипотез и построения первых витрин
- в учебном курсе он играет роль понятной среды, где можно быстро проверить смысл метрики

### SQL as a data engineering language
- SQL нужен не только аналитикам, но и data engineer'ам: для проверок, reconciliation, quality checks и mart-building
- хороший SQL должен быть не просто рабочим, а читаемым: с говорящими CTE, ясными alias и прозрачной логикой агрегирования

### Window functions
- окна нужны там, где обычного `group by` недостаточно
- ranking, running totals, lag/lead и доли внутри группы - это типовые инженерные и аналитические задачи

## Why this module matters
- SQL останется важным даже когда дальше появятся Spark, Airflow, Iceberg и Kafka
- почти любая итоговая проверка пайплайна заканчивается SQL-запросом
- если студент не умеет проверять слой SQL-ом, он не может надежно валидировать данные

## Core analytical patterns
- `join` facts with dimensions
- `cte` for stepwise transformations
- `group by` for marts
- window functions for ranking and trend metrics
- validation queries for counts, nulls, duplicates

## Practice flow
1. Исследовать таблицы и ключи.
2. Построить базовые агрегации.
3. Собрать витрину по продажам.
4. Добавить ranking и window metrics.
5. Проверить качество итоговой витрины.

## Suggested implementation scope
- 150-220 строк SQL и Python-обвязки в notebook
- минимум две витрины и один ranking use case
- обязательны SQL-checks после построения витрины

## Expected output
- студент строит витрины через понятный многошаговый SQL
- умеет использовать окна и CTE
- может объяснить логику каждой метрики и способ проверки результата

## Questions for review
- когда `group by` недостаточен и нужна window function?
- почему marts лучше строить поверх очищенного слоя, а не поверх raw?
- как убедиться, что join не создал дубли?

