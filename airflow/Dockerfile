FROM apache/airflow:2.10.1

# Переключаемся на пользователя root для выполнения команд с правами администратора
USER root

# Установка пакета procps, который содержит ps, и wget
RUN apt-get update && apt-get install -y procps wget

# Установка Java (OpenJDK 17)
RUN apt-get update \
  && apt-get install -y --no-install-recommends \
         openjdk-17-jre-headless \
  && apt-get autoremove -yqq --purge \
  && apt-get clean \
  && rm -rf /var/lib/apt/lists/*


# Возвращаем пользователя airflow
USER airflow

# Устанавливаем Spark
ENV SPARK_VERSION="3.5.2"
ENV HADOOP_VERSION="3"
ENV SPARK_HOME=/usr/local/spark
USER root
RUN mkdir -p /opt/hadoop/etc/hadoop
ENV HADOOP_HOME=/opt/hadoop
ENV HADOOP_CONF_DIR=/opt/hadoop/etc/hadoop
COPY conf/ $HADOOP_CONF_DIR
RUN cd "/tmp" && \
    wget --no-verbose "https://archive.apache.org/dist/spark/spark-${SPARK_VERSION}/spark-${SPARK_VERSION}-bin-hadoop${HADOOP_VERSION}.tgz" && \
    tar -xvzf "spark-${SPARK_VERSION}-bin-hadoop${HADOOP_VERSION}.tgz" && \
    mkdir -p "${SPARK_HOME}/bin" && \
    mkdir -p "${SPARK_HOME}/assembly/target/scala-2.12/jars" && \
    cp -a "spark-${SPARK_VERSION}-bin-hadoop${HADOOP_VERSION}/bin/." "${SPARK_HOME}/bin/" && \
    cp -a "spark-${SPARK_VERSION}-bin-hadoop${HADOOP_VERSION}/jars/." "${SPARK_HOME}/assembly/target/scala-2.12/jars/" && \
    rm "spark-${SPARK_VERSION}-bin-hadoop${HADOOP_VERSION}.tgz" && \
    rm -rf "/tmp/spark-${SPARK_VERSION}-bin-hadoop${HADOOP_VERSION}"
# Возвращаем пользователя airflow
USER airflow
RUN pip install pyspark==3.5.2
# Устанавливаем необходимые пакеты, включая провайдер для Spark
RUN pip install apache-airflow-providers-apache-spark==4.10.0
RUN pip install apache-airflow-providers-yandex==3.12.0
USER root
#RUN  mkdir -p /usr/local/spark/python/lib/ && \
#     cp /home/airflow/.local/lib/python3.12/site-packages/pyspark/python/lib/py4j-0.10.9.7-src.zip  /usr/local/spark/python/lib/ && \
#     cp $(python3 -c "import pyspark, os; print(os.path.join(os.path.dirname(pyspark.__file__), 'python', 'lib', 'pyspark.zip'))") /usr/local/spark/python/lib/pyspark.zip
