FROM bitnami/spark:3.5.0
USER root
RUN apt-get update && apt-get install -y curl
#RUN pip3 install py4j
RUN mkdir -p /opt/hadoop/etc/hadoop
ENV HADOOP_HOME=/opt/hadoop
ENV HADOOP_CONF_DIR=/opt/hadoop/etc/hadoop
ENV PATH=$HADOOP_HOME/bin:$HADOOP_HOME/sbin:$PATH
COPY conf/ $HADOOP_CONF_DIR
COPY apps/ /opt/spark-apps
COPY drivers/*.jar /opt/bitnami/spark/jars/

COPY dataset/* /opt/bitnami/spark/dataset/
RUN pip3 install jupyterlab
CMD jupyter-lab --allow-root --no-browser --ip=0.0.0.0