# Tasks - 09 Data quality, metrics and visualization

## Delivery format
- notebook или markdown+SQL design
- ориентир: 150-220 строк SQL, Python и схем хранения

## Task A - DQ matrix
- выбрать минимум три сущности из разных модулей курса
- описать для каждой сущности проверки на count, duplicates, nulls, freshness и хотя бы одну domain-specific check
- разделить проверки на blocking и informational

## Task B - Historical storage model
- спроектировать таблицу или структуру хранения результатов проверок
- спроектировать таблицу runtime metrics пайплайна
- описать retention и grain хранения метрик

## Task C - Visualization and runbook
- определить 4-6 dashboard widgets
- описать, какую проблему помогает заметить каждый график
- составить короткий runbook: что делать при падении freshness, росте duplicate rate или аномальном runtime

## Expected result
- есть матрица DQ-checks и схема хранения результатов
- есть список operational metrics и дизайн дашборда
- студент понимает, как превращать проверки в практический monitoring layer

## Questions for review
- какие проверки нельзя пропускать на ежедневном pipeline?
- как выбрать порог аномалии для объема данных?
- почему одних только логов недостаточно для operational monitoring?

