# Tasks - 07 Airflow with Spark batch pipelines

## Delivery format
- notebook с разбором pipeline + DAG review
- ориентир: 150-220 строк анализа, SQL и Python

## Task A - Stage contract mapping
- описать входы, выходы и смысл каждой стадии `raw -> ods -> dm -> load`
- зафиксировать storage path или table contract для каждой стадии
- указать, какая стадия является источником правды для downstream check

## Task B - DAG and operator review
- разобрать `SparkSubmitOperator` по каждой задаче
- описать, какие параметры передаются в Spark и зачем они нужны
- предложить улучшения DAG: checks, alerts, branch, retries, task grouping

## Task C - End-to-end validation
- сформулировать набор post-load checks после финальной загрузки в Postgres
- придумать failure scenarios: пустой raw, пустой ods, сломанный JDBC load
- написать краткий runbook: куда смотреть и что проверять при каждом типе сбоя

## Expected result
- студент видит pipeline как систему контрактов, а не как случайный набор job'ов
- умеет предлагать operational improvements
- понимает, как валидировать end-to-end batch pipeline

## Questions for review
- почему отсутствие строки в dm может быть ошибкой предыдущей стадии?
- какие checks должны быть blocking, а какие informational?
- почему runbook полезен даже для учебного проекта?

