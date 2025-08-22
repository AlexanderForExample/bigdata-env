FROM bitnami/spark:3.5.0
USER root

RUN apt-get update \
 && apt-get install -y --no-install-recommends python3-pip curl \
 && rm -rf /var/lib/apt/lists/*

ENV SPARK_HOME=/opt/bitnami/spark \
    SPARK_CONF_DIR=/opt/bitnami/spark/conf \
    HADOOP_CONF_DIR=/opt/bitnami/spark/conf \
    YARN_CONF_DIR=/opt/bitnami/spark/conf

COPY conf/core-site.xml ${SPARK_CONF_DIR}/
COPY conf/yarn-site.xml ${SPARK_CONF_DIR}/
COPY conf/hive-site.xml ${SPARK_CONF_DIR}/

RUN pip3 install --no-cache-dir \
      jupyterlab \
      ipykernel \
      py4j==0.10.9.7

RUN mkdir -p /workspace && chown -R 1001:0 /workspace

USER 1001
WORKDIR /workspace

CMD ["jupyter-lab", "--ip=0.0.0.0", "--port=8888", "--no-browser"]