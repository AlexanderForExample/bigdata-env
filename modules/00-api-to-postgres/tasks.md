# Tasks - 00 API -> Postgres ingestion

## Delivery format
- основной артефакт: `practice.ipynb`
- ожидаемый объем реализации: 150-220 строк Python-кода без учета markdown
- решение должно быть разбито на функции, а не написано единым линейным блоком

## Task A - Resilient API ingestion
- реализовать функцию чтения страниц World Bank API с параметрами `page`, `per_page`, `timeout`
- добавить защиту от пустого или неожиданного ответа
- логировать или выводить прогресс загрузки
- сохранить raw payload в `raw_wb_countries` через upsert

## Task B - Normalization layer
- реализовать отдельную функцию нормализации raw-документов в `countries_dim`
- корректно обработать пустые вложенные поля и числовые координаты
- обеспечить повторный запуск без дублей

## Task C - Data quality and observability
- сравнить raw и normalized counts
- проверить `null` в критичных полях
- проверить дубли по `id`
- вывести минимум 10 строк raw и 10 строк normalized слоя
- оформить короткий technical summary по результату загрузки

## Expected result
- ingestion можно запускать повторно
- в raw хранится JSONB payload, а в `countries_dim` - табличная схема
- есть понятный набор post-load checks

## Questions for review
- почему это уже ETL, а не просто запрос к API?
- что будет, если API начнет отдавать пустые страницы в середине диапазона?
- какие поля ты считаешь бизнес-ключом и почему?

