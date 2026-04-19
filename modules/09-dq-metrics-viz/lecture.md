# 09 - Data quality, metrics and visualization

## Goal
- завершить курс operational layer'ом: качеством данных, метриками и визуализацией
- показать, что успешный запуск pipeline не означает корректные данные
- научить проектировать минимальную observability-систему для data platform

## Technology focus

### Data quality
- DQ - это набор формализованных проверок, которые описывают здоровье данных
- базовые измерения: completeness, uniqueness, freshness, validity, volume consistency
- хороший DQ не пытается проверить вообще все, а фокусируется на рисках конкретного слоя

### Metrics
- кроме данных важны и runtime metrics: длительность DAG, время последнего успешного запуска, размер загрузки, число ошибок
- метрики позволяют видеть не только проблему в таблице, но и деградацию пайплайна как процесса

### Visualization
- dashboard нужен не ради визуального эффекта, а как способ сократить time-to-detect инцидент
- график по row count, freshness lag или duplicate count часто выявляет проблему быстрее, чем чтение логов

## Why this module matters
- этот модуль делает курс ближе к реальной эксплуатации платформы
- именно здесь pipeline перестает быть просто кодом и становится поддерживаемой системой
- без DQ и observability инженер не контролирует качество своего результата

## Core ideas
- checks must be explicit
- results must be stored historically
- metrics should be actionable
- dashboards should highlight anomalies, not просто показывать красивые числа

## Practice flow
1. Выбрать 2-3 критичных таблицы.
2. Составить матрицу DQ-checks.
3. Определить схему хранения результатов проверок.
4. Добавить runtime metrics пайплайна.
5. Спроектировать dashboard widgets.

## Suggested implementation scope
- 150-220 строк кода, SQL и design-заметок
- должны быть зафиксированы entity list, checks, storage schema и widgets
- итог должен быть пригоден как blueprint для следующего инфраструктурного шага

## Expected output
- студент умеет выбрать полезные DQ-checks вместо случайного списка проверок
- может предложить схему хранения DQ results и pipeline metrics
- может объяснить, какие графики действительно полезны для operational monitoring

## Questions for review
- почему `job succeeded` и `data is correct` - это разные утверждения?
- какие проверки стоит запускать на каждом DAG run, а какие периодически?
- как отличить нормальное изменение объема данных от инцидента?

