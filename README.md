# BigData Env

Локальное окружение для изучения и отработки навыков работы с **Apache Spark**, **Hadoop** и **YARN** в Docker, с поддержкой **JupyterLab**.

## Возможности
- Полный Hadoop-кластер (NameNode, DataNode, ResourceManager, NodeManager, HistoryServer)
- Apache Spark с интеграцией в YARN
- JupyterLab для интерактивной работы
- Установленный Python 3.11.8 через Miniconda на всех нодах

## Состав сервисов
- **namenode** — HDFS NameNode  
- **datanode** — HDFS DataNode  
- **resourcemanager** — YARN ResourceManager  
- **nodemanager** — YARN NodeManager (запускает Spark executors)  
- **historyserver** — YARN HistoryServer  
- **spark** — Spark Master  
- **jupyter** — JupyterLab с PySpark  

## Требования
- Docker >= 20.x  
- Docker Compose >= 1.29  
- 8+ ГБ RAM  
- 4+ CPU  

## Установка и запуск
```bash
git clone https://github.com/AlexanderForExample/bigdata-env.git
cd bigdata-env
docker compose up -d
