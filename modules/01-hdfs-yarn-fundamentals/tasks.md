# Tasks - 01 HDFS and YARN fundamentals

## Delivery format
- notebook или набор команд с пояснениями
- ориентир по сложности: 120-180 строк кода, shell-команд и заметок

## Task A - Cluster reconnaissance
- открыть NameNode UI, YARN UI и Spark UI
- описать роли `NameNode`, `DataNode`, `ResourceManager`, `NodeManager`
- указать, какие сервисы относятся к хранению, а какие к исполнению задач
- зафиксировать, где смотреть состояние файловой системы, а где состояние приложения

## Task B - HDFS operations
- создать иерархию директорий в HDFS для учебного датасета
- загрузить минимум два файла разных форматов
- вывести список файлов, размеры и пути
- при возможности проверить права или метаданные файлов

## Task C - Spark job on YARN
- прочитать файл из HDFS через Spark с `master=yarn`
- выполнить простую трансформацию и агрегат
- сохранить application id или статус задачи из YARN UI
- написать короткий вывод: что делает HDFS, а что делает YARN в этом сценарии

## Expected result
- студент не путает storage layer и resource layer
- умеет работать с HDFS CLI
- может показать реальный запуск Spark application через YARN

## Questions for review
- почему HDFS плохо подходит для OLTP?
- почему Spark job может не стартовать даже если HDFS доступен?
- какие симптомы у проблемы на стороне YARN?

