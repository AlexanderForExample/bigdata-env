# 01 - HDFS and YARN fundamentals

## Goal
- понять архитектуру Hadoop storage и resource layer
- научиться работать с HDFS как с distributed filesystem
- увидеть, как Spark-приложение исполняется через YARN, а не просто локально на ноутбуке

## What technologies are studied here

### HDFS
- HDFS - это распределенная файловая система, рассчитанная на большие файлы и batch workload
- файлы разбиваются на блоки, а блоки распределяются по DataNode
- клиент работает с HDFS логически как с файловой системой, но фактически взаимодействует с метаданными и физическими блоками отдельно

### NameNode and DataNode
- NameNode хранит namespace, метаданные, список блоков и их расположение
- DataNode хранит реальные блоки данных
- отказ NameNode критичен для кластера, потому что без него невозможно понимать структуру файловой системы

### YARN
- YARN - это слой управления ресурсами и исполнением приложений
- он не хранит данные и не заменяет Spark
- его задача - распределять CPU/RAM между приложениями и следить за их жизненным циклом

### ResourceManager and NodeManager
- ResourceManager принимает заявку на приложение и планирует ресурсы
- NodeManager работает на конкретной ноде и запускает контейнеры
- Spark on YARN значит, что Spark использует этот слой как cluster manager

## Why this module matters
- без понимания HDFS тяжело осмысленно читать и писать данные в Spark-модулях
- без понимания YARN сложно объяснить, почему job зависла, почему executors не стартуют и где искать статус приложения
- этот модуль помогает перестать воспринимать big data stack как черный ящик

## Architecture view
- локальный файл попадает в HDFS через CLI или Spark write
- HDFS хранит блоки данных в DataNode, а метаданные - в NameNode
- Spark job подается в YARN
- YARN выделяет executors в контейнерах и запускает приложение

## Important concepts

### Why HDFS is not a replacement for Postgres
- HDFS не предназначен для OLTP-запросов, обновления отдельных строк и частых транзакций
- HDFS хорош для больших файлов, append-like сценариев и batch processing
- Postgres и HDFS решают разные задачи в data platform

### Why YARN is not Spark
- Spark - processing engine
- YARN - resource manager
- Spark может работать локально, на standalone cluster, на YARN, на Kubernetes

### Replication and fault tolerance
- HDFS реплицирует блоки, чтобы переживать сбои DataNode
- отказоустойчивость идет не через транзакции, а через распределение блоков и повторное поднятие реплик

## Practice flow
1. Поднять big data stack.
2. Проверить NameNode UI, YARN UI и Spark UI.
3. Создать директорию в HDFS.
4. Положить учебный файл в HDFS.
5. Прочитать его Spark-приложением.
6. Запустить job через YARN и найти ее в UI.

## Suggested implementation scope
- 120-180 строк кода и shell-команд в ноутбуке
- использовать HDFS CLI + SparkSession c `master=yarn`
- в решении должны быть зафиксированы роли сервисов, команды, результат чтения файла и статус YARN application

## Expected output
- студент умеет объяснить, что хранится в HDFS, а что делает YARN
- студент может загрузить и найти файл в HDFS
- студент может показать Spark job в YARN UI

## Questions for review
- что делает NameNode и почему он критичен?
- чем отличается хранение данных от управления ресурсами?
- как понять, что проблема в HDFS, а не в Spark или YARN?

