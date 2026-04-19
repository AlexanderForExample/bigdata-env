from pyspark.sql import SparkSession, functions as F
import os
os.environ["PYSPARK_PYTHON"] = "/opt/conda/bin/python"
os.environ["PYSPARK_DRIVER_PYTHON"] = "/opt/conda/bin/python"
spark = (SparkSession.builder
         .appName("load_to_pg")
         .master("yarn")
         .config("spark.submit.deployMode", "client")
         .config("spark.pyspark.python", "/opt/conda/bin/python")
         .config("spark.executorEnv.PYSPARK_PYTHON", "/opt/conda/bin/python")
         .config("spark.yarn.appMasterEnv.PYSPARK_PYTHON", "/opt/conda/bin/python")
         .enableHiveSupport()
         .getOrCreate())

df = spark.read.table("dm.currency_rates")

jdbc_url = "jdbc:postgresql://postgres-tgt:5432/postgres"

jdbc_props = {
    "user" : "postgres",
    "password" : "postgres",
    "driver": "org.postgresql.Driver",
}

df.write.mode("overwrite").jdbc(jdbc_url, "public_currency_rates_mart", properties = jdbc_props)