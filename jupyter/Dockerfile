FROM jupyter/pyspark-notebook:spark-3.5.0
USER root
COPY drivers/*.jar /usr/local/spark/jars/
USER jovyan
RUN pip install psycopg2-binary mysql-connector-python