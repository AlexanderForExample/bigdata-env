from datetime import datetime, timedelta
from airflow import DAG
from airflow.providers.apache.spark.operators.spark_submit import SparkSubmitOperator

BASE_DIR = "/opt/airflow"
RAW_JOB = f"{BASE_DIR}/spark/currency_rates_raw.py"
ODS_JOB = f"{BASE_DIR}/spark/currency_rates_ods.py"
MART_JOB = f"{BASE_DIR}/spark/dm_currency_rates_ods.py"
LOAD_JOB = f"{BASE_DIR}/spark/load_to_pg.py"

SPARK_MASTER = "yarn"
SPARK_DELPOY = "client"
DRIVER_PATH = "hdfs:///drivers/postgresql-42.7.2.jar"

default_args = {
    "owner": "Alexander",
    "depends_on_past": False,
    "retries" : 1,
    "retry_delay" : timedelta(minutes=3),
}

with DAG(
    dag_id = "etl_pipeline",
    default_args = default_args,
    schedule = "0 * * * *",
    start_date = datetime(2020, 1, 1),
    catchup = False,
) as dag:

    raw = SparkSubmitOperator(
        task_id = "raw",
        application = RAW_JOB,
        conf = {
            "spark.master": SPARK_MASTER,
            "spark.submit.deployMode": SPARK_DELPOY,
        }
    )
    ods = SparkSubmitOperator(
        task_id = "ods",
        application = ODS_JOB,
        conf = {
            "spark.master": SPARK_MASTER,
            "spark.submit.deployMode": SPARK_DELPOY,
        }
    )
    mart = SparkSubmitOperator(
        task_id = "mart",
        application = MART_JOB,
        conf = {
            "spark.master": SPARK_MASTER,
            "spark.submit.deployMode": SPARK_DELPOY,
        }
    )

    load_to_pg = SparkSubmitOperator(
        task_id = "load_to_pg",
        application = LOAD_JOB,
        conf = {
            "spark.master": SPARK_MASTER,
            "spark.submit.deployMode": SPARK_DELPOY,
            "spark.jars": DRIVER_PATH,
        }
    )

    raw >> ods >> mart >> load_to_pg