# Tasks - 04 Spark basics

## Delivery format
- `practice.ipynb` со Spark DataFrame code
- ориентир: 160-220 строк Python/Spark-кода

## Task A - Ingestion and schema handling
- прочитать минимум два входных файла разных форматов
- исследовать schema и привести типы к осмысленному виду
- реализовать helper-функцию для проверки, что обязательные колонки существуют

## Task B - Transform and enrich
- выполнить фильтрацию, join и минимум две агрегации
- подготовить curated DataFrame с понятным business meaning
- добавить контрольные `show`, `count` или `describe` в ключевых точках

## Task C - Write and validate
- записать curated result в Parquet
- перечитать результат и убедиться, что схема и значения корректны
- добавить post-write validation: count, null-check или simple reconciliation

## Expected result
- студент уверенно проходит путь `read -> transform -> write`
- есть понятный curated output
- код организован не как набор случайных ячеек, а как небольшая воспроизводимая pipeline

## Questions for review
- почему `inferSchema` удобно, но не всегда надежно?
- чем опасны неявные string-колонки в расчетах?
- почему post-write checks важны даже в учебной задаче?

