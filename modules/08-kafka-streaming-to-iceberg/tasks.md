# Tasks - 08 Kafka streaming to Iceberg

## Delivery format
- design-heavy notebook со starter code
- ориентир: 170-240 строк кода, схем и пояснений

## Task A - Event contract
- описать структуру события, обязательные поля, ключ сообщения и поля времени
- выделить event time и ingestion time
- продумать, как будут обрабатываться дубли и пустые значения

## Task B - Streaming pipeline design
- собрать код или псевдокод для чтения из Kafka и парсинга JSON
- продумать Bronze/Silver логику
- описать checkpointing, offset handling и основные monitoring points

## Task C - Curated sink and quality checks
- спроектировать запись в curated sink
- предложить набор streaming DQ-checks: freshness, duplicates, malformed messages, volume anomalies
- описать, как будет проверяться корректность sink на нескольких последовательных batch/window interval

## Expected result
- студент умеет описать потоковую архитектуру от source до sink
- понимает, чем streaming checks отличаются от batch checks
- имеет реалистичный blueprint под будущую runnable инфраструктуру

## Questions for review
- почему late events меняют дизайн агрегаций?
- зачем нужен checkpointing?
- почему streaming sink сложнее валидировать, чем batch table?

