# Tasks - 03 Airflow basic

## Delivery format
- DAG-код + notebook/markdown с разбором
- ориентир: 120-180 строк Python-кода и комментариев

## Task A - Build a real DAG skeleton
- сделать DAG минимум из 4 задач
- использовать не только `EmptyOperator`, но и хотя бы одну задачу с реальной Python-логикой
- задать `start_date`, `schedule`, `catchup`, `retries`, `retry_delay`

## Task B - Failure semantics
- создать controlled-failure сценарий или отдельную задачу, которая умеет падать по условию
- посмотреть, как Airflow отображает retries, failed states и upstream/downstream impact
- описать, где это видно в UI и логах

## Task C - Operational review
- зафиксировать, как смотреть Grid/Graph view, logs, DAG run history
- сформулировать, какие поля и статусы инженеру важно смотреть в первую очередь
- предложить 2-3 улучшения DAG с точки зрения эксплуатации

## Expected result
- DAG не является полностью декоративным
- студент умеет объяснить schedule semantics и retry behavior
- есть осмысленный разбор Airflow UI и operational workflow

## Questions for review
- почему orchestration не должна содержать тяжелую бизнес-логику?
- что делать, если DAG зеленый, но данных нет?
- как отличить ошибку кода задачи от ошибки среды выполнения?

