# 08 - Kafka streaming to Iceberg

## Goal
- познакомить студентов с event-driven ingestion и streaming pipeline design
- показать, как Kafka вписывается в data platform
- связать потоковые данные с curated lakehouse layer

## Technology focus

### Kafka
- Kafka - это распределенный log-based брокер сообщений
- данные пишутся в topic, разделенный на partitions
- consumer читает поток сообщений по offset, а не просто "получает последнее сообщение"

### Streaming mindset
- в streaming pipeline нет естественной границы батча на уровне источника, поэтому появляются offset management, watermarking, deduplication и windowing
- то, что в batch решается одним SQL `group by`, в streaming требует аккуратного отношения к времени события и late-arriving data

### Iceberg as streaming sink target
- streaming pipeline редко хочет писать результат просто в случайные файлы
- curated sink должен оставаться табличным, воспроизводимым и пригодным для downstream чтения
- поэтому связка Kafka + Spark Structured Streaming + Iceberg выглядит естественно

## Why this module matters
- batch - не единственная модель данных в платформе
- многие реальные источники событийные: клики, заказы, логи, телеметрия
- студент должен понимать, чем streaming ingestion отличается от nightly batch

## Practice flow
1. Описать event schema.
2. Спроектировать Kafka topic и consumer behavior.
3. Собрать streaming read pipeline.
4. Отделить Bronze и Silver логику.
5. Спроектировать и проверить curated sink.

## Suggested implementation scope
- 170-240 строк кода и design-notes в notebook
- должны быть описаны schema, parsing, validation, sink и monitoring checks
- если Kafka stack пока не поднят, модуль все равно должен давать достаточно конкретный blueprint для реализации

## Expected output
- студент понимает topic, partition, offset, consumer group
- умеет описать streaming pipeline и его контрольные точки
- понимает риски duplicates, late events и freshness lag

## Questions for review
- почему offset важнее, чем просто "номер сообщения"?
- зачем разделять Bronze и Silver слой в streaming?
- какие DQ-checks особенно важны для event pipeline?

