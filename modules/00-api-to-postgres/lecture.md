# 00 - API -> Postgres ingestion

## Goal
- понять, как выглядит самый первый ingestion pipeline в аналитической платформе
- научиться безопасно забирать данные из внешнего API и складывать их в raw-слой
- разложить полуструктурированный JSON в нормализованную таблицу и проверить качество загрузки

## Technology focus

### External API as a source
- внешний API - это нестабильный источник: он может тормозить, отдавать пустые страницы, менять формат или временно быть недоступным
- ingestion из API почти всегда требует pagination, retry, timeout и идемпотентность
- в учебном модуле источник простой, но паттерн переносится на реальный production ingestion

### Postgres as a landing zone
- Postgres удобен как первый целевой слой: прост в запуске, понятен по SQL и хорош для маленьких и средних объемов
- JSONB позволяет быстро сохранять raw payload почти без потерь
- нормализованные таблицы нужны, чтобы дальше работать с данными не через JSON-path, а через обычный SQL

### Raw and normalized layers
- raw-слой хранит данные максимально близко к тому, как они пришли из источника
- normalized layer хранит только нужные поля, но в предсказуемой схеме
- разделение слоев упрощает отладку: если downstream-таблица сломалась, всегда можно вернуться к raw

## Why this module matters
- это первый кирпич всей программы: дальше почти каждый модуль будет повторять ту же идею `source -> raw -> transformed layer`
- здесь закладываются ключевые привычки: не терять raw, делать upsert, проверять counts и nulls
- даже если позже источник будет Kafka, JDBC, Parquet или Iceberg, архитектурный паттерн останется тем же

## Architecture
1. Jupyter или Python-скрипт обращается к World Bank API.
2. Ответ читается страницами через `page` и `per_page`.
3. Каждая запись сохраняется в `raw_wb_countries` как `JSONB`.
4. Из raw-слоя поля раскладываются в `countries_dim`.
5. После загрузки выполняются DQ-checks.

## Data model

### `raw_wb_countries`
- `id` - стабильный идентификатор записи
- `payload` - исходный JSON документа
- `ingested_at` - время фактической загрузки

### `countries_dim`
- `id`, `iso2_code`, `name`
- `region_id`, `region_name`
- `income_id`, `income_name`
- `lending_id`, `lending_name`
- `capital_city`, `longitude`, `latitude`
- `loaded_at`

## Important engineering ideas

### Pagination
- нельзя предполагать, что API отдаст весь набор данных за один запрос
- студент должен уметь читать `meta.pages`, `page`, `per_page` и завершать цикл корректно

### Idempotency
- повторный запуск не должен плодить дубли
- в этом модуле это решается через `ON CONFLICT DO UPDATE`
- в более сложных системах вместо этого могут использоваться watermark, merge/upsert, dedup by business key

### Quality checks
- count raw vs count normalized
- null-rate по критичным полям
- duplicate count по business key
- ручной просмотр нескольких строк после загрузки

## Practice flow
1. Проверить доступность API и Postgres.
2. Создать raw и normalized таблицы.
3. Реализовать ingestion c pagination.
4. Реализовать идемпотентную загрузку в raw.
5. Реализовать нормализацию в `countries_dim`.
6. Добавить проверки качества данных.

## Suggested implementation scope
- notebook или script на 150-220 строк Python-кода
- обязательны функции для `fetch`, `load_raw`, `load_dim`, `run_dq`
- код должен быть разбит на маленькие функции, а не состоять из одного длинного блока

## Expected output
- Postgres содержит raw-таблицу с JSONB payload
- Postgres содержит нормализованную таблицу `countries_dim`
- повторный запуск не создает дубли
- студент может объяснить, зачем raw и normalized слой разделены

## Questions for review
- почему raw-слой полезно хранить даже после нормализации?
- почему pagination, timeout и retries надо продумывать сразу?
- чем ingestion из API отличается от чтения статичного файла?

