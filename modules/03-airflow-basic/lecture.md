# 03 - Airflow basic

## Goal
- понять, зачем нужен orchestration layer и чем он отличается от processing layer
- научиться описывать DAG, задачи, schedule и retries
- освоить Airflow UI как основной инструмент операционной работы с пайплайном

## Technology focus

### Airflow as an orchestrator
- Airflow не обрабатывает данные сам по себе, а управляет тем, когда и в каком порядке выполняются шаги pipeline
- он отвечает за расписание, граф зависимостей, retries, историю запусков и логирование
- это control plane, а не compute engine

### DAG model
- DAG описывает структуру процесса как граф задач без циклов
- каждая task должна иметь четкую ответственность и понятный output
- хороший DAG не дублирует бизнес-логику внутри orchestration слоя: тяжелые трансформации лучше держать в отдельных скриптах

### Airflow UI and operations
- UI нужен не только для красоты: через него удобно смотреть статус, duration, retries, logs и историю запусков
- инженер должен уметь быстро локализовать, на какой задаче упало выполнение и почему

## Why this module matters
- дальше Airflow будет оркестрировать Spark batch pipeline
- без базового понимания DAG model сложно собирать воспроизводимые ETL-процессы
- модуль вводит операционную дисциплину: не просто написать код, а уметь его запускать и сопровождать

## Concepts to emphasize
- `schedule` vs manual run
- `start_date` and `catchup`
- retries and transient failures
- task dependencies
- logs and observability

## Practice flow
1. Поднять Airflow и открыть UI.
2. Создать учебный DAG из нескольких задач.
3. Настроить schedule и retries.
4. Посмотреть граф и logs в UI.
5. Смоделировать простую ошибку и разобрать retry behavior.

## Suggested implementation scope
- 120-180 строк Python-кода и заметок в notebook
- DAG минимум из 4-5 шагов, а не из 2 заглушек
- одна задача должна делать что-то осмысленное: логировать контекст, валидировать таблицу или готовить вход для следующей задачи

## Expected output
- студент понимает разницу между orchestration и processing
- умеет читать Airflow UI и логи
- может написать и объяснить базовый DAG с retry semantics

## Questions for review
- почему DAG не должен превращаться в огромный monolith script?
- зачем нужен `catchup=False` в учебных сценариях?
- как отличить transient failure от ошибки бизнес-логики?

